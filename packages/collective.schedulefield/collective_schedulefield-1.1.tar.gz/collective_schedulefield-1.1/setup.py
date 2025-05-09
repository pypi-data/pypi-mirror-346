from setuptools import find_packages
from setuptools import setup


long_description = (
    open("README.rst").read() + "\n" + "Contributors\n"
    "============\n"
    + "\n"
    + open("CONTRIBUTORS.rst").read()
    + "\n"
    + open("CHANGES.md").read()
    + "\n"
)

setup(
    name="collective.schedulefield",
    version="1.1",
    description="Schedule behaviors for Plone content types",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="iMio",
    author_email="support@imio.be",
    url="https://github.com/IMIO/collective.schedulefield/",
    license="GPL version 2",
    packages=find_packages("src"),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "setuptools",
        "Plone",
        # -*- Extra requirements: -*-
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.contenttypes [test]",
            "Products.CMFPlacefulWorkflow",  # needed for plone.app.testing.layers.PLONE_FIXTURE
            "pytest",
            "pytest-cov",
            "pytest-plone",
            "tox",
        ],
        "dev": [
            "i18ndude",
            "plone.exportimport",
            "plone.meta",
            "zest.releaser",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
