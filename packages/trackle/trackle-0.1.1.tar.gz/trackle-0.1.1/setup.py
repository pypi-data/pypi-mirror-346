from setuptools import setup, find_packages

setup(
    name="trackle",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "sentence-transformers",
        "faiss-cpu",
        "typer",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "trackle=trackle.cli:app",
        ],
    },
)