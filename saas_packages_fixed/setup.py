from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="saas_packages",
    version="0.1.1",
    description="ERPNext SaaS packages + provisioning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Company",
    author_email="dev@yourco.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
