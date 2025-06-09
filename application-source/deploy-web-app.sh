#! /usr/bin/env bash
set -e

podman build --no-cache -t agentic-ai-query .
podman tag localhost/agentic-ai-query:latest docker.io/psamouelian/agentic-ai-query:latest
podman push docker.io/psamouelian/agentic-ai-query:latest

helm uninstall agentic-ai-query --ignore-not-found
helm install agentic-ai-query .