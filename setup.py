from setuptools import setup
import os

package_path = os.path.normpath(os.path.join(os.path.abspath(__file__), os.path.pardir))
os.chdir(package_path)

with open('README.rst') as rm:
    README = rm.read()

confirmed_email_data = [
    'templates/address_confirmed.html',
    'templates/confirmation_email.txt',
    'templates/confirmation_required.html'
]

setup(
    author="Jivan Amara",
    author_email='Development@JivanAmara.net',
    url='https://github.com/JivanAmara/confirmed-email',
    name='django-confirmed-email',
    version='0.0.7',
    packages=['confirmed_email'],
    package_data={'confirmed_email': confirmed_email_data},
    description='Provides an email sender that automatically confirms addresses.',
    long_description=README,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'License :: OSI Approved :: MIT License',
    ]
)
