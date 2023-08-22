# [Demo]
This repo is used for storing code for various demos that I do. 

Currently, this repo was forked from the Crunchy Data Postgres Examples repo. The changes I made are:

* ../kustomize/postgres_sample - used to deploy a single node cluster via command line
* ../kustomize/postgres - deploys a single node cluster, used in a CI/CD demo deploy vai ArgoCD
* ../kustomize/postgres-test - deploys a dual node cluster with pg_monitor. simulates a testing stage in a CI/CD pipeline
* ../kustomize/postgres-prod - deploys a 3 node cluster w/ pg_monitor, pg_exporter, and backups configured to do a full back up every sunday and incremental backups daily.
* ../kustomize/postgres_replica_demo - work in progress - meant to be used in a multi-cloud demo
* ../kustomize/argocd - folder for the creation of argocd projects (requires deployment and of argocd)
  * kubectl create -n argocd
  * kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
  * kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
  * kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

# [PGO](https://github.com/CrunchyData/postgres-operator), Crunchy [Postgres Operator](https://github.com/CrunchyData/postgres-operator) Examples

This repository contains examples for deploying PGO, the Postgres Operator from Crunchy Data, using a variety of examples.

The examples are grouped by various tools that can be used to deploy them.

The best way to get started is to fork this repository and experiment with the examples.

Each of the examples has its own README that guides you through the process of deploying it.

You can find the full [PGO documentation](https://access.crunchydata.com/documentation/postgres-operator/v5/) for the project here:

[https://access.crunchydata.com/documentation/postgres-operator/v5/](https://access.crunchydata.com/documentation/postgres-operator/v5/)

You can find out more information about [PGO](https://github.com/CrunchyData/postgres-operator), the [Postgres Operator](https://github.com/CrunchyData/postgres-operator) from [Crunchy Data](https://www.crunchydata.com) at the project page:

[https://github.com/CrunchyData/postgres-operator](https://github.com/CrunchyData/postgres-operator)
