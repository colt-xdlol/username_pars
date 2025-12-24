from pyrogram import Client
from pyrogram.errors import UsernameNotModified, UsernameInvalid, UsernameOccupied, FloodWait
from pyrogram.raw.functions.account import UpdateUsername
import time
from config import api_id, api_hash, username

async def update_username(client, new_username):
    while True:
        try:
            # Удаляем @ если он есть в начале
            if new_username.startswith('@'):
                new_username = new_username[1:]
                
            # Способ 1: Использование RAW API (рекомендуется)
            await client.invoke(UpdateUsername(username=new_username))
            
            # ИЛИ Способ 2: Через bot API (если не работает способ 1)
            # await client.send(functions.account.UpdateUsernameRequest(username=new_username))
            
            print(f"Username успешно изменен на @{new_username}")
            return True
            
        except UsernameNotModified:
            print(f"Username уже установлен как @{new_username}")
            return True
            
        except UsernameInvalid as e:
            print(f"Некорректный username: {e}")
            return False
            
        except UsernameOccupied:
            print(f"Username @{new_username} уже занят")
            return False
            
        except FloodWait as e:
            print(f"Ограничение от Telegram. Ждем {e.value} секунд...")
            time.sleep(e.value)
            continue
            
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(10)  # частота попыток смены username
            continue

async def main():
    client = Client(
        "my_account",
        api_id=api_id,
        api_hash=api_hash,
        test_mode=True
    )
    
    async with client:
        result = await update_username(client, username)
        if result:
            message = f"Успешно установлен username @{username}"
            print(message)
        else:
            print(f"Не удалось установить username")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())