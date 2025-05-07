from setuptools import setup, find_packages

setup(
    name="trackle",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "sentence-transformers",
        "faiss-cpu",
        "typer",
        "pyyaml",
        "prompt_toolkit",
        "python-dateutil",
    ],
    entry_points={
        "console_scripts": [
            "trackle=trackle.cli:app",
        ],
    },
)