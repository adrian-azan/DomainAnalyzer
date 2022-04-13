import requests
import csv


ote = "https://api.ote-godaddy.com"
headers = dict()

def DomainDetails(domainGroup):

    params = {
        'checkType': 'FULL'
    }
    body = {
        "domains": domainGroup
    }

    response = requests.post('https://api.ote-godaddy.com/v1/domains/available', headers=headers, params=params,json=domainGroup)
    if response.status_code == 200 or response.status_code == 203:
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


    domainGroups = LoadDomainNames(10)

    for group in domainGroups:
        domainDetails = DomainDetails(group)
        if domainDetails != None:
            for domain in domainDetails["domains"]:
                print("{:<5}{:<20}${:.2f}".format(domain["available"],domain["domain"],float(domain["price"])/1000000))







if __name__ == "__main__":
    main()