
class Database:

    @staticmethod
    def get_single_order_from_db(order_id: int) -> dict:
        """Simulation of obtaining data from the database"""
        if order_id == 383:
            return {
                "id": 383,
                "stocks": "TEST-DATA-2",
                "quantity": 350,
                "status": "PENDING"
            }
