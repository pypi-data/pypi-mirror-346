from setuptools import setup, find_packages

setup(
    name="formatted_console_output",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[],
    author="Wesley Marmon",
    author_email="wcmarmon@gmail.com",
    description="A package for formatted console output using ANSI escape codes - colors AND formatting.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
