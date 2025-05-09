import pathlib

import setuptools

setuptools.setup(
    name="monaco_qualifying",
    version="0.1.14",
    description="Analysis of Formula 1 qualification results.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://git.foxminded.ua/liliia-shpytsia-mentoring/task_6_report_of_monaco_2018_racing",
    author="Liliia Shpytsia",
    author_email="fioletowujsemizwetik@gmail.com",
    license="MIT",
    projecr_urls={
        "Homepage": "https://git.foxminded.ua/liliia-shpytsia-mentoring/task_6_report_of_monaco_2018_racing",
        "Issues": "https://git.foxminded.ua/liliia-shpytsia-mentoring/task_6_report_of_monaco_2018_racing/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0.0"]
    },
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_packages_data=True,
    entry_points={"console_scripts": ["monaco_qualifying = monaco_qualifying.cli:main"]},
)
