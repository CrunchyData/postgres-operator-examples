# Szybka instalacja
kubectl apply -k kustomize/install/namespace
# instalacja operatora, podstawowe konfiguracje
kubectl apply --server-side -k kustomize/install/default
# check - sprawdzenie czy dziala
kubectl -n postgres-operator get pods \
  --selector=postgres-operator.crunchydata.com/control-plane=postgres-operator \
  --field-selector=status.phase=Running


# instalcja instanjci bazy danych "hippo"
kubectl apply -k kustomize/postgres
# check
kubectl -n postgres-operator describe postgresclusters.postgres-operator.crunchydata.com hippo
# lista pod
kubectl -n postgres-operator get pods \
  --selector=postgres-operator.crunchydata.com/cluster=hippo,postgres-operator.crunchydata.com/instance

kubectl -n postgres-operator get svc --selector=postgres-operator.crunchydata.com/cluster=hippo



# uninstall
kubectl delete -k kustomize/install/namespace





kubectl api-resources --verbs=list --namespaced -o name | xargs -n 1 kubectl get --show-kind --ignore-not-found -n postgres-operator


kubectl get namespace postgres-operator -o json > temp.json

kubectl replace --raw "/api/v1/namespaces/postgres-operator/finalize" -f ./temp.json
