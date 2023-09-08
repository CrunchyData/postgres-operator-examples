# Demo
This repo is used for storing code for various demos that I do. 

Currently, this repo was forked from the Crunchy Data Postgres Examples repo. The changes I made are:

* ../kustomize/postgres_sample - used to deploy a single node cluster via command line
* ../kustomize/postgres - deploys a single node cluster, used in a CI/CD demo deploy vai ArgoCD
* ../kustomize/postgres-test - deploys a dual node cluster with pg_monitor. simulates a testing stage in a CI/CD pipeline
* ../kustomize/postgres-prod - deploys a 3 node cluster w/ pg_monitor, pg_exporter, and backups configured to do a full back up every sunday and incremental backups daily.
* ../kustomize/postgres_replica_demo - work in progress - meant to be used in a multi-cloud demo
* ../kustomize/argocd - folder for the creation of argocd projects (requires deployment and of argocd)

# ArgoCD

To create/deploy Argo, follow the steps below.
  ```console
  kubectl create -n argocd
  ```
  ```console
  kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
  ```
  ```console
  kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
  ```
  ```console
  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
  ```

At this point you should have ArgoCD running in your cluster. You will have to log into the cluster to get the public IP address of the ArgoCD instance.

Once logged in, you will see a blank project space. Then, via command line, run:

```console
kubectl apply -k postgres-operator-examples/kustomize/argocd
```

This will create 4 projects in you ArgoCD project space. You can then synce each one to create clusters for the demo. The demo requires the following namespaces which are create in the first step:
* demo
* demo-test
* demo-prod

# Demo steps
 1) create namespaces
 
```console
   oc apply -k postgres-operator-examples/kustomize/install/namespace

```  

 2) deploy PGO: 
 
```console
   oc apply --server-side -k postgres-operator-examples/kustomize/install/default/

``` 
 3) Create a single cluster via command line in the sample namespace:
 
```console
   oc apply -k postgres-operator-examples/kustomize/postgres_sample/

```
 4) Create the ArgoCD projects:
 
```console
   oc apply -k postgres-operator-examples/kustomize/argocd/

```

## To clean up the demo space:
   
 1) delete ArgoCD project 
   
```console
   oc delete -k postgres-operator-examples/kustomize/argocd/

``` 
   
 2) patch ArgoCD toe remove hanging projects
   
  
```console
   bash postgres-operator-examples/kustomize/argocd/cleanup.sh

```
 3) delete sample cluster
   
   
```console
   oc delete -k postgres-operator-examples/kustomize/postgres_sample/

```  
 4) delete PGO

```console
   oc delete -k postgres-operator-examples/kustomize/install/default/

```
  5) delete namespaces
   
```console
   oc delete -k postgres-operator-examples/kustomize/install/namespace

``` 
    





# [PGO](https://github.com/CrunchyData/postgres-operator), Crunchy [Postgres Operator](https://github.com/CrunchyData/postgres-operator) Examples

This repository contains examples for deploying PGO, the Postgres Operator from Crunchy Data, using a variety of examples.

The examples are grouped by various tools that can be used to deploy them.

The best way to get started is to fork this repository and experiment with the examples.

Each of the examples has its own README that guides you through the process of deploying it.

You can find the full [PGO documentation](https://access.crunchydata.com/documentation/postgres-operator/v5/) for the project here:

[https://access.crunchydata.com/documentation/postgres-operator/v5/](https://access.crunchydata.com/documentation/postgres-operator/v5/)

You can find out more information about [PGO](https://github.com/CrunchyData/postgres-operator), the [Postgres Operator](https://github.com/CrunchyData/postgres-operator) from [Crunchy Data](https://www.crunchydata.com) at the project page:

[https://github.com/CrunchyData/postgres-operator](https://github.com/CrunchyData/postgres-operator)
