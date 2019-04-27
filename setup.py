from distutils.core import setup
setup(
  name = 'robloxapi',         # How you named your package folder (MyLib)
  packages = ['robloxapi'],   # Chose the same as "name"
  version = '2.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A Python wrapper for roblox',   # Give a short description about your library
  author = 'Iranathan',                   # Type in your name
  author_email = 'iranathan8@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['python_roblox', 'roblox', 'robloxapi'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'beautifulsoup4'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license

    'Programming Language :: Python :: 3.6',
  ],
)
