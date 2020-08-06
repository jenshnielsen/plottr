from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='plottr',
    description='A tool for live plotting and processing data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Wolfgang Pfaff',
    author_email='wolfgangpfff@gmail.com',
    url='https://github.com/toolsforexperiments/plottr',
    packages=find_packages(include=("plottr*",)),
    package_data={'plottr': ['resource/gfx/*']},
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'pandas>=0.22',
        'xarray',
        'pyqtgraph>=0.10.0',
        'matplotlib',
        'numpy',
        'lmfit',
        'h5py>=2.10.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering'
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "plottr-monitr = plottr.apps.monitr:script",
            "plottr-inspectr = plottr.apps.inspectr:script",
            "plottr-autoplot-ddh5 = plottr.apps.autoplot:script",
        ],
    }
)
