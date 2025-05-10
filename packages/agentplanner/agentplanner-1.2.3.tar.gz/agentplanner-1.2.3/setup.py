from setuptools import setup, find_packages

setup(
    name='agentplanner',
    version="1.2.3",  # Change this to a new version
    description='A lightweight multi-agent orchestration framework for GenAI pipelines',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Raghavendra',
    author_email='dosinarayanaraghavendra@gmail.com',
    url='https://github.com/narayanaraghavendra/agentplanner',
    packages=find_packages(include=["agentplanner", "agentplanner.*"]),
    install_requires=[
        'langchain>=0.1.0',
        'chromadb>=0.4.0',
        'pinecone-client>=2.0',
        'weaviate-client>=3.0',
        'faiss-cpu>=1.7.2',
        'milvus>=2.0',
        'pymongo>=3.11',
        'numpy>=1.21.0',
        'transformers>=4.5.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.8',
)

