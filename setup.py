from setuptools import setup, find_packages
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.resolve()

long_description = (BASE_DIR / "README.md").read_text(encoding="utf-8")

setup(
    name="subpubpy",
    version="0.0.4",
    description="Multithreading supported python package for publisher and subscriber model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeart7.com",
    author="Rahul Singh",
    author_email="rajput.rahul8510@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="subpubpy, setuptools, development",
    package_dir={"": "src"},  
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    install_requires=[],
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    package_data={},
    entry_points={},
    project_urls={
        "Home page": "https://github.com/Rahul-singh98/subpubpy",
        "Bug Reports": "https://github.com/Rahul-singh98/subpubpy/issues",
        "Feedback": "https://codeart7.com/feedback",
    },
)