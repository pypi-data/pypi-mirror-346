#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $BOLD$YELLOW"Datalayer Local Plane"$NOCOLOR$NOBOLD
echo

# export OTEL_PYTHON_LOG_LEVEL=debug
export OTEL_PYTHON_LOG_LEVEL=info
echo -e $YELLOW"Setting OTEL_PYTHON_LOG_LEVEL=${OTEL_PYTHON_LOG_LEVEL}"$NOCOLOR
echo

export OTEL_SDK_DISABLED="true"
echo -e $YELLOW"Setting OTEL_SDK_DISABLED=${OTEL_SDK_DISABLED}"$NOCOLOR
echo

export DATALAYER_PUB_SUB_ENGINE="kafka"
echo -e $YELLOW"Setting DATALAYER_PUB_SUB_ENGINE=${DATALAYER_PUB_SUB_ENGINE}"$NOCOLOR

export DATALAYER_KAFKA_URL="localhost:9092"
echo -e $YELLOW"Setting DATALAYER_KAFKA_URL=${DATALAYER_KAFKA_URL}"$NOCOLOR

export DATALAYER_VAULT_URL="http://localhost:8200"
echo -e $YELLOW"Setting DATALAYER_VAULT_URL=${DATALAYER_VAULT_URL}"$NOCOLOR
echo

export DATALAYER_RTC_ROOM_WS_URL="ws://localhost:9900/api/spacer/v1/rooms"
echo -e $YELLOW"Setting DATALAYER_RTC_ROOM_WS_URL=${DATALAYER_RTC_ROOM_WS_URL}"$NOCOLOR
echo

echo -e $YELLOW"Starting local IAM service..."$NOCOLOR
echo open http://localhost:9700/api/iam/version
echo open http://localhost:9700/api/iam/v1/ping
cd $DATALAYER_SERVICES_HOME/iam && \
  make start &
echo

echo -e $YELLOW"Starting local Spacer service..."$NOCOLOR
echo open http://localhost:9900/api/spacer/version
echo open http://localhost:9900/api/spacer/v1/ping
cd $DATALAYER_SERVICES_HOME/spacer && \
  make start &
echo

echo -e $YELLOW"Starting local Library service..."$NOCOLOR
echo open http://localhost:9800/api/library/version
echo open http://localhost:9800/api/library/v1/ping
cd $DATALAYER_SERVICES_HOME/library && \
  make start &
echo

echo -e $YELLOW"Starting local Success service..."$NOCOLOR
echo open http://localhost:3300/api/success/version
echo open http://localhost:3300/api/success/v1/ping
cd $DATALAYER_SERVICES_HOME/success && \
  make start &
echo

echo -e $YELLOW"Starting local Growth service..."$NOCOLOR
echo open http://localhost:3300/api/growth/version
echo open http://localhost:3300/api/growth/v1/ping
cd $DATALAYER_SERVICES_HOME/growth && \
  make start &
echo

echo -e $YELLOW"Starting local Inbounds service..."$NOCOLOR
echo open http://localhost:7667/api/inbounds/version
echo open http://localhost:7667/api/inbounds/v1/ping
cd $DATALAYER_SERVICES_HOME/inbounds && \
  make start &
echo

echo -e $YELLOW"Starting local Support service..."$NOCOLOR
echo open http://localhost:2200/api/support/version
echo open http://localhost:2200/api/support/v1/ping
cd $DATALAYER_SERVICES_HOME/support && \
  make start &
echo

echo -e $YELLOW"Starting local AI Agent service..."$NOCOLOR
echo open http://localhost:4400/api/ai-agents/version
echo open http://localhost:4400/api/ai-agents/v1/ping
cd $DATALAYER_SERVICES_HOME/ai-agents && \
  make start &
echo

wait

uname_out="$(uname -s)"

case "${uname_out}" in
    Linux*)     export OS=LINUX;;
    Darwin*)    export OS=MACOS;;
#    CYGWIN*)    OS=CYGWIND;;
#    MINGW*)     OS=MINGW;;
    *)          export OS="UNSUPPORTED:${unameOut}"
esac

function kill_port() {
    case "${OS}" in
        LINUX)     fuser -k $1/tcp;;
        MACOS)     lsof -i TCP:$1 | grep LISTEN | awk '{print $2}' | xargs kill -9;;
        *)         echo "Unsupported operating system ${OS}"
    esac    
}

kill_port 2200
kill_port 3300
kill_port 4400
kill_port 6660
kill_port 9700
kill_port 9800
kill_port 9900
