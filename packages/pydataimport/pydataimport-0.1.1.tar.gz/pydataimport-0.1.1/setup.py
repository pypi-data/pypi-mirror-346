from setuptools import setup, find_packages

setup(
    name="pydataimport",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "certifi>=2024.6.2",
        "charset-normalizer>=3.3.2",
        "idna>=3.7",
        "numpy>=2.0.0",
        "pandas>=2.2.2",
        "pyodbc>=5.1.0",
        "python-dateutil>=2.9.0",
        "pytz>=2024.1",
        "requests>=2.32.3",
        "six>=1.16.0",
        "tzdata>=2024.1",
        "urllib3>=2.2.2",
    ],
    author="nmol",
    author_email="connect@nmol.in",
    description="To fetch data from API and import to SQL Server in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nmol2/pydataimport",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 