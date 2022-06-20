from mailbox import linesep
import matplotlib.pyplot as plt
import numpy as np
import sys

from numpy.lib.twodim_base import mask_indices

#Get from the raw data of each benchmark item

#lifecycle
def edit_data_lifecycle(file_name,create_time_list,start_time_list,stop_time_list,remove_time_list):
    file = open(file_name)
    lines = file.readlines()

    for i in range(0,len(lines)):
        line = lines[i].split()

        if(len(line) == 0): continue
        if(line[0] != "real"): continue

        if(lines[i-1].split()[0] == "create"):
            create_time_list.append(float(line[1]))
        elif(lines[i-1].split()[0] == "start"):
            start_time_list.append(float(line[1]))
        elif(lines[i-1].split()[0] == "stop"):
            stop_time_list.append(float(line[1]))
        elif(lines[i-1].split()[0] == "remove"):
            remove_time_list.append(float(line[1]))

    file.close()

#resource_storage
def edit_data_resource_storage(file_name,storage_size_list):
    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.split()

        if(len(line) == 0): continue
        
        if(line[5] == "/"):
            storage_size_list.append(int(line[2]))

    file.close()

#resource_cpu
def edit_data_resource_cpu(file_name,idle_list):
    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.split()

        if(len(line) == 0): continue

        if(line[1] == "all"):
            idle_list.append(float(line[11]))

    file.close()

#resource_memory
def edit_data_resource_memory(file_name,mem_size_list):
    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.split()

        if(len(line) == 0): continue
        
        if(line[0] == "Mem:"):
            mem_size_list.append(float(line[3]))

    file.close()

#sysbench(fileIO,cpu,memory)
def edit_data_sysbench(runtime,file_name,total_time_list):
    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.split()

        if(len(line) < 3): continue

        if(line[0] == "total" and line[1] == "time:"):
            total_time_list.append(float(line[2][:-1]))
    
    print("\n"+runtime)
    print(total_time_list)

    file.close()

#syscall(UnixBench)
def edit_data_syscall(runtime,file_name,score_list):
    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.split()
     
        if(len(line) < 4): continue
        
        if(line[3] == "Score"):
            score_list.append(float(line[6]))

    print("\n"+runtime)
    print(score_list)

    file.close()

#network
def edit_data_network(runtime,file_name,bandwidth_list):
    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.split()

        if(len(line) != 8): continue
        
        if(line[7] == "MBytes/sec"):
            bandwidth_list.append(float(line[6]))

    print("\n"+runtime)
    print(bandwidth_list)

    file.close()

#syscall_collect 
def edit_data_syscall_collect(file_name,syscall_count_list,syscall_name_list):
    file = open(file_name)
    lines = file.readlines()

    if(len(lines) == 0): return
    
    for i in range(len(lines)):
        line = lines[i].split()
        syscall_count_list.append(int(line[0]))
        syscall_name_list.append(line[1])

    file.close()

#Function for taking data from csv in syscall_collect
def Get_Name_CVE(syscall_name,CVE_list):
	file = open("allitems.csv",errors="ignore")
	lines = file.readlines()

	for i in range(0,len(lines)):
		if(syscall_name in lines[i]):
			line = lines[i].split(',')
			CVE_list.append(line[0])
	file.close()

def Get_Score_EPSS(CVE_name,EPSS_score_list):
    file = open("epss_scores.csv",errors="ignore")
    lines = file.readlines()

    for i in range(0,len(lines)):
        line=lines[i].split(',')
        if(CVE_name == line[0]):
            EPSS_score_list.append(float(line[1]))
    file.close()





#Main
#Arguments of command are stored in variables
if(len(sys.argv) > 0):
    benchmark = str(sys.argv[1])
    container_num = int(sys.argv[2])
    low_level_runtime_list = []
for i in range(len(sys.argv) - 3):
    low_level_runtime_list.append(str(sys.argv[i+3]))

