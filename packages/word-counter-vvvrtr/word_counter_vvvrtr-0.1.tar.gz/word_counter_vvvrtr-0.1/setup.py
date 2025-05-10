from setuptools import setup, find_packages

setup(
    name="word_counter_vvvrtr",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["wordcount=word_counter.cli:main"]
    },
    author="vvvrtr",
    description="Пакет для подсчёта слов и символов в тексте",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vvtteu/word_counter",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)