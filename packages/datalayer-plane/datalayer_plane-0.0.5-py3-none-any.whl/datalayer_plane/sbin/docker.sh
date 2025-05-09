#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

declare -a DOCKER_FILES=(
  "datalayer-iam"
  "datalayer-operator"
  "datalayer-jupyter"
  "datalayer-jupyter-companion"
  "datalayer-ai-agents"
  "datalayer-manager"
  "datalayer-spacer"
  "datalayer-library"
  "datalayer-success"
  "datalayer-growth"
  "datalayer-mailer"
  "datalayer-solr"
  "ingress-nginx-controller"
  "jupyter-python"
  "whoami"
#  "datalayer-jump"
#  "example-simple"
#  "example-tornado"
#  "kubectl"
  )

declare -a DOCKER_IMAGES=(
  "datalayer/datalayer-iam:latest"
  "datalayer/datalayer-jupyter-companion:latest"
  "datalayer/datalayer-jupyter:latest"
  "datalayer/datalayer-library:latest"
  "datalayer/datalayer-operator:latest"
  "datalayer/datalayer-ai-agents:latest"
  "datalayer/datalayer-success:latest"
  "datalayer/datalayer-solr:latest"
  "datalayer/datalayer-spacer:latest"
  "datalayer/jupyter-python:latest"
)
