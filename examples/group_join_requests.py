import robloxapi, asyncio
client = robloxapi.Client("COOKIE")

async def main():
    group = await client.get_group(2695946)
    requests = await group.get_join_requests()
    for request in requests:
        if request.user['name'] == 'aaldricc':
            await request.accept()

asyncio.run(main())