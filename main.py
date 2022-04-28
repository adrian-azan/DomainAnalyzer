import requests
import json
import csv
import time

from Limiter import Limiter
from Timer import Timer


env = ""
headers = dict()
URLS = dict()

appraisal = True

def DomainDetails(domainGroup, checkType = 'FULL'):
    params = {
        'checkType': checkType
    }

    response = requests.post(URLS[env]["availableURL"], headers=headers, params=params,json=domainGroup)

    while response.status_code == 429:
        print("Sleeping for: {}".format(response.json()["retryAfterSec"]))
        time.sleep(response.json()["retryAfterSec"])
        response = requests.post(URLS[env]["availableURL"], headers=headers, params=params,json=domainGroup)

    if response.status_code == 200 or response.status_code == 203:
        return response.json()

    print(response.json())
    return None

def AppraisalDetails(domainName):
    response = requests.get("{}/{}".format(URLS[env]["appraisalURL"],domainName), headers=headers)

    while response.status_code == 429:
        print("Sleeping for: {}".format(response.json()["retryAfterSec"]))
        time.sleep(response.json()["retryAfterSec"])
        response = requests.get("{}/{}".format(URLS[env]["appraisalURL"], domainName), headers=headers)

    if response.status_code == 200:
        return response.json()["govalue"]

    print(response.json())
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
    global appraisal
    limiter = Limiter()
    timer = Timer()
    domainGroups = LoadDomainNames(50)
    output = []

    for group in domainGroups:

        while limiter.check() == False:
            time.sleep(1)

        limiter.add()
        domainDetails = DomainDetails(group)

        if domainDetails != None:
            for domain in domainDetails["domains"]:
                if appraisal and domain["available"]:
                    while limiter.check() == False:
                        time.sleep(1)

                    limiter.add()
                    output.append({
                        "domain": domain["domain"],
                        "price": domain["price"]/1000000,
                        "appraisal": AppraisalDetails(domain["domain"])
                    })
                elif domain["available"]:
                    output.append({
                        "domain": domain["domain"],
                        "price": domain["price"] / 1000000,
                        "appraisal": ""
                    })



    with open("DomainDetails.csv",'w', newline='') as fout:
        writer = csv.DictWriter(fout,fieldnames=["domain","price","appraisal"])
        writer.writeheader()
        writer.writerows(output)


def UrlSetup():
    global URLS, env

    with open("URLS.json") as fin:
        URLS = json.load(fin)
        env = URLS["environment"]


def KeySetup():
    global headers

    with open("secret.txt", 'r') as fin:
        fin.readline()
        key, secret = fin.readline().split(',')
        key = key.strip()
        secret = secret.strip()

    headers = {'Authorization': 'sso-key {}:{}'.format(key, secret),
               'Accept': 'application/json'}


if __name__ == "__main__":
    UrlSetup()
    KeySetup()
    main()

