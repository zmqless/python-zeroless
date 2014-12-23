from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='zeroless',
      version='0.1',
      description='A pythonic approach for distributed systems with ZeroMQ.',
      long_description=readme(),
      url='https://github.com/zmqless/zeroless',
      author='Lucas Lira Gomes',
      author_email='x8lucas8x@gmail.com',
      license='LGPL3',
      packages=['zeroless'],
      install_requires=[
          'pyzmq',
      ],
      zip_safe=False)
