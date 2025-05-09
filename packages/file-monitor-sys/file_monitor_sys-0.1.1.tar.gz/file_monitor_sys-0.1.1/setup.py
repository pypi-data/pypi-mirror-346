from setuptools import setup, find_packages

setup(
    name="file-monitor-sys",
    version="0.1.1",
    packages=find_packages(include=["file_monitor", "file_monitor.*"]),
    install_requires=[
        "watchdog>=3.0.0",
    ],
    entry_points={
        'console_scripts': [
            'file-monitor = file_monitor.main:main',
        ],
    },
)
