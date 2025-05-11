from setuptools import setup, find_packages

setup(
    name='gPhotosAlbum_JPEGcompression',
    version='2.1.7',
    author='Abhishek Venkatachalam',
    author_email='abhishek.venkatachalam06@gmail.com',
    description='Takes Google Photos Album (visible to anyone with url) and produces a zip file with compressed JPEGS.',
    long_description=(
        "For more information about the author, visit [LinkedIn](https://www.linkedin.com/in/abhishek-venkatachalam-62121049/).\n\n"
        + open('README.md').read()
    ),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pillow',
        'tqdm',
        'requests'
    ],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)