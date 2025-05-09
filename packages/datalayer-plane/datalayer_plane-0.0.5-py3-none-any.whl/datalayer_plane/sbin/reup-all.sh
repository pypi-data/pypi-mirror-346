#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Reup All Services"$NOCOLOR$NOBOLD
echo

for SERVICE in datalayer-iam datalayer-operator datalayer-jupyter datalayer-spacer datalayer-library datalayer-manager datalayer-ai-agents datalayer-success datalayer-growth
do
    echo -----------------------------------------------
    echo -e $BOLD"Redeploying [${GREEN}$SERVICE${NOCOLOR}]"$NOBOLD
    echo
    p reup $SERVICE
    echo
done
