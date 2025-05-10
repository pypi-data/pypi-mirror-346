from setuptools import setup

# try:
#     import pypandoc
#     long_description = pypandoc.convert_file('README.md', 'rst')
# except(IOError, ImportError):
#     long_description = open('README.md').read()

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='pysat-abel',
    version = "0.1.3",
    description='Python implementation for Spline-based Abel Transform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.coria-cfd.fr/littinm/pysat',
    author='Mijail Littin, Alexandre Poux, Guillaume Lefevre, Marek Mazur, Felipe Escudero, Andrés Fuentes, Jérôme Yon',
    author_email='littinm@coria.fr',
    packages=['pysat'],
    install_requires = [ "scipy", "numpy", 'abel', 'joblib'],  # ✅ correct key

    classifiers=[
        'Intended Audience :: Science/Research',
    ],
    license='MIT',  # or whatever license you’re using
)