#!/bin/bash
docker run i-it --rm -d -p 8888:8888 -v ~/src/project-notebooks:/home/jovyan/project_notebooks jupyter/tensorflow-notebook start-notebook.sh
