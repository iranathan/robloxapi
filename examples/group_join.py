import robloxapi, asyncio
client = robloxapi.Client("COOKIE")  # or client.login


"""
Joins a group.
"""
async def main():
    group = await client.get_group(3788537)
    print(f"joining {group.name}")
    await group.join('2captcha token')
    await group.leave()  # No captcha with leaving groups

asyncio.run(main())