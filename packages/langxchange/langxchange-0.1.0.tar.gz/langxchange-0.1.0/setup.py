from setuptools import setup, find_packages

setup(
    name="langxchange",
    version="0.1.0",
    description="API management and vectorization library for LLM integrations",
    author="Timothy Owusu",
    author_email="tim@ikolilu.com",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "sentence-transformers",
        "chromadb",
        "pinecone-client",
        "sqlalchemy",
        "pymongo",
        "pymysql",
        "numpy",
        "psycopg2-binary"
        "google-generativeai",
        "openai",
        "anthropic",
        "weaviate-client",
        "qdrant-client",
        "elasticsearch",
        "elasticsearch-dsl",
        "opensearch-py",
        "faiss-cpu",
        "faiss-gpu",
    ],
    python_requires=">=3.7",
)
