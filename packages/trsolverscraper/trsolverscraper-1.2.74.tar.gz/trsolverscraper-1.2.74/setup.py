from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="trsolverscraper",
    version="1.2.74",
    packages=find_packages(),
    install_requires=[
        "requests>=2.9.2",
        "requests-toolbelt>=0.9.1",
        "brotli",
    ],
    author="Original: VeNoMouS, Modified: TRSolver",
    description="A Python module to bypass Cloudflare's anti-bot page (fork of cloudscraper)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/trsolverscraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 