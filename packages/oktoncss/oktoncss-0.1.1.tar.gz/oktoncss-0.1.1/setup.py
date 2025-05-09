from setuptools import setup, find_packages

setup(
    name="oktoncss",
    version="0.1.1",
    description="Créer des interfaces graphiques de bureau avec un style CSS",
    author="Brayan Tematio",
    author_email="brayantematio1@email.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
