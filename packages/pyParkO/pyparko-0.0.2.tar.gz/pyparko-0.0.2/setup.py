import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyParkO",
    version="0.0.2",
    author="ZengJH",
    author_email="z1714833751@163.com",
    description="pyParkO is a Python-based implementation of the Parker-Oldenburg Algorithm "
                "for calculating gravity anomalies from a density interface and "
                "recovering the density interface from gravity anomalies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
