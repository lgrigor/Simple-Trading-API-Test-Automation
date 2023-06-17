import time

import pytest

from Resources.API.database import Database
from Resources.API.order import Order


@pytest.mark.api_test
class TestOrders(Order, Database):

    @pytest.mark.create_order
    def test_post_order(self):
        response = self.send_post_order("EUR-AMD", 3000)
        assert self.verify_status_code(response, 201)
        assert self.verify_response_key_value_class(response, "id", int)
        assert self.verify_response_key_value(response, "status", "PENDING")
        assert self.verify_response_key_value(response, "stocks", "EUR-AMD")
        assert self.verify_response_key_value(response, "quantity", 3000)

    @pytest.mark.create_order
    @pytest.mark.get_one_order
    def test_content_after_post_order(self):
        response = self.send_post_order("EUR-USD", 1200)
        order_id = self.get_value_from_response(response, "id")
        assert self.verify_status_code(response, 201)
        assert self.verify_response_key_value_class(response, "id", int)
        assert self.verify_response_key_value(response, "status", "PENDING")
        assert self.verify_response_key_value(response, "stocks", "EUR-USD")
        assert self.verify_response_key_value(response, "quantity", 1200)

        time.sleep(5)
        response = self.send_get_single_order(order_id)
        assert self.verify_status_code(response, 200)
        assert self.verify_response_key_value_class(response, "id", int)
        assert self.verify_response_key_value(response, "status", "EXECUTED")
        assert self.verify_response_key_value(response, "stocks", "EUR-USD")
        assert self.verify_response_key_value(response, "quantity", 1200)

    @pytest.mark.create_order
    @pytest.mark.cancel_order
    @pytest.mark.get_one_order
    def test_content_after_delete_order(self):
        response = self.send_post_order("USD-CAD", 4500)
        order_id = self.get_value_from_response(response, "id")
        assert self.verify_status_code(response, 201)
        assert self.verify_response_key_value_class(response, "id", int)
        assert self.verify_response_key_value(response, "status", "PENDING")
        assert self.verify_response_key_value(response, "stocks", "USD-CAD")
        assert self.verify_response_key_value(response, "quantity", 4500)

        response = self.send_delete_order(order_id)
        assert self.verify_status_code(response, 204)

        time.sleep(1)
        response = self.send_get_single_order(order_id)
        assert self.verify_status_code(response, 200)
        assert self.verify_response_key_value_class(response, "id", int)
        assert self.verify_response_key_value(response, "status", "CANCELLED")
        assert self.verify_response_key_value(response, "stocks", "USD-CAD")
        assert self.verify_response_key_value(response, "quantity", 4500)

    @pytest.mark.get_one_order
    def test_get_single_order(self):
        response = self.send_get_single_order(383)
        expected_data = self.get_single_order_from_db(383)
        assert self.verify_status_code(response, 200)
        assert self.verify_response_content(response, expected_data)

    @pytest.mark.get_all_orders
    def test_get_all_orders(self):
        response = self.send_get_all_orders()
        assert self.verify_status_code(response, 200)

    @pytest.mark.negative_test
    @pytest.mark.cancel_order
    def test_delete_order_with_non_existing_id(self):
        response = self.send_delete_order(9999)
        assert self.verify_status_code(response, 404)
        assert self.verify_response_key_value(response, "code", 404)
        assert self.verify_response_key_value(response, "message", "Order not found")
        assert self.verify_response_data_length(response, 2)

    @pytest.mark.negative_test
    @pytest.mark.get_one_order
    def test_get_order_with_non_existing_id(self):
        response = self.send_get_single_order(9999)
        assert self.verify_status_code(response, 404)
        assert self.verify_response_key_value(response, "code", 404)
        assert self.verify_response_key_value(response, "message", "Order not found")
        assert self.verify_response_data_length(response, 2)

    @pytest.mark.negative_test
    @pytest.mark.create_order
    def test_post_order_without_stock(self):
        expected_status_code = 400
        expected_error_message = "Missing stocks"
        response = self.send_post_order(stocks="", quantity=100)
        assert self.verify_status_code(response, expected_status_code)
        assert self.verify_response_key_value(response, "code", expected_status_code)
        assert self.verify_response_key_value(response, "message", expected_error_message)
        assert self.verify_response_data_length(response, 2)

        response = self.send_post_order(stocks=None, quantity=100)
        assert self.verify_status_code(response, expected_status_code)
        assert self.verify_response_key_value(response, "code", expected_status_code)
        assert self.verify_response_key_value(response, "message", expected_error_message)
        assert self.verify_response_data_length(response, 2)

    @pytest.mark.negative_test
    @pytest.mark.create_order
    def test_post_order_without_quantity(self):
        expected_status_code = 400
        expected_error_message = "Missing quantity"
        response = self.send_post_order(stocks="AUD-EUR", quantity=0)
        assert self.verify_status_code(response, expected_status_code)
        assert self.verify_response_key_value(response, "code", expected_status_code)
        assert self.verify_response_key_value(response, "message", expected_error_message)
        assert self.verify_response_data_length(response, 2)

        response = self.send_post_order(stocks="AUD-EUR", quantity=-1)
        assert self.verify_status_code(response, expected_status_code)
        assert self.verify_response_key_value(response, "code", expected_status_code)
        assert self.verify_response_key_value(response, "message", expected_error_message)
        assert self.verify_response_data_length(response, 2)

        response = self.send_post_order(stocks="AUD-EUR", quantity=None)
        assert self.verify_status_code(response, expected_status_code)
        assert self.verify_response_key_value(response, "code", expected_status_code)
        assert self.verify_response_key_value(response, "message", expected_error_message)
        assert self.verify_response_data_length(response, 2)

    @pytest.mark.negative_test
    @pytest.mark.create_order
    def test_post_order_with_extra_properties(self):
        input_data = {"rate": 140.66, "change": 0.57}
        input_stocks = "GBP-JPY"
        input_quantity = 1000
        expected_status_code = 400
        expected_error_message = "Redundant properties - ['rate', 'change']"
        expected_response_length = 2
        response = self.send_post_order(stocks=input_stocks, quantity=input_quantity, additional_data=input_data)
        assert self.verify_status_code(response, expected_status_code)
        assert self.verify_response_key_value(response, "code", expected_status_code)
        assert self.verify_response_key_value(response, "message", expected_error_message)
        assert self.verify_response_data_length(response, expected_response_length)
