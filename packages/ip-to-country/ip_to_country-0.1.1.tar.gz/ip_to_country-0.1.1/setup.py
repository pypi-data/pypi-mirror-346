from setuptools import setup, find_packages

setup(
    name='ip-to-country',
    version='0.1.1',
    description='Convert IP addresses to countries using delegated registry data',
    author='Pieter-Jan Coenen',
    author_email='pieterjan.coenen@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={'ip_to_country': ['../data/iso3166.csv', '../data/ipv4_ranges.pkl', '../data/ipv6_ranges.pkl']},  # Include your CSV
    install_requires=[],
    python_requires='>=3.6',
)