// g++ cpp-linux-tcp-socket-server.cpp -o server
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
// const char* host = "192.168.1.27";
// int port = 59152;
#define SERV_IP "192.168.1.43"   //服務器ip
#define SERV_PORT 4000        //服務器端口

int main()
{
    int sock_fd, new_fd;
    socklen_t addrlen;
    struct sockaddr_in my_addr, client_addr;
    memset(&my_addr, 0, sizeof(my_addr));
    memset(&client_addr, 0, sizeof(client_addr));
    int status;
    // char indata[1024] = {0}, outdata[1024] = {0};
    int on = 1;

    // create a socket
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd == -1) {
        perror("Socket creation error");
        exit(1);
    }

    // for "Address already in use" error message
    if (setsockopt(sock_fd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(int)) == -1) {
        perror("Setsockopt error");
        exit(1);
    }

    // server address
    my_addr.sin_family = AF_INET;
    // my_addr.sin_addr.s_addr = inet_addr(SERV_IP); 
    my_addr.sin_addr.s_addr = inet_addr(SERV_IP);    
    my_addr.sin_port = htons(SERV_PORT);

    if (bind(sock_fd, (sockaddr *)& my_addr, sizeof(my_addr)) == -1) {
        perror("Binding error");
        exit(1);
    }
    printf("server start at: %s:%d\n", inet_ntoa(my_addr.sin_addr), SERV_PORT);

    if (listen(sock_fd, 5) == -1) {
        perror("Listening error");
        exit(1);
    }
    printf("wait for connection...\n");

    addrlen = sizeof(client_addr);

    while (1) {
        printf("wait for connection...\n");
        new_fd = accept(sock_fd, (struct sockaddr *)&client_addr, &addrlen);
        printf("connected by %s:%d\n", inet_ntoa(client_addr.sin_addr),
            ntohs(client_addr.sin_port));

        while (1) {
            char indata[1024] = {0}, outdata[1024] = {0};
            int nbytes = recv(new_fd, indata, sizeof(indata), 0);
            if (nbytes <= 0) {
                close(new_fd);
                printf("client closed connection.\n");
                break;
            }
            printf("recv: %s\n", indata);
            std::cout<<"Before sprint:"<<indata<<"  "<<outdata<<std::endl;
            // sprintf(outdata, "echo %s", indata);
            std::cout<<"After sprint:"<<indata<<"  "<<outdata<<std::endl;
            send(new_fd, outdata, strlen(outdata), 0);
            
        }
    }
    close(sock_fd);

    return 0;
}