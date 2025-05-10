from setuptools import setup

# Parse README.md as long_description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Parse requirements.txt as install_requires
with open("requirements.txt", "r", encoding="utf-8") as f:
    require = f.read().splitlines()

setup(
    name="ProtY",
    version="1.0.1",
    description="The project is about using a pretrained protein transformer architecture to create embeddings of various proteins, and then performing nonlinear dimensionality reduction on those embeddings to see which kinds of similarities in protein function/structure we can restore.",
    author="Csapó Bence, Galló Dominik, Uhlár Brigitta",
    author_email="uhlarbrigi@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uhlarbrigi/PEPTIDE-SEQUENCE-EMBEDDING-AND-CLUSTERING-VISUALIZATION.git",
    project_urls={
        "Bug Tracker": "https://github.com/uhlarbrigi/PEPTIDE-SEQUENCE-EMBEDDING-AND-CLUSTERING-VISUALIZATION/issues",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    packages=["ProtY"],
    install_requires=require,
    python_requires=">=3.10"
)
