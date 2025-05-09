import setuptools
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "description.md").read_text()

def get_install_requires():
    """Returns requirements.txt parsed to a list"""
    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets

setuptools.setup(
    name="torchfsm",
    version="0.0.1",
    author="Qiang Liu, Felix Koehler, Nils Thuerey",
    author_email="qiangliu.7@outlook.com",
    description="Fourier Spectral Method with PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://qiauil.github.io/torchfsm",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=get_install_requires(),
)
