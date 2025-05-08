from setuptools import setup, find_packages

setup(
    name="calculadora-manuesy-api",
    version="0.1.1",
    author="Manuely Lemos",
    author_email="manumeireleslemos@gmail.com",
    description="Uma calculadora básica com FastAPI",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic"

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
