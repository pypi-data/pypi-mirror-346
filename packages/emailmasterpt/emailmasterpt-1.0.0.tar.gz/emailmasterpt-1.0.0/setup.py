from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="emailmasterpt",
    version="1.0.0",
    author="Wuotans",
    author_email="matheus.silva231996@gmail.com",
    description="Interface unificada para envio de emails com múltiplos provedores e agendamento",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seuusuario/emailmasterpt",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "apscheduler>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-mock>=3.0.0",
            "twine>=3.0.0",
        ],
    },
    include_package_data=True,
)