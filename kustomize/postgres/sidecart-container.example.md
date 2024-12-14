apiVersion: postgres-operator.crunchydata.com/v1beta1
kind: PostgresCluster
metadata:
  name: sidecar-hippo
spec:
  postgresVersion: 16
  instances:
    - name: instance1
      containers:
      - name: testcontainer
        image: mycontainer1:latest
      - name: testcontainer2
        image: mycontainer1:latest
      dataVolumeClaimSpec:
        accessModes:
        - "ReadWriteOnce"
        resources:
          requests:
            storage: 1Gi
  backups:
    pgbackrest:
      repos:
      - name: repo1
        volume:
          volumeClaimSpec:
            accessModes:
            - "ReadWriteOnce"
            resources:
              requests:
                storage: 1Gi
  proxy:
    pgBouncer:
      containers:
      - name: bouncertestcontainer1
        image: mycontainer1:latest
