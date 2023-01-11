#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main(int argc, char **argv)
{
    int connection_max = 100000;
    int connection_count = 0;
    while (connection_count < connection_max)
    {

        int sd;
        struct sockaddr_in addr;

        if ((sd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
        {
            perror("socket");
        }

        addr.sin_family = AF_INET;
        addr.sin_port = htons(connection_count + 1024);
        addr.sin_addr.s_addr = inet_addr("192.168.11.3");

        if (connect(sd, (struct sockaddr *)&addr, sizeof(struct sockaddr_in)) < 0)
        {
            continue;
        }

        if (send(sd, "I am send process", 17, 0) < 0)
        {
            perror("send");
            continue;
        }

        printf("%d\n",connection_count);
        connection_count += 1;
    }
}
