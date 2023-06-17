import requests

from Resources.API.common import Common


class Order(Common):

    def send_get_all_orders(self):
        response = requests.get(self.BASE_URL + self.ALL_ORDERS_ENDPOINT)
        return response

    def send_get_single_order(self, order_id: int):
        response = requests.get(self.BASE_URL + self.SINGLE_ORDER_ENDPOINT.format(order_id))
        return response

    def send_post_order(self, stocks: str | None, quantity: int | None, additional_data=None):
        headers = {"Content-Type": "application/json"}
        json_data = dict()

        if stocks is not None:
            json_data["stocks"] = stocks
        if quantity is not None:
            json_data["quantity"] = quantity

        if additional_data:
            json_data.update(additional_data)

        response = requests.post(self.BASE_URL + self.CREATE_ORDER_ENDPOINT, headers=headers, json=json_data)
        return response

    def send_delete_order(self, order_id: int):
        response = requests.delete(self.BASE_URL + self.DELETE_ORDER_ENDPOINT.format(order_id))
        return response
