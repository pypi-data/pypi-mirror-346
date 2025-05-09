#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"[$1] Logs"$NOCOLOR$NOBOLD
echo

case "$1" in

  iam)
    kubectl logs -n datalayer-api $(kubectl get pod -n datalayer-api --selector=app=iam -o jsonpath='{.items...metadata.name}') -f
    ;;

  jupyter)
    kubectl logs -n datalayer-api $(kubectl get pod -n datalayer-api --selector=app=jupyter -o jsonpath='{.items...metadata.name}') -f
    ;;

  operator)
    kubectl logs -n datalayer-jupyter $(kubectl get pod -n datalayer-jupyter --selector=app=operator -o jsonpath='{.items...metadata.name}') -f
    ;;

  growth)
    kubectl logs -n datalayer-api $(kubectl get pod -n datalayer-api --selector=app=growth -o jsonpath='{.items...metadata.name}') -f
    ;;

  growth)
    kubectl logs -n datalayer-api $(kubectl get pod -n datalayer-api --selector=app=growth -o jsonpath='{.items...metadata.name}') -f
    ;;

  inbounds)
    kubectl logs -n datalayer-api $(kubectl get pod -n datalayer-api --selector=app=inbounds -o jsonpath='{.items...metadata.name}') -f
    ;;

  outbounds)
    kubectl logs -n datalayer-growth $(kubectl get pod -n datalayer-growth --selector=app=outbounds -o jsonpath='{.items...metadata.name}') -f
    ;;

  *)
    echo -e $RED$BOLD"💔  Unknown: $1"$NOBOLD$NOCOLOR 1>&2
    echo

esac
