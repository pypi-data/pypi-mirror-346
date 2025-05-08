from setuptools import setup
from pathlib import Path
import platform

if platform.system() != "Windows":
    sys.exit("This package only works on Windows.")
    
setup(
    name='anv',
    version='1.0',
    license='MIT',
    packages=[],
    author='AnvPy (Android Versatile Python)',
    author_email='techanvpy@gmail.com',
    include_package_data=True,
    data_files=[('Scripts', ['anv.exe'])],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    description='A command line tool to manage anvpy projects',
    long_description=Path("README.md").read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/techAnvPy/AnvPy',
    project_urls={ 
        'Github': 'https://github.com/techAnvPy/AnvPy',
        'Youtube': 'https://youtube.com/playlist?list=PL9pITIt_f9Msvsm_fLnysBH3Oakgw0el5&si=AguxrYK4I8zaChp6',
        'Telegram': ' https://t.me/andropython',
    }
)
