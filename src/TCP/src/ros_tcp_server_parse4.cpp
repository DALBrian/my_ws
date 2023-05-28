#include <unistd.h>
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <sstream>
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <tcp_ros/arm.h> //customized msg type.
using namespace std;

/**
 * @brief Create a ros node which is a ros publisher public info gets from TCP
 * @details For the scenario that get the KUKA's arm coordinate and publish to ROS. Add rosparam and packet check before publish.
 * @author Small Brian
 * @date 2023/04/21
 **/
class TCPConnect{
public:
    TCPConnect(string ip, int port);
    ~TCPConnect();
    void checkaccept();
    void tcpclose();
    bool tcprecv(vector<double> &msg);
    void tcpsend(tcp_ros::arm& msg);
    bool dataparse(std::string& input, vector<double> &msg);
    
private:
    // const char* host = "192.168.1.102";
    // int port_ = 7000;
    int sock_fd, new_fd;
    socklen_t addrlen;
    struct sockaddr_in my_addr, client_addr;
    int status;
    int on = 1;
    bool updated;
};
TCPConnect::TCPConnect(string ip, int port){
    std::cout<<"TCPConnect to: "<<ip<<":"<<port<<std::endl;
    const char* host = ip.c_str();
    // const char* host = "127.0.0.1";
    int port_ = port;
    my_addr.sin_family = AF_INET;
    inet_aton(host, &my_addr.sin_addr);
    my_addr.sin_port = htons(port_);
    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    cout<<"Line 1"<<endl;
    if (sock_fd == -1){
        perror("Socket creat error");
        exit(1);
    }
    cout<<"Line 2"<<endl;
    if (setsockopt(sock_fd, SOL_SOCKET, SO_REUSEADDR, &on,  sizeof(int)) == -1){
        perror("Setsockopt error");
        exit(1);
    }
    cout<<"Line 3"<<endl;
    status = bind(sock_fd, (struct sockaddr *)&my_addr, sizeof(my_addr));
    if (status == -1){
        perror("Binding error");
        exit(1);
    }
    cout<<"Line 4"<<endl;
    status = listen(sock_fd, 5);
    if (status == -1) {
        perror("Listening error");
        exit(1);
    }

}
TCPConnect::~TCPConnect(){
    ROS_INFO("TCP server closing TCP connection");
    close(sock_fd);
}
void TCPConnect::checkaccept(){
    cout<<"Check connection status"<<endl;
    printf("Waiting for connection \n");
    addrlen = sizeof(client_addr);
        new_fd = accept(sock_fd, (struct sockaddr *)&client_addr, &addrlen);
        printf("Connection established by %s:%d\n", inet_ntoa(client_addr.sin_addr),
            ntohs(client_addr.sin_port));   
}
bool TCPConnect::tcprecv(vector<double> &msg){
    char indata[1024] = {0}, outdata[1024] = {"Message received"};
    stringstream input;
    int nbytes = recv(new_fd, indata, sizeof(indata), 0); // receive data from tcp client(KUKA arm)
        if (nbytes <= 0){ // if received data length < 0, it must be abnormal
            close(new_fd);
            printf("Client closed.\n");
            checkaccept();
            return false;
        }else{
            send(new_fd, outdata, strlen(outdata), 0); // send message back to client; optional
            // printf("recv: %s\n", indata);
            input << indata;
            std::string input_ = input.str();
            size_t check = input_.find("joint", 0); //if received data doesn't contain "joint", it may not from arm
            ROS_WARN("The received msg size: %d", nbytes);
            ROS_WARN("The check: %ld", check);
            if (check != -1){return dataparse(input_, msg);}
        } 
        return false;
}
bool TCPConnect::dataparse(std::string& input, vector<double> &msg){
    cout<<"  message from arm: "<<input<<endl;
    bool check_sum1, check_sum2;
    std::string j1 = "<joint1>"; //start mark
    std::string j11 = "</joint1>"; // end mark
    std::string a1, a2, a3, a4, a5, a6;
    size_t p1, p2, p3, p4, p5, p6;
    size_t p11, p22, p33, p44, p55, p66;
    size_t l1 = j1.length();
    p1 = input.find("<joint1>", 0); p11 = input.find("</joint1>", 0);
    p2 = input.find("<joint2>", 0); p22 = input.find("</joint2>", 0);
    p3 = input.find("<joint3>", 0); p33 = input.find("</joint3>", 0);
    p4 = input.find("<joint4>", 0); p44 = input.find("</joint4>", 0);
    p5 = input.find("<joint5>", 0); p55 = input.find("</joint5>", 0);
    p6 = input.find("<joint6>", 0); p66 = input.find("</joint6>", 0);
    if (p1 != -1 && p66 != -1){
        a1 = input.substr(p1 + l1, p11 - p1 - l1);
        a2 = input.substr(p2 + l1, p22 - p2 - l1);
        a3 = input.substr(p3 + l1, p33 - p3 - l1);
        a4 = input.substr(p4 + l1, p44 - p4 - l1);
        a5 = input.substr(p5 + l1, p55 - p5 - l1);
        a6 = input.substr(p6 + l1, p66 - p6 - l1);
        cout<<"a1: "<<a1<<"a2: "<<a2<<"a3: "<<a3<<"a4: "<<a4<<"a5: "<<a5<<"a6: "<<a6<<endl;
        msg.push_back(std::stof(a1)); msg.push_back(std::stof(a2)); msg.push_back(std::stof(a3)); 
        msg.push_back(std::stof(a4)); msg.push_back(std::stof(a5)); msg.push_back(std::stof(a6));
        check_sum1 = true;
    }else{check_sum1 = false;}
    
    size_t px, py, pz, pa, pb, pc;
    size_t pxx, pyy, pzz, paa, pbb, pcc;
    size_t lpx, lpxx;
    std::string x, y, z, a, b, c;
    std::string PX = "<PX>"; lpx = PX.length();

    px = input.find("<PX>", 0); pxx = input.find("</PX>", 0);
    py = input.find("<PY>", 0); pyy = input.find("</PY>", 0);
    pz = input.find("<PZ>", 0); pzz = input.find("</PZ>", 0);
    pa = input.find("<PA>", 0); paa = input.find("</PA>", 0);
    pb = input.find("<PB>", 0); pbb = input.find("</PB>", 0);
    pc = input.find("<PC>", 0); pcc = input.find("</PC>", 0);
    if(px != -1 && pcc != -1){
        x = input.substr(px + lpx, pxx - px - lpx);
        y = input.substr(py + lpx, pyy - py - lpx);
        z = input.substr(pz + lpx, pzz - pz - lpx);
        a = input.substr(pa + lpx, paa - pa - lpx);
        b = input.substr(pb + lpx, pbb - pb - lpx);
        c = input.substr(pc + lpx, pcc - pc - lpx);
        cout<<"x: "<<x<<"y: "<<y<<"z: "<<z<<"a: "<<a<<"b: "<<b<<"c: "<<c<<endl;
        msg.push_back(std::stof(x)); msg.push_back(std::stof(y)); msg.push_back(std::stof(z)); 
        msg.push_back(std::stof(a)); msg.push_back(std::stof(b)); msg.push_back(std::stof(c)); 
        check_sum2 = true;
    }else{check_sum2 = false;}
    if(check_sum1 && check_sum2){
        return true;
    }else{return false;}
}

