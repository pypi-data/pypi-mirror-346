from setuptools import setup, find_packages

VERSION = "0.0.2"
DESCRIPTION = "Checa o estado das linhas de trem de São Paulo (CPTM, Metro, Viaquatro e Viamobilidade)"
LONG_DESCRIPTION = """
Interface para a API [DiretoDosTrens](https://static.diretodostrens.com.br/swagger/
)

Visite https://github.com/Philliaezer/DiretoDosTrens para saber mais
"""

setup(
    name="diretodostrens",
    version=VERSION,
    author="Anderson Duarte",
    author_email="reddragondggda@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=[
    "trens", "trem",
    "diretodostrens", "api",
     "sp", "são paulo", "cptm",
      "metro", "viamobilidade",
      "viaquatro"
  ],
    classifiers=[
        "Development Status :: 3 - Alpha", 
        "Intended Audience :: Developers", 
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)