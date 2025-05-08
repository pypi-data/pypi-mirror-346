from setuptools import setup, find_packages

setup(
    name='streambotcore',
    version='0.2.0',
    description='Unified modular Discord and Twitch bot framework',
    author='AmongTheCouch23',
    author_email='AmongTheCouch_Studios@hotmail.com',
    packages=find_packages(),
    install_requires=[
        'discord.py',
        'twitchio',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
