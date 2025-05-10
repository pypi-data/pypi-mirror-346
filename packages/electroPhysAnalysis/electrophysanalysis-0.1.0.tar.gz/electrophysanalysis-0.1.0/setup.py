from setuptools import setup, find_packages

setup(
    name='electroPhysAnalysis',
    version='0.1.0',
    author='Gerardo Zerbetto De Palma',
    author_email='g.zerbetto@gmail.com',
    description='Visualizador interactivo de registros ABF con promediado por selección',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/GeraZerbetto/electroPhysAnalysis',
    packages=find_packages(),
    install_requires=[
        'pyabf',
        'PyQt5',
        'matplotlib',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'electrophys=electroPhysAnalysis.gui:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