void TCPConnect::tcpsend(tcp_ros::arm& msg){
    std:string SX, SY, SZ, SA, SB, SC, output;
    std::stringstream sendmsg;
    SX = std::to_string(msg.x); SY = std::to_string(msg.y); SZ = std::to_string(msg.z);
    SA = std::to_string(msg.a); SB = std::to_string(msg.b); SC = std::to_string(msg.c);
    output = "<Sensor><Status><IsOut>FALSE</IsOut></Status><StepMode>0</StepMode><SX>" + SX + "</SX><SY>" + SY
        + "</SY><SZ>" + SZ + "</SZ><SA>" + SA + "</SA><SB>" + SB + "</SB><SC>" + SC + "</SC></Sensor>";
    char sendmsg_[output.length() + 1];
    strcpy(sendmsg_, output.c_str());
    send(new_fd, sendmsg_, strlen(sendmsg_), 0);
}

int main(int argc, char **argv){
    ros::init(argc, argv, "ros_tcp_server");
    ROS_INFO("This is ros_tcp_server");
    ros::NodeHandle nh_;
    ros::Publisher command_pub = nh_.advertise<tcp_ros::arm>("arm_command", 1000);
    ros::Rate loop_rate(0.5);

    std::string arm_ip, my_ip;
    int arm_port;
    nh_.param("arm_ip", arm_ip, std::string("192.168.1.27"));
    nh_.param("my_ip", my_ip, std::string("192.168.1.43"));
    nh_.param("arm_port", arm_port, int(7000));
    std::cout<<"arm_IP: "<<arm_ip<<std::endl;
    std::cout<<"my_ip: "<<my_ip<<std::endl;
    std::cout<<"arm_port: "<<arm_port<<std::endl;

    TCPConnect tcp(my_ip, arm_port);
    tcp.checkaccept();
    vector<double> msg;
    size_t index = 0;
    tcp_ros::arm arm_coord;
    while (ros::ok()){
        cout<<"Line1"<<", Index of while: "<<index <<endl; index += 1;
        tcp_ros::arm arm_coord;
        cout<<"Line2"<<endl;
        if (tcp.tcprecv(msg)){
            cout<<"Line3"<<endl;
            arm_coord.a1 = msg[0]; arm_coord.a2 = msg[1]; arm_coord.a3 = msg[2]; 
            arm_coord.a4 = msg[3]; arm_coord.a5 = msg[4]; arm_coord.a6 = msg[5]; 
            arm_coord.x = msg[6]; arm_coord.y = msg[7]; arm_coord.z = msg[8]; 
            arm_coord.a = msg[9]; arm_coord.b = msg[10]; arm_coord.c = msg[11]; 
            cout<<"Line4"<<endl;
            command_pub.publish(arm_coord);
        }
        cout<<"Line5"<<endl;
        // ros::spin();
        ros::spinOnce();
        loop_rate.sleep();
    }
    return 0;
}