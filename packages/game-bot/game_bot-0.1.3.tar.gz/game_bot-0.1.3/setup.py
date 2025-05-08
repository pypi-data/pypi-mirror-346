from setuptools import setup, find_packages

setup(
    name='game_bot',
    version='0.1.3',
    packages=find_packages(where='src/python'),
    package_dir={'': 'src/python'},
    install_requires=[
        'pywin32>=305',
        'opencv-python>=4.8.0',
        'paddleocr>=2.6.1.3',
        'numpy>=1.24.0',
        'mss>=10.0.0',
        'keyboard>=0.13.5',
    ],
    entry_points={
        'console_scripts': [
            'picker=game_bot.picker:main'
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
    ],
    platforms=['Windows'],
)