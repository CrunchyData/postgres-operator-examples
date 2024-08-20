This is a customized fork of [CrunchyData's Postgres Operator](https://github.com/CrunchyData/postgres-operator-examples/).

Userdocs could be found [here](https://access.crunchydata.com/documentation/postgres-operator/latest/quickstart).


# Apolo deployment example:
```bash
apolo run \
  --pass-config \
  --entrypoint "./entrypoints/pgo.sh install postgresql pgv --set 'instanceReplicas=2' --set 'pgBouncerReplicas=2' --set 'preset_name=cpu-medium' --set 'bouncer_preset_name=cpu-small' --set 'users[0].name=myuser' --set 'users[0].databases[0]=mydb'" \
  ghcr.io/neuro-inc/app-deployment
```

# Kubernetes deployment:
## All-in-one deployment
[Optionally]
Generate backup configuration with

`python gen_config.py pgvector helm/app/values.yaml helm/app/values-default.yaml --subapp=postgrescluster`

Install app with

`helm upgrade --install pgvector -n pgvector --create-namespace helm/app/  -f helm/app/values-postgres-default.yaml --dependency-update`

## Deploy components separately
### Install Postgres Operator (PRGO) and corresponding CRDs for k8s:

`helm upgrade --install postgres-operator -n postgres-operator --create-namespace helm/install`

When `--set singleNamespace=true`, PGO watches for and responds to PostgresClusters only in namespace, where it is installed. In this case, change namespace name in the following commands from `pgvector` to `postgres-operator` or other name you used to install operator itself.

## Deploy Postgres (includes PGVector extension).
### Minimal config:
- 1 instance (no HA) with 2Gb RAM, 1vCPU, 2Gb storage (default StorageClass)
- no pgBouncer, no TLS, no monitoring
- pgBackRest stores backups in local PVCs
- no default users or databases created

`helm upgrade --install pgvector -n pgvector --create-namespace helm/postgres`

### Default Apolo config:
- 3 postgres replicas (high availability config, 1 master and 2 slaves controlled by Patroni). Resources: 2Gb RAM, 1vCPU, 20Gb storage (default StorageClass)
- 2 pgBouncer replicas
- Enabled Prometheus metrics exporter
- 1 default `postgres` user with SUPERUSER privileges is created.

Install dependencies with `make setup`.

`python gen_config.py pgvector helm/postgres/values-default-template.yaml helm/postgres/values-default.yaml` -- creates default config with backup information at `helm/postgres/values-default.yaml` values file.

`helm upgrade --install pgvector -n pgvector --create-namespace helm/postgres -f helm/postgres/values.yaml -f helm/postgres/values-default.yaml`

### Usage
When deployed, PostgresCluster CRD creates corresponding pods, PVCs, enables replication, backups and high availability.

It also creates secrets within the same namespace with access credentials that will enable users to gain access to this Postgres cluster.
To get them, hit:
`kubectl -n pgvector get secret -l postgres-operator.crunchydata.com/role=pguser -o json | jq '.items[].data | map_values(@base64d)'`

Now you could use these credentials from within other apps in this cluster or platform jobs to access postgres.

Note: the user can not be "SUPERUSER" to connect using pgbouncer, so you will need to create a dedicated unprivileged user.
To add a dedicated user and databases, adjust the values-default.yaml file with additional entries, for instance:

```yaml
users:
  - name: postgres
  - name: apolo
    databases:
      - apolo
```
More information regarding user management could be found [here](https://access.crunchydata.com/documentation/postgres-operator/latest/tutorials/basic-setup/user-management#managing-the-postgres-user).

#### Endpoint
Optionally, perform port-fowarding of PGBouncer service from cluster to your local machine with:
`kubectl -n pgvector port-forward svc/pgvector-pgbouncer 5432`

Or use `pgvector-pgbouncer.pgvector.svc.cluster.local` domain name if you are connecting from within the job.

#### PGVector extension

Enable extension in your database using command:
`CREATE EXTENSION vector;`


## Removal
Remove postgrescluster release from the corresponding namespace:
`helm uninstall pgvector -n pgvector`

<details>
<summary> TODOs </summary>
- pgBackRest
  - If pgBackRest stores backups in platform managed S3 bucket, we need to adjust [--repo-s3-uri-style](https://pgbackrest.org/configuration.html#section-repository/option-repo-s3-uri-style) (https://access.crunchydata.com/documentation/postgres-operator/latest/tutorials/backups-disaster-recovery/backups#using-s3)
  - need to add default schedule for pgBackRest
  - current installation does not expose posgtes outside the cluster (no ingress configuration for now).



</details>


<details>

<summary> Readme from original repo </summary>
## Examples for Using [PGO](https://github.com/CrunchyData/postgres-operator), the Postgres Operator from Crunchy Data

This repository contains a collection of installers and examples for deploying, operating and maintaining Postgres clusters using PGO, the Postgres Operator from Crunchy Data as part of [Crunchy Postgres for Kubernetes](https://www.crunchydata.com/products/crunchy-postgresql-for-kubernetes).

The use of these examples with PGO and other container images (aside from those provided by Crunchy Data) will require modifications of the examples.

#### Using these Examples

The examples are grouped by various tools that can be used to deploy them.
Each of the examples has its own README that guides you through the process of deploying it.
The best way to get started is to fork this repository and experiment with the examples.
The examples as provided are designed for the use of PGO along with Crunchy Data's Postgres distribution, Crunchy Postgres, as Crunchy Postgres for Kubernetes.  For more information on the use of container images downloaded from the Crunchy Data Developer Portal or other third party sources, please see 'License and Terms' below.

#### Help with the Examples

* For general questions or community support, we welcome you to join our [community Discord](https://discord.gg/BnsMEeaPBV).
* If you believe you have discovered a bug, please open an issue in the [PGO project](https://github.com/CrunchyData/postgres-operator).
* You can find the full Crunchy Postgres for Kubernetes documentation [here](https://access.crunchydata.com/documentation/postgres-operator/v5/).
* You can find out more information about PGO, the Postgres Operator from [Crunchy Data](https://www.crunchydata.com), at the [project page](https://github.com/CrunchyData/postgres-operator).

#### FAQs, License and Terms

For more information regarding PGO, the Postgres Operator project from Crunchy Data, and Crunchy Postgres for Kubernetes, please see the [frequently asked questions](https://access.crunchydata.com/documentation/postgres-operator/latest/faq).

For information regarding the software versions of the components included and Kubernetes version compatibility, please see the [components and compatibility section of the Crunchy Postgres for Kubernetes documentation](https://access.crunchydata.com/documentation/postgres-operator/latest/references/components).

The examples provided in this project repository are available subject to the [Apache 2.0](https://github.com/CrunchyData/postgres-operator-examples/blob/-/LICENSE.md) license with the PGO logo and branding assets covered by our [trademark guidelines](https://github.com/CrunchyData/postgres-operator/blob/-/docs/static/logos/TRADEMARKS.md).

The examples as provided in this repo are designed for the use of PGO along with Crunchy Data's Postgres distribution, Crunchy Postgres, as Crunchy Postgres for Kubernetes. The unmodified use of these examples will result in downloading container images from Crunchy Data repositories - specifically the Crunchy Data Developer Portal. The use of container images downloaded from the Crunchy Data Developer Portal are subject to the [Crunchy Data Developer Program terms](https://www.crunchydata.com/developers/terms-of-use).

</details>
