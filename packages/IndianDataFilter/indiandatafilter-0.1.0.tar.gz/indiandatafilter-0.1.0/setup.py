from setuptools import setup, find_packages
setup(
    name="IndianDataFilter",  # Your package name on PyPI
    version="0.1.0",
    author="Sharvesh Subhash",
    author_email="cod.sharvesh2002@gmail.com",
    description="Check if the data is from an Indian source.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sharveshsubhash/IndianDataFilter",  # Replace with your repo
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="Indian source checker",
    python_requires=">=3.7",
    install_requires=[
        "requests"
    ],
    license="MIT",
    entry_points={
        "console_scripts": [
            "IndianDataFilter=IndianDataFilter.indianblog:cli"
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
