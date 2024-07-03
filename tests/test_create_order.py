import allure
import pytest
import requests
from data_create_order import DataTestOrder
from urls import Urls


class TestCreateOrder:
    @pytest.mark.parametrize('color', [DataTestOrder.color_black, DataTestOrder.color_grey, DataTestOrder.color_black_and_grey, DataTestOrder.color_is_none])
    @allure.title('Проверка создания заказа с разными вариантами указания цветов')
    @allure.description('Создание заказа с указанием одного из двух цветов, созданием заказа с указанием двух цветов '
                        'и без указания цвета. Проверяем, что заказ создался с помощью кода ответа и наличия поля track')
    def test_create_order_with_colors(self, color):
        payload = {
            "firstName": DataTestOrder.firstName,
            "lastName": DataTestOrder.lastName,
            "address": DataTestOrder.address,
            "metroStation": DataTestOrder.metroStation,
            "phone": DataTestOrder.phone,
            "rentTime": DataTestOrder.rentTime,
            "deliveryDate": DataTestOrder.deliveryDate,
            "comment": DataTestOrder.comment,
            "color": color
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/orders", json=payload)
        assert response.status_code == 201 and response.json()["track"] is not None
        print(response.json()["track"])

