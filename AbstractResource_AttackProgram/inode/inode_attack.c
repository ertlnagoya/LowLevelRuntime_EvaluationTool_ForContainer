#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>

int main(void)
{
    int fd = 1;
    int file_num = 20000000;

    for (int i = 0; i < file_num;  i++)
    {
        char fname[1024];
        sprintf(fname, "./memo/memo%d.txt",i);
        fd = open(fname, O_CREAT|O_WRONLY);
        close(fd);
    }
    return 0;
}
