# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from jupyter_core.paths import jupyter_data_dir
import subprocess
import os
import errno
import stat


# One could call get_config() directly, but it isn't defined in every
# environment. This solution makes the linter happy.
c = globals()['get_config']()
# c = get_config()

c.NotebookApp.ip = '*'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False

# Kernel config
c.InteractiveShellApp.matplotlib = 'notebook'


# Generate a self-signed certificate
if 'GEN_CERT' in os.environ:
    print("*** Creating self-signed certificate")
    dir_name = jupyter_data_dir()
    print("jupyter data dir: {}".format(dir_name))
    pem_file = os.path.join(dir_name, 'notebook.pem')
    try:
        os.makedirs(dir_name)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dir_name):
            pass
        else:
            raise
    # Generate a certificate if one doesn't exist on disk
    subprocess.check_call(['openssl', 'req', '-new',
                           '-newkey', 'rsa:2048',
                           '-days', '365',
                           '-nodes', '-x509',
                           '-subj', '/C=XX/ST=XX/L=XX/O=generated/CN=generated',
                           '-keyout', pem_file,
                           '-out', pem_file])
    # Restrict access to the file
    os.chmod(pem_file, stat.S_IRUSR | stat.S_IWUSR)
    c.NotebookApp.certfile = pem_file

# passwd hash created using notebook.auth.passwd()
c.NotebookApp.password = u'sha1:8471295b2d9a:2d07c7f0ab380357b2affe0b152f8059359d3c9b'
