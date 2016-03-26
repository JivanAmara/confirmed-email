from setuptools import setup
import os

package_path = os.path.normpath(os.path.join(os.path.abspath(__file__), os.path.pardir))
os.chdir(package_path)

with open('README.rst') as rm:
    README = rm.read()

setup(
    author="Jivan Amara",
    author_email='Development@JivanAmara.net',
    url='https://github.com/JivanAmara/confirmed-email',
    name='confirmed-email',
    version='0.0.1',
    packages=['confirmed_email'],
    description='Provides an email sender that automatically confirms addresses.',
    long_description=README,
)
