from setuptools import setup, find_packages

setup(
    name='talem_ai_cli',
    version='0.0.2',
    author='Hemit Patel',
    description='Administrative tool for RAG apps',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'click',
        'aiofiles',
        'PyPDF2',
        'pypdf',
        'pyfiglet',
        'langchain',
        'langchain-community',
        'langchain-astradb',
        'langchain-huggingface',
    ],
    entry_points={
        'console_scripts': [
            'talemai = main.__init__:main',  # Adjust path as needed
        ],
    },
)
