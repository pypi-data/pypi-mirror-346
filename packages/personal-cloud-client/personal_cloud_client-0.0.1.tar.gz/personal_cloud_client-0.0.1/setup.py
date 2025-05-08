from setuptools import setup, find_packages

setup(
    name="personal_cloud_client",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "cloud_client=personal_cloud_client.cli:main"
        ],
    },
)
