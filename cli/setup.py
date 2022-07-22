from setuptools import setup, find_packages


setup(
   name='sarf',
   version='0.2.0',
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
   description='This package allows you to save cli tools outputs into sarf',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   install_requires=[
       "dependency-injector",
        "awesome-messages",
        "pyyaml"
   ],
   entry_points = {
       "console_scripts": [
           "sarf = sarf.sarf:main"
       ]
   }
)
