from setuptools import find_packages, setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md', 'r').read()


install_requires = [
    'Django>=1.8,<1.12',
    'wagtail>=1.10,<1.14',
]


testing_extras = [
    'mock>=2.0.0',
    'coverage>=3.7.0',
]


setup(
    name='wagtail-flags',
    url='https://github.com/cfpb/wagtail-flags',
    author='CFPB',
    author_email='tech@cfpb.gov',
    description='Feature flags for Wagtail sites',
    long_description=long_description,
    license='CC0',
    version='2.0.8',
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
    },
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 1.8',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
