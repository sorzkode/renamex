import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='renamex',
    version='1.0.0',
    description='Bulk file renaming utility.',
    url='https://github.com/sorzkode/',
    author='Mister Riley',
    author_email='<sorzkode@proton.me>',
    packages=setuptools.find_packages(),
    install_requires=['pyfiglet', 'click', 'tkinter'],
    long_description='Renamomicon Ex-Bulkus...the script of the dead. AKA an Evil Dead themed bulk file renaming utility.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
