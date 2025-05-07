###############################################################################
# pKa-ANI								      #
###############################################################################

from setuptools import find_packages
from distutils.core import setup

setup(name='pkaani',
      version="0.1.7",
      description="A Python package to calculate pKa values for proteins",
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      author="Hatice GOKCAN, Olexandr ISAYEV",
      author_email="olexandr@olexandrisayev.com",
      url="https://github.com/isayevlab/pKa-ANI",
      download_url="https://github.com/isayevlab/pKa-ANI",
      python_requires='>=3.10',
      install_requires=["numpy", "scipy", "torch", "torchani", "scikit-learn==1.6.1", "ase", "joblib", "setuptools"],
      packages=find_packages(),
      include_package_data=False,
      entry_points={'console_scripts': ['pkaani = pkaani.run:main', ]},
      )


