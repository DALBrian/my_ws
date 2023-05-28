// g++ cpp-linux-tcp-socket-client.cpp -o client
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
using namespace std;
const char* host = "192.168.1.44";
int port = 59152;

int main()
{
    int sock_fd;
    struct sockaddr_in serv_name;
    int status;
    char indata[1024] = {0}, outdata[1024] = {0};

    // create a socket
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd == -1) {
        perror("Socket creation error");
        exit(1);
    }

    // server address
    serv_name.sin_family = AF_INET;
    inet_aton(host, &serv_name.sin_addr);
    // serv_name.sin_addr.s_addr = (inet_addr("192.168.1.27")); 
    serv_name.sin_port = htons(port);

    status = connect(sock_fd, (struct sockaddr *)&serv_name, sizeof(serv_name));
    if (status == -1) {
        perror("Connection error");
        exit(1);
    }
    int index = 0;
    while (1) {
        cout<<"Iteration time: "<<index<<endl;index ++;
        printf("Please input message: ");
        std::cin>>outdata;
        printf("Sending: %s\n", outdata);
        send(sock_fd, outdata, strlen(outdata), 0);
        cout<<"Waiting for message from server."<<endl;
        int nbytes = recv(sock_fd, indata, sizeof(indata), 0);
        cout<<"input size: "<<nbytes<<endl;
        if (nbytes <= 0) {
            close(sock_fd);
            printf("Server closed connection.\n");
            break;
        }
        printf("recv: %s\n", indata);
    }

    return 0;
}