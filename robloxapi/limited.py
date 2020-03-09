from .utils.classes import Reseller
from typing import List


class Limited:
    """
    Represents a limited
    """
    def __init__(self, request, limited_id, serial_number, user_asset_id, average_price):
        """
        Created a limited.
        :param request: Used to send requests
        :param limited_id: The id of the limited
        :param serial_number: The serial number of the limited
        :param user_asset_id: The user asset id
        :param average_price: The average price of the limited
        """
        self.request = request
        self.id = limited_id
        self.serial_number = serial_number
        self.user_asset_id = user_asset_id
        self.average_price = average_price
        self.original_price = original_price

    async def get_resellers(self) -> List[Reseller]:
        r = self.request.request(url="https://economy.roblox.com/v1/assets/128158439/resellers?limit=100", method='GET')
        data = r.json()['data']
        sellers = []
        for user in data:
            sellers.append(Reseller(user['price'], user['seller']['name'], user['seller']['id'], user['serialNumber']))
        return sellers
