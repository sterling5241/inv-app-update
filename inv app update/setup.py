from setuptools import setup, find_packages

setup(
    name='inv-app-update',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'pandas',
        'pillow',
        'matplotlib',
        'qrcode',
        'pywin32',
    ],
    entry_points={
        'console_scripts': [
            'inv-app=main:main',
        ],
    },
)
