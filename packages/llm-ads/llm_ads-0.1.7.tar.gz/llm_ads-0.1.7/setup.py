from setuptools import setup, find_packages

setup(
    name="llm-ads",
    version="0.1.7",
    description="FastAPI middleware for LLM ad serving integration",
    author="Reasonic Team",
    packages=find_packages(include=["llm_ads", "llm_ads.*"]),
    install_requires=[
        "fastapi>=0.109.0,<0.110.0",
        "pydantic>=2.7.0",
        "starlette>=0.36.0,<0.37.0",
        "sqlalchemy>=2.0.0,<2.1.0",
        "asyncpg>=0.29.0,<0.30.0",
        "python-dotenv>=1.0.0,<1.1.0",
        "loguru>=0.7.0,<0.8.0",
        "httpx>=0.26.0,<0.27.0",
        "uvicorn>=0.27.0,<0.28.0",
        "tenacity>=8.3.0,<8.4.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.12.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.8.0"
        ],
    },
    python_requires=">=3.8",
) 
