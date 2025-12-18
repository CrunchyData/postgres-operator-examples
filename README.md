# Examples for Using [PGO](https://github.com/CrunchyData/postgres-operator), the Postgres Operator from Crunchy Data

This repository contains a collection of examples for deploying, operating, and maintaining Postgres clusters using PGO, the Postgres Operator from Crunchy Data as part of [Crunchy Postgres for Kubernetes](https://www.crunchydata.com/products/crunchy-postgresql-for-kubernetes). Using these examples assumes that you already have PGO running. The kustomize installer for PGO can be found in the [postgres-operator](https://github.com/CrunchyData/postgres-operator) repo. The PGO helm installer can be [installed via the OCI registry](https://access.crunchydata.com/documentation/postgres-operator/latest/installation/helm).

The use of these examples with PGO and other container images (aside from those provided by Crunchy Data) will require modifications of the examples.

### Using these Examples

The examples are grouped by various tools that can be used to deploy them.
Each of the examples has its own README that guides you through the process of deploying it.
The best way to get started is to fork this repository and experiment with the examples.
The examples as provided are designed for the use of PGO along with Crunchy Data's Postgres distribution, Crunchy Postgres, as Crunchy Postgres for Kubernetes.  For more information on the use of container images downloaded from the Crunchy Data Developer Portal or other third party sources, please see 'License and Terms' below.

By default, these examples are set to use the `v1` version of the PostgresCluster API, which is only available in PGO v6. If you plan to use these examples with PGO v5, or want to use the older API with PGO v6, you will need to change the version suffix in the `apiVersion` of the PostgresCluster manifests to `v1beta1`.

### Help with the Examples

* For general questions or community support, we welcome you to join our [community Discord](https://discord.gg/BnsMEeaPBV).
* If you believe you have discovered a bug, please open an issue in the [PGO project](https://github.com/CrunchyData/postgres-operator).
* You can find the full Crunchy Postgres for Kubernetes documentation [here](https://access.crunchydata.com/documentation/postgres-operator/v5/).
* You can find out more information about PGO, the Postgres Operator from [Crunchy Data](https://www.crunchydata.com), at the [project page](https://github.com/CrunchyData/postgres-operator).

### FAQs, License and Terms

For more information regarding PGO, the Postgres Operator project from Crunchy Data, and Crunchy Postgres for Kubernetes, please see the [frequently asked questions](https://access.crunchydata.com/documentation/postgres-operator/latest/faq).

For information regarding the software versions of the components included and Kubernetes version compatibility, please see the [components and compatibility section of the Crunchy Postgres for Kubernetes documentation](https://access.crunchydata.com/documentation/postgres-operator/latest/references/components).

The examples provided in this project repository are available subject to the [Apache 2.0](https://github.com/CrunchyData/postgres-operator-examples/blob/-/LICENSE.md) license with the PGO logo and branding assets covered by our [trademark guidelines](https://github.com/CrunchyData/postgres-operator/blob/-/docs/static/logos/TRADEMARKS.md).

The examples as provided in this repo are designed for the use of PGO along with Crunchy Data's Postgres distribution, Crunchy Postgres, as Crunchy Postgres for Kubernetes. The unmodified use of these examples will result in downloading container images from Crunchy Data repositories - specifically the Crunchy Data Developer Portal. The use of container images downloaded from the Crunchy Data Developer Portal are subject to the [Crunchy Data Developer Program terms](https://www.crunchydata.com/developers/terms-of-use).
