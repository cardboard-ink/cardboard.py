from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cardboard.py',
    version='0.0.1',
    author='YumYummity',
    author_email='034nop@gmail.com',
    description='API wrapper for https://cardboard.ink/api/v1/',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cardboard-ink/cardboard.py/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.9',
    install_requires=[
        'requests',
        'aiohttp'
    ],
)