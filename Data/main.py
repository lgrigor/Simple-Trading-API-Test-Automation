

class Main:

    # URLS
    BASE_URL = "http://localhost:8000"
    WEBSOCKET_URL = 'ws://localhost:8000/ws'

    # APPS
    JMETER = r"D:\apache-jmeter-5.5\bin\jmeter.bat"

    # ENDPOINTS
    ALL_ORDERS_ENDPOINT = "/orders"
    SINGLE_ORDER_ENDPOINT = "/orders/{}"
    CREATE_ORDER_ENDPOINT = "/orders"
    DELETE_ORDER_ENDPOINT = "/orders/{}"
