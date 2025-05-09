from setuptools import setup, find_packages
setup(
    name='track_logging_model',
    version='1.0.0',
    packages=find_packages(),
    description='Log parameters, metrics, and artifacts using track logging model .',
    author='Radhika Menon',
    author_email='Radhika.Menon@cognizant.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)