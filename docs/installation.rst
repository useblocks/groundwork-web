Installation
============


Virtual Environment
-------------------
If you like, you can setup a virtual environment for python before installation::

    python -m venv NAME_OF_ENV

pip
---
groundwork-web can be easily installed by using pip::

    pip install groundwork-web

After installation, all plugins were automatically registered and available.

git and buildout
----------------

If need the source code of groundwork-web, it's helpful to use also buildout to integrate other groundwork
libraries as source code as well::

    git clone https://github.com/useblocks/groundwork-web
    python bootstrap.py
    bin/buildout

