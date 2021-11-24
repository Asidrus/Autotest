import requests


response = requests.post(url='https://division.bakalavr-magistr.ru/orders',
                         data='month=2021-11&real_crm_id=&filter_division_category_id=&date_from=&date_to=&source=&status_id=&manager_num=1322&phone=&fio=&email=&source_order_num=&del_test_orders_pwd=',
                         cookies={'_ga': 'GA1.2.1632160139.1634802152', '_ym_uid': '1634802152557629371', '_ym_d':'1634802152',
                                  'tmr_lvid':'e316a2c7e3478e0c1210d0eedd06a761', 'tmr_lvidTS': '1634802152623', 'tmr_reqNum':'4',
                                  'PHPSESSID':'3b6bf8dba8754016d7d5905812868426', 'mrm':'71f846e5685d896c65b1905dc1cba8de1000'})

with open('test.html', 'w') as file:
    file.write(response.content.decode('windows-1251'))
