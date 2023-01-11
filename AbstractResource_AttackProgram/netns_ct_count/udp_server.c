#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main(int argc, char **argv)
{
    int connection_count = 0;
    while (1)
    {
        int sd;
        struct sockaddr_in addr;

        socklen_t sin_size;
        struct sockaddr_in from_addr;

        char buf[2048];

        if ((sd = socket(AF_INET, SOCK_DGRAM, 0)) < 0)
        {
            perror("socket");
            return -1;
        }

        addr.sin_family = AF_INET;
        addr.sin_port = htons(connection_count + 1024);
        addr.sin_addr.s_addr = INADDR_ANY; 

        if (bind(sd, (struct sockaddr *)&addr, sizeof(addr)) < 0)
        {
            perror("bind");
            return -1;
        }

        memset(buf, 0, sizeof(buf));

        if (recvfrom(sd, buf, sizeof(buf), 0,
                     (struct sockaddr *)&from_addr, &sin_size) < 0)
        {
            perror("recvfrom");
            return -1;
        }

        printf("%s\n", buf);

        connection_count += 1;
    }
    return 0;
}
