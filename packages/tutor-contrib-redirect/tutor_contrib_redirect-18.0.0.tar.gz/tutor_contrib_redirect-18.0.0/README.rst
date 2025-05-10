redirect plugin for `Tutor <https://docs.tutor.edly.io>`__
##########################################################

Easily redirect www to non-www LMS host in Kubernetes deployments of Open edX.

Requires nginx-ingress and cert-manager, as used by `Harmony <https://github.com/openedx/openedx-k8s-harmony>`_


Installation
************

.. code-block:: bash

    pip install git+https://github.com/aulasneo/tutor-contrib-redirect.git

Usage
*****

.. code-block:: bash

    tutor plugins enable redirect
    tutor k8s start

By default, the subdomain redirected is ``www``. If you want something else, set ``REDIRECT_SUBDOMAIN``.

License
*******

This software is licensed under the terms of the AGPLv3.
