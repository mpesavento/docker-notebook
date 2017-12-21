#!/bin/bash
docker run -it --rm -p 8888:8888 -v ~/src/project_notebooks:/home/jovyan/project_notebooks jupyter/tensorflow-notebook start-notebook.sh
