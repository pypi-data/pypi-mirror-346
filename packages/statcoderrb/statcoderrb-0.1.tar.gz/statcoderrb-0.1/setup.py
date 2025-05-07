from setuptools import setup, find_packages

setup(
    name="statcoderrb",
    version="0.1",
    packages=find_packages(),
    description="A collection of statistical analysis code blocks",
    author="Ritik Raj Bhaskar",
    author_email="ritikraj5442rr@gmail.com.com",
    url="https://github.com/Ritik-Raj-Bhaskar/statcoderrb",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "matplotlib",
        "seaborn",
        "scipy",
        "pandas",
    ],
)
