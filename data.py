#!/usr/bin/env python
# coding: utf-8

# In[76]:


nazwa=[]
adres=[]
cena=[]

for i in range(0,7):
    link=driver.page_source
    soup=BeautifulSoup(link,"html.parser")
    ceny= soup.find_all("div",{"class":"petrol pb"})
    for item in ceny:
        new=str(item.text.strip())
        new=new[new.find("4")-1:new.find("4")+4]
        cena.append(new)
    adresy= soup.find_all("div",{"class":"name shorter"})
    for item in adresy:
        new=str(item.text.strip())
        new=new[new.find(" ")+1:len(new)]
        adres.append(new)
    nazwy= soup.find_all("div",{"class":"address"})
    for item in nazwy:
        new=str(item.text.strip())
        nazwa.append(new)
    next_page = driver.find_elements_by_class_name('mobile-txt')
    next_page[1].click()
    time.sleep(4)
    i += 1


# In[118]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from docx import Document
from docx.shared import Inches
from io import BytesIO

#driver = webdriver.Chrome()
#driver.get("https://mapa.nocowanie.pl/warszawa/ceny_paliw/")
#nazwa=[]
#adres=[]
#cena_lpg=[]
#cena_on=[]
#cena_pb98=[]
#cena_pb95=[]


# In[147]:


link=driver.page_source
soup=BeautifulSoup(link,"html.parser")
ceny= soup.find_all("ul",{"class":"block-list"})
new=str(item.text.strip())
new=new[new.find("LPG: ")+5:new.find("LPG: ")+9]
cena_lpg.append(new)
new=str(item.text.strip())
new=new[new.find("ON: ")+4:new.find("ON: ")+9]
cena_on.append(new)
new=str(item.text.strip())
new=new[new.find("Pb98: ")+6:new.find("Pb98: ")+10]
cena_pb98.append(new)
new=str(item.text.strip())
new=new[new.find("Pb95: ")+6:new.find("Pb95: ")+10]
cena_pb95.append(new)
adresy= soup.find_all("span",{"class":"f--md"})
adres.append(adresy[0].text.strip())
nazwy= soup.find_all("div",{"class":"map__controls-header"})
nazwa.append(nazwy[0].text.strip())


# In[148]:


tabela=pd.DataFrame({ 'nazwa':nazwa,'adres':adres,"cena lpg": cena_lpg, "cena on": cena_on, "cena pb98": cena_pb98 , "cena pb95": cena_pb95}) 
tabela.to_excel("ceny_paliw_202010.xls")
tabela


# In[ ]:




