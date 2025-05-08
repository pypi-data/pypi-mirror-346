from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_desc = f.read()

setup(
    name="ibb-veri-merkezi",
    version="0.1.0",
    author="ilker turan",
    author_email="email@example.com",
    description="İstanbul Büyükşehir Belediyesi'nin (İBB) Açık Veri Merkezi dahilindeki servisler için kolay erişim sağlar.",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url="https://github.com/aribilgiogr/ibb-veri-merkezi",
    packages=find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "pandas>=2.2.3",
        "requests>=2.32.3"
    ]
)
