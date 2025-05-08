from setuptools import setup, find_packages

setup(
    name="lightchat",
    version="0.1.0",
    description="Lightweight GPT2 training and deployment toolkit",
    author="RePromptsQuest",
    author_email="reprompts@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "transformers>=4.30.0",
        "datasets>=2.14.0",
        "torch>=1.13.0",
        "accelerate>=0.26.0",
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.22.0",
        "typer[all]>=0.9.0",
        "rich>=13.4.0",
    ],
    entry_points={
        "console_scripts": [
            "lightchat=lightchat.cli:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
)
