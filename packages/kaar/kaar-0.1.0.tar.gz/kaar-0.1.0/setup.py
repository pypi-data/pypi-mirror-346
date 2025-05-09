from setuptools import setup, find_packages

setup(
    name="kaar",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.34.0",
        "pyyaml>=6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "kaar=kaar.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Kubernetes AI-powered Analysis and Remediation (KAAR) using Amazon Bedrock",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kaar",
    license="MIT",
    include_package_data=True,
    package_data={
        'kaar': ['../config.yaml'],
    },
)
