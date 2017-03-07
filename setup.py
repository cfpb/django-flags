from setuptools import find_packages, setup

install_requires = [
    'Django>=1.8,<1.11',
    'wagtail>=1.6,<1.9',
]


testing_extras = [
    'mock>=2.0.0',
    'coverage>=3.7.0',
    'flake8>=2.2.0',
]


setup(
    name='wagtail-flags',
    url='https://github.com/cfpb/wagtail-flags',
    author='CFPB',
    author_email='tech@cfpb.gov',
    license='CC0',
    version='1.0.2',
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
    },
    classifiers=[
        'License :: Public Domain',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
    ]
)
