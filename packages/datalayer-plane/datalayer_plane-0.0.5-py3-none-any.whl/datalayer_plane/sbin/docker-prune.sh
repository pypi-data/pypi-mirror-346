#!/usr/bin/env bash

# Copyright (c) 2023-2024 Datalayer, Inc.
#
# Datalayer License

echo -e $YELLOW$BOLD"Docker system prune --force..."$NOBOLD$NOCOLOR
echo

# Just use docker images -a options to know all the images with layers.
# To know particular layers of particular images you can use `docker history $image_name`.
# Also there is a option to remove dangling images by which you can delete it.
# Dangling images: Docker images consist of multiple layers.
# Dangling images are layers that have no relationship to any tagged images.
# They no longer serve a purpose and consume disk space.
# They can be located by adding the filter flag, -f with a value of dangling=true to the docker images command.
# When you're sure you want to delete them, you can add the -q flag, then pass their ID to `docker rmi`.
docker system prune
docker system prune --force
echo

echo -e $YELLOW$BOLD"Deleting Live Docker Containers..."$NOBOLD$NOCOLOR
echo
docker rm $(docker ps -a -q)
echo

echo -e $YELLOW$BOLD"Deleting Dangling Docker Images..."$NOBOLD$NOCOLOR
echo
docker rmi $(docker images -f dangling=true -q)
echo

echo -e $YELLOW$BOLD"Deleting Orphaned Docker Images..."$NOBOLD$NOCOLOR
echo
docker rmi -f --no-prune=false $(docker images | awk '/^<none>/ {print $3}')
echo

# echo -e $YELLOW$BOLD"Deleting all images"$NOBOLD$NOCOLOR
# echo
# docker rmi $(docker images -q)
# echo

echo -e $YELLOW$BOLD"Deleting Unused Docker Volumes..."$NOBOLD$NOCOLOR
echo
docker volume ls
docker volume prune
echo
