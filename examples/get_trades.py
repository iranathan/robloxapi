import robloxapi, asyncio
client = robloxapi.Client("COOKIE")

"""
Gets all trades
"""
async def main():
    trades = await client.get_trades()
    for trade in trades:
        await trade.decline()

asyncio.run(main())