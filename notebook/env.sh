#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Set default values for environment variables required by notebook compose
# configuration file.

# Container name
: "${NAME:=my-notebook}"
export NAME

# Exposed container port
: ${PORT:=8888}
export PORT

# MJP: set path to project-notebooks
# : "${NOTEBOOK_PATH:=/Users/mpesavento/src/project_notebooks}"
# : "${WORK_VOLUME:=$NOTEBOOK_PATH}"

# Container work volume name
: "${WORK_VOLUME:=$NAME-work}"
export WORK_VOLUME

# Container secrets volume name
: "${SECRETS_VOLUME:=$NAME-secrets}"
export SECRETS_VOLUME
