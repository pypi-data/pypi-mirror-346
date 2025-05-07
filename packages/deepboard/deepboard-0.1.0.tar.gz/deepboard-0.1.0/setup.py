from setuptools import setup
import os

if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "No description found"

long_description = long_description.replace("./assets/", "https://raw.githubusercontent.com/anthol42/deepboard/main/assets/")

# Load version
with open("deepboard/__version__.py", "r") as f:
    version = f.read().split("=")[1].strip().strip("\"")

setup(
    name="deepboard",
    version=version,
    author="Anthony Lavertu",
    author_email="alavertu2@gmail.com",
    include_package_data=True,
    description="A tool to log you experiment results and explore them in a gui",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anthol42/deepboard",
    project_urls={
        "Issues": "https://github.com/anthol42/deepboard/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    keywords=[
        "deepboard", "deep", "board", "pytorch", "torch", "tensorflow", "jax", "tensorboard"
    ],
    python_requires=">=3.9",
    install_requires=[
        "python-fasthtml",
        "fh-plotly",
        "MarkupSafe",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "deepboard=deepboard.gui.entry:main"
        ]
    },
    packages=["deepboard"],
)