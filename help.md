kubectl apply -k kustomize/install/namespace


kubectl apply --server-side -k kustomize/install/default

kubectl apply -k kustomize/cn-accounts
kubectl apply -k kustomize/cn-lms
kubectl apply -k kustomize/cn-lms-prod
kubectl apply -k kustomize/cn-mattermost


kubectl -n postgres-operator get svc --selector=postgres-operator.crunchydata.com/cluster=cn-lms

