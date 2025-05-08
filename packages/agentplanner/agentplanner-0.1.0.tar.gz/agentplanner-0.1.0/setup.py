from setuptools import setup, find_packages

setup(
    name="agentplanner",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "torch",
        "huggingface_hub",
        "requests",
        "python-dotenv",
    ],
    description="AgentPlanner: A powerful multi-agent framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Raghavendra",
    author_email="dosinarayanaraghavendra@gmail.com",
    url="https://github.com/narayanaraghavendra/agentplanner",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
