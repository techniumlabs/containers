import datetime
import json
import os
import re
import yaml
from git import Repo
from packaging import version


from azure.containerregistry import ContainerRegistryClient
from azure.identity import DefaultAzureCredential


registory = os.environ['REGISTORY'] #"techniumrca.azurecr.io"
account_url = "https://" + registory
client = ContainerRegistryClient(account_url, DefaultAzureCredential())
repo = Repo(search_parent_directories=True)
changed_file = []

def generateTrivyReport():
    images = readYAMLFile()
    for img in images:
        print("-----------start-----------")
        latest_image_tag = get_image_tag(img['repository_name']).name
        image_name = "{}/{}:{}".format(registory,img['repository_name'],latest_image_tag)#latest image
        os.popen("docker pull {}".format(image_name)).read()
        print(image_name)
        os.popen('trivy  image -f json -o ./result.json --severity HIGH,CRITICAL {}'.format(image_name)).read()
        result = readReport()
        result = result[0]
        if(len(result['Vulnerabilities'])):
           parse_for_base_images(img["docker_file_path"],img["base_img_repo_name"])
    git_push()
            

def readYAMLFile():
   stream = open("child_image_info.yaml", 'r')
   return yaml.load(stream)

def readReport():
     stream = open("result.json", 'r')
     return json.load(stream)

def get_image_tag(repo_name):
    tag_list = list(client.list_tag_properties(repo_name,order_by="timedesc"))
    print([tag.name for tag in  tag_list])
    return tag_list[0]

def parse_for_base_images(file_path,base_img_repo_name):
    print("---- docker file path ----", file_path)
    base_image_pattern = re.compile(r'''\s*FROM\s+(?P<image>[^\s]+?)$''')
    with open(file_path, 'r+') as fp:
        lines = fp.readlines()
        updated_lines = []
        last_updated_date_flag = False
        last_updated_date = "last_updated_date={}".format(datetime.datetime.now()) 
        for line in lines:
            match = base_image_pattern.match(line)
            if match:
                image_name_full_name = match.group("image")
                image_repo = image_name_full_name.split(":")[0].split("/")[-1]
                current_version = image_name_full_name.split(":")[-1]
                print("Image name = {} | Current Version = {} | Path = {}".format(image_repo,current_version,file_path))
                # get_docker_tag(image_name)
                latest_version = get_image_tag(base_img_repo_name).name
                print(latest_version,"--------latest_version",current_version,"--------current")
                if version.parse(latest_version) > version.parse(current_version):
                    line = line.replace(current_version,latest_version)
                    
            elif line.find('LABEL last_updated_date') >= 0:
                line = "LABEL {}".format(last_updated_date)
                last_updated_date_flag = True
            
            updated_lines.append(line)
        if not last_updated_date_flag:
            last_line = str(updated_lines[-1])
            if last_line.find('# last_updated_date') >= 0:
                updated_lines[-1] = '# {}'.format(last_updated_date)
                last_updated_date_flag = True
            else:
                updated_lines.append('# {}'.format(last_updated_date))

        print("--update--")
        if len(updated_lines):
            fp.seek(0)
            fp.truncate()
            fp.writelines(updated_lines)
            print(updated_lines)
            changed_file.append(file_path)
            
def git_push():
    print("--------git-------")
    try:
        repo.index.add(changed_file)
        repo.index.commit("Azure pipeline Update Dockerfile")
        origin = repo.remote(name="origin")
        origin.push()
        print('*******Done**********')
    except Exception as e:
        print(e)    


generateTrivyReport()
