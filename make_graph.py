import matplotlib.pyplot as plt
import numpy as np
import sys

#ここを修正する
def edit_data_lifecycle(file_name,real_list,user_list,sys_list):
    file = open(file_name)
    lines = file.readlines()
    for line in lines:
        line = line.split()
        if(len(line) != 0):
            if(line[0] == "real"):
                real_list.append(float(line[1]))
            elif(line[0] == "user"):
                user_list.append(float(line[1]))
            elif(line[0] == "sys"):
                sys_list.append(float(line[1]))
    file.close()

def edit_data_resource_memory(file_name,mem_list,swap_list):
    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.split()
        if(len(line) != 0):
            if(line[0] == "Mem:"):
                mem_list.append(float(line[3]))
            elif(line[0] == "Swap:"):
                swap_list.append(float(line[3]))
    file.close()

def edit_data_sysbench(runtime,file_name,total_time_list):
    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.split()
        if(len(line) >= 3):
            if(line[0] == "total" and line[1] == "time:"):
                total_time_list.append(float(line[2][:-1]))
    print("\n"+runtime)
    print(total_time_list)
    file.close()

def edit_data_syscall(runtime,file_name,score_list):
    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.split()
        if(len(line) >= 4):
            if(line[3] == "Score"):
                score_list.append(float(line[6]))
    print("\n"+runtime)
    print(score_list)
    file.close()

def edit_data_network(runtime,file_name,bandwidth_list):
    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.split()
        if(len(line) == 8):
            if(line[7] == "MBytes/sec"):
                bandwidth_list.append(float(line[6]))
    print("\n"+runtime)
    print(bandwidth_list)
    file.close()

#main
benchmark = str(sys.argv[1])
container_num = int(sys.argv[2])
low_level_runtime = []
for i in range(len(sys.argv) - 3):
    low_level_runtime.append(str(sys.argv[i+3]))

if(benchmark == "lifecycle"):
    time_val = ["Real_Time","User_Time","Sys_Time"]
    operation = ["Create","Start","Stop","Remove"]
    for h in range(len(time_val)):
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)
        graph_list = [ax1,ax2,ax3,ax4]
        real_list = []
        user_list = []
        sys_list = []
        for i in range(0,len(low_level_runtime)):
            edit_data_lifecycle(benchmark+"/"+low_level_runtime[i]+".txt",real_list,user_list,sys_list)
        all_list = [real_list,user_list,sys_list]
        x_line = np.linspace(1,len(low_level_runtime),len(low_level_runtime))
        for j in range(0,4):
            for i in range(0,len(low_level_runtime)):
                graph_list[j].bar(x_line[i], all_list[h][j+4*i],label=low_level_runtime[i])
                graph_list[j].text(x_line[i],all_list[h][j+4*i],all_list[h][j+4*i] ,ha='center', va='bottom')
            graph_list[j].set_xlabel(operation[j] + " (" + str(container_num) + "containers)")
            graph_list[j].set_ylabel("Time(sec)")
            graph_list[j].tick_params(labelbottom=False,bottom=False)
        fig.legend(labels=low_level_runtime,loc='upper center',ncol=4)
        plt.subplots_adjust(wspace=0.4,hspace=0.3)
        plt.savefig("lifecycle/"+time_val[h]+".png")
        plt.show()
elif(benchmark == "resource_memory"):
    total_memory = []
    fig = plt.figure()
    for i in low_level_runtime:
        mem_list = []
        swap_list = []
        edit_data_resource_memory(benchmark+"/"+i+".txt",mem_list,swap_list)
        total_memory.append((max(mem_list) + max(swap_list)) - (min(mem_list) + min(swap_list)))
        x_line = np.linspace(1,len(mem_list),len(mem_list))
        plt.plot(x_line, [(x + y) for (x, y) in zip(mem_list, swap_list)],label=i,marker="o")
    plt.ylim(0,max(mem_list) + max(swap_list) + 500)
    plt.xlabel("Time(sec)")
    plt.ylabel("Memory(MB)")
    plt.legend()
    plt.savefig("resource_memory/Resource_Memory.png")
    plt.show()
    #ここから各コンテナのメモリ使用量
    fig = plt.figure()
    for i in range(len(low_level_runtime)):
        plt.bar(x_line[i], total_memory[i],label=low_level_runtime[i])
        plt.text(x_line[i], total_memory[i],total_memory[i], ha='center', va='bottom')
    plt.tick_params(labelbottom=False,bottom=False)
    plt.xlabel("Runtime")
    plt.ylabel("Memory Usage(MB) : " +str(container_num) + " containers")
    plt.legend()
    plt.savefig(benchmark+"/"+"Memory_Usage.png")
    plt.show()
else:
    if(benchmark == "syscall"): y_label = "Score"
    elif(benchmark == "network"): y_label = "Bandwidth(MBytes-sec)"
    else: y_label = "Total_Time(sec)"
    max_list = []
    min_list = []
    avg_list = []
    all_list = [max_list,min_list,avg_list]
    all_name = ["Max","Min","Avg"]
    for i in low_level_runtime:
        result_list = []
        if(benchmark == "syscall"): edit_data_syscall(i,benchmark+"/"+i+".txt",result_list)
        elif(benchmark == "network"): edit_data_network(i,benchmark+"/"+i+".txt",result_list)
        else: edit_data_sysbench(i,benchmark+"/"+i+".txt",result_list)
        max_list.append(max(result_list))
        min_list.append(min(result_list))
        avg_list.append(sum(result_list) / len(result_list))
    x_line = np.linspace(1,len(low_level_runtime),len(low_level_runtime))

    for n in range(len(all_list)):
        fig = plt.figure()
        for i in range(len(low_level_runtime)):
            plt.bar(x_line[i], all_list[n][i],label=low_level_runtime[i])
            plt.text(x_line[i], all_list[n][i],all_list[n][i], ha='center', va='bottom')
        plt.tick_params(labelbottom=False,bottom=False)
        plt.xlabel("Runtime")
        plt.ylabel(all_name[n]+"_"+ y_label)
        plt.legend()
        plt.savefig(benchmark+"/"+all_name[n]+"_"+y_label+".png")
        plt.show()
    
