#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    int connection_max = 100000;
    int connection_count = 0;
    while (connection_count < connection_max)
    {
        int sd;
        struct sockaddr_in addr;

        if ((sd = socket(AF_INET, SOCK_DGRAM, 0)) < 0)
        {
            perror("socket");
            return -1;
        }

        addr.sin_family = AF_INET;
        addr.sin_port = htons(connection_count + 1024);
        addr.sin_addr.s_addr = inet_addr("192.168.11.8");

        
        if (sendto(sd, "I am send process", 17, 0,
                   (struct sockaddr *)&addr, sizeof(addr)) < 0)
        {
            perror("sendto");
            return -1;
        }
	
        printf("%d\n", connection_count);
        connection_count += 1;

    }
}
