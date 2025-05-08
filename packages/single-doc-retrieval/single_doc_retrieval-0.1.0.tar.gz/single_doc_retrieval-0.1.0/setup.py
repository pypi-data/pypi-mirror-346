from setuptools import setup, find_packages

setup(
    name="single_doc_retrieval",
    version="0.1.0",
    author="Vahan Martirosyan", 
    author_email="vahan@kiwidata.com",
    description="A retrieval pipeline for single documents.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="", 
    package_dir={'': 'src'},
    packages=find_packages(where="src"),
    install_requires=[
        "openai",
        "numpy",
        # Add other dependencies as needed
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Choose your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10', # Specify your Python version
) 