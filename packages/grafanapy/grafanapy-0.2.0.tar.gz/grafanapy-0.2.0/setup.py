
from setuptools import setup, find_packages

with open('README.md','r') as f:
    description = f.read()

setup(
    name="grafanapy",
    version="0.2.0",
    description="Serve pandas DataFrames as Grafana-compatible JSON APIs",
    author="Aref Farzaneh",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pandas"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    long_description=description,
    long_description_content_type='text/markdown',
)
