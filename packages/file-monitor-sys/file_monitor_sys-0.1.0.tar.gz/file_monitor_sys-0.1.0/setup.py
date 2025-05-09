from setuptools import setup, find_packages

setup(
    name="file-monitor-sys",
    version="0.1.0",
    packages=find_packages(include=["file_monitor", "file_monitor.*"]),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'file-monitor = file_monitor.main:main',
        ],
    },
)
