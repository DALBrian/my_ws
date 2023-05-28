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
    void tcpsend();
    void tcprecv();
    void start();
private:
    const char* host = "192.168.1.44";
    int port = 59152;
    
    int sock_fd, new_fd;
    socklen_t addrlen;
    struct sockaddr_in my_addr, serv_name;
    int status;
    char indata[1024] = {0}, outdata[1024] = {0};
    int on = 1;
    bool updated;
};
TCPConnect::TCPConnect(){
    //TCP
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd == -1) {
        perror("Socket creation error");
        exit(1);
    }

    // server address
    serv_name.sin_family = AF_INET;
    inet_aton(host, &serv_name.sin_addr);
    serv_name.sin_port = htons(port);
    std::cout<<"Connecting to server at "<<host<<":"<<port<<std::endl;
    status = connect(sock_fd, (struct sockaddr *)&serv_name, sizeof(serv_name));
    if (status == -1) {
        perror("Connection error");
        exit(1);
    }
}
void TCPConnect::tcpsend(){
    while(1){
    printf("Type message you wanna send: ");
    std::cin>>outdata;
    printf("send: %s \n", outdata);
    send(sock_fd, outdata, strlen(outdata), 0);
    }
}

void TCPConnect::tcprecv(){
    while(1){
    std::cout<<"Waiting for message from server"<<std::endl;
    int nbytes = recv(sock_fd, indata, sizeof(indata), 0);
    if (nbytes <= 0){
        close(sock_fd);
        printf("server connection close \n");
    }else{
    printf("Receiving message from server: %s\n", indata);
    }
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
    printf("This is main function \n");
    TCPConnect tcp;
    tcp.start();
    return 0;
}