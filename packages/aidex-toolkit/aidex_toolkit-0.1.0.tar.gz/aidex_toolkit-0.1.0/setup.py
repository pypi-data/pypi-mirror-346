from setuptools import setup, find_packages

setup(
    name='aidex_toolkit',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
    ],
    author='Godsave Kawurem',
    author_email='godsaveogbidor@gmail.com',
    description='Ai/ML trainings package and guide from scratch with sample data support.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Perfect-Aimers-Enterprise/aidex_toolkit.git',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
