import robloxapi, asyncio
client = robloxapi.Client("COOKIE")


"""
Gets all users of a group.
"""
async def main():
    group = await client.get_group(2695946)
    async for member in group.get_members():
        print(f"{member.name} has role {member.role.name}")

asyncio.run(main())