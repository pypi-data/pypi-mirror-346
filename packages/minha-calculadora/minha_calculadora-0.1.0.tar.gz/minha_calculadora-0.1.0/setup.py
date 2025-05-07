from setuptools import setup, find_packages

setup(
    name="minha_calculadora",
    version="0.1.0",
    packages=find_packages(),
    description="Uma biblioteca de operações matemáticas com FastAPI exceptions.",
    author="Seu Nome",
    author_email="seu@email.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "fastapi"
    ]
)
