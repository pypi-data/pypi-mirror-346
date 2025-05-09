from setuptools import setup, find_packages

setup(
    name="sexy_ai",
    version="0.1",
    packages=find_packages(),  # Automatically finds submodules
    install_requires=[],  # Add dependencies if needed
    author="Your Name",
    description="An AI-powered project",
    long_description="A powerful AI package",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)