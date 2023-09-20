
import pathlib
from setuptools import setup
from setuptools import find_packages

from pyumldiagrams import __version__ as pyumldiagramsVersion

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README  = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name='pyumldiagrams',
    version=pyumldiagramsVersion,
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Draw UML diagrams in various formats',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/hasii2011/pyumldiagrams',
    packages=find_packages(),
    package_data={
        'pyumldiagrams.image.resources': ['*.ttf', 'pyumldiagrams/image/resources/*.ttf', 'py.typed'],
        'pyumldiagrams':               ['py.typed'],
        'pyumldiagrams.image':         ['py.typed'],
        'pyumldiagrams.pdf':           ['py.typed'],
        'pyumldiagrams.pdf.resources': ['py.typed'],
        'pyumldiagrams.xmlsupport':    ['py.typed'],
    },
    install_requires=['fpdf2>=2.7.4', 'Pillow>=10.0.0', 'codeallybasic==0.5.2']
)
