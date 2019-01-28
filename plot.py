import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import math
import csv
import datetime as dt 
import random as r 
import codecs 
import cStringIO
headers = ["Tiempo","Voltaje", "Angulo"]
df = pd.read_csv('/home/mariana/Escritorio/spel/ADCS/Python/Sensor/datos.csv',names=headers)
print (df)
x = df['Tiempo']
y1 = df['Voltaje']
y2 = df['Angulo']
f = plt.figure(1)
plt.plot(x, y1)
plt.title('Voltaje vs Tiempo')
plt.ylabel('Voltaje [V]')
plt.xlabel('Tiempo [ms]')
f.show()

g = plt.figure(2)
plt.plot(x, y2)
plt.title('Angulo vs Tiempo')
plt.ylabel('Angulo [deg]')
plt.xlabel('Tiempo [ms]')
g.show()


plt.show()