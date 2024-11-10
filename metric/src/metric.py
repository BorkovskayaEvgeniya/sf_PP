import pika
import json
import csv

# Временное хранилище для сообщений y_true и y_pred
storage = {}

# Функция для обработки и записи данных в файл
def process_and_log(id, y_true, y_pred):
    absolute_error = abs(y_true - y_pred)
    with open('./logs/metric_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id, y_true, y_pred, absolute_error])
    print(f'Записано в log: id={id}, y_true={y_true}, y_pred={y_pred}, absolute_error={absolute_error}')

# Функция обработки сообщений из очередей y_true и y_pred
def callback(ch, method, properties, body):
    message = json.loads(body)
    message_id = message['id']
    value = message['body']
    
	# Определяем, из какой очереди поступило сообщение и сохраняем его в хранилище
    if method.routing_key == 'y_true':
        if message_id in storage:
            y_pred = storage.pop(message_id)  # Получаем предсказание
            process_and_log(message_id, value, y_pred)
        else:
            storage[message_id] = value  # Сохраняем истинное значение
    elif method.routing_key == 'y_pred':
        if message_id in storage:
            y_true = storage.pop(message_id)  # Получаем истинное значение
            process_and_log(message_id, y_true, value)
        else:
            storage[message_id] = value  # Сохраняем предсказание

try:
	# Подключаемся к RabbitMQ
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
	channel = connection.channel()
    
	# Объявляем очереди y_true и y_pred
	channel.queue_declare(queue='y_true')
	channel.queue_declare(queue='y_pred')
    
	# Подписываемся на очереди y_true и y_pred
	channel.basic_consume(queue='y_true', on_message_callback=callback, auto_ack=True)
	channel.basic_consume(queue='y_pred', on_message_callback=callback, auto_ack=True)
    
	print('...Ожидание сообщений, для выхода нажмите CTRL+C')
	# Запускаем режим ожидания прихода сообщений
	channel.start_consuming()

except Exception as e:
	print(f'Не удалось подключиться к очереди: {e}')
