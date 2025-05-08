from setuptools import setup, find_packages

setup(
    name="websearch4ai",
    version="0.0.1",
    description="A Python library for AI web search",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Zino",
    author_email="gushante@163.com",
    url="https://github.com/zinodynn/websearch4ai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)