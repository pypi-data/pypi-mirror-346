from setuptools import setup, find_packages

requires = [
    "lenstronomy>=1.11.0",
    "numpy>=1.17.0",
    "scipy>=0.19.1",
    "jax>=0.4.12",
    "jaxlib>=0.4.12",
]
tests_require = ["pytest"]

setup(
    name="jaxtronomy",
    version="0.0.9.1",
    url="https://github.com/lenstronomy/JAXtronomy",
    author="jaxtronomy developers",
    description="lenstronomy, but in JAX",
    packages=find_packages(),
    license="BSD-3",
    install_requires=requires,
    tests_require=tests_require,
    keywords="jaxtronomy",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
    ],
)
