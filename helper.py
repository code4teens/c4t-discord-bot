import requests

def handle_request_from(URL):
  r = requests.get(URL)

  assert (r.status_code == 200), r.status_code
  return r.json()