from setuptools import setup, find_packages

VERSION = '1.1.0'
require_pakages = [
    'requests',
    'kssdutils',
    'urllib3==1.26.15'
]
setup(name='ssbpp',
      version=VERSION,
      description="SSBPP: A Real-time Strain Submission and Monitoring Platform for Epidemic Prevention Based on Phylogenetic Placement ",
      classifiers=[],
      keywords='ssbpp',
      author='Hang Yang',
      author_email='1090692248@qq.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=require_pakages,
      entry_points={
          'console_scripts': [
              'ssbpp = ssbpp.case:main'
          ]
      }
      )
