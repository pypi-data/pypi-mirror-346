from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mlflow_cors",
    version="0.1.1",
    author="David",
    author_email="zdent09@gmail.com",
    description="MLflow CORS extension for enabling cross-origin requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mlflow_cors",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.9",
    install_requires=[
        'flask-cors',
        "mlflow>=2.15.0, <2.18.0",
    ],
    entry_points={
        'mlflow.app': [
            'mlflow_cors=mlflow_cors:create_app',
        ],
    },
)