from setuptools import setup, find_packages


setup(
   name='sarf',
   version='0.3.0',
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
   description='''SARF CLI. A security assesment tool that serves as a glue between security
tools. SARF also let you write vulnerabilities using vulnerability templates and store them
inside reports of a project. SARF is prepared to be extended with in your own environment
to satisfy your needs.
''',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   install_requires=[
        "dependency-injector>=4.41,<5.0",
        "awesome-messages=>=1.0.0,<2.0",
        "PyYAML>=6.0,<7.0",
        "PyInquirer>=1.0.3,<2.0",
        "datalift>=0.1.2,<1.0",
        "sarf-simple-crud>=0.1.0,<1.0"
   ],
   entry_points = {
       "console_scripts": [
           "sarf = sarf.sarf:main"
       ]
   }
)
