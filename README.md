This example demonstrate how to deploy docker-stack notebook containers to any Docker Machine-controlled host using Docker Compose.

## Prerequisites

* [Docker Engine](https://docs.docker.com/engine/) 1.10.0+
* [Docker Machine](https://docs.docker.com/machine/) 0.6.0+
* [Docker Compose](https://docs.docker.com/compose/) 1.6.0+

See the [installation instructions](https://docs.docker.com/engine/installation/) for your environment.

## Quickstart

Build and run a `jupyter/minimal-notebook` container on a VirtualBox VM on local desktop.

```
# create a Docker Machine-controlled VirtualBox VM
bin/vbox.sh mymachine

# activate the docker machine
eval "$(docker-machine env mymachine)"

# build the notebook image on the machine
notebook/build.sh

# bring up the notebook container
notebook/up.sh
```

To stop and remove the container:

```
notebook/down.sh
```


## FAQ

### How do I specify which docker-stack notebook image to deploy?

You can customize the docker-stack notebook image to deploy by modifying the `notebook/Dockerfile`.  For example, you can build and deploy a `jupyter/all-spark-notebook` by modifying the Dockerfile like so:

```
FROM jupyter/all-spark-notebook:55d5ca6be183
...
```

Once you modify the Dockerfile, don't forget to rebuild the image.

```
# activate the docker machine
eval "$(docker-machine env mymachine)"

notebook/build.sh
```

### Can I run multiple notebook containers on the same VM?

Yes. Set environment variables to specify unique names and ports when running the `up.sh` command.

```
NAME=my-notebook PORT=9000 notebook/up.sh
NAME=your-notebook PORT=9001 notebook/up.sh
```

To stop and remove the containers:

```
NAME=my-notebook notebook/down.sh
NAME=your-notebook notebook/down.sh
```

### Where are my notebooks stored?

The `up.sh` creates a Docker volume named after the notebook container with a `-work` suffix, e.g., `my-notebook-work`.


### Can multiple notebook containers share the same notebook volume?

Yes. Set the `WORK_VOLUME` environment variable to the same value for each notebook.

```
NAME=my-notebook PORT=9000 WORK_VOLUME=our-work notebook/up.sh
NAME=your-notebook PORT=9001 WORK_VOLUME=our-work notebook/up.sh
```

### How do I run over HTTPS?

To run the notebook server with a self-signed certificate, pass the `--secure` option to the `up.sh` script.  You must also provide a password, which will be used to secure the notebook server.  You can specify the password by setting the `PASSWORD` environment variable, or by passing it to the `up.sh` script.  

```
PASSWORD=a_secret notebook/up.sh --secure

# or
notebook/up.sh --secure --password a_secret
```

### Can I use Let's Encrypt certificate chains?

Sure.  If you want to secure access to publicly addressable notebook containers, you can generate a free certificate using the [Let's Encrypt](https://letsencrypt.org) service.


This example includes the `bin/letsencrypt.sh` script, which runs the `letsencrypt` client to create a full-chain certificate and private key, and stores them in a Docker volume.  _Note:_ The script hard codes several `letsencrypt` options, one of which automatically agrees to the Let's Encrypt Terms of Service.

The following command will create a certificate chain and store it in a Docker volume named `mydomain-secrets`.

```
FQDN=host.mydomain.com EMAIL=myemail@somewhere.com \
  SECRETS_VOLUME=mydomain-secrets \
  bin/letsencrypt.sh
```

Now run `up.sh` with the `--letsencrypt` option.  You must also provide the name of the secrets volume and a password.

```
PASSWORD=a_secret SECRETS_VOLUME=mydomain-secrets notebook/up.sh --letsencrypt

# or
notebook/up.sh --letsencrypt --password a_secret --secrets mydomain-secrets
```

Be aware that Let's Encrypt has a pretty [low rate limit per domain](https://community.letsencrypt.org/t/public-beta-rate-limits/4772/3) at the moment.  You can avoid exhausting your limit by testing against the Let's Encrypt staging servers.  To hit their staging servers, set the environment variable `CERT_SERVER=--staging`.

```
FQDN=host.mydomain.com EMAIL=myemail@somewhere.com \
  CERT_SERVER=--staging \
  bin/letsencrypt.sh
```

Also, be aware that Let's Encrypt certificates are short lived (90 days).  If you need them for a longer period of time, you'll need to manually setup a cron job to run the renewal steps. (You can reuse the command above.)

### Can I deploy to any Docker Machine host?

Yes, you should be able to deploy to any Docker Machine-controlled host.  To make it easier to get up and running, this example includes scripts to provision Docker Machines to VirtualBox and IBM SoftLayer, but more scripts are welcome!

To create a Docker machine using a VirtualBox VM on local desktop:

```
bin/vbox.sh mymachine
```

To create a Docker machine using a virtual device on IBM SoftLayer:

```
export SOFTLAYER_USER=my_softlayer_username
export SOFTLAYER_API_KEY=my_softlayer_api_key
export SOFTLAYER_DOMAIN=my.domain

# Create virtual device
bin/softlayer.sh myhost

# Add DNS entry (SoftLayer DNS zone must exist for SOFTLAYER_DOMAIN)
bin/sl-dns.sh myhost
```


## Troubleshooting

### Unable to connect to VirtualBox VM on Mac OS X when using Cisco VPN client.

The Cisco VPN client blocks access to IP addresses that it does not know about, and may block access to a new VM if it is created while the Cisco VPN client is running.

1. Stop Cisco VPN client. (It does not allow modifications to route table).
2. Run `ifconfig` to list `vboxnet` virtual network devices.
3. Run `sudo route -nv add -net 192.168.99 -interface vboxnetX`, where X is the number of the virtual device assigned to the VirtualBox VM.
4. Start Cisco VPN client.



# jupyter notebook - tensorflow README

![docker pulls](https://img.shields.io/docker/pulls/jupyter/tensorflow-notebook.svg) ![docker stars](https://img.shields.io/docker/stars/jupyter/tensorflow-notebook.svg) [![](https://images.microbadger.com/badges/image/jupyter/tensorflow-notebook.svg)](https://microbadger.com/images/jupyter/tensorflow-notebook "jupyter/tensorflow-notebook image metadata")

# Jupyter Notebook Scientific Python Stack + Tensorflow

## What it Gives You

* Everything in [Scipy Notebook](https://github.com/jupyter/docker-stacks/tree/master/scipy-notebook)
* Tensorflow and Keras for Python 3.x (without GPU support)

## Basic Use

The following command starts a container with the Notebook server listening for HTTP connections on port 8888 with a randomly generated authentication token configured.

```
docker run -it --rm -p 8888:8888 jupyter/tensorflow-notebook
```

Take note of the authentication token included in the notebook startup log messages. Include it in the URL you visit to access the Notebook server or enter it in the Notebook login form.

## Tensorflow Single Machine Mode

As distributed tensorflow is still immature, we currently only provide the single machine mode.

```
import tensorflow as tf

hello = tf.Variable('Hello World!')

sess = tf.Session()
init = tf.global_variables_initializer()

sess.run(init)
sess.run(hello)
```

## Notebook Options

The Docker container executes a [`start-notebook.sh` script](../base-notebook/start-notebook.sh) script by default. The `start-notebook.sh` script handles the `NB_UID`, `NB_GID` and `GRANT_SUDO` features documented in the next section, and then executes the `jupyter notebook`.

You can pass [Jupyter command line options](https://jupyter.readthedocs.io/en/latest/projects/jupyter-command.html) through the `start-notebook.sh` script when launching the container. For example, to secure the Notebook server with a custom password hashed using `IPython.lib.passwd()` instead of the default token, run the following:

```
docker run -d -p 8888:8888 jupyter/tensorflow-notebook start-notebook.sh --NotebookApp.password='sha1:74ba40f8a388:c913541b7ee99d15d5ed31d4226bf7838f83a50e'
```

For example, to set the base URL of the notebook server, run the following:

```
docker run -d -p 8888:8888 jupyter/tensorflow-notebook start-notebook.sh --NotebookApp.base_url=/some/path
```

For example, to disable all authentication mechanisms (not a recommended practice):

```
docker run -d -p 8888:8888 jupyter/tensorflow-notebook start-notebook.sh --NotebookApp.token=''
```

You can sidestep the `start-notebook.sh` script and run your own commands in the container. See the *Alternative Commands* section later in this document for more information.

## Docker Options

You may customize the execution of the Docker container and the command it is running with the following optional arguments.

* `-e GEN_CERT=yes` - Generates a self-signed SSL certificate and configures Jupyter Notebook to use it to accept encrypted HTTPS connections.
* `-e NB_UID=1000` - Specify the uid of the `jovyan` user. Useful to mount host volumes with specific file ownership. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adjusting the user id.)
* `-e NB_GID=100` - Specify the gid of the `jovyan` user. Useful to mount host volumes with specific file ownership. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adjusting the group id.)
* `-e GRANT_SUDO=yes` - Gives the `jovyan` user passwordless `sudo` capability. Useful for installing OS packages. For this option to take effect, you must run the container with `--user root`. (The `start-notebook.sh` script will `su jovyan` after adding `jovyan` to sudoers.) **You should only enable `sudo` if you trust the user or if the container is running on an isolated host.**
* `-v /some/host/folder/for/work:/home/jovyan/work` - Mounts a host machine directory as folder in the container. Useful when you want to preserve notebooks and other work even after the container is destroyed. **You must grant the within-container notebook user or group (`NB_UID` or `NB_GID`) write access to the host directory (e.g., `sudo chown 1000 /some/host/folder/for/work`).**

## SSL Certificates

You may mount SSL key and certificate files into a container and configure Jupyter Notebook to use them to accept HTTPS connections. For example, to mount a host folder containing a `notebook.key` and `notebook.crt`:

```
docker run -d -p 8888:8888 \
    -v /some/host/folder:/etc/ssl/notebook \
    jupyter/tensorflow-notebook start-notebook.sh \
    --NotebookApp.keyfile=/etc/ssl/notebook/notebook.key
    --NotebookApp.certfile=/etc/ssl/notebook/notebook.crt
```

Alternatively, you may mount a single PEM file containing both the key and certificate. For example:

```
docker run -d -p 8888:8888 \
    -v /some/host/folder/notebook.pem:/etc/ssl/notebook.pem \
    jupyter/tensorflow-notebook start-notebook.sh \
    --NotebookApp.certfile=/etc/ssl/notebook.pem
```

In either case, Jupyter Notebook expects the key and certificate to be a base64 encoded text file. The certificate file or PEM may contain one or more certificates (e.g., server, intermediate, and root).

For additional information about using SSL, see the following:

* The [docker-stacks/examples](https://github.com/jupyter/docker-stacks/tree/master/examples) for information about how to use [Let's Encrypt](https://letsencrypt.org/) certificates when you run these stacks on a publicly visible domain.
* The [jupyter_notebook_config.py](jupyter_notebook_config.py) file for how this Docker image generates a self-signed certificate.
* The [Jupyter Notebook documentation](https://jupyter-notebook.readthedocs.io/en/latest/public_server.html#using-ssl-for-encrypted-communication) for best practices about running a public notebook server in general, most of which are encoded in this image.


## Conda Environments

The default Python 3.x [Conda environment](http://conda.pydata.org/docs/using/envs.html) resides in `/opt/conda`. 

The commands `jupyter`, `ipython`, `python`, `pip`, and `conda` (among others) are available in both environments. For convenience, you can install packages into either environment regardless of what environment is currently active using commands like the following:

```
# install a package into the default (python 3.x) environment
pip install some-package
conda install some-package
```


## Alternative Commands

### start.sh

The `start.sh` script supports the same features as the default `start-notebook.sh` script (e.g., `GRANT_SUDO`), but allows you to specify an arbitrary command to execute. For example, to run the text-based `ipython` console in a container, do the following:

```
docker run -it --rm jupyter/tensorflow-notebook start.sh ipython
```

Or, to run JupyterLab instead of the classic notebook, run the following:

```
docker run -it --rm -p 8888:8888 jupyter/tensorflow-notebook start.sh jupyter lab
```

This script is particularly useful when you derive a new Dockerfile from this image and install additional Jupyter applications with subcommands like `jupyter console`, `jupyter kernelgateway`, etc.

### Others

You can bypass the provided scripts and specify your an arbitrary start command. If you do, keep in mind that certain features documented above will not function (e.g., `GRANT_SUDO`).

