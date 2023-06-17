import pytest
import websockets

from Resources.API.order import Order
from Resources.API.websocket_resource import WebsocketResource


@pytest.mark.api_test
class TestWebbSocket(WebsocketResource, Order):

    @pytest.mark.create_order
    @pytest.mark.cancel_order
    @pytest.mark.websocket
    @pytest.mark.asyncio
    async def test_websocket_notification(self):
        async with websockets.connect(self.WEBSOCKET_URL) as websocket:
            response = self.send_post_order("EUR-AMD", 3000)
            order_id = self.get_value_from_response(response, "id")
            expected_message = f"Order {order_id} has been executed. Status: PENDING"
            actual_message = await self.get_message_from_websocket(websocket=websocket, timeout=10)
            assert actual_message == expected_message

            expected_message = f"Order {order_id} has been executed. Status: EXECUTED"
            actual_message = await self.get_message_from_websocket(websocket=websocket, timeout=10)
            assert actual_message == expected_message

            self.send_delete_order(order_id)
            expected_message = f"Order {order_id} has been executed. Status: CANCELLED"
            actual_message = await self.get_message_from_websocket(websocket=websocket, timeout=10)
            assert actual_message == expected_message
