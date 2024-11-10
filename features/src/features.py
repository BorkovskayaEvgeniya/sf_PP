import pika
import numpy as np
import json
import time
from sklearn.datasets import load_diabetes
from datetime import datetime

 
# Создаём бесконечный цикл для отправки сообщений в очередь
while True:
    try:
        # Загружаем датасет о диабете
        X, y = load_diabetes(return_X_y=True)
        # Формируем случайный индекс строки
        random_row = np.random.randint(0, X.shape[0]-1)
 
        # Создаём уникальный идентификатор для сообщения
        message_id = datetime.timestamp(datetime.now())
   	 
    	# Формируем сообщение для очереди y_true
        message_y_true = {
        	'id': message_id,
        	'body': y[random_row]
    	}
   	 
    	# Формируем сообщение для очереди features
        message_features = {
        	'id': message_id,
        	'body': list(X[random_row])
    	}


        # Создаём подключение по адресу rabbitmq:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
 
        # Объявляем очереди y_true и features
        channel.queue_declare(queue='y_true')
        channel.queue_declare(queue='features')
   	 
    	# Публикуем сообщение в очередь y_true
        channel.basic_publish(exchange='',
                          	routing_key='y_true',
                          	body=json.dumps(message_y_true))
        print('Сообщение с правильным ответом отправлено в очередь')
   	 
    	# Публикуем сообщение в очередь features
        channel.basic_publish(exchange='',
                          	routing_key='features',
                          	body=json.dumps(message_features))
        print('Сообщение с вектором признаков отправлено в очередь')
   	 
    	# Закрываем подключение
        connection.close()
   	 
    	# Добавляем задержку перед следующей отправкой
        time.sleep(10)

    except Exception as e:
        print(f'Не удалось подключиться к очереди: {e}')
        time.sleep(5)  # Повторная попытка подключения через 5 секунд
 
        