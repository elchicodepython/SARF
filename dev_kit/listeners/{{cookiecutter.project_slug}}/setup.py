from setuptools import setup, find_packages


setup(
   name='{{cookiecutter.project_slug}}',
   version='{{cookiecutter.package_version}}',
   author='{{cookiecutter.author_name}}',
   author_email='{{cookiecutter.author_email}}',
   packages=find_packages(),
   license='{{cookiecutter.license}}',
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   description='{{cookiecutter.listener_description}}',
   install_requires=[
       "sarf_listener",
   ],
   entry_points = {
       "console_scripts": [
           "{{cookiecutter.project_slug}} = {{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}:main"
       ]
   }
)
