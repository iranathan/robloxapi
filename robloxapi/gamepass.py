from .utils.errors import *
import json


class Gamepass:
    def __init__(self, request, product_id, product_name, product_price, product_image, product_creator, product_onsale):
        self.request = request
        self.id = product_id
        self.name = product_name
        self.price = product_price
        self.image = product_image
        self.creator = product_creator
        self.for_sale = product_onsale

    async def buy(self):
        if not self.for_sale:
            raise NotFound("That gamepass is not for sale.")
        data = json.dumps({
            "expectedCurrency": 1,
            "expectedPrice": self.price
        })
        r = await self.request.request(url=f'https://economy.roblox.com/v1/purchases/products/{self.id}', data=data, method="POST")
        return r.status_code
