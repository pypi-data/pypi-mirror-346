from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vipentium",
    version="1.1.0",  # Replace with your desired version
    author="suresh",  # Replace with your name or organization
    description="Powerful & user-friendly Python testing – streamlined workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://suresh-pyhobbyist.github.io/vipentium/", 
    packages=find_packages(),
    install_requires=[],  # List any dependencies your framework needs
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
    entry_points={
        'console_scripts': [
            'vipentium-runner = vipentium.vipentium_runner:main'  # Adjust if your main script has a different name
        ],
    }
)



