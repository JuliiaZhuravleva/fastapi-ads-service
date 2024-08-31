import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(response):
    print(f"Код статуса: {response.status_code}")
    print("Тело ответа:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    print("-" * 30)


def create_advertisement():
    print("Создание объявления...")
    data = {
        "title": "Новый ноутбук",
        "description": "Абсолютно новый ноутбук, не использовался",
        "price": 999.99,
        "author": "Иван Иванов"
    }
    response = requests.post(f"{BASE_URL}/advertisement", json=data)
    print_response(response)
    return response.json()["id"]


def get_advertisement(ad_id):
    print(f"Получение объявления с id {ad_id}...")
    response = requests.get(f"{BASE_URL}/advertisement/{ad_id}")
    print_response(response)
    return response.json() if response.status_code == 200 else None


def update_advertisement(ad_id):
    print(f"Обновление объявления с id {ad_id}...")
    data = {
        "price": 899.99,
        "description": "Слегка б/у ноутбук, отличное состояние"
    }
    response = requests.patch(f"{BASE_URL}/advertisement/{ad_id}", json=data)
    print_response(response)
    return response.json() if response.status_code == 200 else None


def delete_advertisement(ad_id):
    print(f"Удаление объявления с id {ad_id}...")
    response = requests.delete(f"{BASE_URL}/advertisement/{ad_id}")
    print_response(response)
    return response.json() if response.status_code == 200 else None


def search_advertisements(params):
    print("Поиск объявлений...")
    response = requests.get(f"{BASE_URL}/advertisement", params=params)
    print_response(response)
    return response.json() if response.status_code == 200 else None

def run_tests():
    # Создание
    ad_id = create_advertisement()
    if not ad_id:
        print("Ошибка создания объявления")
        return

    # Получение
    ad = get_advertisement(ad_id)
    if not ad:
        print("Ошибка получения объявления")
        return

    # Обновление
    updated_ad = update_advertisement(ad_id)
    if not updated_ad:
        print("Ошибка обновления объявления")
        return

    # Проверка обновления
    if updated_ad['price'] != 899.99 or updated_ad['description'] != "Слегка б/у ноутбук, отличное состояние":
        print("Ошибка проверки обновления")
        return

    # Поиск
    search_results = search_advertisements({"min_price": 500, "max_price": 1000})
    if not search_results:
        print("Ошибка поиска")
        return

    # Удаление
    delete_result = delete_advertisement(ad_id)
    if not delete_result or delete_result['status'] != "deleted":
        print("Ошибка удаления объявления")
        return

    # Проверка удаления
    deleted_ad = get_advertisement(ad_id)
    if deleted_ad is not None:
        print("Ошибка проверки удаления")
        return

    print("Все тесты пройдены успешно!")


if __name__ == "__main__":
    run_tests()