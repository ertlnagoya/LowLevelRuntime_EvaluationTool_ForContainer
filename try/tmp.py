CVE_list = []

def Get_Name_CVE(syscall_name):
	file = open("allitems.csv",errors="ignore")
	lines = file.readlines()
	for i in range(0,len(lines)):
		if(syscall_name in lines[i]):
			line = lines[i].split(',')
			print(line[0])
			CVE_list.append(line[0])
	file.close()

score_list = []
def Get_Score_EPSS(CVE_name):
	file = open("epss_scores.csv",errors="ignore")
	lines = file.readlines()
	for i in range(0,len(lines)):
		line = lines[i].split(',')
		if(CVE_name == line[0]):
			print(str(line[0]) + " : " + str(line[1]))
			score_list.append(float(line[1]))
	file.close()

Get_Name_CVE("mmap()")
for i in range(len(CVE_list)):
	Get_Score_EPSS(CVE_list[i])
