# libraries
from io import StringIO
import io, base64
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import pandas as pd


# function

def parserFn(ip, oid):
    inputfile = open('./templates/module_logs/BitRateFile.txt')
    fileTable = inputfile.readlines()
    valuesTable = []
    
    global hours
    hours=[]

    for line in fileTable:
        line = line[:-1]
        lineValueTable = line.split(';')
        if (lineValueTable[3] == ip and lineValueTable[4] == oid):
            valuesTable.append(lineValueTable[5])
            hours.append(lineValueTable[1])
    
    return valuesTable


def graphFn(valuesTable):
    relativeValuesTable = []

    for i in range(0,len(valuesTable)-1):
        relativeValuesTable.append((int(valuesTable[i+1])-int(valuesTable[i]))/10)


    #ordonées + asbcisses
    x_axis=hours[:-1]
    y_axis=[]

    for i in relativeValuesTable:
        y_axis.append(i/1000)



    # data
    df = pd.DataFrame({
        'x_axis': x_axis, 
        'y_axis': y_axis
    })
    
    # plot
    fig = plt.figure(figsize=(8,5))
    plt.plot('x_axis', 'y_axis', data = df, linestyle = '-', marker = 'o')
    plt.xlabel("Time")
    plt.ylabel("Bitrate (Kb/s)")     
    fig.autofmt_xdate()

    # Convert plot to PNG image
    imgdata = io.BytesIO()
    FigureCanvasAgg(fig).print_png(imgdata)
    
    # Encode PNG image to base64 string
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(imgdata.getvalue()).decode('utf8')

    return pngImageB64String