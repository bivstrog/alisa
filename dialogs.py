from taxi import take_coor, taxi

trip = {}

user = {}

clas = {
    '«Эконом»': 'econom',
    '«Комфорт»': 'business',
    '«Комфорт+»': 'comfortplus',
    '«Минивен»': 'minivan',
    '«Бизнес»': 'vip'    
}

def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name', то возвращаем её значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


def hello_dialog(res, req):
    user_id = req['session']['user_id']
    
    if req['session']['new']:
        res['response']['text'] = 'Здравствуйте! Назовите своё имя!'
        res['response']['tts'] = 'Здравствуйте! Назовите своё имя!'
        user[user_id] = {
            'first_name': None
        }
        
        trip[user_id] = {
            'address_1': None,
            'coordinates_1': None,
            'coordinatesX_1': None,
            'coordinatesY_1': None,
            'start_1' : False,
            'end_1' : False,
            'address_2': None,
            'coordinates_2': None,
            'coordinatesX_2': None,
            'coordinatesY_2': None,
            'start_2' : False,
            'end_2' : False,
            'clas': None
        }        
        return

    if user[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = 'Не расслышала имя. Повторите, пожалуйста!'
            res['response']['tts'] = 'Не рассл+ышала имя. Повторите, пожалуйста!'
            return
        else:
            user[user_id]['first_name'] = first_name
            # как видно из предыдущего навыка, сюда мы попали, потому что пользователь написал своем имя.
            # Предлагаем ему воспользоваться такси
            res['response']['text'] = f'Приятно познакомиться, {first_name.title()}! Я могу сказать стоимость поездки на такси из пункта А в пункт В! \n {first_name.title()}, назовите пункт начала поездки. \n Формат ввода: *Страна*, *Населенный пункт*, ул. *Улица*, *Дом*'
            res['response']['tts'] = f'Приятно познак+омиться, {first_name.title()}! Я могу сказать ст+оимость поездки на такси из пункта А в пункт В! {first_name.title()}, назов+ите пункт начала поездки. Форм+ат ввода: Страна, Насел+ённый пункт, Улица, Дом'
            trip[user_id]['start_1'] = True
            return
    
    _name = user[req['session']['user_id']]['first_name']
    
    if trip[user_id]['end_1'] == False:
        ans = req['request']['original_utterance']
        trip[user_id]['coordinates_1'] = take_coor(ans)
        if trip[user_id]['coordinates_1'][0] == False:
            res['response'] = {
                'text': f'{_name.title()}, введите корректный адрес. \n Формат ввода: *Страна*, *Населенный пункт*, ул. *Улица*, *Дом*',
                'tts': f'{_name.title()}, введ+ите корр+ектный адрес. Форм+ат ввода: Страна, Насел+ённый пункт, Улица, Дом'
            }
            return
        else:
            trip[user_id]['address_1'] = trip[user_id]['coordinates_1'][0]
            res['response'] = {
                'text': f'{_name.title()}, а теперь назовите пункт конца поездки. \n Формат ввода: *Страна*, *Населенный пункт*, ул. *Улица*, *Дом*',
                'tts': f'{_name.title()}, а теп+ерь назов+ите пункт конца по+ездки. Форм+ат ввода: Страна, Насел+ённый пункт, Улица, Дом'
            }
            trip[user_id]['coordinatesX_1'] = trip[user_id]['coordinates_1'][1][0]
            trip[user_id]['coordinatesY_1'] = trip[user_id]['coordinates_1'][1][1]
            trip[user_id]['end_1'] = True
            trip[user_id]['start_2'] = True
            return
    
    if trip[user_id]['end_2'] == False:
        ans = req['request']['original_utterance']
        trip[user_id]['coordinates_2'] = take_coor(ans)
        if trip[user_id]['coordinates_2'][0] == False:
            res['response'] = {
                'text': f'{_name.title()}, введите корректный адрес. \n Формат ввода: *Страна*, *Населенный пункт*, ул. *Улица*, *Дом*',
                'tts': f'{_name.title()}, введ+ите корр+ектный адрес. Форм+ат ввода: Страна, Насел+ённый пункт, Улица, Дом'
            }
            return
        else:
            trip[user_id]['address_2'] = trip[user_id]['coordinates_2'][0]
            trip[user_id]['coordinatesX_2'] = trip[user_id]['coordinates_2'][1][0]
            trip[user_id]['coordinatesY_2'] = trip[user_id]['coordinates_2'][1][1]            
            trip[user_id]['end_2'] = True
            res['response']['text'] = f'{_name.title()}, осталось выбрать тариф. Воспользуйтесь кнопками!!!'
            res['response']['buttons'] = [
                {
                    'title': '«Эконом»',
                    'hide': True
                    },
                {
                    'title': '«Комфорт»',
                    'hide': True
                },
                {
                    'title': '«Комфорт+»',
                    'hide': True
                },
                {
                    'title': '«Минивен»',
                    'hide': True
                },        
                {
                    'title': '«Бизнес»',
                    'hide': True
                }
            ]
            return
    if trip[user_id]['end_2'] == True:
        trip[user_id]['clas'] = clas[req['request']['original_utterance']]
        ans = taxi(trip[user_id]['coordinatesX_1'], trip[user_id]['coordinatesY_1'], trip[user_id]['coordinatesX_2'], trip[user_id]['coordinatesY_2'], trip[user_id]['clas'])# элемент словаря 
        res['response']['text'] = f'{_name.title()}, ваш маршрут готов. \n Цена вашей поездки: ' + ans['options'][0]['price_text'] + '\n Время ожидания составит ' + str(int(ans['options'][0]['waiting_time']//60)) + ' минут.\n Время поездки по Яндекс.Навигатору составит ' + str(int(ans['time']//60)) + ' минут.'
        res['response']['tts'] = f'{_name.title()}, ваш маршр+ут готов. Цена вашей по+ездки: ' + ans['options'][0]['price_text'] + ' Время ожид+ания сост+авит ' + str(int(ans['options'][0]['waiting_time']//60)) + ' мин+ут. Время по+ездки по Яндекс навиг+атору сост+авит ' + str(int(ans['time']//60)) + ' мин+ут.'
        res['response']['end_session'] = True
        return