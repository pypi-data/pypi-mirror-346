from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agensight",
    version="0.2.4",
    author="Deepesh Agrawal",
    description="A Python SDK for logging and visualizing OpenAI agent interactions, with a built-in CLI and web dashboard.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "requests",
        "flask",
        "flask_cors",
        "fastapi==0.115.0",
        "uvicorn==0.34.0",
        "sqlalchemy==2.0.40",
        "pydantic==2.11.0",
        "starlette==0.46.2",
        "typing-extensions>=4.13.0",
        "python-multipart==0.0.9",
        "werkzeug>=2.0.0",
        "jinja2>=3.0.0",
        "aiofiles>=0.8.0",
        "click>=8.0.0",
        "opentelemetry-sdk",
        "opentelemetry-api",
        "opentelemetry-instrumentation",
        "opentelemetry-instrumentation-openai",
        "anthropic"
    ],
    entry_points={
        "console_scripts": [
            "agensight=cli.main:main",
        ],
    },
    python_requires=">=3.7",
    include_package_data=True,
)

