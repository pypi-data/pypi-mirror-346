# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skywalking',
 'skywalking.agent',
 'skywalking.agent.protocol',
 'skywalking.bootstrap',
 'skywalking.bootstrap.cli',
 'skywalking.bootstrap.cli.utility',
 'skywalking.bootstrap.hooks',
 'skywalking.bootstrap.loader',
 'skywalking.client',
 'skywalking.command',
 'skywalking.command.executors',
 'skywalking.log',
 'skywalking.meter',
 'skywalking.meter.pvm',
 'skywalking.plugins',
 'skywalking.profile',
 'skywalking.protocol',
 'skywalking.protocol.browser',
 'skywalking.protocol.common',
 'skywalking.protocol.ebpf',
 'skywalking.protocol.event',
 'skywalking.protocol.language_agent',
 'skywalking.protocol.logging',
 'skywalking.protocol.management',
 'skywalking.protocol.profile',
 'skywalking.protocol.service_mesh_probe',
 'skywalking.sampling',
 'skywalking.trace',
 'skywalking.utils',
 'sw_python',
 'sw_python.src']

package_data = \
{'': ['*']}

install_requires = \
['grpcio', 'grpcio-tools', 'packaging', 'psutil<=5.9.5', 'wrapt']

extras_require = \
{'all': ['requests>=2.26.0',
         'kafka-python',
         'uvloop>=0.17.0,<0.18.0',
         'aiokafka>=0.8.0,<0.9.0',
         'aiohttp>=3.7.4,<4.0.0'],
 'async': ['uvloop>=0.17.0,<0.18.0',
           'aiokafka>=0.8.0,<0.9.0',
           'aiohttp>=3.7.4,<4.0.0'],
 'asynchttp': ['uvloop>=0.17.0,<0.18.0', 'aiohttp>=3.7.4,<4.0.0'],
 'asynckafka': ['uvloop>=0.17.0,<0.18.0', 'aiokafka>=0.8.0,<0.9.0'],
 'http': ['requests>=2.26.0'],
 'kafka': ['kafka-python'],
 'sync': ['requests>=2.26.0', 'kafka-python']}

entry_points = \
{'console_scripts': ['sw-python = skywalking.bootstrap.cli.sw_python:start']}

setup_kwargs = {
    'name': 'apache-skywalking',
    'version': '1.2.0',
    'description': 'The Python Agent for Apache SkyWalking, which provides the native tracing/metrics/logging/profiling abilities for Python projects.',
    'long_description': '# SkyWalking Python Agent\n\n<img src="http://skywalking.apache.org/assets/logo.svg" alt="Sky Walking logo" height="90px" align="right" />\n\n**SkyWalking-Python**: The Python Agent for Apache SkyWalking provides the native tracing/metrics/logging/profiling abilities for Python projects.\n\n**[SkyWalking](https://github.com/apache/skywalking)**: Application performance monitor tool for distributed systems, especially designed for microservices, cloud native and container-based (Kubernetes) architectures.\n\n\n[![GitHub stars](https://img.shields.io/github/stars/apache/skywalking-python.svg?style=for-the-badge&label=Stars&logo=github)](https://github.com/apache/skywalking-python)\n[![Twitter Follow](https://img.shields.io/twitter/follow/asfskywalking.svg?style=for-the-badge&label=Follow&logo=twitter)](https://twitter.com/AsfSkyWalking)\n\n![Release](https://img.shields.io/pypi/v/apache-skywalking)\n![Version](https://img.shields.io/pypi/pyversions/apache-skywalking)\n![Build](https://github.com/apache/skywalking-python/actions/workflows/CI.yaml/badge.svg?event=push)\n\n## Documentation\n\n- [Official documentation](https://skywalking.apache.org/docs/#PythonAgent)\n- [Blog](https://skywalking.apache.org/blog/2021-09-12-skywalking-python-profiling/) about the Python Agent Profiling Feature\n\n## Capabilities\n\n| Reporter  | Supported?      | Details                                                    | \n|:----------|:----------------|:-----------------------------------------------------------|\n| Trace     | ✅ (default: ON) | Automatic instrumentation + Manual SDK                     |            \n| Log       | ✅ (default: ON) | Direct reporter only. (Tracing context in log planned)     |\n| Meter     | ✅ (default: ON) | Meter API + Automatic PVM metrics                          |\n| Event     | ❌ (Planned)     | Report lifecycle events of your awesome Python application |\n| Profiling | ✅ (default: ON) | Threading and Greenlet Profiler                            |\n\n## Installation Requirements\n\nSkyWalking Python Agent requires [Apache SkyWalking 8.0+](https://skywalking.apache.org/downloads/#SkyWalkingAPM) and Python 3.8+.\n\n> If you would like to try out the latest features that are not released yet, please refer to this [guide](docs/en/setup/faq/How-to-build-from-sources.md) to build from sources.\n\n## Live Demo\n- Find the [live demo](https://skywalking.apache.org/#demo) with Python agent on our website.\n- Follow the [showcase](https://skywalking.apache.org/docs/skywalking-showcase/next/readme/) to set up preview deployment quickly.\n\n## Contributing\n\nBefore submitting a pull request or pushing a commit, please read our [contributing](CONTRIBUTING.md) and [developer guide](docs/en/contribution/Developer.md).\n\n## Contact Us\n* Mail list: **dev@skywalking.apache.org**. Mail to `dev-subscribe@skywalking.apache.org`, follow the reply to subscribe the mail list.\n* Send `Request to join SkyWalking slack` mail to the mail list(`dev@skywalking.apache.org`), we will invite you in.\n* Twitter, [ASFSkyWalking](https://twitter.com/AsfSkyWalking)\n* For Chinese speaker, send `[CN] Request to join SkyWalking slack` mail to the mail list(`dev@skywalking.apache.org`), we will invite you in.\n* [bilibili B站 视频](https://space.bilibili.com/390683219)\n\n## License\nApache 2.0\n',
    'author': 'Apache Software Foundation',
    'author_email': 'dev@skywalking.apache.org',
    'maintainer': 'Apache SkyWalking Community',
    'maintainer_email': 'dev@skywalking.apache.org',
    'url': 'https://skywalking.apache.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.13',
}


setup(**setup_kwargs)
