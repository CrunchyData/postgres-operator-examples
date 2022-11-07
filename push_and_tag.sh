#Grab the images that need to be tagged and then pushed
CONTROLLER_IMAGE_CLUSTER=$(cat helm/install/values.yaml | shyaml get-value controllerImages.cluster)
CONTROLLER_IMAGE_UPGRADE=$(cat helm/install/values.yaml | shyaml get-value controllerImages.upgrade)
RELATED_IMAGES=$(cat helm/install/values.yaml | shyaml values relatedImages image | awk '{print $2}' | sed '/^$/d')

# docker login
echo $GCR_CREDENTIALS | base64 -d > keyfile.json
docker login -u _json_key --password-stdin https://gcr.io < keyfile.json
echo $HARBOR_PASSWORD | docker login -u $HARBOR_USERNAME --password-stdin https://harbor.devops.indico.io
# pull images

#pull postgres-operator controller image
docker pull $CONTROLLER_IMAGE_CLUSTER
IMAGE_BASE=$(basename $CONTROLLER_IMAGE_CLUSTER)
#push to gcr
docker tag $CONTROLLER_IMAGE_CLUSTER gcr.io/new-indico/$IMAGE_BASE
docker push gcr.io/new-indico/$IMAGE_BASE
#push to harbor
docker tag $CONTROLLER_IMAGE_CLUSTER harbor.devops.indico.io/indico/$IMAGE_BASE
docker push harbor.devops.indico.io/indico/$IMAGE_BASE
#Remove Junk
docker rmi $CONTROLLER_IMAGE_CLUSTER gcr.io/new-indico/$IMAGE_BASE harbor.devops.indico.io/indico/$IMAGE_BASE

#pull postgres-operator upgrade image
docker pull $CONTROLLER_IMAGE_UPGRADE
IMAGE_BASE=$(basename $CONTROLLER_IMAGE_UPGRADE)
#push to gcr
docker tag $CONTROLLER_IMAGE_UPGRADE gcr.io/new-indico/$IMAGE_BASE
docker push gcr.io/new-indico/$IMAGE_BASE
#push to harbor
docker tag $CONTROLLER_IMAGE_UPGRADE harbor.devops.indico.io/indico/$IMAGE_BASE
docker push harbor.devops.indico.io/indico/$IMAGE_BASE
#Remove Junk
docker rmi $CONTROLLER_IMAGE_UPGRADE gcr.io/new-indico/$IMAGE_BASE harbor.devops.indico.io/indico/$IMAGE_BASE

for ri in $RELATED_IMAGES;
do
    IMAGE=$ri
    docker pull $IMAGE
    IMAGE_BASE=$(basename $IMAGE)
    #push to gcr
    docker tag $IMAGE gcr.io/new-indico/$IMAGE_BASE
    docker push gcr.io/new-indico/$IMAGE_BASE
    #push to harbor
    docker tag $IMAGE harbor.devops.indico.io/indico/$IMAGE_BASE
    docker push harbor.devops.indico.io/indico/$IMAGE_BASE
    #Remove Junk
    docker rmi $IMAGE gcr.io/new-indico/$IMAGE_BASE harbor.devops.indico.io/indico/$IMAGE_BASE
done

