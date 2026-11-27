import urllib.request

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())

# 1. Russian
resp_ru = opener.open('http://127.0.0.1:8000/?lang=ru').read().decode('utf-8')
print('RU test 1 (Всё в одном месте):', 'Всё в одном месте' in resp_ru)
print('RU test 2 (Главная):', 'Главная' in resp_ru)
print('RU test 3 (Объявления):', 'Объявления' in resp_ru)

# 2. Subsequent request without ?lang (session/cookie persistence)
resp_persist = opener.open('http://127.0.0.1:8000/').read().decode('utf-8')
print('Persistence test (remains RU):', 'Всё в одном месте' in resp_persist)

# 3. English
resp_en = opener.open('http://127.0.0.1:8000/?lang=en').read().decode('utf-8')
print('EN test 1 (Everything in one place):', 'Everything in one place' in resp_en)
print('EN test 2 (Home):', 'Home' in resp_en)
print('EN test 3 (Listings):', 'Listings' in resp_en)

# 4. Uzbek
resp_uz = opener.open('http://127.0.0.1:8000/?lang=uz').read().decode('utf-8')
print('UZ test 1 (Hamma narsa bir joyda):', 'Hamma narsa bir joyda' in resp_uz)
print('UZ test 2 (Bosh Sahifa):', 'Bosh Sahifa' in resp_uz)
