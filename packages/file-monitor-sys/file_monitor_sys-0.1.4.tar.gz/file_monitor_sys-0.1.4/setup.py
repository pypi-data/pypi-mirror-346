from setuptools import setup, find_packages

setup(
    name="file_monitor_sys",
    version="0.1.4",
    description="A file monitoring system with email alerts and logging",
    author="Your Name",
    author_email="your.email@example.com",
    python_requires=">=3.6",
    packages=find_packages(where="file_monitor"),
    package_dir={"": "file_monitor"},
    install_requires=[
        "watchdog",
        "yagmail",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
