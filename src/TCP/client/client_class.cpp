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
    void tcpsend();
private:
    const char* host = "192.168.1.27";
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

    status = connect(sock_fd, (struct sockaddr *)&serv_name, sizeof(serv_name));
    if (status == -1) {
        perror("Connection error");
        exit(1);
    }
}
void TCPConnect::tcpsend(){
    printf("Input message: ");
    std::cin>>outdata;
    printf("send: %s \n", outdata);
    send(sock_fd, outdata, strlen(outdata), 0);

    int nbytes = recv(sock_fd, indata, sizeof(indata), 0);
    if (nbytes <= 0){
        close(sock_fd);
        printf("server connection close \n");
    }
    printf("recv: %s\n", indata);

}

int main(int argc, char **argv){
    printf("This is main code \n");
    TCPConnect tcp;
    tcp.tcpsend();

    return 0;
}