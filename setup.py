from setuptools import setup

setup(
      name='SeaPy',
      version='0.0',
      description="Statistical Energy Analysis module for Python.",
      long_description=open('README.txt').read(),
      author='Frederik Rietdijk',
      author_email='fridh@fridh.nl',
      license='LICENSE.txt',
      packages=['seapy'],
      scripts=['bin/beams.py'],
      zip_safe=False,
      install_requires=[
          'numpy',
          'matplotlib'
          ],
      )