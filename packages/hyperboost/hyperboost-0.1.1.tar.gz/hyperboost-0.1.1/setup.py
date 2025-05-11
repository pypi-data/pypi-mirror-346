from setuptools import setup, find_packages

setup(
    name='hyperboost',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21',
        'scikit-learn>=1.0',
        'scipy>=1.7',
        'matplotlib>=3.4'
    ],
    description='Библиотека для оптимизации гиперпараметров с использованием байесовской оптимизации и эволюционных алгоритмов',
    author='itbert',
    # author_email='',
    url='https://github.com/itbert/hyperboost',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
