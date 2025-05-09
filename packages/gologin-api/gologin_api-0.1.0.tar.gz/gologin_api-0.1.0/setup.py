from setuptools import setup, find_packages

setup(
    name="gologin_api",
    version="0.1.0",
    description="Tiny wrapper for GoLogin and fingerprint API via Google Apps Script",
    author="Tu Hoang",
    url="https://github.com/yourusername/gologin_api",
    packages=find_packages(),
    install_requires=[
        "requests>=2.0",
    ],
    python_requires=">=3.6",
)
