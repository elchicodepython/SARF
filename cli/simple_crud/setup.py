from setuptools import setup, find_packages


setup(
   name='sarf_simple_crud',
   version='0.1.0',
   author='Samuel López Saura',
   author_email='samuellopezsaura@gmail.com',
   packages=find_packages(),
   license='MIT',
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   description='''An extremely simple and basic interface for creating CRUD apps
with an example of implementation using a JSON database.''',
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown"
)
