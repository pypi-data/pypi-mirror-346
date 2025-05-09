from setuptools import setup, find_packages

setup(
    name="calculadoraapi-fastapi-breno",
    version="0.1.3",
    description="Calculadora API utilizando FastAPI",
    author="Breno Amâncio",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.95.2,<0.100.0",  # Compatível com Pydantic v1
        "pydantic==1.10.7",
        "uvicorn==0.22.0"
    ],
    include_package_data=True,
    python_requires=">=3.9, <=3.12.5"
)