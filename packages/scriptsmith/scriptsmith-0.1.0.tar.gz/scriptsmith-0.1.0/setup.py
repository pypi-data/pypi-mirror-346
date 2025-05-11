from setuptools import setup, find_packages

setup(
    name="scriptsmith",
    version="0.1.0",
    description="A CLI tool for managing tasks and scripts using Supabase",
    author="Aditya Mathur",
    author_email="aditya360@live.com",
    packages=find_packages(),
    install_requires=[
        "supabase",
        "click",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "scriptsmith = scriptsmith.main:cli"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)