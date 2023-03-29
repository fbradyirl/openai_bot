#!/bin/bash

GIT_HASH=$(git log -1 --pretty=%h)

git diff-index --quiet HEAD --; ec=$?

if ! (( ec == 0 )); then
  VERSION="${GIT_HASH}-modified"
else
  VERSION="${GIT_HASH}"
fi

REPO="openai_bot"
TAG="$REPO:$VERSION"
LATEST="${REPO}:latest"
BUILD_TIMESTAMP=$( date '+%F_%H:%M:%S' )

# create an isolated Builder Instance that supported multiple platforms:
docker buildx create --name multi-builder --use || true

# Build and push multi-arch:
# linux/arm64/v8: arm64 (Apple M1)
# linux/amd64: amd64 (Intel)
docker buildx build \
--push \
--platform linux/arm64/v8,linux/amd64 -t "$TAG" -t "$LATEST" --build-arg VERSION="$VERSION" --build-arg BUILD_TIMESTAMP="$BUILD_TIMESTAMP" --build-arg USER .

# (optional) Clean up the builder
#docker buildx rm multi-builder
