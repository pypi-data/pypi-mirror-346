#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Removing Datalayer Plane"$NOCOLOR$NOBOLD
echo

function kubernetes_telepresence() {
  RELEASE=kubernetes-telepresence
  NAMESPACE=ambassador
  helm delete $RELEASE --namespace $NAMESPACE
}

function kubernetes_dashboard() {
  RELEASE=kubernetes-dashboard
  NAMESPACE=kube-system
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_nginx() {
  RELEASE=datalayer-nginx
  NAMESPACE=datalayer-nginx
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_traefik() {
  RELEASE=datalayer-traefik
  NAMESPACE=datalayer-traefik
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_ceph_operator() {
  RELEASE=datalayer-ceph-operator
  NAMESPACE=datalayer-storage
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_ceph_cluster() {
  RELEASE=datalayer-ceph-cluster
  NAMESPACE=datalayer-storage
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_shared_filesystem() {
  RELEASE=datalayer-shared-filesystem
  NAMESPACE=datalayer-storage
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_cert_manager() {
  RELEASE=datalayer-cert-manager
  NAMESPACE=datalayer-cert-manager
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_datashim() {
  RELEASE=datalayer-datashim
  NAMESPACE=datalayer-datashim
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_cuda_operator() {
  RELEASE=datalayer-cuda-operator
  NAMESPACE=datalayer-cuda-operator
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_solr_operator() {
  RELEASE=datalayer-solr-operator
  NAMESPACE=datalayer-solr-operator
  helm delete $RELEASE --namespace $NAMESPACE
  kubectl delete \
    -n $NAMESPACE \
    -f https://solr.apache.org/operator/downloads/crds/v0.8.0/all-with-dependencies.yaml
}

function datalayer_config() {
  RELEASE=datalayer-config
  NAMESPACE=datalayer-config
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_inbounds() {
  RELEASE=datalayer-inbounds
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_outbounds() {
  RELEASE=datalayer-outbounds
  NAMESPACE=datalayer-growth
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_vault() {
  RELEASE=datalayer-vault
  NAMESPACE=datalayer-vault
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_kafka() {
  RELEASE=datalayer-kafka
  NAMESPACE=datalayer-kafka
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_pulsar() {
  RELEASE=datalayer-pulsar
  NAMESPACE=datalayer-pulsar
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_ldap() {
  RELEASE=datalayer-ldap
  NAMESPACE=datalayer-ldap
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_ldapadmin() {
  RELEASE=datalayer-ldap
  NAMESPACE=datalayer-ldap
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_keycloak() {
  RELEASE=datalayer-keycloak
  NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_falco() {
  RELEASE=datalayer-falco
  NAMESPACE=datalayer-falco
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_observer() {
  RELEASE=datalayer-observer
  NAMESPACE=datalayer-observer
  kubectl delete -f $PLANE_HOME/etc/helm/charts/datalayer-falco/falcosidekick-grafana.yaml
  kubectl delete -f $PLANE_HOME/etc/helm/charts/datalayer-falco/falcosidekick-prometheusrule.yaml
  helm delete $RELEASE --namespace $NAMESPACE
  echo 
  echo You will need to remove manually the CR opentelemetry.io/v1beta1/opentelemetrycollectors.
  echo To achieve that you will need to remove manually the finalizer on them.
  echo Once the CR is removed, the associated resources should be released.
  echo 
}

function datalayer_manager() {
  RELEASE=datalayer-manager
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_iam() {
  RELEASE=datalayer-iam
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_success() {
  RELEASE=datalayer-success
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_support() {
  RELEASE=datalayer-support
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_growth() {
  RELEASE=datalayer-growth
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_operator() {
  RELEASE=datalayer-operator
  NAMESPACE=datalayer-jupyter
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_openfga() {
  RELEASE=datalayer-openfga
  NAMESPACE=datalayer-openfga
#  --no-hooks
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_ai_agents() {
  RELEASE=datalayer-ai-agents
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_spacer() {
  RELEASE=datalayer-spacer
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_library() {
  RELEASE=datalayer-library
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_jupyter() {
  RELEASE=datalayer-jupyter
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function jupyterhub() {
  RELEASE=jupyterhub
  NAMESPACE=jupyterhub
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_jump() {
  RELEASE=datalayer-jump
  NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_content() {
  RELEASE=datalayer-content
  NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function datalayer_minio() {
  RELEASE=datalayer-minio
  NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
#  kubectl minio tenant delete $RELEASE -n $NAMESPACE
#  kubectl minio delete
#  kubectl delete namespace $NAMESPACE
}

function datalayer_editor() {
  RELEASE=datalayer-editor
  NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function jupyterpool() {
  RELEASE=jupyterpool
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function jupyter_server() {
  RELEASE=jupyter-server
  NAMESPACE=datalayer-api
  helm delete $RELEASE --namespace $NAMESPACE
}

function jupyter_editor() {
  RELEASE=jupyter-editor
  NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function example_simple() {
  RELEASE=example-simple
  NAMESPACE=datalayer
  helm delete $RELEASE --namespace $NAMESPACE
}

function commands() {
  echo -e $YELLOW"💛  Valid commands: [ datalayer-cert-manager | datalayer-datashim | datalayer-operator | datalayer-ai-agents | datalayer-inbounds | datalayer-outbounds | datalayer-openfga | datalayer-cuda-operator | datalayer-solr-operator | datalayer-config | datalayer-vault | datalayer-pulsar | kubernetes-dashboard | datalayer-ldap | datalayer-ldapadmin | datalayer-keycloak | datalayer-iam | datalayer-success | datalayer-support | datalayer-growth | datalayer-manager | datalayer-spacer | datalayer-library | datalayer-run | datalayer-nginx | datalayer-traefik | jupyterhub | jupyterpool | jupyter-server | jupyter-editor | datalayer-minio | datalayer-jump | datalayer-content | datalayer-editor | example-simple | example-simple ]"$NOCOLOR 1>&2
}

CMDS="$1"

if [ -z "$CMDS" ]; then
  echo -e $RED$BOLD"💔  No command to execute has been provided."$NOCOLOR$NOBOLD 1>&2
  echo
  exit 1
fi

function apply_cmd() {

  echo -e $BOLD"✋  Removing [$BLUE$1$NOCOLOR]"$NOBOLD
  echo

  case "$1" in

    kubernetes-telepresence)
      kubernetes_telepresence
      ;;

    kubernetes-dashboard)
      kubernetes_dashboard
      ;;

    datalayer-nginx)
      datalayer_nginx
      ;;

    datalayer-traefik)
      datalayer_traefik
      ;;

    datalayer-ceph-operator)
      datalayer_ceph_operator
      ;;

    datalayer-ceph-cluster)
      datalayer_ceph_cluster
      ;;

    datalayer-shared-filesystem)
      datalayer_shared_filesystem
      ;;

    datalayer-cert-manager)
      datalayer_cert_manager
      ;;

    datalayer-inbounds)
      datalayer_inbounds
      ;;

    datalayer-outbounds)
      datalayer_outbounds
      ;;

    datalayer-datashim)
      datalayer_datashim
      ;;

    datalayer-cuda-operator)
      datalayer_cuda_operator
      ;;

    datalayer-solr-operator)
      datalayer_solr_operator
      ;;

    jupyterpool)
      jupyterpool
      ;;

    jupyter-server)
      jupyter_server
      ;;

    jupyter-editor)
      jupyter_editor
      ;;

    datalayer-config)
      datalayer_config
      ;;

    datalayer-vault)
      datalayer_vault
      ;;

    datalayer-kafka)
      datalayer_kafka
      ;;

    datalayer-pulsar)
      datalayer_pulsar
      ;;

    datalayer-ldap)
      datalayer_ldap
      ;;

    datalayer-ldapadmin)
      datalayer_ldapadmin
      ;;

    datalayer-keycloak)
      datalayer_keycloak
      ;;

    datalayer-falco)
      datalayer_falco
      ;;

    datalayer-observer)
      datalayer_observer
      ;;

    datalayer-manager)
      datalayer_manager
      ;;

    datalayer-iam)
      datalayer_iam
      ;;

    datalayer-success)
      datalayer_success
      ;;

    datalayer-support)
      datalayer_support
      ;;

    datalayer-growth)
      datalayer_growth
      ;;

    datalayer-operator)
      datalayer_operator
      ;;

    datalayer-openfga)
      datalayer_openfga
      ;;

    datalayer-ai-agents)
      datalayer_ai_agents
      ;;

    datalayer-spacer)
      datalayer_spacer
      ;;

    datalayer-library)
      datalayer_library
      ;;

    datalayer-jupyter)
      datalayer_jupyter
      ;;

    jupyterhub)
      jupyterhub
      ;;

    datalayer-minio)
      datalayer_minio
      ;;

    datalayer-jump)
      datalayer_jump
      ;;

    datalayer-content)
      datalayer_content
      ;;

    datalayer-editor)
      datalayer_editor
      ;;

    example-simple)
      example_simple
      ;;

    *)
      echo -e $RED$BOLD"💔  Unknown command: $1"$NOBOLD$NOCOLOR 1>&2
      echo
      commands
      echo
      exit 1

  esac

  echo
  echo -e $BOLD"🛑  [$BLUE$1$NOCOLOR] is removed."$NOBOLD

}

IFS=',' read -ra CMD_SPLITS <<< "$CMDS"
for i in "${CMD_SPLITS[@]}"; do
  apply_cmd $i
  echo
done
