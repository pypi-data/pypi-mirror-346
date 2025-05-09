from setuptools import setup, find_packages

setup(
    name="offpath-minihook",
    version="0.1.0",
    description="Lightweight security hook for LLM agents",
    author="Offpath Security",
    author_email="info@offpath.ai",
    url="https://offpath.ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "langchain": ["langchain>=0.0.200"],
        "openai": ["openai>=0.27.0"],
        "all": [
            "langchain>=0.0.200",
            "openai>=0.27.0",
        ],
    },
)
