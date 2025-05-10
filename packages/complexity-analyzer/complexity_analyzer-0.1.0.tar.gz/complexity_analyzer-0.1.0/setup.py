from setuptools import setup, find_packages

setup(
    name="complexity-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.0.0",
        "numpy>=1.18.0",
        "scipy>=1.4.0",
    ],
    author="Soumyaranjan sahoo",  # Replace with your name
    author_email="sahoosoumya242004@gmail.com",  # Replace with your email
    description="A tool to analyze time and space complexity of Python code with visualizations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/i-soumya18/complexity_analyzer",  # Update with your repo if applicable
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
    ],
    keywords="complexity analysis, big o notation, algorithm, performance, profiling, visualization",
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'complexity-analyzer=complexity_analyzer.cli:main',
        ],
    },
)