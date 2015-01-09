# -*- coding: utf-8 -*-

import sys

from setuptools import setup

from setuptools.command.test import test as TestCommand

class Pytest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='zeroless',
      version='0.5.0',
      description='ZeroMQ for Pythonistas™',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Networking',
          'Topic :: Communications',
          'Topic :: Internet',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)'
      ],
      keywords='pyzmq zeromq zmq networking distributed socket',
      url='https://github.com/zmqless/zeroless',
      author='Lucas Lira Gomes',
      author_email='x8lucas8x@gmail.com',
      license='LGPLv2+',
      packages=['zeroless'],
      install_requires=[
          'pyzmq',
      ],
      cmdclass = {'test': Pytest},
      tests_require=['pytest'],
      zip_safe=False)
