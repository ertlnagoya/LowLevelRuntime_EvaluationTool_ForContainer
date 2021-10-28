import matplotlib.pyplot as plt
import numpy as np
import sys

def edit_data_memory(file_name,mem_list,swap_list):
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

def edit_data_syscall(file_name,score_list):
    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.split()
        if(len(line) >= 4):
            if(line[3] == "Score"):
                score_list.append(float(line[6]))
    print(score_list)
    file.close()

#main
benchmark = str(sys.argv[1])
low_level_runtime = []
for i in range(len(sys.argv) - 2):
    low_level_runtime.append(str(sys.argv[i+2]))


if(benchmark == "memory"):
    fig = plt.figure()
    for i in low_level_runtime:
        mem_list = []
        swap_list = []
        edit_data_memory(benchmark+"/"+i+".txt",mem_list,swap_list)
        x_line = np.linspace(1,len(mem_list),len(mem_list))
        plt.plot(x_line, [(x + y)/1024 for (x, y) in zip(mem_list, swap_list)],label=i,marker="o")

    plt.xlabel("Time(sec)")
    plt.ylabel("Memory(GB)")
    plt.legend()
    plt.savefig("memory/Memory.png")
    plt.show()
elif(benchmark == "syscall"):
    y_label = "Score"
    max_list = []
    min_list = []
    avg_list = []
    all_list = [max_list,min_list,avg_list]
    all_name = ["Max","Min","Avg"]
    for i in low_level_runtime:
        result_list = []
        edit_data_syscall(benchmark+"/"+i+".txt",result_list)
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
    
