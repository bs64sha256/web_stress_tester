from tkinter import ttk

import requests
import concurrent.futures
import time
import tkinter

def stress_test(url, num_requests, num_threads):
    """
    Простой стресс-тест веб-сайта.  НЕ подходит для серьёзного тестирования.
    """
    results = []
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_url = {executor.submit(make_request, url): url for _ in range(num_requests)}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                response_time, status_code = future.result()
                results.append({'url': url, 'response_time': response_time, 'status_code': status_code})
            except requests.exceptions.RequestException as e:
                results.append({'url': url, 'error': str(e)})


    end_time = time.time()
    total_time = end_time - start_time
    average_response_time = sum(r['response_time'] for r in results if 'response_time' in r) / len(results) if results else 0


    print(f"Завершено {len(results)} запросов за {total_time:.2f} секунд.")
    print(f"Среднее время ответа: {average_response_time:.2f} секунд.")
    print("Результаты:")
    for result in results:
        print(result)

def make_request(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    response_time = end_time - start_time
    return response_time, response.status_code

# Пример использования
url = "https://vision.maximumtest.ru/meeting/meetingId/34248#2801796" #Замените на нужный URL
num_requests = 1  # Количество запросов
num_threads = 2  # Количество потоков

stress_test(url, num_requests, num_threads)
if __name__ == '__main__':
    root = tkinter.Tk()

    ttk.Style().theme_use('xpnative')

    root.title('Stress Tester')
    root.geometry('400x395+50+50')
    root.resizable(False, False)

    url_label = ttk.Label(root, text='Введите URL-адрес тестируемого веб-ресурса:')
    url_label.place(x=10, y=10)
    url_entry = ttk.Entry(root, width=53)
    url_entry.place(x=10, y=35)
    power = ttk.Spinbox(root, from_=1.0, to=99999999.0, width=17)
    power.place(x=10, y=70)
    power_lbl = ttk.Label(root, text=' - Суммарное количество запросов')
    power_lbl.place(x=170, y=70)
    threads = ttk.Spinbox(root, from_=1.0, to=99999999.0, width=17)
    threads.place(x=10, y=95)
    threads_lbl = ttk.Label(root, text=' - количество потоков')
    threads_lbl.place(x=170, y=95)
    btn = ttk.Button(root, text='Начать', cursor='hand2', width=53)
    btn.place(x=10, y=120)

    root.mainloop()
