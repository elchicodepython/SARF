from setuptools import setup, find_packages


setup(
   name='sarf_zeromq_bridge',
   version='0.1.1',
   author='Samuel López Saura',
   author_email='samuellopezsaura@gmail.com',
   packages=find_packages(),
   license='MIT',
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   description='Bridge between SARF messages and zeroMQ protocol',
   install_requires=[
       "sarf_listener",
       "awesome_messages>=1.0",
       "pyzmq>=24.0.1,<25.0.0"
   ],
   entry_points = {
       "console_scripts": [
           "sarf_zeromq_bridge = sarf_zeromq_bridge.zeromq_bridge:main"
       ]
   }
)
