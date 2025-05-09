#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Pushing Datalayer Helm Charts"$NOCOLOR$NOBOLD
echo

cd $PLANE_HOME/etc/helm/charts

for HELM_CHART in iam jupyter operator
do
    echo -----------------------------------------------
    echo -e $BOLD"Packaging Helm Chart [${GREEN}datalayer-$HELM_CHART${NOCOLOR}]"$NOBOLD
    echo
    rm *.tgz || true
    helm package datalayer-$HELM_CHART
    echo
    echo -e $BOLD"Pushing Helm Chart [${GREEN}datalayer-$HELM_CHART${NOCOLOR}]"$NOBOLD
    echo
    helm push *.tgz oci://$DATALAYER_HELM_REGISTRY
    rm *.tgz || true
    echo
done
