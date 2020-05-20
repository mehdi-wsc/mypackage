import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mypackage_wsc",
    version="1.0.0",
    author="mehdi wsc",
    author_email="kerbedjm@gmail.com",
    description="wedeployer package version beta",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mehdi-wsc/mypackage.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
