import requests
import csv


ote = "https://api.ote-godaddy.com"
headers = dict()

def DomainDetails(domainName):

    params = {
        'domain': domainName,
        'checkType': 'FULL'
    }

    response = requests.get('https://api.ote-godaddy.com/v1/domains/available', headers=headers, params=params)
    if response.status_code == 200:
        return response.json()

    return None



def main():
    global headers
    key = ""
    secret = ""
    with open("secret.txt", 'r') as fin:
        fin.readline()
        key,secret = fin.readline().split(',')
        key = key.strip()
        secret = secret.strip()

    headers = {'Authorization': 'sso-key {}:{}'.format(key, secret),
     'Accept': 'application/json'}


    print(DomainDetails("example.com"))





if __name__ == "__main__":
    main()