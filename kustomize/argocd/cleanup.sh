#!/bin/bash

oc project argocd

kubectl patch app monitoring  -p '{"metadata": {"finalizers": null}}' --type merge
echo "monitoring patched"
kubectl patch app demo-test -p '{"metadata": {"finalizers": null}}' --type merge
echo "demo-test patched"
kubectl patch app demo-prod -p '{"metadata": {"finalizers": null}}' --type merge
echo "demo-prod patched"
kubectl patch app demo-dev  -p '{"metadata": {"finalizers": null}}' --type merge
echo "demo-dev patched"
echo "all clean"
