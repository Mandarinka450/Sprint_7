import allure
import requests
from data_login_courier import DataLoginCourier
from urls import Urls


class TestLoginCourier:
    @allure.title('Проверка авторизации курьера в системе')
    @allure.description('При запросе передаются два обязательных поля (их всего два). Проверяем, что приходит '
                        'ожидаемый код и тело ответа, то есть статус код и поле id, которое не пустое')
    def test_success_login_courier_with_all_needed_fields(self):
        payload = {
            "login": DataLoginCourier.login,
            "password": DataLoginCourier.password
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        assert response.status_code == 200 and response.json()["id"] is not None

    @allure.title('Проверка авторизации курьера с неверным логином')
    @allure.description('Проверяем, что при отправке запроса с неверным логином приходит ошибка')
    def test_login_courier_with_wrong_login(self):
        payload = {
            "login": "lalala_lala",
            "password": DataLoginCourier.password
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        assert response.status_code == 404 and response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Проверка авторизации курьера с неверным паролем')
    @allure.description('Проверяем, что при отправке запроса с неверным паролем приходит ошибка')
    def test_login_courier_with_wrong_password(self):
        payload = {
            "login": DataLoginCourier.login,
            "password": "1234567890"
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        assert response.status_code == 404 and response.json()["message"] == "Учетная запись не найдена"

    @allure.title('Проверка авторизации курьера с отсутствием одного из обязательных полей (в данном случае пароля)')
    @allure.description('Проверяем, что приходит ожидаемый код и тело ответа, которые говорят об ошибке')
    def test_login_courier_without_one_of_needed_fields(self):
        payload = {
            "login": DataLoginCourier.login
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        assert response.status_code == 400 and response.json()["message"] == "Недостаточно данных для входа"

    @allure.title('Проверка авторизации несуществующего курьера')
    @allure.description('Проверяем, что приходит ожидаемый код и тело ответа, которые говорят об ошибке')
    def test_login_non_existent_courier(self):
        payload = {
            "login": "Ada-Vong",
            "password": "1234567890"
        }
        response = requests.post(f"{Urls.BASE_URL}/api/v1/courier/login", data=payload)
        assert response.status_code == 404 and response.json()["message"] == "Учетная запись не найдена"
