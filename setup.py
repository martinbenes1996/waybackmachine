
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
  version = '0.1.2',
  author = 'Martin Beneš',
  author_email = 'martinbenes1996@gmail.com',
  description = 'Envelope for archive.org API.',
  long_description = long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  license='MPL',
  url = 'https://github.com/martinbenes1996/waybackmachine',
  download_url = 'https://github.com/martinbenes1996/waybackmachine/archive/0.1.2.tar.gz',
  keywords = ['waybackmachine', 'archive', 'web', 'html', 'webscraping'],
  install_requires = reqs,
  package_dir={'': '.'},
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'Intended Audience :: Other Audience',
    'Environment :: Web Environment',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
    'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)