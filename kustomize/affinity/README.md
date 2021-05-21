# Postgrescluster with Custom Pod & Node Affinity/Anti-Affinity

## Assumptions
This example assumes you have the Crunchy PostgreSQL Operator installed
- on a three node kubernetes cluster
- in the postgres-operator namespace

## Example setup
In the example we will use nodes named node1, node2, and node3. You will
need to update these names to match the node names in your three node
cluster.

Add labels to two of your nodes using the following commands:
```
kubectl label node node1 pgo-key=instance
kubectl label node node2 pgo-key=repo-host
```

## Create the cluster
Create the cluster using kubectl and kustomize
```
kubectl apply -k examples/affinity
```

## Verify
Check the pods created in the postgres-operator namespace. Use
kubectl to get the pods and show the node they are assigned to:

```
kubectl get pods -n postgres-operator -o wide
```

- Pods created for intance1 should be assigned to node1
- Pods created for the repo-host should be assigned to node2
- The third pod, created for instance2, cannot be created on node2 and has a
pod-anti-affinity preference to avoid nodes with other intstances. This pod
should be assigned to node3.
