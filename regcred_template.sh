# create the secret (access portal username is typically your Crunchy email)
# Change namespace as needed
kubectl create secret docker-registry [SECRET-NAME] -n [DEST_NS] \
  --docker-server=registry.crunchydata.com \
  --docker-username=<ACCESS_PORTAL_USERNAME> \
  --docker-email=<ACESS_PORTAL_USERNAME> \
  --docker-password=<YOUR PASSWORD>
  
# I've started having to run this to get the registry secret to work
kubectl secrets link default timmregcred --for=pull

# Command that allows you to copy a secret from one namespace to another
# NOTE: the 'neat' part here is a kubectl plugin (https://github.com/itaysk/kubectl-neat)
# If on Mac, install 'neat' with:
kubectl krew install neat
kubectl neat get -- secret [SECRET] --namespace=postgres-operator -o yaml | sed 's/namespace: .*/namespace: [destinationNS]/' | kubectl apply -f -