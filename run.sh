#!/bin/bash

# 기본 변수 설정
IMAGE_NAME="resource-alert"
CONTAINER_NAME="resource-alert"
ENV_FILE=".env"
DOCKER_SOCK="/var/run/docker.sock" # Docker 소켓 경로

# 실행 중인 컨테이너가 이미 있는지 확인
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping and removing existing container: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME && docker rm $CONTAINER_NAME
fi

# 컨테이너 실행
echo "Starting container: $CONTAINER_NAME"
docker run \
  --name $CONTAINER_NAME \
  --env-file $ENV_FILE \
  -v $DOCKER_SOCK:$DOCKER_SOCK \
  -d $IMAGE_NAME

# 실행 상태 확인
if [ $? -eq 0 ]; then
    echo "Container $CONTAINER_NAME started successfully."
    echo "Use 'docker logs $CONTAINER_NAME' to view logs."
else
    echo "Failed to start container $CONTAINER_NAME."
fi
