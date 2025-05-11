from setuptools import setup, find_packages

setup(
    name="vba-sync",
    version="0.1.0",
    author="Andrey Kolesov",
    author_email="never-ya@yandex.ru",
    description="Export and import VBA macros from Word (.docm) and Excel (.xlsm)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/AndyTakker/vba-sync ",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Office Suites",
        "Environment :: Win32 (MS Windows)"
    ],
    python_requires='>=3.7',
    install_requires=[
        "pywin32",
    ],
    entry_points={
        "console_scripts": [
            "vba-sync=vba_sync.cli:main",
        ],
    },
)