from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="coocan",
    version="0.5.6",
    author="wauo",
    author_email="markadc@126.com",
    description="Air Spider Framework",
    packages=find_packages(),
    python_requires=">=3.10",

    long_description=long_description,
    long_description_content_type="text/markdown",

    install_requires=[
        'click>=8.0.0', 'httpx', 'loguru'
    ],
    entry_points={
        'console_scripts': [
            'coocan=coocan.cmd.cli:main',
        ],
    },
    package_data={
        'coocan': ['templates/*'],
    },
    include_package_data=True
)
