#Grab the images that need to be tagged and then pushed
IMAGE=$(cat helm/install/values.yaml | shyaml get-value image.image)
RELATED_IMAGES=$(cat helm/install/values.yaml | shyaml values relatedImages image | awk '{print $2}' | sed '/^$/d')

# docker login
echo $GCR_CREDENTIALS | base64 -d > keyfile.json
docker login -u _json_key --password-stdin https://gcr.io < keyfile.json
echo $HARBOR_PASSWORD | docker login -u $HARBOR_USERNAME --password-stdin https://harbor.devops.indico.io
# pull images

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

