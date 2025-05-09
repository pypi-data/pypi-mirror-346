from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fml-md",
    version="0.1.0",
    author="OwPor",
    author_email="concepcionrayvincent@gmail.com",
    description="Fibonacci Markup Language - where indentation follows the Fibonacci sequence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OwPor/fml-md",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.6",
    install_requires=[
        "click>=8.0.0",
        "markdown>=3.3.0",
        "pygments>=2.7.0",
    ],
    entry_points={
        "console_scripts": [
            "fml=fml.cli:cli",
        ],
    },
    include_package_data=True,
    keywords="fibonacci, markup, language, indentation",
)
