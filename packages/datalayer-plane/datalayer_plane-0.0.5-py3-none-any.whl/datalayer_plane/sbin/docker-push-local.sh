#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Push Datalayer Docker Images to Local Registry"$NOCOLOR$NOBOLD
echo

function tag-and-push() {
  docker tag datalayer/$1:$2 localhost:5000/$1:$2
  docker push localhost:5000/$1:$2
}

tag-and-push 'k8s-sidecar' '1.8.2'

tag-and-push 'hdfs-nn' '2.9.0'
tag-and-push 'hdfs-dn' '2.9.0'

tag-and-push 'spark-base' '2.4.0'
tag-and-push 'spark' '2.4.0'
tag-and-push 'spark-py' '2.4.0'
tag-and-push 'spark-r' '2.4.0'
tag-and-push 'spark-resource-staging-server' '2.2.0'
tag-and-push 'spark-shuffle-service' '2.2.0'
tag-and-push 'spark-base' '2.2.0'
tag-and-push 'spark-init' '2.2.0'
tag-and-push 'spark-driver' '2.2.0'
tag-and-push 'spark-driver-py' '2.2.0'
tag-and-push 'spark-executor' '2.2.0'
tag-and-push 'spark-executor-py' '2.2.0'

tag-and-push 'editor' '0.0.1'

tag-and-push 'jupyterhub' '0.0.1'
tag-and-push 'jupyterhub-image-awaiter' '0.0.1'
tag-and-push 'jupyterhub-network-tools' '0.0.1'
tag-and-push 'jupyterhub-pod-culler' '0.0.1'
tag-and-push 'jupyterhub-http-proxy' '0.0.1'
tag-and-push 'jupyterhub' '0.0.1'
