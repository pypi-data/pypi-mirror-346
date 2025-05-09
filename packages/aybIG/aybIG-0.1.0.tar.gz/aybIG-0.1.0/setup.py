from setuptools import setup, find_packages

setup(
    name='aybIG',  # The name of your package
    version='0.1.0',  # The current version of your package
    description='Instagram API logic for user data extraction',  # Short description of your package
    long_description=open('README.md').read(),  # Long description read from your README.md
    long_description_content_type='text/markdown',
    author='AYOUB QADDA',
    packages=find_packages(),  # This will automatically find your package
    install_requires=[],  # List any dependencies your package has here
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
