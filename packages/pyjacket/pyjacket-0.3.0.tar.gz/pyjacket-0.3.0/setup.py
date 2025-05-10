import setuptools

__version__ = '0.3.0'

GIT_USER = 'Kasper-Arfman'
NAME = 'pyjacket'

requires = [
    'numpy>=1.25.2', 
    'opencv-contrib-python>=4.8.0.76', 
    'imageio>=2.31.2', 
    'matplotlib>=3.7.1', 
    'pandas>=2.1.0', 
    'Pillow>=10.0.0', 
    'scikit-image>=0.21.0', 
    'scipy>=1.11.2',
    'nd2>=0.10.1',
    'tifffile>=2024.7.2',
    'PIMS>=0.6.1'
    ]

setuptools.setup(
    name=NAME,
    version=__version__,
    author='Kasper Arfman',
    author_email='Kasper.arf@gmail.com',
    
    download_url=f'http://pypi.python.org/pypi/{NAME}',
    project_urls={
        # 'Documentation': 'https://pyglet.readthedocs.io/en/latest',
        'Source': f'https://github.com/{GIT_USER}/{NAME}',
        'Tracker': f'https://github.com/{GIT_USER}/{NAME}/issues',
    },
    description='Lorem ipsum',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url=f'https://github.com/{GIT_USER}/{NAME}',
    # license='MIT'
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent"
    ],
    # python_requires="",
    # entry_points=[],
    install_requires=requires,
    # # Add _ prefix to the names of temporary build dirs
    # options={'build': {'build_base': '_build'}, },
    # zip_safe=True,
)

