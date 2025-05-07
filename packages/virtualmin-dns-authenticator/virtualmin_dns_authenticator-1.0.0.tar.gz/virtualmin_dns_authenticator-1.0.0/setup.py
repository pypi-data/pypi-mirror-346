from setuptools import setup, find_packages

setup(
    name="virtualmin-dns-authenticator",
    version="1.0.0",
    description="DNS Authenticator plugin for Certbot using Virtualmin API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Gri_89",
    author_email="gri.chernikov@gmail.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "certbot>=1.0",
        "requests>=2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "certbot.plugins": [
            "virtualmin-dns = virtualmin_dns_authenticator.authenticator:Authenticator",
        ],
    },
    python_requires=">=3.7",
)