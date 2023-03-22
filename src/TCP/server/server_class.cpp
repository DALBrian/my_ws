#include <unistd.h>
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

using namespace std;
class TCPConnect{
public:
    TCPConnect();
    void tcprecv();
    void checkaccept();
private:
    const char* host = "0.0.0.0";
    int port = 7000;
    
    int sock_fd, new_fd;
    socklen_t addrlen;
    struct sockaddr_in my_addr, client_addr;
    int status;
    // char indata[1024] = {0}, outdata[1024] = {0};
    int on = 1;
    bool connected;
};

TCPConnect::TCPConnect(){

    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd == -1){
        perror("socket creat error");
        exit(1);
    }

    if (setsockopt(sock_fd, SOL_SOCKET, SO_REUSEADDR, &on,  sizeof(int)) == -1){
        perror("setsockopt error");
        exit(1);
    }
    my_addr.sin_family = AF_INET;
    inet_aton(host, &my_addr.sin_addr);
    my_addr.sin_port = htons(port);

    status = bind(sock_fd, (struct sockaddr *)&my_addr, sizeof(my_addr));
    if (status == -1){
        perror("Binding error");
        exit(1);
    }
    status = listen(sock_fd, 5);
    if (status == -1) {
        perror("Listening error");
        exit(1);
    }
    
}
void TCPConnect::checkaccept(){
// new_fd = accept(sock_fd, (struct sockaddr *)&client_addr, &addrlen);
//         printf("connected by %s:%d\n", inet_ntoa(client_addr.sin_addr),
//             ntohs(client_addr.sin_port));
    cout<<"Testing function"<<endl;
}
void TCPConnect::tcprecv(){
    // printf("waiting for connection \n");
    addrlen = sizeof(client_addr);
    while (1) {
        printf("Waiting for connection \n");
        new_fd = accept(sock_fd, (struct sockaddr *)&client_addr, &addrlen);
        printf("Connected by %s:%d\n", inet_ntoa(client_addr.sin_addr),
            ntohs(client_addr.sin_port));
        
        while (1) {
            char indata[1024] = {0}, outdata[1024] = {"Message Received"};
            int nbytes = recv(new_fd, indata, sizeof(indata), 0);
            if (nbytes <= 0){
                close(new_fd);
                printf("client closed.\n");
                break;
            }
            printf("recv: %s\n", indata);
            // sprintf(outdata, "echo %s", indata);
            send(new_fd, outdata, strlen(outdata), 0);
        }
    }
    close(sock_fd);

}

int main(int argc, char **argv){
    printf("This is main \n");
    TCPConnect tcp;
    tcp.tcprecv();

    return 0;
}