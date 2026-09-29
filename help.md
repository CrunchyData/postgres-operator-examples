kubectl apply -k kustomize/install/namespace


kubectl apply --server-side -k kustomize/install/default

kubectl apply -k kustomize/cn-accounts-backup
kubectl delete -k kustomize/cn-accounts-backup

kubectl apply -k kustomize/cn-lms-prod
kubectl delete -k kustomize/cn-lms-dev
kubectl apply -k kustomize/cn-mattermost
kubectl apply -k kustomize/cn-ch-mattermost
kubectl apply -k kustomize/cn-mixeway-flow

kubectl apply -k kustomize/cn-keycloak

kubectl -n postgres-operator get svc --selector=postgres-operator.crunchydata.com/cluster=cn-lms-prod

# usuwanie terminng
kubectl patch pvc postgres-backup-pvc-new -p '{"metadata":{"finalizers":null}}'


kubectl apply -k kustomize/cn-lms-dev-backup

# update
kubectl apply -k kustomize/postgres --dry-run='server'

kubectl delete -k kustomize/cn-lms-dev 


kubectl -n postgres-operator annotate postgrescluster cn-lms-dev postgres-operator.crunchydata.com/allow-upgrade="cn-lms-dev-upgrade"
