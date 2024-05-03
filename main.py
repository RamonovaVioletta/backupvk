import requests
import logging
import json
from vk import VKAPIClient
from yandex import YANDEXAPIClient

if __name__ == '__main__':
    data_json = []
    logging.basicConfig(filename="myapi.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logger = logging.getLogger("myapi.log")
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    vk_access_token = input('Токен доступа для ВК: ')
    vk_user_id = int(input('User Id пользователя ВК: '))
    yandex_access_token = input('Токен от Яндекс Полигон: ')

    vk_client = VKAPIClient(token=vk_access_token)
    photos_info_items = vk_client.get_user_photos(vk_user_id)['response']['items']
    photos_list = vk_client.photos_info(photos_info_items)
    logger.info('Получили доступ к API VK')

    ya_client = YANDEXAPIClient(yandex_access_token)
    logger.info('Получили доступ к API Yandex')

    ya_client.create_folder('PhotosVK')
    logger.info('Создание папки с именем PhotosVK на Яндекс Диске')

    for photo in photos_list:
        response = requests.get(photo['url'])
        image_name = f"{photo['likes']}.jpg"
        file_info = ya_client.get_file_info('PhotosVK/', image_name)

        if file_info.json().get('error') == None:
            image_name = f"{photo['likes']}_{photo['date']}.jpg"
            logger.info('Файл с таким именем уже существует! Добавляем к имени файла дату загрузки фотографии!')
            logger.info(f'Теперь файл называется {image_name}')

        with open(image_name, 'wb') as file:
            file.write(response.content)

        yandex_response = ya_client.get_yandex_upload_photos('PhotosVK/', image_name)

        with open(image_name, 'rb') as file:
            try:
                requests.put(yandex_response.json()['href'], files={'file': file})
                logger.info(f'Фотография с именем {image_name} успешно загружена в папку PhotosVK')

                data_json.append(
                    {
                        'file_name': image_name,
                        'size': photo['size']
                    }
                )
            except:
                logger.info('Фото с таким именем уже существует! Вы загружаете фотографию, которая уже хранится в папке PhotosVK')
                logger.error('Отмена загрузки фото!')
                data_json.append(
                    {
                        'file_name': image_name,
                        'size': photo['size'],
                        'error': 'Файл уже загружен на Яндекс Диск'
                    }
                )

    logger.warning('\n')
    logger.warning('Работа программы завершена.')

    with open('data.json', 'w') as file:
        json.dump(data_json, file)