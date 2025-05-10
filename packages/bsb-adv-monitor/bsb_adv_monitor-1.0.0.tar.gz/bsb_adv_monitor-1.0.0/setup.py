from setuptools import setup, find_packages

setup(
    name='bsb-adv-monitor',
    version='1.0.0',
    description='Advanced device monitoring tool by BLACK SPAMMER BD',
    author='BLACK SPAMMER BD',
    author_email='your@email.com',  # এখানে তোর ইমেইল দিন
    url='https://github.com/BlackSpammerBd/bsb-adv-monitor',
    packages=find_packages(),
    install_requires=[
        'flask',
        'pyngrok',
        'requests',
        'keyboard',
        'opencv-python',
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'sp=bsb_adv_monitor.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
