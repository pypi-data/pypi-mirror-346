from setuptools import setup, find_packages

setup(
    name='astraX',
    version='0.1.0',
    author='Raghavendra',
    author_email='dosinarayanaraghavendra@gmail.com',
    description='astraX: An Powerful Agents framework',
    long_description="Agent Framework",
    long_description_content_type='text/markdown',
    url='https://github.com/narayanaraghavendra/astraX',  # your repo
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'transformers',
        'torch',
        'sentence-transformers',
        'huggingface_hub',
        'requests',
        'tqdm'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

