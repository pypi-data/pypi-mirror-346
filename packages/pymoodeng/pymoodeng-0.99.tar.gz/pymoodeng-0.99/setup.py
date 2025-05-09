from setuptools import setup

setup(
    name='pymoodeng',
    version='0.99',
    description='A Python package for simple system simulations and potential transition fuel calculations.',
    author=['Kiss Márkus', 'Tari Zalán', 'Varga Benedek'],
    author_email=['kiss.markus@hallgato.ppke.hu', 'tari.zalan@itk.ppke.hu', 'varga.benedek@hallgato.ppke.hu'],
    packages=["numpy >= 2.2.4",
  "pandas >= 2.2.3" ,
  "matplotlib >= 3.10.1" ,
  "sphinx >= 8.2.3" ,
  "sphinx_rtd_theme >= 3.0.2"],
    install_requires=[
        'numpy',
        'pandas',
    ],
)