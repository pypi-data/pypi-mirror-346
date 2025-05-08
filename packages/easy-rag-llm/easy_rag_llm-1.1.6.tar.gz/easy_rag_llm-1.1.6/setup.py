from setuptools import setup, find_packages

setup(
    name="easy-rag-llm",
    version="1.1.6",
    author="Aiden-Kwak",
    author_email="duckracoon@gist.ac.kr",
    description="Easily implement RAG workflows with pre-built modules and context expansion.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Aiden-Kwak/easy_rag",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "faiss-cpu",
        "numpy>=1.19.0",
        "tqdm>=4.65.0",
        "pypdf>=3.7.0",
        "openai>=1.0.0",
        "requests>=2.28.0",
        "python-dotenv>=0.19.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: General",
    ],
    keywords="rag llm openai deepseek context-expansion nlp",
    python_requires=">=3.8",
    project_urls={
        "Bug Reports": "https://github.com/Aiden-Kwak/easy_rag/issues",
        "Source": "https://github.com/Aiden-Kwak/easy_rag",
    },
)
