from setuptools import setup

with open("README.md") as f:
  long_description = f.read()

setup(
  name = 'mh_z19',
  packages = ['mh_z19'], # this must be the same as the name above
  version = '3.0.3',
  description = 'mh-z19 CO2 concentration sensor library for All models of Raspberry Pi',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Takeyuki UEDA',
  author_email = 'gde00107@nifty.com',
  license='MIT',
  url = 'https://github.com/UedaTakeyuki/mh-z19', # use the URL to the github repo
  keywords = ['sensor', 'IoT', 'Raspberry Pi', 'mh-z19', 'CO2'], # arbitrary keywords
  classifiers = ['Development Status :: 5 - Production/Stable',
                 'Programming Language :: Python',
                 'Topic :: Terminals'
  ],
  install_requires=[
    'getrpimodel',
    'pyserial',
    'requests',
    'argparse',
    'RPi.GPIO'
  ]
)
