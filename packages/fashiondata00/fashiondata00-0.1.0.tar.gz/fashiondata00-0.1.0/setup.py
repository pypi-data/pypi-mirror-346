from setuptools import setup, find_packages

setup(
    name='fashiondata00',
    version='0.1.0',
    description='Excel-style SUMIFS function for pandas',
    author='fashiondata00',
    author_email='fashiondata00@gmail.com',
    packages=find_packages(),
    install_requires=['pandas'],
    include_package_data=True,
    zip_safe=False,
)
