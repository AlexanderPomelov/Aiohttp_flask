import aiohttp
import asyncio


async def main():
    client = aiohttp.ClientSession()

    ### Создание объявление

    response = await client.post(
        'http://127.0.0.1:8080/announcement',
        json={'title': 'announcement_1', 'description': '`12213', 'owner': 'user'})

    print(response.status)
    print(await response.text())
    await client.close()


### Получение объявления по его ID

    # response = await client.get(
    #     'http://127.0.0.1:8080/announcement/1',
    #
    # )
    #
    # print(response.status)
    # print(await response.text())
    # await client.close()

### Изменение названия объявления по его ID

    # response = await client.patch(
    #         'http://127.0.0.1:8080/announcement/1',
    #         json={'title': 'announcement_444'}
    # )
    # print(response.status)
    # print(await response.text())
    # await client.close()


### Проверка измененного объявления

    # response = await client.get(
    #     'http://127.0.0.1:8080/announcement/1',
    #
    # )
    #
    # print(response.status)
    # print(await response.text())
    # await client.close()


###Удаление объявления по его ID

    # response = await client.delete(
    #     "http://127.0.0.1:8080/announcement/1",
    # )
    # print(response.status)
    # print(await response.text())
    # await client.close()

asyncio.run(main())
