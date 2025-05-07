from setuptools import setup, find_packages

setup(
    name="avalAgent",
    version="1.0.0",
    author="Amirhossein Derhami",
    author_email="D3rhami@gmail.com",
    description="An AI agent wrapper using LangChain and OpenAI with retry and logging support.",
    packages=find_packages(),
    install_requires=[
        "pydantic~=2.11.4",
        "setuptools~=75.8.2",
        "requests~=2.32.3",
        "langchain-core~=0.3.58",
        "langchain-openai~=0.3.16",
        "openai~=1.77.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
)
