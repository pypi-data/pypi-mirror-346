"""Setup script for CodaiCLI."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codaicli",
    version="1.0.0",
    author="Codai",
    author_email="codaicli.wrist796@passmail.net",
    description="AI-powered CLI assistant for code projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codai.app/cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "rich>=10.0.0",
        "click>=8.0.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "openai": ["openai>=1.0.0"],
        "gemini": ["google-generativeai>=0.1.0"],
        "claude": ["anthropic>=0.5.0"],
        "all": [
            "openai>=1.0.0",
            "google-generativeai>=0.1.0",
            "anthropic>=0.5.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "codaicli=codaicli.cli:cli",
        ],
    },
)