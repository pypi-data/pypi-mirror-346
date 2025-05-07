from setuptools import setup, find_packages

setup(
    name="calc_lib_jhonin",
    version="0.1.0",
    description="A simple calculator API using FastAPI",
    author="Jonathan Castro Silva",
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
            "calc_lib_jhonin=app.main:main",
        ],
    },
)