#Generate Bar Graph
def Make_Bar_Graph(result_list,y_label,graph_name):
    x_line = np.linspace(1,len(low_level_runtime_list),len(low_level_runtime_list))
    fig = plt.figure()
    for i in range(len(low_level_runtime_list)):
        plt.bar(x_line[i], result_list[i],label=low_level_runtime_list[i])
        plt.text(x_line[i],result_list[i],result_list[i], ha='center', va='bottom')
    plt.tick_params(labelbottom=False,bottom=False)
    plt.xlabel("Runtime")
    plt.ylabel(y_label)
    fig.legend(labels=low_level_runtime_list,loc='upper center',ncol=4)
    plt.savefig(benchmark + "/" + graph_name + ".png")
    print(benchmark + "/" + graph_name + ".png")
    plt.show()

#Prepare a list of max, min, avg firstly and use it later.
max_list = []
min_list = []
avg_list = []
result_kind_list = [max_list,min_list,avg_list]
result_kind_name = ["Max","Min","Avg"]

#Different operation for each item of benchmark with if
if(benchmark == "lifecycle"):
    ope_name_list = ["Create","Start","Stop","Remove"]
    #Edit into easy data format from raw txt
    for i in low_level_runtime_list:
        create_time_list = []
        start_time_list = []
        stop_time_list = []
        remove_time_list = []

        ope_time_list = [create_time_list,start_time_list,stop_time_list,remove_time_list]
        edit_data_lifecycle(benchmark+"/"+i+".txt",create_time_list,start_time_list,stop_time_list,remove_time_list)

        for result_list in ope_time_list:
            max_list.append(max(result_list))
            min_list.append(min(result_list))
            avg_list.append(round(sum(result_list) / len(result_list),2))

    for j in range(len(result_kind_list)):
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)
        graph_list = [ax1,ax2,ax3,ax4]
        #Make graphs for each item in the life cycle (Create, Start, etc.)
        for k in range(len(ope_name_list)):
            x_line = np.linspace(1,len(low_level_runtime_list),len(low_level_runtime_list))
            #Write data of each low-level runtime to the graph
            for l in range(0,len(low_level_runtime_list)):   
                graph_list[k].bar(x_line[l], result_kind_list[j][k+4*l],label=low_level_runtime_list[l])
                graph_list[k].text(x_line[l],result_kind_list[j][k+4*l],result_kind_list[j][k+4*l] ,ha='center', va='bottom')
            graph_list[k].set_xlabel(ope_name_list[k])
            graph_list[k].set_ylabel("Time(sec)")
            graph_list[k].tick_params(labelbottom=False,bottom=False)
        fig.legend(labels=low_level_runtime_list,loc='upper center',ncol=4)
        plt.subplots_adjust(wspace=0.4,hspace=0.4)
        plt.savefig("lifecycle/"+result_kind_name[j]+".png")
        plt.show()

elif(benchmark == "resource_storage"):
    storage_diff_list = []
    #Write the current size of the storage minus the initial size to the graph
    for i in range(len(low_level_runtime_list)):
        storage_size_list = []

        edit_data_resource_storage(benchmark+"/"+low_level_runtime_list[i]+".txt",storage_size_list)
        storage_diff_list.append(storage_size_list[1]-storage_size_list[0])

    Make_Bar_Graph(storage_diff_list,"Storage Usage(MB) : " +str(container_num) + " containers","Storage_Usage")

elif(benchmark == "resource_cpu" or benchmark == "resource_memory"):
    #Graph of resource usage per 1 second
    fig = plt.figure()
    total_list = []
    if(benchmark == "resource_cpu"): y_label = "Transition_CPU_Usage_Rate(%)"
    elif(benchmark == "resource_memory"): y_label = "Transition_Free_Memory(MB)"
    ##Make graphs
    for i in low_level_runtime_list:
        result_list = []

        if(benchmark == "resource_cpu"): edit_data_resource_cpu(benchmark+"/"+i+".txt",result_list)
        elif(benchmark == "resource_memory"): edit_data_resource_memory(benchmark+"/"+i+".txt",result_list)
        total_list.append(max(result_list) - min(result_list))
        x_line = np.linspace(1,len(result_list),len(result_list))
        plt.plot(x_line, result_list ,label=i,marker="o")
    plt.ylim(0,)
    plt.xlabel("Time(sec)")
    plt.ylabel(y_label)
    fig.legend(labels=low_level_runtime_list,loc='upper center',ncol=4)
    plt.savefig(benchmark+"/"+y_label+".png")
    plt.show()
    
    #Graph of difference in resource usage before and after container create
    if(benchmark == "resource_cpu"): y_label = "Diff_CPU_Usage_Rate(%)"
    elif(benchmark == "resource_memory"): y_label = "Diff_Memory_Usage(MB)"

    Make_Bar_Graph(total_list,y_label + " : " +str(container_num) + " containers",y_label)

