from setuptools import setup, find_packages

setup(
    name="llm-samplers",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "numpy>=1.24.0",
    ],
    author="Ian Timmis",
    author_email="ianmtimmis@gmail.com",
    description="A library for advanced LLM sampling techniques",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iantimmis/samplers",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 