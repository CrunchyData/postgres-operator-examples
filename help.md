kubectl apply -k kustomize/install/namespace


kubectl apply --server-side -k kustomize/install/default


kubectl apply -k kustomize/postgres





kubectl -n postgres-operator get svc --selector=postgres-operator.crunchydata.com/cluster=cn-lms

