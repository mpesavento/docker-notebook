# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Pick your favorite docker-stacks image
FROM jupyter/tensorflow-notebook



USER jovyan

# Add permanent pip/conda installs, data files, other user libs here
# e.g., RUN pip install jupyter_dashboards

USER root

# Add permanent apt-get installs and other root commands here
# e.g., RUN apt-get install npm nodejs

# copy our version of the notebook config in, overwriting the base-notebook version
COPY jupyter_notebook_config.py /etc/jupyter/
