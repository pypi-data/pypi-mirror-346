from setuptools import setup, find_packages

setup(
    name="metatemplating",
    version="1.0.2",
    description="A Python templating engine for dynamic text generation.",
    author="guanxiaohan",
    author_email="13792898752@163.com",
    url="https://github.com/guanxiaohan/MetaTemplating",
    license="MIT",
    packages=find_packages(),
    install_requires=["uuid", "json"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
)