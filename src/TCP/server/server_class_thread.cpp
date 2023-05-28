#include <unistd.h>
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <thread>

using namespace std;
class TCPConnect{
public:
    TCPConnect();
    void tcprecv();
    void checkaccept();
    void tcpsend();
    void start();
private:
    const char* host = "172.31.1.11";
    int port = 59152;
    
    int sock_fd, new_fd;
    socklen_t addrlen;
    struct sockaddr_in my_addr, client_addr;
    int status;
    // char indata[1024] = {0}, outdata[1024] = {0};
    int on = 1;
    bool connected;
    char indata[1024] = {0}, outdata[1024]={};
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
    cout<<"Checking connection status"<<endl;
        printf("Waiting for connection \n");
        addrlen = sizeof(client_addr);
        new_fd = accept(sock_fd, (struct sockaddr *)&client_addr, &addrlen);
        printf("Connection established by %s:%d\n", inet_ntoa(client_addr.sin_addr),
            ntohs(client_addr.sin_port));   
}
void TCPConnect::tcprecv(){
    addrlen = sizeof(client_addr);
    while (1) {
        printf("Waiting for connection \n");
        new_fd = accept(sock_fd, (struct sockaddr *)&client_addr, &addrlen);
        printf("Connected by %s:%d\n", inet_ntoa(client_addr.sin_addr),
            ntohs(client_addr.sin_port));
        
        while (1) {
           
            int nbytes = recv(new_fd, indata, sizeof(indata), 0);
            if (nbytes <= 0){
                close(new_fd);
                printf("client closed.\n");
                break;
            }
            printf("recv: %s\n", indata);

        }
    }
    close(sock_fd);

}
void TCPConnect::tcpsend(){
    while(1){
    printf("Type message you wanna send: ");
    std::cin>>outdata;
    printf("send: %s \n", outdata);
    send(sock_fd, outdata, strlen(outdata), 0);
    }
}

void TCPConnect::start(){
    std::cout<<"Starting function initialied"<<std::endl;
    std::thread t1(&TCPConnect::tcpsend, this);
    std::thread t2(&TCPConnect::tcprecv, this);
    t1.join();
    t2.join();
}

int main(int argc, char **argv){
    printf("This is main \n");
    TCPConnect tcp;
    tcp.start();
    return 0;
}