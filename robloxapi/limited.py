class Limited:
    def __init__(self, request, limited_id, serial_number, user_asset_id, average_price):
        self.request = request
        self.id = limited_id
        self.serial_number = serial_number
        self.user_asset_id = user_asset_id
        self.average_price = average_price
        self.original_price = original_price

    async def get_resellers(self):
        r = self.request.request(url="https://economy.roblox.com/v1/assets/128158439/resellers?limit=100", method='GET')
        data = r.json()['data']
