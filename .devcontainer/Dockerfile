FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# Remove Yarn APT repo to avoid GPG errors during feature installs
RUN rm -f /etc/apt/sources.list.d/yarn.list /etc/apt/sources.list.d/yarn*.list || true
