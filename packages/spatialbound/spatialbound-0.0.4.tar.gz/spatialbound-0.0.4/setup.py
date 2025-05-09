from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spatialbound",
    version="0.0.4",
    author="Mohamed R. Ibrahim",
    author_email="contact@spatialbound.com",
    description="Spatialbound API client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spatialbound/spatialbound_api",
    project_urls={
        "Bug Tracker": "https://github.com/spatialbound/spatialbound_api/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.15.0",
    ],
    include_package_data=True,
)