from setuptools import setup, find_packages

setup(
    name='beamz',
    version='0.0.1',
    packages=find_packages(),
    description='Reserved package name.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Quentin Wach',
    author_email='quentin.wach@gmail.com',
    url='https://github.com/quentinwach/beamz',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)