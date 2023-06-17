import pytest
import websockets

from Data.main import Main
from Resources.API.websocket_resource import WebsocketResource
from Resources.JM.jmeter_resource import JmeterResource


@pytest.mark.performance_test
class TestPerformance(JmeterResource, WebsocketResource, Main):

    @pytest.mark.websocket
    @pytest.mark.create_order
    @pytest.mark.parametrize("jmx_file", ["post_performance_test.jmx"])
    async def test_api_performance(self, jmx_file, cleanup_log_directory):

        log_directory = cleanup_log_directory
        jmeter_log = rf"{log_directory}\jmeter.log"
        output_xml = rf"{log_directory}\output.xml"
        expected_response_structure = {"id": "random", "stocks": "EUR-USD", "quantity": 125, "status": "PENDING"}
        expected_response_status_code = 201

        async with websockets.connect(self.WEBSOCKET_URL) as websocket:
            print('INFO: Websocket connections is set!')
            self.run_jmeter_in_thread(arguments=(jmx_file, jmeter_log, output_xml))
            execution_times = await self.run_websocket_message_catcher(websocket, 40)

        average_execution_delay = self.calculate_average_execution_delay(execution_times)
        standard_deviation = self.calculate_standard_deviation(execution_times, average_execution_delay)
        self.wait_until_files_are_created(files=(output_xml, jmeter_log))
        assert self.check_response_content(output_xml, expected_response_structure, expected_response_status_code)
        print("METRIC: Average execution delay -", average_execution_delay)
        print("METRIC: Standard deviation -", standard_deviation)
