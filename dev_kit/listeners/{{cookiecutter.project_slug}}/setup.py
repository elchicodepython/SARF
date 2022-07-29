from setuptools import setup, find_packages


setup(
   name='{{cookiecutter.project_slug}}',
   version='0.1.0',
   author='Samuel López Saura',
   author_email='samuellopezsaura@gmail.com',
   packages=find_packages(),
   license='MIT',
   url='https://github.com/elchicodepython/SARF-Security-Assesment-and-Reporting-Framework',
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   description='This module allows you to save SARF tools messages into postgresql',
   install_requires=[
       "sarf_listener",
   ],
   entry_points = {
       "console_scripts": [
           "{{cookiecutter.project_slug}} = {{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}:main"
       ]
   }
)
