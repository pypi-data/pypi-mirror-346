from setuptools import setup, find_packages

# Read README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fivitech-mt5-connector",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    version="0.2.18",
    install_requires=[
        "MT5Manager>=5.0.3906",
        "pandas>=1.0.0",
        "numpy>=1.19.0",
        "pytz>=2021.1",
        "requests>=2.26.0",
        "python-dateutil>=2.8.2",
        "tenacity>=8.2.3", # Added for retry logic
    ],
    extras_require={
        'dev': [
            'build>=1.0.0',
            'twine>=4.0.0',
            'pytest>=7.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
        ],
    },
    author="Fivitech",
    author_email="contact@fivitech.com",
    description="A private MetaTrader5 connection and management package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fivitech/mt5-connector",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7",
)
