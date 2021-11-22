import json

def open_file ():
    with open('data.json', 'r') as data_file:
        return json.load(data_file)     

def save_file(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4) 
    
def add_item (data, name, ip, oid):
    oidlist = oid.split(',') # make a list from sting separated from coma
    oidlistdict=[] # make an epmty lis

    for oid in oidlist :

        oidlistdict.append({'oid':oid}) # apppend
     
    data['equipements'].append({
            'name': name, 
            'ip': ip,
            'oids': oidlistdict })
    save_file(data) 

def mod_item(data, name, field, value):
    for equipement in data['equipements']:
        if equipement['name'] == name:
            print (equipement[field])
            equipement[field] = value
    save_file(data)
    
def delete_item(data, name):
    for i in data['equipements']:
        if i['name'] == name:
            data['equipements'].remove(i)
    save_file(data)
 