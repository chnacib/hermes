import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="aws-hermes",
    version="0.0.1",
    author="Carlos Silva & Delano Lima",
    author_email="xxx@xxx.com",
    description=("A tool to analyse AWS Services."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chnacib/aws-sdk-hermes",
    project_urls={
        # "Bug Tracker": "https://github.com/liuzheng1990/python_packaging_demo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    dependencies=[
        "boto3==1.24.11",
        "pandas==1.4.2",
        "openpyxl==3.0.10",
        "pandas==1.4.2",
        "awscli==1.18.69",
        "python-dotenv==0.20.0",
        "progress==1.6",
    ],
    # install_requires=["requests"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "aws-hermes = src.main:init",
        ]
    }
)
