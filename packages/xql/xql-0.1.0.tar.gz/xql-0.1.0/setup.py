from setuptools import setup, find_packages

setup(
    name='xql',
    version='0.1.0',  # Use semantic versioning
    packages=find_packages(),  # Automatically discover all packages
    install_requires=[
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'bcrypt',
        'pydantic',
        'requests',
        'python-jose',  # For JWT handling
    ],
    include_package_data=True,  # Ensure static files are included in the package
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',  # Adjust for your Python version
    ],
    python_requires='>=3.12',  # Make sure the required Python version is defined
    entry_points={
        'console_scripts': [
            'xql = xql_main:main_function',  # This is for CLI functionality if needed
        ],
    },
)
