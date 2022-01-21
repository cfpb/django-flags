from setuptools import find_packages, setup


install_requires = ["Django>=1.11,<4.1"]

testing_extras = [
    "coverage>=3.7.0",
    "django-debug-toolbar>=3.2,<4",
    "jinja2",
]

docs_extras = [
    "mkdocs>=0.17",
    "mkdocs-rtd-dropdown>=0.0.11",
    "pymdown-extensions>=4.11",
]

setup(
    name="django-flags",
    url="https://github.com/cfpb/django-flags",
    author="CFPB",
    author_email="tech@cfpb.gov",
    description="Feature flags for Django projects",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="CC0",
    version="5.0.6",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={"testing": testing_extras, "docs": docs_extras},
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
