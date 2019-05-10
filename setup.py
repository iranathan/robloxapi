from setuptools import setup, find_packages
setup(
    name="robloxapi",
    version="2.5",
    packages=find_packages(),
    scripts=['when_install.py'],


    install_requires=[
    'requests',
    'beautifulsoup4',
    'html2text'
    ],

    author="iranathan",
    description="A Python wrapper for roblox",
    license="MIT",
    keywords="https://github.com/iranathan/robloxapi",
    url="https://github.com/iranathan/robloxapi",   
    project_urls={
        "Documentation": "https://github.com/iranathan/robloxapi/wiki",
        "Source Code": "https://github.com/iranathan/robloxapi",
    }


)
