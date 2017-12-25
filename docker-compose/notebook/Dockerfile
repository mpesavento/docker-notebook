# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Pick your favorite docker-stacks image
FROM jupyter/tensorflow-notebook



USER jovyan

# Add permanent pip/conda installs, data files, other user libs here
# e.g., RUN pip install jupyter_dashboards

USER root

# create SSL cert
RUN mkdir certs
WORKDIR /root/certs
RUN openssl req \
    -x509 \
    -nodes \
    -days 365 \
    -newkey rsa:1024 \
    -subj "/C=US/ST=CA/L=SanFrancisco/O=Peztek/CN=www.peztek.com" \
    -keyout notebook.pem \
    -out notebook.pem
WORKDIR /root

# Add permanent apt-get installs and other root commands here
# e.g., RUN apt-get install npm nodejs

# copy our version of the notebook config in, overwriting the base-notebook version
COPY jupyter_notebook_config.py /etc/jupyter/

CMD ["jupyter", "notebook", "--port=8888", "--ip=0.0.0.0", "--no-browser", "--allow-root"]