from datetime import datetime
from itertools import accumulate
from selenium import webdriver
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np

import sys
sys.path.append("..")

driver = webdriver.Firefox()
lowlevelruntime = ["runc","crun","gVisor","Kata Containers"]
release_date_list = [datetime.datetime(2015,12,12),datetime.datetime(2019,1,19),datetime.datetime(2018,5,2),datetime.datetime(2018,4,19)]

def Search_CVE(cve_num,cve_link_list,total_score):
    total_score = 0
    for j in range(cve_num):
        cve_element = driver.find_element(by=By.XPATH, value='//*[@id="TableWithRules"]/table/tbody/tr[' + str(j+1) +']/td[1]/a')
        cve_link_list.append(cve_element.get_attribute("href"))
        split_start_num = cve_link_list[j].find("CVE-")
        cve_name = cve_link_list[j][split_start_num:]
        print(cve_name)
        epss_score = Get_Score_EPSS(cve_name)
        print(epss_score)
        if(epss_score != None) :total_score+=epss_score
    total_score_list.append(total_score)
    print("\ntotal score : " + str(total_score) + "\n\n")


def Search_CVE_Date(cve_link_list,cve_date_list,release_date):
    for k in range(len(cve_link_list)):
        driver.get(cve_link_list[k])
        cve_date = driver.find_element(by=By.XPATH, value='//*[@id="GeneratedTable"]/table/tbody/tr[11]/td[1]/b')
        cve_date_format = datetime.datetime( int(cve_date.text[0:4]),int(cve_date.text[4:6]),int(cve_date.text[6:8]) )
        cve_date_list.append(cve_date_format)
    cve_date_list.sort()
    #First, insert release date
    cve_date_list.insert(0,release_date)


def Get_Score_EPSS(cve_name):
    file = open("epss_scores.csv",errors="ignore")
    lines = file.readlines()

    for l in range(0,len(lines)):
        line=lines[l].split(',')
        if(cve_name == line[0]):
            file.close()
            return float(line[1])


def Make_Graph(cve_date_list,lowlevelruntime):
    y_label = "Accumulation_CVE_"+lowlevelruntime
    ax = plt.subplot()
    y_line = np.linspace(0,len(cve_date_list),len(cve_date_list))
    ax.plot(cve_date_list, y_line ,linestyle = "solid",label=lowlevelruntime,marker="o")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlim(cve_date_list[0], datetime.datetime(cve_date_list[len(cve_date_list)-1].year + 1,1,1))
    plt.yticks(np.arange(0, len(cve_date_list) + 1, 1))
    plt.xlabel("Date")
    plt.ylabel(y_label)
    plt.savefig("gompertz_cve/"+y_label+".png")
    plt.show()

#Generate EPSS-Score Bar Graph
def Make_EPSS_Graph(result_list):
    y_label = "EPSS*CVE"
    x_line = np.linspace(1,len(lowlevelruntime),len(lowlevelruntime))
    fig = plt.figure()
    for i in range(len(lowlevelruntime)):
        plt.bar(x_line[i], result_list[i],label=lowlevelruntime[i])
        plt.text(x_line[i],result_list[i],result_list[i], ha='center', va='bottom')
    plt.tick_params(labelbottom=False,bottom=False)
    plt.xlabel("Runtime")
    plt.ylabel(y_label)
    fig.legend(labels=lowlevelruntime,loc='upper center',ncol=4)
    plt.savefig("gompertz_cve/" + y_label + ".png")
    plt.show()

#Main
total_score_list = []
for i in range(len(lowlevelruntime)):
    print(lowlevelruntime[i])
    driver.get("https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword="+lowlevelruntime[i])
    form = driver.find_element(by=By.XPATH, value='//*[@id="CenterPane"]/div[1]/b')
    cve_num = int(form.text)
    cve_link_list = []
    cve_date_list = []
    total_score = 0
    Search_CVE(cve_num,cve_link_list,total_score_list)
    Search_CVE_Date(cve_link_list,cve_date_list,release_date_list[i])
    Make_Graph(cve_date_list,lowlevelruntime[i])
    #print(cve_date_list)
Make_EPSS_Graph(total_score_list)

driver.quit()
