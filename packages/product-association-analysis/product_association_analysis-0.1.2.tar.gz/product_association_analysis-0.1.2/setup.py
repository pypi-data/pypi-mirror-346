from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="product-association-analysis",
    version="0.1.2",
    author="Alexandre Junior",
    author_email="seu.email@exemplo.com",  # Adicione seu email (opcional mas recomendado)
    description="Ferramenta para análise de associação de produtos em dados de transações",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/product-association-analysis",
    project_urls={
        "Bug Tracker": "https://github.com/seu-usuario/product-association-analysis/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
        "openpyxl>=3.0.0",
        "matplotlib>=3.0.0",
        "seaborn>=0.11.0",
        "numpy>=1.18.0",
    ],
    entry_points={
        "console_scripts": [
            "product-association-analysis=product_association.cli:main",
        ],
    },
)