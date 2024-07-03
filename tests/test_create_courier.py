import allure
import requests
from data_create_courier import DataTestCourier
from urls import Urls


class TestsCreateCourier:
    @allure.title('Проверка создания курьера в системе')
    @allure.description('Проверяем, что курьер действительно создался, что поле id приходит в теле ответа. После '
                        'выолпнения теста удаляем тестовые данные')
    def test_success_create_courier(self):
        payload = {
            "login": DataTestCourier.login,
            "password": DataTestCourier.password,
            "firstName": DataTestCourier.firstName
        }
        requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload)
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        id_courier = response.json()["id"]
        # Проверяем, что такой курьер создался
        assert response.status_code == 200 and id_courier is not None
        # Удаление тестовых данных
        requests.delete(f"{Urls.BASE_URL}/api/v1/courier/{id_courier}")

    @allure.title('Проверка создания двух одинаковых курьеров')
    @allure.description('Создаем два раза курьеров с одними и те же данными. Проверяем, что при повторной отправке '
                        'запроса на создание курьера приходит соответствующий код и тело ответа, то есть ошибка')
    def test_create_two_identical_courier(self):
        payload = {
            "login": DataTestCourier.login,
            "password": DataTestCourier.password,
            "firstName": DataTestCourier.firstName
        }
        # Создаем курьера первый раз
        requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload)
        response_first = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        id_courier = response_first.json()["id"]
        # Создаем такого же курьера второй раз
        response_second = requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload)
        assert response_second.status_code == 409 and response_second.json()["message"] == "Этот логин уже используется. Попробуйте другой."

        # Удаление тестовых данных
        requests.delete(f"{Urls.BASE_URL}/api/v1/courier/{id_courier}")

    @allure.title('Проверка создания курьера с заполнением только обязательных полей')
    @allure.description('Проверяем, что при заполнении двух обязательных полей курьер успешно создается и приходит верный код и тело ответа')
    def test_create_courier_with_complete_all_needed_fields(self):
        payload = {
            "login": DataTestCourier.login,
            "password": DataTestCourier.password
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload)
        assert response.status_code == 201 and response.json()["ok"] is True

        # Удаление тестовых данных
        response_for_delete = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        id_courier = response_for_delete.json()["id"]
        requests.delete(f"{Urls.BASE_URL}/api/v1/courier/{id_courier}")

    @allure.title('Проверка создания курьера с уже существующим логином')
    @allure.description('При создании курьера с уже существующим логином приходит ошибка. Проверяем соответствующий код и тело ответа')
    def test_create_courier_with_login_is_exists(self):
        payload_one = {
            "login": DataTestCourier.login,
            "password": DataTestCourier.password,
            "firstName": DataTestCourier.firstName
        }
        payload_two = {
            "login": DataTestCourier.login,
            "password": "PooPooPiDuPoo",
            "firstName": "Gaara"
        }
        requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload_one)
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload_two)
        assert response.status_code == 409 and response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

        # Удаление тестовых данных
        response_for_delete = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload_one)
        id_courier = response_for_delete.json()["id"]
        requests.delete(f"{Urls.BASE_URL}/api/v1/courier/{id_courier}")

    @allure.title('Проверка создания курьера при условии, что одного из обязательных полей нет в теле запроса')
    @allure.description('Если нет одного из обязательных полей для создания курьера, приходит ошибка. Проверяем '
                        'соответствующий код и тело ответа')
    def test_create_courier_without_one_of_needed_fields(self):
        payload = {
            "login": DataTestCourier.login
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier", data=payload)
        assert response.status_code == 400 and response.json()["message"] == "Недостаточно данных для создания учетной записи"
