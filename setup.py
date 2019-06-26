import pathlib
import re

from setuptools import setup, find_packages

WORK_DIR = pathlib.Path(__file__).parent
PACKAGE_DIR = WORK_DIR / 'anystrenum'

with open('README.md', 'r') as file:
    README = file.read()


def get_version():
    """
    Read version
    :return: str
    """
    txt = (PACKAGE_DIR / '__init__.py').read_text('utf-8')
    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


setup(
    name='AnyStrEnum',
    version=get_version(),
    author='MrMrRobat',
    author_email='appkiller16@gmail.com',
    description='Elegant implementation of Enum which inherits from str or bytes',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/MrMrRobat/AnyStrEnum',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7  ',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
