"""
groundwork web
==============
"""
from setuptools import setup, find_packages
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('groundwork_web/version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='groundwork-web',
    version=version,
    url='http://groundwork-web.readthedocs.org',
    license='MIT license',
    author='team useblocks',
    author_email='info@useblocks.com',
    description="Package for hosting groundwork apps and plugins like groundwork_web_app or groundwork_web_plugin.",
    long_description=__doc__,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    package_data={'': ['*.html']},
    include_package_data=True,
    platforms='any',
    install_requires=['groundwork-database', 'groundwork',
                      'Flask>0.10.1', 'Flask-Admin', 'Flask-Restless',
                      'pytest-runner', 'sphinx', 'docutils'],
    tests_require=['pytest', 'pytest-flake8'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': ["groundwork_web = "
                            "groundwork_web.applications.groundwork_web_app:start_app"],
        'groundwork.plugin': ["groundwork_web_plugin = "
                              "groundwork_web.plugins.gw_web.gw_web:GwWeb",
                              "groundwork_web_manager_plugin = "
                              "groundwork_web.plugins.gw_web_manager.gw_web_manager:GwWebManager"
                              ],
    }
)
