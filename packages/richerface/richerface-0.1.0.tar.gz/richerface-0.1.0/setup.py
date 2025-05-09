from setuptools import setup, find_packages

setup(
    name="richerface",
    version="0.1.0",
    description="A package for training and evaluating facial recognition models.",
    author="Akshay",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "tensorflow>=2.0",
        "opencv-python",
        "matplotlib",
        "numpy"
    ],
    entry_points={
        'console_scripts': [
            'train-face=richerface.face:train_model'
        ]
    },
)
 