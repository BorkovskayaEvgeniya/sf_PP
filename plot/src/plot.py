import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import time

while True:
    try:
        print("Чтение данных из metric_log.csv...")
        data = pd.read_csv('./logs/metric_log.csv')

    	# Проверка, есть ли в данных столбец absolute_error и не пуст ли он
        if 'absolute_error' not in data.columns or data['absolute_error'].empty:
            print("Нет данных для построения графика. Ожидание новых данных...")
        else:
            print("Данные загружены, построение графика...")

        	# Строим гистограмму абсолютных ошибок с жёлтыми столбцами
            plt.figure(figsize=(10, 6))
            counts, bins, _ = plt.hist(
            	data['absolute_error'], bins=10, edgecolor='black', color='orange', alpha=0.6, density=True
        	)

        	# Добавляем плавную линию плотности с использованием KDE
            kde = gaussian_kde(data['absolute_error'])
            xs = np.linspace(bins[0], bins[-1], 200)
            plt.plot(xs, kde(xs), color='orange', linewidth=2)

            plt.title('Distribution of Absolute Errors')
            plt.xlabel('absolute_error')
            plt.ylabel('Count')

        	# Сохраняем гистограмму в файл
            plt.savefig('./logs/error_distribution.png')
            plt.close()
            print("Гистограмма сохранена в logs/error_distribution.png")
   	 
    	# Задержка перед следующим обновлением
        time.sleep(10)

    except Exception as e:
        print(f'Ошибка при построении графика: {e}')
        time.sleep(10)