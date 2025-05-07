from setuptools import setup, find_packages

setup(
    name="bakery-build",
    version="1.0.4",
    author="Bradley Hutchings",
    author_email="bkhnapa@gmail.com",
    description="a simple build automation library and CLI tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="."),
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
    ],
    entry_points={
        "console_scripts": [
            "bake=bake.bake_cli:main",
        ],
    },
)
