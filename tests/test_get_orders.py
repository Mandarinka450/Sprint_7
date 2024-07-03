import allure
import requests
from urls import Urls


class TestGetOrders:
    @allure.title('Проверка получения списка заказов')
    @allure.description('Проверяем, что в ответ на запрос приходит список заказов')
    def test_get_not_null_list_of_orders(self):
        response = requests.get(f"{Urls.BASE_URL}/api/v1/orders")
        assert response.status_code == 200 and response.json()["orders"] is not None
