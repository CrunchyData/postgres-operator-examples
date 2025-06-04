# Requirements:
# 1. harbor.devops.indico.io is already added as a helm repo (named harbor)
# 2. cm-push is already installed as a helm plugin
for url in $( cat required_repos.txt )
do
  helm repo add $url $url
done
for filename in 'helm/install' 'helm/postgres';
do
  if [ -d $filename ]; then
    VERSION=$(grep appVersion ./$filename/Chart.yaml | awk '{print $2}' | tr -d '\n')
    CHART=$(grep ^name ./$filename/Chart.yaml | awk '{print $2}' | tr -d '\n')
    helm dependency build ./$filename
    helm package $filename --version $VERSION
    helm push $CHART-$VERSION.tgz oci://harbor.devops.indico.io/indico-charts
  fi 
done
