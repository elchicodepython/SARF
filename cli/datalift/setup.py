from setuptools import setup, find_packages


setup(
   name='datalift',
   version='0.2.0',
   author='Samuel López Saura',
   author_email='samuellopezsaura@gmail.com',
   packages=find_packages(),
   license='MIT',
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   description='''Datalift it is a command-line tool designed to tools outputs to a storage service.
Users can input data either by passing a filename or through stdout from another tool.''',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   install_requires=[
       "dependency-injector>=4.41,<5.0",
       "boto3>1.34,<2.0",
   ],
   entry_points = {
       "console_scripts": [
           "datalift = datalift.datalift:main"
       ]
   }
)
