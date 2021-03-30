import requests

def handle_request_from(URL):
  r = requests.get(URL)

  assert (r.status_code == 200), r.status_code
  return r.json()

def joke_command():
  try:
    data = handle_request_from('https://official-joke-api.appspot.com/random_joke')

  except Exception as error:
    print(f'~joke: {error}')

    return 'Something weng wrong..'

  else:
    return f'{data["setup"]}\n\n{data["punchline"]}'

def ip_command():
  try:
    data = handle_request_from('https://api.ipify.org/?format=json')

  except Exception as error:
    print(f'~ip: {error}')

    return 'Something weng wrong..'

  else:
    return data['ip']

def iplocation_command():
  try:
    data1 = handle_request_from('https://api.ipify.org/?format=json')
    ip = data1['ip']
    data2 = handle_request_from(f'https://ipinfo.io/{ip}/geo')
    data3 = handle_request_from(f'https://api.ip2country.info/ip?{ip}')

  except Exception as error:
    print(f'~iplocation: {error}')

    return 'Something weng wrong..'

  else:
    d = dict()
    d['text'] = f'{data2["city"]}, {data2["region"]}, {data2["country"]}'
    d['emoji'] = data3['countryEmoji']

    return d