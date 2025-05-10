from setuptools import setup, find_packages

setup(
    name="wordfrequencer",
    version="0.1.0",
    description="A package to count word frequency and display it in a table format.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Md. Ismiel Hossen Abir",
    author_email="ismielabir1971@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires='>=3.6',
)