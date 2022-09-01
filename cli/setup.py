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
       "dependency-injector",
        "awesome-messages",
        "pyyaml",
        "pyinquirer"
   ],
   entry_points = {
       "console_scripts": [
           "sarf = sarf.sarf:main"
       ]
   }
)
