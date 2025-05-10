from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="serapis-metrics",  # Este nombre debe ser único en PyPI
    version="1.0.1",  # Incrementa este número
    description="A metrics collection library for Serapis projects with multi-Python support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adtTEyS/Serapis-Metrics",
    author="Serapis Team",
    author_email="rcebrian@typsa.es",  # Cambia esto por tu email
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: IronPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=2.7",
    install_requires=[],
    keywords="metrics, pyrevit, revit, serapis",
    project_urls={
        "Bug Reports": "https://github.com/adtTEyS/Serapis-Metrics/issues",
        "Source": "https://github.com/adtTEyS/Serapis-Metrics",
    },
)