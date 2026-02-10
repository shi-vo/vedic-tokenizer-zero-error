
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vedic-tokenizer",
    version="0.1.0",
    author="Ganesh",
    author_email="your.email@example.com",
    description="A Zero-Error Lossless Tokenization System for Sanskrit with 100% Accuracy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vedic-tokenizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Intended Audience :: Science/Research",
    ],
    python_requires='>=3.8',
    install_requires=[
        # No external dependencies currently for the core tokenizer
    ],
    include_package_data=True,
    package_data={
        "vedic_tokenizer": ["data/*.json"],
    },
)
