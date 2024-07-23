from setuptools import setup, find_packages

setup(
    name="telegram-bot",
    version="0.1.0",
    author="Dmitry",
    author_email="d.chistyakov.work@gmail.com",
    description="My assistant telegram bot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
