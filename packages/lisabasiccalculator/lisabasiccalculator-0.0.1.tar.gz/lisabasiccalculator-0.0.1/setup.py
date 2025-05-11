from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

# Read content from README.txt and CHANGELOG.txt
with open('README.txt', 'r') as f:
    long_description = f.read()

with open('CHANGELOG.txt', 'r') as f:
    long_description += '\n\n' + f.read()

setup(
  name='lisabasiccalculator',
  version='0.0.1',
  description='A very basic calculator',
  long_description=long_description,
  long_description_content_type='text/x-rst',  # or 'text/markdown' if your README is Markdown
  url='',  
  author='Joshua Lowe',
  author_email='lisakajula@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=[]  # Include required dependencies if any
)
