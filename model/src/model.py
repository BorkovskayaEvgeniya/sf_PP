import pika
import pickle
import numpy as np
import json

# Читаем файл с сериализованной моделью
with open('myfile.pkl', 'rb') as pkl_file:
	regressor = pickle.load(pkl_file)

try:
    # Создаём подключение к RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    
	# Объявляем очереди features и y_pred
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_pred')
    
	# Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):
        print(f'Получен вектор признаков {body}')
   	 
    	# Декодируем сообщение
        message = json.loads(body)
        message_id = message['id']
        features = message['body']
   	 
    	# Выполняем предсказание с использованием модели
        pred = regressor.predict(np.array(features).reshape(1, -1))
   	 
    	# Формируем сообщение для отправки в очередь y_pred
        message_y_pred = {
        	'id': message_id,
        	'body': pred[0]
    	}
   	 
    	# Отправляем предсказание в очередь y_pred
        channel.basic_publish(exchange='',
                          	routing_key='y_pred',
                          	body=json.dumps(message_y_pred))
        print(f'Предсказание {pred[0]} с id {message_id} отправлено в очередь y_pred')
    
	# Извлекаем сообщение из очереди features
    channel.basic_consume(
    	queue='features',
    	on_message_callback=callback,
    	auto_ack=True
	)
    
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
	# Запускаем режим ожидания прихода сообщений
    channel.start_consuming()

except Exception as e:
	print(f'Не удалось подключиться к очереди: {e}')
