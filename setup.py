from setuptools import find_packages, setup


install_requires = [
    'Django>=1.8,<1.11',
    'wagtail>=1.6,<1.9',
]


testing_extras = [
    'coverage>=3.7.0',
    'flake8>=2.2.0',
]


setup(
    name='wagtail-flags',
    version='0.1',
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
    }
)
