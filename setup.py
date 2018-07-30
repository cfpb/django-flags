from setuptools import find_packages, setup


long_description = open('README.md', 'r').read()

install_requires = [
    'Django>=1.8,<2.1',
]

testing_extras = [
    'mock>=2.0.0',
    'coverage>=3.7.0',
]

docs_extras = [
    'mkdocs>=0.17',
    'mkdocs-rtd-dropdown>=0.0.11',
    'pymdown-extensions>=4.11',
]

setup(
    name='django-flags',
    url='https://github.com/cfpb/django-flags',
    author='CFPB',
    author_email='tech@cfpb.gov',
    description='Feature flags for Django projects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='CC0',
    version='3.0.0',
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
        'docs': docs_extras,
    },
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 2.0',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
