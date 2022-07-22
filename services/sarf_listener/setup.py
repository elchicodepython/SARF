from setuptools import setup, find_packages


setup(
   name='sarf_listener',
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
   description='Dependency required by sarf listeners',
   install_requires=[
       "sarf",
   ],
)
