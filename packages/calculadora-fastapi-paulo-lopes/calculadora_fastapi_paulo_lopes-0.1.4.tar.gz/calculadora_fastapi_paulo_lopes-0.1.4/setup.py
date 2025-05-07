from setuptools import setup, find_packages

setup(
    name="calculadora-fastapi-paulo-lopes",
    version="0.1.4",
    description="A simple calculator API using FastAPI",
    author="Paulo Lopes",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.95.2",
        "pydantic==1.10.7",
        "uvicorn==0.22.0"
    ],
    include_package_data=True,
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "calculadora-fastapi-paulo-lopes=calculadora_fastapi.main:main",
        ],
    },
)