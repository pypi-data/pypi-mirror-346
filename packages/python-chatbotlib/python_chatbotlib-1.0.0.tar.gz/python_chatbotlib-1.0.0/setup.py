from setuptools import setup, find_packages

setup(
    name='python-chatbotlib',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.32.3',
        'beautifulsoup4>=4.12.3'
    ],
    entry_points={
        "console_scripts": [
            "chatbotlib = chatbotlib.cli:main",
        ],
    },
)