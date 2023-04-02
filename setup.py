from setuptools import setup, find_packages

setup(
    name="hn-summaries",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.9.3",
        "requests>=2.26.0",
    ],
    author="Filip Maric",
    description="A simple Hacker News scraper and GUI that displays post summaries using GPT.",
    url="https://github.com/filipmrc/hn-summaries",
)