elif(benchmark == "syscall_collect"):
    x_line = np.linspace(1,len(low_level_runtime_list),len(low_level_runtime_list))
    Top_num = 5 #Specify how many syscalls to display
    total_score_list = []
    #Calculate score with the type and number of syscall and EPSS-score
    for i in range(len(low_level_runtime_list)):
        fig = plt.figure()
        syscall_count_list = []
        syscall_name_list = []

        edit_data_syscall_collect(benchmark+"/"+low_level_runtime_list[i]+"_sort.txt",syscall_count_list,syscall_name_list)
        Top_syscall_count_list = []
        Top_syscall_name_list = []
        #Save Top's syscalls to list
        for j in range(Top_num):
            if(len(syscall_name_list) -1 < j): continue
            Top_syscall_count_list.append(syscall_count_list[j])
            Top_syscall_name_list.append(syscall_name_list[j])

        #Scoring with EPSS-score
        output_text = ""
        output_text += low_level_runtime_list[i]
        total_score = 0
        #Research CVEs which use each syscall
        for k in range(len(syscall_name_list)):
            output_text += "\n\nsyscall name : " + syscall_name_list[k] + "\n["
            CVE_list = []
            Get_Name_CVE(" " + syscall_name_list[k]+"()",CVE_list)
            score_list = []
            #Get EPSS-score assigned to each CVE
            for l in range(len(CVE_list)):
                Get_Score_EPSS(CVE_list[l],score_list)
                output_text += str(CVE_list[l]) + " : " + str(score_list[l]) + ", "
            #Add the number of syscall * EPSS-score score to the total score
            total_score += syscall_count_list[k] * sum(score_list)
            output_text += "]"
        output_text += "\n\n" + str(total_score) + "\n\n"
        total_score_list.append(round(total_score,4))
        with open("syscall_collect/" + low_level_runtime_list[i]+"_total_score.txt", mode='w') as f:
            f.write(output_text)
        f.close()
        #print(output_text)

        #Make graph of Top's syscall breakdown
        plt.pie(Top_syscall_count_list,counterclock=False,startangle=90,autopct="%1.1f%%")
        plt.xlabel(low_level_runtime_list[i] + " Top " + str(Top_num) + " syscall")
        fig.legend(labels=Top_syscall_name_list,loc='upper center',ncol=4)
        plt.savefig(benchmark+"/"+ low_level_runtime_list[i] +"_Syscall_Collect.png")
        #plt.show()
        
    #Make graph of the total score for each runtime
    Make_Bar_Graph(total_score_list,"Total_Score","Total_Score")

else:
    if(benchmark == "syscall"): y_label = "Score"
    elif(benchmark == "network"): y_label = "Bandwidth(MBytes-sec)"
    else: y_label = "Total_Time(sec)"
    #Find max, min, and avg values
    for i in low_level_runtime_list:
        result_list = []        

        if(benchmark == "syscall"): edit_data_syscall(i,benchmark+"/"+i+".txt",result_list)
        elif(benchmark == "network"): edit_data_network(i,benchmark+"/"+i+".txt",result_list)
        else: edit_data_sysbench(i,benchmark+"/"+i+".txt",result_list)
        max_list.append(max(result_list))
        min_list.append(min(result_list))
        avg_list.append(round(sum(result_list) / len(result_list),4))
    x_line = np.linspace(1,len(low_level_runtime_list),len(low_level_runtime_list))
    #Make graphs of max, min, and avg values
    for j in range(len(result_kind_list)):
        Make_Bar_Graph(result_kind_list[j],result_kind_name[j]+"_"+y_label,result_kind_name[j]+"_"+y_label)
