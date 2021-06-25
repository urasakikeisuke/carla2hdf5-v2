#!/bin/bash

CARLA_VERSION="0.9.11"

docker run \
  -it --rm \
  -p 2000-2002:2000-2002 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --privileged \
  --net=host \
  -e DISPLAY=$DISPLAY\
  --gpus all \
  --name="carla-server-0.9.11" \
  carla-server:${CARLA_VERSION} \
  bash

# bash -c "SDL_HINT_CUDA_DEVICE=0 ./CarlaUE4.sh -opengl"