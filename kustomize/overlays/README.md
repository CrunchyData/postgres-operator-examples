# Using Local S3 Repos in Each Data Center

## Introduction
Overlays provide a method to configure development, production, and standby with unique configurations based on a base configuration.  The combination of declarative Postgres and overlays provides an efficient way to control configuration creep and enforce standards that are common between all environments. 

For the streaming replication for standby, the Postgres primary database must be exposed external to the cluster.  In this example that is accomplished by using a Load Balancer service type.

The UBI images are used in this example.  These UBI based images are only available to active Crunchy Data support subscribers.  There is also an assumption that the necessary image pull secrets have been configured in the targeted namespaces.

Note that several of the manifest and other files have place holders for environment specific values.  The placeholders are identified by <xxxxxx>.

## Creating Environments

### Base
A postgres cluster called 'over' is used in this example.  The 'over' Postgres cluster requires the 'overuser' with access to two databases (overdb, underdb).  The user and databases, along with some Postgres parameter settings, will be a standard that is required in every environment.  By setting it in the base, all overlays will start with this configuration.

### Development
The Kustomize overlay will add '-dev' to the cluster name and all created Kubernetes objects. The only modification for development is to setup a weekly full backup to the pgBackRest repository.

To deploy the development cluster, ensure that your context is set to the appropriate Kubernetes cluster and execute the following command:

```kubectl apply -k overlays/development```

### UAT
The Kustomize overlay will add '-uat' to the cluster name and all created Kubernetes objects. The following modifications are made for UAT:

  - Weekly full and incremental backup scheduled to repo1.
  - Increase number of instances to 2 (one primary and one replica).
  - Monitoring enabled.

To deploy the uat cluster, ensure that your context is set to the appropriate Kubernetes cluster and execute the following command:

```kubectl apply -k overlays/uat```


### Production
The Kustomize overlay will add '-uat' to the cluster name and all created Kubernetes objects. The following modifications are made for UAT:

  - Weekly full and incremental backup scheduled to repo1.
  - Increase number of instances to 3 (one primary and two replicas).
  - Adjustment to archive_timeout to keep RPO on standby to 10 minutes.
  - Secret created for S3 authentication.
  - S3 pgBackRest is added for standby database creation and log shipping (repo2).
  - A weekly full backup scheduled for repo2 (S3).
  - Monitoring enabled.
  - Settings for manual backup of type full to S3 repository.

Optionally, if streaming replication will be used a Load Balancer service is created.  If streaming replication is not used and logs will be shipped via S3 bucket (default), this resource can be commented out of the kustomization.yaml's resource section.

To deploy the uat cluster, ensure that your context is set to the appropriate Kubernetes cluster and execute the following command:

```kubectl apply -k overlays/production```

Once the cluster has reached full ready state, the next step is to trigger the initial full backup to the S3 repository.  This full backup will be used to instantiate the standby database.

```kubectl annotate postgrescluster over-prod postgres-operator.crunchydata.com/pgbackrest-backup="$( date '+%F_%H:%M:%S' )"```


### Standby (Default Configuration)
Use the 'standby' overlay will create a standby Postgres cluster that uses the default log shipping via S3 bucket.  The only prerequisite for this default configuration is to have an initial backup present in the S3 repository.

To deploy the standard standby cluster, ensure that your context is set to the appropriate Kubernetes cluster and execute the following command:

```kubectl apply -k overlays/standby```

### Standby (Streaming Configuration)
Use the 'standbystream' overlay will create a standby Postgres cluster that uses streaming replication.  The S3 repository is still required to instantiate the standby cluster and as a fallback log shipping path if network connectivity is disrupted between the standby cluster and the primary.

There are several prerequisite steps to setup this streaming replication:

  - A full backup must be present in the S3 repository.
  - The certificate used for the replication user must be copied from the primary database.
  - The Postgres manifest updated with the IP address assigned to the Load Balancer service of the primary cluster.

Replication User Certificate:

On the primary cluster, pull the certificate values for the replication user and update the cert-repl.yaml with these values.

```kubectl get secret over-prod-replication-cert -o jsonpath={.data}```

External IP:

On the primary cluster, get the external IP address for the over-lb-prod service.

```kubectl get service over-lb-prod```

Update the Postgres manifest patroni.dynamicConfiguration.standby_cluster with this external IP addres.

To deploy the standard standby cluster, ensure that your context is set to the appropriate Kubernetes cluster and execute the following command:

```kubectl apply -k overlays/standbystream```


