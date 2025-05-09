from setuptools import find_packages, setup

setup(
    name='netbox-vpn-inventory',
    version='0.1.0',
    description='Plugin NetBox para inventário de VPNs',
    author='Seu Nome',
    author_email='seu@email.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
)
