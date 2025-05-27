kubectl apply -k kustomize/install/namespace


kubectl apply --server-side -k kustomize/install/default

kubectl apply -k kustomize/cn-accounts-backup
kubectl delete -k kustomize/cn-accounts-backup

kubectl apply -k kustomize/cn-lms-dev
kubectl apply -k kustomize/cn-lms-prod
kubectl apply -k kustomize/cn-mattermost
kubectl apply -k kustomize/mm-mattermost

kubectl -n postgres-operator get svc --selector=postgres-operator.crunchydata.com/cluster=cn-lms-prod

# usuwanie terminng
kubectl patch pvc postgres-backup-pvc-new -p '{"metadata":{"finalizers":null}}'
