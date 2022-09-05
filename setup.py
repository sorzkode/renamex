import setuptools

setuptools.setup(
    name='renamex',
    version='1.0.0',
    description='Bulk file renaming utility.',
    url='https://github.com/sorzkode/',
    author='sorzkode',
    author_email='<sorzkode@proton.me>',
    packages=setuptools.find_packages(),
    install_requires=['pyfiglet', 'click'],
    long_description='Renamomicon Ex-Bulkus...the script of the dead. AKA an Evil Dead themed bulk file renaming utility.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT',
        'Operating System :: OS Independent',
        ],
)