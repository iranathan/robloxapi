from .utils.errors import *
import json


class Gamepass:
    """
    Represents a gamepass
    """
    def __init__(self, request, product_id: int, product_name: str, product_price: int, product_image: str, product_creator, product_onsale: bool):
        """
        Construct a new gamepass class.
        :param request: Used to send requests
        :param product_id: The id of the gamepass
        :param product_name: The name of the gamepass
        :param product_price: The price of the gamepass
        :param product_image: A url of the image of the gamepass
        :param product_creator: The creator of the gamepass
        :param product_onsale: If the gamepass is onsale
        """
        self.request = request
        self.id = product_id
        self.name = product_name
        self.price = product_price
        self.image = product_image
        self.creator = product_creator
        self.for_sale = product_onsale

    async def buy(self):
        """
        Buys the gamepass
        :return: StatusCode
        """
        if not self.for_sale:
            raise NotFound("That gamepass is not for sale.")
        data = json.dumps({
            "expectedCurrency": 1,
            "expectedPrice": self.price
        })
        r = await self.request.request(url=f'https://economy.roblox.com/v1/purchases/products/{self.id}', data=data, method="POST")
        return r.status_code
