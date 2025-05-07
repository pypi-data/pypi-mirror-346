from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quantumgeometrytensor",
    version="0.2.2",
    packages=find_packages(),
    author='JinxiongJia',
    author_email='jiajinxiong0402@126.com',
    description='This is a package using calculate the quantum geometry including Zeeman QGT, S_QGT as well as the corresponding dipole quantities',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jiajinxiong/QuantumGeometryTensor',
    install_requires=["numpy"],  # Dependencies
    python_requires='>=3.7',
)
