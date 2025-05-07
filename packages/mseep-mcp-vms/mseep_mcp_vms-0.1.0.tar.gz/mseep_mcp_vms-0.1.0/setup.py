
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-vms",
    version="0.1.0",
    description="VMS Video Fetch",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['mcp[cli]>=1.2.1', 'numpy>=2.2.4', 'pillow>=11.1.0'],
    keywords=["mseep"] + [],
)
