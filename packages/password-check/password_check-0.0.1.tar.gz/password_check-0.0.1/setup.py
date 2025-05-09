from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

setup(
    name="password-check",
    version="0.0.1",
    author="Larissa Batista",
    author_email="larissabatista0704@gmail.com",
    description="Checks whether passwords meet security criteria.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LarissaBSantos/password_check",
    packages=find_packages(),
    python_requires = ">=3.7",
)