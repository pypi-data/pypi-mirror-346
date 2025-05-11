from setuptools import setup, find_packages
from pathlib import Path

readme_path = Path(__file__).parent / 'README.md'
with open(readme_path, encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CryptoPaySDK',
    version='1.5.1',  
    author='outodev',
    author_email='outodev@gmail.com',  
    description='Python SDK for Crypto Pay API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/outodev/CryptoPaySDK',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests>=2.25.1'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    keywords='cryptobot crypto pay api sdk send cryptopay',
)