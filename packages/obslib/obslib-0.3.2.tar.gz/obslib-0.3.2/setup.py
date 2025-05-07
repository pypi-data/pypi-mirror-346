import os

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    README = readme_file.read()

setup_args = {
    "name": "obslib",
    "version": os.environ["BUILD_VERSION"],
    "description": "Object Based Specification Library",
    "long_description_content_type": "text/markdown",
    "long_description": README,
    "license": "MIT",
    "packages": find_packages(where="src", include=["obslib", "obslib.*"]),
    "author": "Jesse Reichman",
    "keywords": ["Object", "Specification", "Library", "yaml", "json"],
    "url": "https://github.com/archmachina/obslib",
    "download_url": "https://pypi.org/project/obslib/",
    "entry_points": {"console_scripts": []},
    "package_dir": {"": "src"},
    "install_requires": ["PyYAML>=6.0.0", "Jinja2>=3.1.0"],
}

if __name__ == "__main__":
    setup(**setup_args, include_package_data=True)
