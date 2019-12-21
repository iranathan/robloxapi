==========================
 Roblox API Documentation
==========================

Current documentation for Roblox API. Need any further assistance join our server! https://discord.gg/ZVcBRbV

======
Client
======

async def get_group(group_id: int) -> Group:
============================================

Get a Group class with a group id

Parameters
~~~~~~~~~~~
- Group ID

Output
~~~~~~~
- :ref: `Group`

Example
~~~~~~~~
.. code-block:: python

   import robloxapi, asyncio
   rbx = robloxapi.Client('Cookie')

   async def main():
      group = await rbx.get_group()

   asyncio.run(main())

async def get_user_by_username(username: str) -> User:
======================================================

Get a User class with a username

Parameters
~~~~~~~~~~~
- Username

Output
~~~~~~~
- :ref: `User`

Example
~~~~~~~~
.. code-block:: python

   import robloxapi, asyncio
   rbx = robloxapi.Client('Cookie')

   async def main():
      group = await rbx.get_user_by_username("ROBLOX")

   asyncio.run(main())

async def get_user_by_id(roblox_id: int) -> User:
======================================================

Get a User class with a user id

Parameters
~~~~~~~~~~~
- Roblox Id

Output
~~~~~~~
- :ref: `User`

Example
~~~~~~~~
.. code-block:: python

   import robloxapi, asyncio
   rbx = robloxapi.Client('Cookie')

   async def main():
      User = await rbx.get_user_by_id(1)

   asyncio.run(main())

async def get_user(name=None, id=None) -> User:
===============================================

A proxy for get_user_by_id, get_user_by_username

Parameters
~~~~~~~~~~~
- Username (Optional)
- Roblox Id (Optional)

Output
~~~~~~~
- :ref: `User`

Example
~~~~~~~~
.. code-block:: python

   import robloxapi, asyncio
   rbx = robloxapi.Client('Cookie')

   async def main():
      roblox_by_name = await rbx.get_user(name="ROBLOX")
      roblox_by_id = await rbx.get_user(id=1)
      print(roblox_by_name == roblox_by_id) # -> True

   asyncio.run(main())