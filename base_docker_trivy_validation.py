import os
import yaml
import json


def generateTrivyReport():
    base_image_info = readYAMLFile()
    vulnerabilities = []
    for base_img in base_image_info:
        os.popen("docker pull {}".format(base_img["image"])).read()
        stream = os.popen('trivy  image -f json -o ./result.json --severity HIGH,CRITICAL {}'.format(base_img['image']))
        output = stream.read()
        result = readReport()
        result = result[0]
        if(len(result['Vulnerabilities'])):
           
            for vulnerability in result['Vulnerabilities']:
                vulnerabilities.append({"image":base_img["image"],"name": vulnerability['PkgName'],"Description": vulnerability['Description']})
    if len(vulnerabilities):
         raise Exception(vulnerabilities)
def readYAMLFile():
   stream = open("base_image_info.yaml", 'r')
   return yaml.load(stream)

def readReport():
     stream = open("result.json", 'r')
     return json.load(stream)

generateTrivyReport()