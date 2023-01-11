#include <unistd.h>
#include <stdio.h>

void child_action()
{
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
        printf("%d\n",proc_num);
        parent_action(proc_num - 1);
    }
    else if(pid < 0)
    {
        printf("error");
    }
}

int main(void)
{
    int child_proc_num = 5000000;
    
    parent_action(child_proc_num);
    sleep(60);
    return 0;
}
