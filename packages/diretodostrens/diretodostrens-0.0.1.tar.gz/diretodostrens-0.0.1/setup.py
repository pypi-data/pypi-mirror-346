from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "DiretoDosTrens"
LONG_DESCRIPTION = """
Interface para a API diretodostrens.

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
    keywords=["trens", "trem", "diretodostrens", "api", "sp", "são paulo"],
    classifiers=[
        "Development Status :: 4 - Beta", 
        "Intended Audience :: Developers", 
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)