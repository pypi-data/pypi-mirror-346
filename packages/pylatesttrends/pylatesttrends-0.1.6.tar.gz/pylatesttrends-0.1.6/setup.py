from setuptools import setup, find_packages

setup(
    name="pylatesttrends",
    version="0.1.6",
    description="Get the latest trends from Google Trends",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Farasat Ali",
    author_email="63093876+faraasat@users.noreply.github.com",
    license="GPLv3",
    python_requires=">=3.9",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["selenium", "pandas", "webdriver_manager"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Homepage": "https://github.com/faraasat/pylatesttrends",
    },
)
