#!/bin/bash
BUILD_DIR=$(dirname $(readlink -f $0))

PYTHON_VERSION="3.7.9"
CARLA_VERSION="0.9.11"
CARLA_EGG_VERSION="0.9.11"

docker build \
    -t carla-server:${CARLA_VERSION} \
    -f ${BUILD_DIR}/Dockerfile.server \
    --build-arg CARLA_VERSION=${CARLA_VERSION} \
    ${BUILD_DIR}

docker build \
    -t carla2hdf5:${CARLA_VERSION} \
    -f ${BUILD_DIR}/Dockerfile.carla2hdf5 \
    --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
    --build-arg CARLA_VERSION=${CARLA_VERSION} \
    --build-arg CARLA_EGG_VERSION=${CARLA_EGG_VERSION} \
    ${BUILD_DIR}
