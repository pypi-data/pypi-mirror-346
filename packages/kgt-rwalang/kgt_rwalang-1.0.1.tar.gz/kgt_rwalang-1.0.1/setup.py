import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_desc = fh.read()

setuptools.setup(
    name="kgt_rwalang",
    version="1.0.1",
    author="Kigalithm Ltd.",
    author_email="foss@kigalithm.com",
    description="An enhanced language detector for Kinyarwanda",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/kigalithm/rwalang",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.7",
    install_requires=[
        "scikit-learn>=1.6.1",
        "numpy>=2.2.5",
        "joblib>=1.5.0",
        "pandas>=2.2.3",
    ],
    include_package_data=True,
    package_data={
        'kgt_rwalang': ['models/*.joblib']
    },
)