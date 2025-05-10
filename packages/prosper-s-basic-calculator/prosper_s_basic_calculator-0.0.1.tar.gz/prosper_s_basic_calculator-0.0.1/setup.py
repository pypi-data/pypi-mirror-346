from setuptools import setup, find_packages

# Classifiers
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

# Setup Configuration
setup(
    name="prosper_s_basic_calculator",  # Package name
    version="0.0.1",
    description="A basic calculator",
    long_description=open('README.txt', encoding='utf-8').read() + '\n\n' + open('CHANGELOG.txt', encoding='utf-8').read(),
    long_description_content_type="text/plain",  # Added to specify the type of long_description
    url='',  # Add your project URL if available
    author='Prosper A.',
    author_email="prosperaigbe545@gmail.com",  # Your email
    license="MIT",  # License type
    classifiers=classifiers,  # Classifiers for your project
    keywords="calculator",  # Keywords related to your project
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[]  # Add dependencies if you have any, or leave it empty
)


