#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $YELLOW$BOLD"Installing Docker"$NOBOLD$NOCOLOR
echo

function install_on_linux() {
    if ["${awk -F= '/^NAME/{print $2}' /etc/os-release}" == "Ubuntu"]
    then
        echo
    else
        sudo yum update -y
#        sudo yum install -y yum-utils \
#            device-mapper-persistent-data \
#            lvm2
#        sudo yum-config-manager \
#            --add-repo \
#            https://download.docker.com/linux/centos/docker-ce.repo
#        sudo yum update -y
#        sudo yum install -y docker-ce docker-ce-cli containerd.io
        yum install -y docker
    fi
    sudo systemctl start docker
#    sudo service docker start
#    sudo /etc/init.d/docker start
    sudo docker run hello-world
}

function install_on_macos() {
    echo
}

case "${OS}" in
    LINUX)     install_on_linux;;
    MACOS)     install_on_macos;;
    *)         echo "Unsupported operating system ${OS}"
esac
