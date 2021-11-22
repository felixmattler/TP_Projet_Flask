import io
from flask import Flask, jsonify, request, render_template, redirect
import json
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure

from python_json.json_reader import *
from snmp_functions import *
import graph_functions


#########################################
#                                       #
#               FUNCTIONS               #
#                                       #
######################################### 

def listEqpt():
    with open('data.json', 'r') as data_file:
        data = json.load(data_file)
        return (data['equipements'])

app = Flask(__name__)


### MAIN INDEX ###

@app.route('/', methods=['GET', 'POST'])
def index():
    eqpt_liste = listEqpt()
    return render_template('main_template.html', eqpt_liste = eqpt_liste)


#########################################
#                                       #
#          MODULE CONFIGURATION         #
#                                       #
#########################################

# ADD 

@app.route('/config/add', methods=['GET'])
def add_eqpt():
    return render_template('module_config/add_eqpt.html')

@app.route('/config/add/ok', methods=['POST'])
def add_eqpt_ok():
    
    data_name = request.form['form_name']
    data_ip = request.form['form_ip']
    data_oid =  request.form['form_oid']

    data_json = open_file()
    add_item(data_json, data_name, data_ip, data_oid)
    eqpt = {
        "render_name": data_name,
        "render_ip": data_ip,
        "render_oid": data_oid
    }
    return render_template('module_config/add_eqpt_ok.html', eqpt=eqpt)


# DEL


@app.route('/config/del', methods=['GET'])
def del_eqpt():
    eqpt_liste = listEqpt()
    
    return render_template('module_config/del_eqpt.html', eqpt_liste=eqpt_liste)

@app.route('/config/del/ok', methods=['GET', 'POST'])
def del_eqpt_ok():
    
    data_name = request.form['form_name']

    data_json = open_file()
    delete_item(data_json, data_name)
    eqpt = {
        "render_name": data_name,
    }
    return render_template('module_config/del_eqpt_ok.html', eqpt=eqpt)

# MOD

@app.route('/config/mod', methods=['GET'])
def mod_eqpt():
    eqpt_liste = listEqpt()
    return render_template('module_config/mod_eqpt.html', eqpt_liste=eqpt_liste)

@app.route('/config/mod/ok', methods=['GET', 'POST'])
def mod_eqpt_ok():
    
    data_name = request.form['form_name']
    data_field = request.form['form_field']
    data_value = request.form['form_value']

    data_json = open_file()
    mod_item(data_json, data_name, data_field, data_value)
    
    eqpt = {
        "render_name": data_name,
        "render_field": data_field,
        "render_value": data_value
    }
    return render_template('module_config/mod_eqpt_ok.html', eqpt=eqpt)


#########################################
#                                       #
#          MODULE SURVEILLANCE          #
#                                       #
#########################################

@app.route('/surveillance', methods=['GET'])
def surveillance_main():
    eqpt_liste = listEqpt()
    return render_template('module_surveillance/surveillance_main.html', eqpt_liste = eqpt_liste)

@app.route('/surveillance/result', methods=['GET', 'POST'])
def surveillance_result():
    data_ip = request.form['form_ip']
    data_oid = request.form['form_oid']

    snmp_result = snmpget(data_ip, data_oid)

    # GRAPH CODE
    valuesTable = graph_functions.parserFn(data_ip, data_oid)
    graph = graph_functions.graphFn(valuesTable)

    eqpt_liste = listEqpt()

    return render_template('module_surveillance/surveillance_result.html', snmp_result = snmp_result, eqpt_liste = eqpt_liste, graph = graph)


#########################################
#                                       #
#            MODULE LOGS                #
#                                       #
######################################### 

@app.route('/logs', methods=['GET'])
def logs_main():
    return render_template('module_logs/logs_main.html')



#########################################
#                                       #
#                  MAIN                 #
#                                       #
#########################################

if __name__ == '__main__':
    app.run(debug=True)