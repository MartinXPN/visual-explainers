from setuptools import setup, find_packages

setup(
    name='explainers',
    version='0.0.1',
    description='Visual Explainers built with Manim',
    author='Martin Mirakyan',
    author_email='mirakyanmartin@gmail.com',
    python_requires='>=3.9',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'manim>=0.18.0',
        'numpy>=1.26.4',
    ],
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Full list of Trove classifiers: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
    ],
)
