from setuptools import setup, find_packages

# No direct import so we can install the package
with open('flake8_vedro_allure_id_plugin/__init__.py') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'").strip('"')
            break
    else:
        version = '0.1.0'

setup(
    name="flake8-vedro-allure-id",
    version=version,
    description="Flake8 plugin to enforce @allure.id() decorator for Vedro Scenario classes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Team",
    author_email="your.email@example.com",
    url="https://github.com/your-org/flake8-vedro-allure-id",
    packages=find_packages(),
    install_requires=[
        "flake8 >= 3.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "flake8.extension": [
            "UGC = flake8_vedro_allure_id_plugin.plugin:AllureIdPlugin",
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
) 