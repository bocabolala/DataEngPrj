# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random, re
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


private_net = "UPPMAX 2022/1-1 Internal IPv4 Network"
# private_net = 'SNIC Network'
floating_ip_pool_name = "Public External IPv4 Network"
floating_ip = "130.238.28.110"
image_name = "Ubuntu 20.04 - 2021.03.23"
client_key_name = "Group7Key"

identifier = random.randint(1000,9999)

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

f_L = nova.flavors.find(name="ssc.large")
f_M = nova.flavors.find(name="ssc.medium")

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")

cfg_file_path = os.getcwd()+'universal.txt'
if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path)
else:
    sys.exit("universal.txt is not in current working directory") 

secgroups = ['default']

print ("Creating instances ... ")
instance_w1 = nova.servers.create(name="G7_prod1", image=image, flavor=f_M, key_name=client_key_name, userdata=userdata, nics=nics,security_groups=secgroups)

instance_w2 = nova.servers.create(name="G7_prod2", image=image, flavor=f_M, key_name=client_key_name, userdata=userdata, nics=nics,security_groups=secgroups)

instance_w3 = nova.servers.create(name="G7_dev1", image=image, flavor=f_M, key_name=client_key_name, userdata=userdata, nics=nics,security_groups=secgroups)

instance_w4 = nova.servers.create(name="G7_dev2", image=image, flavor=f_M, key_name=client_key_name, userdata=userdata, nics=nics,security_groups=secgroups)

inst_status_w1 = instance_w1.status
inst_status_w2 = instance_w2.status
inst_status_w3 = instance_w3.status
inst_status_w4 = instance_w4.status

print ("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status_w1 == 'BUILD' or inst_status_w2 == 'BUILD':
    print ("Instance: "+instance_w1.name+" is in "+inst_status_w1+" state, sleeping for 5 seconds more...")
    print ("Instance: "+instance_w2.name+" is in "+inst_status_w2+" state, sleeping for 5 seconds more...")
    print ("Instance: "+instance_w3.name+" is in "+inst_status_w3+" state, sleeping for 5 seconds more...")
    print ("Instance: "+instance_w4.name+" is in "+inst_status_w4+" state, sleeping for 5 seconds more...")
    time.sleep(5)

    instance_w1 = nova.servers.get(instance_w1.id)
    inst_status_w1 = instance_w1.status

    instance_w2 = nova.servers.get(instance_w2.id)
    inst_status_w2 = instance_w2.status

    instance_w3 = nova.servers.get(instance_w3.id)
    inst_status_w3 = instance_w3.status

    instance_w4 = nova.servers.get(instance_w4.id)
    inst_status_w4 = instance_w4.status


ip_address_w1 = None
for network in instance_w1.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_w1 = network
        break
if ip_address_w1 is None:
    raise RuntimeError('No IP address assigned!')

ip_address_w2 = None
for network in instance_w2.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_w2 = network
        break
if ip_address_w2 is None:
    raise RuntimeError('No IP address assigned!')

ip_address_w3 = None
for network in instance_w3.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_w3 = network
        break
if ip_address_w3 is None:
    raise RuntimeError('No IP address assigned!')

ip_address_w4 = None
for network in instance_w4.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_w4 = network
        break
if ip_address_w4 is None:
    raise RuntimeError('No IP address assigned!')

print ("Instance: "+ instance_w1.name +" is in " + inst_status_w1 + " state" + " ip address: "+ ip_address_w1)
print ("Instance: "+ instance_w2.name +" is in " + inst_status_w2 + " state" + " ip address: "+ ip_address_w2)
print ("Instance: "+ instance_w3.name +" is in " + inst_status_w3 + " state" + " ip address: "+ ip_address_w3)
print ("Instance: "+ instance_w4.name +" is in " + inst_status_w4 + " state" + " ip address: "+ ip_address_w4)
