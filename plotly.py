import numpy as ny
import plotly as plotly
import plotly.graph_objs as go

## Convert the String array to a float array

def returnFloatArray(x):
    newArray = []
    for val in x:
        #print(val)
        newArray.append(stringToFloat(val))
    return newArray

## Concert each String to a float number

def stringToFloat(number):
    if number != " ":
        return float(number)

dataInsertion = ny.loadtxt("insertion.txt", delimiter = ",",dtype = 'str')
dataQuick = ny.loadtxt("quck.txt", delimiter = ",", dtype = 'str')
dataShell = ny.loadtxt("shell.txt", delimiter = ",", dtype = 'str')
dataSize = ny.loadtxt("size.txt", delimiter = ",", dtype = 'str')

dataQuick = returnFloatArray(dataQuick)
dataInsertion = returnFloatArray(dataInsertion)
dataShell = returnFloatArray(dataShell)
dataSize = returnFloatArray(dataSize)

# Traces
trace0 = go.Scatter(
    x=dataSize,
    y=dataInsertion,
    name='Insertion',
    mode='lines'
)
trace1 = go.Scatter(
    x=dataSize,
    y=dataShell,
    name='Shell',
    mode='lines'
)
trace2 = go.Scatter(
    x=dataSize,
    y=dataQuick,
    name='Quick',
    mode='lines'
)

data = [trace0,trace1,trace2]

layout = go.Layout(
    title='Complexity Tutorial 1',
    xaxis=dict(
        title='Size',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Time(seconds)',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)

fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename='graph.html')
