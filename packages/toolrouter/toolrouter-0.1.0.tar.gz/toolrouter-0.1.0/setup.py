from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="toolrouter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "isort>=5.9.1",
            "flake8>=3.9.2",
            "twine>=3.4.1",
            "build>=0.7.0",
        ],
    },
    author="ToolRouter",
    author_email="admin@toolrouter.ai",
    description="Python client for the ToolRouter API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://toolrouter.ai",
    project_urls={
        "Bug Tracker": "https://github.com/toolrouter/toolrouter-python/issues",
        "Documentation": "https://docs.toolrouter.ai",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
) 