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

def LoadDomainNames(groupSize = 1):
    primaries = list()
    secondaries = list()
    extensions = list()
    domains = list()

    with open("DomainNames.csv", 'r') as fin:
        fin.readline()
        reader = csv.DictReader(fin, fieldnames=['primary','secondary','extension'])

        for row in reader:
            if row['primary'] != '':
                primaries.append(row['primary'])

            if row['secondary'] != '':
                secondaries.append(row['secondary'])

            if row['extension'] != '':
                extensions.append(row['extension'])


    for primary in primaries:
        for secondary in secondaries:
            for extension in extensions:
                domains.append("{}{}.{}".format(primary,secondary,extension))

    domainGroups = [domains[i:i+groupSize] for i in range(0,len(domains),groupSize)]
    return domainGroups

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


    for i in LoadDomainNames(5):
        print(i)





if __name__ == "__main__":
    main()