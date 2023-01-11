#include <unistd.h>
#include <fcntl.h>

void child_action()
{
        int fd;
        fd = open("/dev/ptmx", O_RDONLY);
        
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
    int child_proc_num = 5000;
    
    parent_action(child_proc_num);
    sleep(60);
    return 0;
}
