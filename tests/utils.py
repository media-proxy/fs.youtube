# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    from unittest import mock
except ImportError:
    import mock

import os
import time
import fs

try:
    import docker
    docker_client = docker.from_env(version='auto')
    docker_client.info()
except Exception:
    DOCKER = False
else:
    DOCKER = True

try:
    from unittest import mock  # pylint: disable=unused-import
except ImportError:
    import mock  # pylint: disable=unused-import

CI = os.getenv('CI', '').lower() == 'true'
FSVERSION = tuple(map(int, fs.__version__.split('.')))

if DOCKER:
    pass
time.sleep(15)
