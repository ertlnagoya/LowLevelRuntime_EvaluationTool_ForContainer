#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <signal.h>


void child_action()
{
        int fd = 1;

        while(fd > 0)
        {
            fd = open("memo.txt", O_RDONLY);
        }

        sleep(60);
}

void parent_action(int proc_num)
{
    pid_t pid;
    
    if(proc_num < 0) return;
    
    if((pid = fork()) == 0)
    {
        child_action();
    }
    else if(pid > 0)
    {
        parent_action(proc_num - 1);
    }
}

int main(void)
{
    char *command = "touch memo.txt";
    int res;
    res = system(command);
    
    
    int child_proc_num = 20;
    
    parent_action(child_proc_num);
    sleep(60);
    return 0;
}
