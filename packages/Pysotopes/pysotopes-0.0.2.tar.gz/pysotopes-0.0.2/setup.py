from setuptools import setup, find_packages


VERSION = '0.0.2'
DESCRIPTION = 'A basic UI building library built on top on tkinter'


# Setting up
setup(
    name="Pysotopes",
    version=VERSION,
    author="HapooIsLuv",
    author_email="<Hapoo@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'UI', 'library'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)