import robloxapi, asyncio
client = robloxapi.Client()

"""
This should get all the gamepasses a user has.
"""

async def main():
    ira = await client.get_user_by_id(109503558)
    gamepasses = await ira.get_gamepasses()
    for gamepass in gamepasses:
        print(gamepass.name, gamepass.price)

asyncio.run(main())
