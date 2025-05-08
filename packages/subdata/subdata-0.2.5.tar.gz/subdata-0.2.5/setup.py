from setuptools import setup, find_packages

with open('README.md', 'r', encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='subdata',  # Replace with your package’s name
    version='0.2.5',
    # packages=find_packages(),
    packages = ['src/subdata'],
    include_package_data=True,
    install_requires=[ # List your dependencies here
        'pandas',
        'numpy',
        'huggingface_hub',
        'pyarrow',
        # 'fastparquet'
    ],
    url = 'https://github.com/frohleon/subdata_library',
    author='Leon Fröhling',  
    author_email='leon.froehling@gesis.org',
    description='A Python library for automatically creating targeted hate speech datasets.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
