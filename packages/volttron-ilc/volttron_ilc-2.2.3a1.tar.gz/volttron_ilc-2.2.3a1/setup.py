# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ilc']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=2.0.0',
 'scipy>=1.6.0',
 'sympy>=1.12,<2.0',
 'transitions>=0.9.0,<0.10.0',
 'volttron-core>=2.0.0rc0']

entry_points = \
{'console_scripts': ['volttron-ilc = ilc.ilc_agent:main']}

setup_kwargs = {
    'name': 'volttron-ilc',
    'version': '2.2.3a1',
    'description': 'ILC supports traditional demand response as well as transactive energy services. ILC manages controllable loads while also mitigating service-level excursions (e.g., occupant comfort, minimizing equipment ON/OFF cycling) by dynamically prioritizing available loads for curtailment using both quantitative (deviation of zone conditions from set point) and qualitative rules (type of zone).IXME',
    'long_description': '# Intelligent Load Control (ILC) Agent\n\n![Eclipse VOLTTRON 10.0.5rc0](https://img.shields.io/badge/Eclipse%20VOLTTRON-10.0.5rc0-red.svg)\n![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)\n![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)\n[![pypi version](https://img.shields.io/pypi/v/volttron-ilc.svg)](https://pypi.org/project/volttron-ilc/)\n\nMain branch tests:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [![Main Branch Passing?](https://github.com/eclipse-volttron/volttron-ilc/actions/workflows/run-tests.yml/badge.svg?branch=main)](https://github.com/eclipse-volttron/volttron-ilc/actions/workflows/run-tests.yml)\n\nDevelop branch tests:&nbsp;&nbsp; [![Develop Branch Passing?](https://github.com/eclipse-volttron/volttron-ilc/actions/workflows/run-tests.yml/badge.svg?branch=develop)](https://github.com/eclipse-volttron/volttron-ilc/actions/workflows/run-tests.yml)\n\n\nILC supports traditional demand response as well as transactive energy\nservices. ILC manages controllable loads while also mitigating\nservice-level excursions (e.g., occupant comfort, minimizing equipment\nON/OFF cycling) by dynamically prioritizing available loads for curtailment\nusing both quantitative (deviation of zone conditions from set point) and\nqualitative rules (type of zone).\n\n## Requirements\n\n* python >= 3.10\n* volttron >= 10.0 \n* sympy >= 1.12\n* transitions >= 0.9.0\n\n## Documentation\n\nMore detailed documentation can be found on\n[ReadTheDocs](https://eclipse-volttron.readthedocs.io/en/latest/external-docs/volttron-ilc/index.html). The RST source\nof the documentation for this agent is located in the "docs" directory of this repository.\n\n## ILC Agent Configuration\n\nThe  ILC agent, requires four configuration files per device cluster (i.e., homogenous set of devices).  These\nfiles should be loaded into the agent\'s config store via vctl config command line interface.  Samples of these files\nmay be found in the sample_configs directory of this repository:\n 1. config - ILC (main) configuration.\n 2. control_config - Contains information related to the control of device cluster. \n 3. criteria_config - Contains information related to the use of real time data to prioritize devices within\n    cluster for load management. \n 4. pairwise_criteria.json - Contains information related to the relative importance of each criteria for a device cluster.\n    \nFull documentation of ILC configurations can be found on\n[ReadTheDocs](https://eclipse-volttron.readthedocs.io/en/latest/external-docs/volttron-ilc/index.html).\nA web-based configuration tool has been developed to simplify creation of the configuration files for ILC.\nThe web tool can be accessed [here](https://ilc-configuration-tool.web.app/).\n\nInstructions for the configuration web-tool can be found [here](https://userguide-ilc.readthedocs.io/en/latest/).\n\n## Installation\n\nBefore installing, VOLTTRON should be installed and running.  Its virtual environment should be active.\nInformation on how to install of the VOLTTRON platform can be found\n[here](https://github.com/eclipse-volttron/volttron-core).\n\nInstall and start the Intelligent Load Control Agent.\n\n```shell\nvctl config store ilc.agent config <path of config file>\nvctl config store ilc.agent control_config <path to device_control_config>\nvctl config store ilc.agent criteria_config <path to device_criteria_config>\nvctl config store ilc.agent pairwise_criteria.json <path to pairwise_criteria_config>\nvctl install volttron-ilc --vip-identity ilc.agent --tag ilc --start\n```\n\nView the status of the installed agent\n\n```shell\nvctl status\n```\n\n## Development\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)\n',
    'author': 'Robert Lutes',
    'author_email': 'robert.lutes@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eclipse-volttron/volttron-ilc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
