import robloxapi, asyncio
client = robloxapi.Client("COOKIE")

async def main():
    group = await client.get_group(2695946)
    members = await group.get_members()
    for member in members:
        await member.promote()

asyncio.run(main())