from distutils.core import setup
setup(
  name = 'robloxapi',
  packages = ['robloxapi', 'robloxapi.utils'],
  version = '3.1',   
  license='MIT',       
  description = 'A Python wrapper for roblox',
  author = 'Iranathan',                
  author_email = 'iranathan8@gmail.com',
  url = 'https://github.com/user/reponame', 
  keywords = ['python_roblox', 'roblox', 'robloxapi'],
  install_requires=[            
          'requests',
          'beautifulsoup4'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      

    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.6',
  ],
)
