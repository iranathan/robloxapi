import robloxapi, asyncio
client = robloxapi.Client("COOKIE")


"""
Promote a user in a specified group.
"""
async def main():
    group = await client.get_group(1)
    oldrole, newrole = await group.promote(1)
    print(f"The user was promoted from {oldrole.name} to {newrole.name}")

asyncio.run(main())