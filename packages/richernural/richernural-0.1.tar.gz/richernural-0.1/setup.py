from setuptools import setup, find_packages

setup(
    name='richernural',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'opencv-python',
        'tensorflow',
        'scikit-learn',
        'torch'
    ],
    author='Akshay',
    description='MNIST SVM and Neural Network example with PyTorch and sklearn',
    url='https://github.com/yourusername/mnist_model_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
