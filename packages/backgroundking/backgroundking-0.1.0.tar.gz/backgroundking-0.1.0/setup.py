from setuptools import setup, find_packages

setup(
    name='backgroundking',
    version='0.1.0',
    description='Background threading utility with dynamic daemon control',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sailesh Wankar',
    author_email='saileshwankar929@gmail.com',
    url='https://github.com/yourusername/backgroundking',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
