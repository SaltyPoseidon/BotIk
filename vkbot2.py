import threading
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
from bs4 import BeautifulSoup as bs
import time


#Переменные


headers = {'accept': '*/*', 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
base_url = 'http://meneger23.ru/'
vk_session = vk_api.VkApi(token='8eed6a93e6df015a71fb755368a37f3e2abe2a32f0f3f5958ced243ca686186c15f5d508ec91d41721760')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
twex='Неизвестная команда, попробуйте следующее:\nНовости - оформление подписки на рассылку\nРасписание - расписание звонков'
ring = '1 урок:  8:00 — 8:40\n2 урок:  8:45 — 9:25\n3 урок:  9:50 — 10:30\n4 урок:  10:35 — 11:15\n5 урок: 	11:25 — 12:05\n6 урок:  12:10 — 12:50\n7 урок:  13:35 — 14:15\n8 урок:  14:20 — 15:00'


#Функции

Users = []

def pars(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find('div', attrs={'class':"blog_content"})
        date = divs.find('div', attrs={'class':'modnews-date'}).text
        title = divs.find('h4', attrs={'class': "newsflash-title"}).text
        description = divs.find('p').text
        href = divs.find('a')['href']
        text = (date + " " + title + " " + description + " " + 'http://meneger23.ru/' + href)
        return text
    else:
        print('ERROR')

new = pars(base_url,headers)
actual='df'


def sendinio():
    actual = 'da'
    new = pars(base_url, headers)
    while True:
        time.sleep(900)
        if new != actual:
            actual = new
            for i in Users:
                vk.messages.send(
                    user_id = int(i),
                    random_id = get_random_id(),
                    message=pars(base_url,headers)
                )

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        # Слушаем longpoll, если пришло сообщение то:
        if event.text == 'Новости' or event.text == 'новости':  # Если написали заданную фразу
            Users.append(event.user_id)  # Добавляем идентификатор пользователя в базу данных
            print(event.user_id)
            print(Users)
            MUsers = Users
            Users = set(Users)
            Users = list(Users)
            print(Users)
            print(MUsers)
            if MUsers == Users:
                f = open('bub.txt', 'a')
                f.write(str(event.user_id) + '\n')
                f.close()
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Отлично, вы подписались на рассылку!\n' + pars(base_url,headers)
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message='Вы уже подписались на рассылку!'
                )
        elif event.text == 'Расписание' or event.text == 'расписание':  # Если написали заданную фразу
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Вот расписание звонков:\n' + ring
            )
        elif event.text == 'Оценки' or event.text == 'оценки':
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message='Для получения уведомлений об упеваемости введите логин и пароль Вконтакте:\n(Первым сообщением нужно отправить логин, а вторым - пароль\n'

            )
        else:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=twex
            )

x = threading.Thread(target = pars, args = (base_url,headers))
x.start()







