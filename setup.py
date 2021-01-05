import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mytrading",
    version="0.0.1",
    author="TimoRobin",
    author_email="Dont@email.me",
    description="messing around",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timorobin/trading",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)