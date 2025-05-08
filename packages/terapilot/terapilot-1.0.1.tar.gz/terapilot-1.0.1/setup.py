from setuptools import setup, find_packages

setup(
    name="terapilot",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        'cohere>=4.0',
        'requests>=2.25',
        'python-dotenv>=0.19',
        'pathlib>=1.0; python_version < "3.4"'
    ],
    entry_points={
        'console_scripts': [
            'terapilot=terapilot.cli:main',
        ],
    },
    python_requires='>=3.6',
)