from setuptools import setup,find_packages

setup(
    name='prprogVentas1',
    version='0.0.1',
    author='Jorddy Antonio cabana Rojas',
    author_email='jorddy.crojas@gmail.com',
    description='Paquete para gestionar ventas, precios, impuestos y descuentos',
    long_description=open('README').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yatoriZ/prprogVentas1',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7'
)