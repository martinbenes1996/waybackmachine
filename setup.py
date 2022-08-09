
import os

# versions
__version__ = os.environ.get('VERSION_NEW', '0.4.0')

# requirements
try:
  with open('requirements.txt') as f:
    reqs = f.read().splitlines()
except:
  reqs = []

import setuptools
with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
  name = 'waybackmachine',
  version = __version__,
  author = u'Martin Beneš',
  author_email = 'martinbenes1996@gmail.com',
  description = 'Envelope for archive.org API.',
  long_description = long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  license='MPL',
  project_urls={
    "Homepage": "https://pypi.org/project/waybackmachine/",
    "Documentation": 'https://jpeglib.readthedocs.io/en/latest/',
    "Source": 'https://github.com/martinbenes1996/waybackmachine',
  },
  keywords = ['waybackmachine', 'archive', 'web', 'html', 'webscraping'],
  install_requires = reqs,
  package_dir={'': '.'},
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Other Audience',
    'Environment :: Web Environment',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
    'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    'Programming Language :: Python :: 3',
  ],
)