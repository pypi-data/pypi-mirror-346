from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='mcmath',
  version='0.0.1',
  author='Alx',
  author_email='proshka20081010@gmail.com',
  description='MCMATH',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/alxprgs/mcmath',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='mcmath',
  project_urls={},
  python_requires='>=3.10'
)