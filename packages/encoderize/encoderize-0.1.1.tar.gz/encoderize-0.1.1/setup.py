from setuptools import setup, find_packages

setup(
    name="encoderize",
    version="0.1.1",
    keywords="encoderize, encoder, barcode, svg, visualizer",
    packages=find_packages(),
    install_requires=[
        "svgwrite",
        "treepoem",  # For barcode generation
    ],
    python_requires=">=3.8",
    author="DrWheelicus",
    author_email="haydenpmac@gmail.com",
    description="A collection of functions to generate various visual representations of text in SVG format",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DrWheelicus/encoderize",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    entry_points={
        'console_scripts': [
            'encoderize=encoderize.cli:main',
        ],
    },
) 