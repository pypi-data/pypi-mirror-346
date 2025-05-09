#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Redeploying Datalayer Plane"$NOCOLOR$NOBOLD
echo

DATALAYER_PLANE_SHOW_HEADER=false plane down $1

DATALAYER_PLANE_SHOW_HEADER=false plane up $1
