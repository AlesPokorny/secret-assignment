from setuptools import find_packages, setup

setup(
    name="secret-assignment",
    version="1886.1.29",
    description="Speed dating assignment",
    author="Itsa me, Mario!",
    url="https://github.com/AlesPokorny/secret-assignment",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "click",
        "numpy==1.26.4",
        "matplotlib==3.8.3",
        "flake8",
        "black",
        "mypy",
        "pytest-cov",
        "pytest",
        "pre-commit",
    ],
    tests_require=["pytest", "pytest-cov", "teamcity-messages"],
    python_requires=">=3.11",
)
