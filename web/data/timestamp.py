import hashlib
import requests
import json


def stamp(text):
	token = 'bc6387ec-052a-49d0-b102-ded9edfcb4a7'
	sha = sha(text)
	url = 'http://api.originstamp.org/api/%s' %sha
	h = {'Content-Type':'application/json','Authorization':token}
	r = requests.get(url,headers=h)
	j = json.loads(r.text)
	return (False if j['created']=='false' else True,True if j['multi_seed']['submit_status']>2 else False)

def sha(text):
	return hashlib.sha256(text).hexdigest()

	
if __name__ == '__main__':
    print stamp("Helloword")