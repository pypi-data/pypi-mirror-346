from setuptools import setup, find_packages

setup(
    name='pykeflow',
    version='0.1.0',
    description='Programmatic GitHub Actions workflow generator with clean YAML support',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='PJ Hayes',
    author_email='archood2next@gmail.com',
    url='https://github.com/ArchooD2/pykeflow',
    packages=find_packages(),  # Looks for pykeflow/ with __init__.py
    python_requires='>=3.7',
    install_requires=[
        'ruamel.yaml',
        'snaparg',
    ],
    entry_points={
        'console_scripts': [
            'pykeflow=pykeflow.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities',
    ],
    license='MPL-2.0',
)
