import asyncio
import re
import time


class WebsocketResource:

    @staticmethod
    async def get_message_from_websocket(websocket, timeout) -> str | None:
        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=timeout)
            return message
        except asyncio.TimeoutError:
            return None

    async def run_websocket_message_catcher(self, websocket, expected_message_count: int) -> dict:
        execution_times = dict()
        for i in range(expected_message_count):
            text = await self.get_message_from_websocket(websocket, 5)
            if text:
                order_id = re.search(r"\d+", text).group()
                print("INFO: ", text, order_id)
                if order_id not in execution_times:
                    execution_times[order_id] = time.time()
                else:
                    execution_times[order_id] = round(time.time() - execution_times[order_id], 5)

        print(f"INFO: Execution times - {execution_times}")
        return execution_times
