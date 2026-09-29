## Step 1: Take a Full Backup

kubectl annotate -n postgres-operator postgrescluster accounts \
  postgres-operator.crunchydata.com/pgbackrest-backup="$(date)"
  <!-- - with overwrite -->
kubectl annotate -n postgres-operator postgrescluster hippo --overwrite \
  postgres-operator.crunchydata.com/pgbackrest-backup="$(date)"

## Step 2: Configure the Upgrade Parameters through a PGUpgrade object
# update 13-14
kubectl apply -f - <<EOF
apiVersion: postgres-operator.crunchydata.com/v1beta1
kind: PGUpgrade
metadata:
  name: accounts-upgrade
spec:
  image: registry.developers.crunchydata.com/crunchydata/crunchy-upgrade:ubi8-5.4.3-0
  postgresClusterName: accounts
  fromPostgresVersion: 14
  toPostgresVersion: 15
EOF

# w tym momencie process powinien byc w trakcie i czeka na zamkniecie bazy
  If you look at the status of the PGUpgrade object at this point, you should see a condition saying this:
type: "progressing",
status: "false",
reason: "PGClusterNotShutdown",
message: "PostgresCluster instances still running",


## Step 3: Shutdown and Annotate the Cluster
kubectl -n postgres-operator annotate postgrescluster accounts postgres-operator.crunchydata.com/allow-upgrade="hippo-upgrade"

## Shutdown database
kubectl patch -n postgres-operator postgrescluster accounts --type merge -p '{"spec":{"shutdown":true}}'

# czekamy na Update status
    type: "Progressing"
    status: "false"
    reason: "PGUpgradeCompleted"

    type:   "Succeeded" status: "true"
    reason: "PGUpgradeSucceeded"

# ponownie go uruchom przez
kubectl -n postgres-operator apply -k kustomize/postgres


<!-- kubectl -n postgres-operator apply -k kustomize/postgres -->




kubectl exec -it <pod-name> --namespace <namespace> -- df -h
