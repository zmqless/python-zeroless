from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='zeroless',
      version='0.2.0',
      description='A pythonic approach for distributed systems with ZeroMQ.',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
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
      zip_safe=False)
