#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Port Forward to Kafka Broker"$NOCOLOR$NOBOLD
echo

echo
echo Connect to http://localhost:9092 for Kafka Broker
echo
echo Read more on https://datalayer.tech/docs/platform/kubernetes/services/system/kafka
echo

kubectl port-forward -n datalayer-kafka service/datalayer-kafka-kafka-brokers 9092:9092
