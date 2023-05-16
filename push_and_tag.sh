CRUNCHY_REGISTRY=registry.crunchydata.com
#Grab the images that need to be tagged and then pushed
CONTROLLER_IMAGE_CLUSTER=$(cat helm/install/values.yaml | shyaml get-value controllerImages.cluster)
CONTROLLER_IMAGE_UPGRADE=$(cat helm/install/values.yaml | shyaml get-value controllerImages.upgrade)
RELATED_IMAGES=$(cat helm/install/values.yaml | shyaml values relatedImages image | awk '{print $2}' | sed '/^$/d')

# docker login
echo $GCR_CREDENTIALS | base64 -d > keyfile.json
docker login -u _json_key --password-stdin https://gcr.io < keyfile.json
echo $HARBOR_PASSWORD | docker login -u $HARBOR_USERNAME --password-stdin https://harbor.devops.indico.io
echo $CRUNCHY_PASSWORD | docker login -u $CRUNCHY_USERNAME --password-stdin https://$CRUNCHY_REGISTRY
# pull images

#pull postgres-operator controller image
IMAGE_BASE=$(basename $CONTROLLER_IMAGE_CLUSTER)
PRIVATE_IMAGE=$CRUNCHY_REGISTRY/crunchydata/$IMAGE_BASE
docker pull $PRIVATE_IMAGE
#push to gcr
docker tag $PRIVATE_IMAGE gcr.io/new-indico/$IMAGE_BASE
docker push gcr.io/new-indico/$IMAGE_BASE
#push to harbor
docker tag $PRIVATE_IMAGE harbor.devops.indico.io/indico/$IMAGE_BASE
docker push harbor.devops.indico.io/indico/$IMAGE_BASE
#Remove Junk
docker rmi $PRIVATE_IMAGE gcr.io/new-indico/$IMAGE_BASE harbor.devops.indico.io/indico/$IMAGE_BASE

#pull postgres-operator upgrade image
IMAGE_BASE=$(basename $CONTROLLER_IMAGE_UPGRADE)
PRIVATE_IMAGE=$CRUNCHY_REGISTRY/crunchydata/$IMAGE_BASE
docker pull $PRIVATE_IMAGE
#push to gcr
docker tag $PRIVATE_IMAGE gcr.io/new-indico/$IMAGE_BASE
docker push gcr.io/new-indico/$IMAGE_BASE
#push to harbor
docker tag $PRIVATE_IMAGE harbor.devops.indico.io/indico/$IMAGE_BASE
docker push harbor.devops.indico.io/indico/$IMAGE_BASE
#Remove Junk
docker rmi $PRIVATE_IMAGE gcr.io/new-indico/$IMAGE_BASE harbor.devops.indico.io/indico/$IMAGE_BASE

for ri in $RELATED_IMAGES;
do
    IMAGE=$ri
    IMAGE_BASE=$(basename $IMAGE)
    PRIVATE_IMAGE=$CRUNCHY_REGISTRY/crunchydata/$IMAGE_BASE
    docker pull $PRIVATE_IMAGE
    #push to gcr
    docker tag $PRIVATE_IMAGE gcr.io/new-indico/$IMAGE_BASE
    docker push gcr.io/new-indico/$IMAGE_BASE
    #push to harbor
    docker tag $PRIVATE_IMAGE harbor.devops.indico.io/indico/$IMAGE_BASE
    docker push harbor.devops.indico.io/indico/$IMAGE_BASE
    #Remove Junk
    docker rmi $PRIVATE_IMAGE gcr.io/new-indico/$IMAGE_BASE harbor.devops.indico.io/indico/$IMAGE_BASE
done
