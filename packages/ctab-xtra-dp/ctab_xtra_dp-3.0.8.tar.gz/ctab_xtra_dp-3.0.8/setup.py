from setuptools import setup, find_packages

def read_requirements():
    with open("ctab_xtra_dp/requirements.txt", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="ctab_xtra_dp",
    version="3.0.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),  # List dependencies here, e.g., ["numpy", "requests"]
    description="A sample Python package",
    long_description=open("ctab_xtra_dp/README.md").read(),
    long_description_content_type="text/markdown",
    author="kem0sabe",
    author_email="martivl@stud.ntnu.no",
    url="https://github.com/Kem0sabe/CTAB_XTRA_DP_REVISED/",  # Update with your GitHub or website
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
