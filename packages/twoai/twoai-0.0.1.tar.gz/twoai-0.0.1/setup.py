from setuptools import setup, find_packages

setup(
    name="twoai",
    version="0.0.1",
    author="Your Name",
    author_email="support@two.ai",
    description="A simple hello world package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sutra-dev",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
