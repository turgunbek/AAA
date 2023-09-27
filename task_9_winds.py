import requests

response = requests.get('https://www.7timer.info/bin/astro.php?lon=113.2&lat=23.1&ac=0&unit=metric&output=json&tzshift=0').json()
dataseries = response['dataseries']
for i in range(len(dataseries)):
    direction = dataseries[i]['wind10m']['direction']
    speed = dataseries[i]['wind10m']['speed']
    print(f'направление: {direction}, скорость: {speed}')
