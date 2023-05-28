#include <iostream>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>
#include <errno.h>
#include <sys/socket.h>
#define SERV_PORT 4000        //服務器端口
#define SERV_IP "192.168.1.43"   //服務器ip
using namespace std;

int main(int argc,char** argv)
{
    int servfd,clitfd;   //創建兩個文件描述符，servfd爲監聽套接字，clitfd用於數據傳輸
	struct sockaddr_in serv_addr,clit_addr; //創建地址結構體，分別用來存放服務端和客戶端的地址信息
	memset(&serv_addr,0,sizeof(serv_addr));  //初始化
	memset(&clit_addr,0,sizeof(clit_addr));  //初始化

	if((servfd = socket(AF_INET,SOCK_STREAM,0)) == -1)  //創建套接字
	{
		cout<<"creat socket failed : "<<strerror(errno)<<endl;//如果出錯則打印錯誤
		return 0;
	} 
        //給服務端的地址結構體賦值
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(SERV_PORT); //將主機上的小端字節序轉換爲網絡傳輸的大端字節序（如果主機本身就是大端字節序就不用轉換了）
	serv_addr.sin_addr.s_addr = inet_addr(SERV_IP); //將字符串形式的ip地址轉換爲點分十進制格式的ip地址
	// serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	// serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
        //綁定地址信息到監聽套接字上，第二個參數強轉是因爲形參類型爲sockaddr ，而實參類型是sockaddr_in 型的
	if(bind(servfd,(sockaddr *)& serv_addr,sizeof(serv_addr)) == -1)
	{
		cout<<"bind failed for follow reason : "<<strerror(errno)<<endl;
		return 0;
	}
        
        //將servfd套接字置爲監聽狀態
	if(listen(servfd,1024) == -1)
	{
		cout<<"listen failed : "<<strerror(errno)<<endl;
		return 0;
	}
    else{
    cout<<"Init Success ! "<<endl;
	cout<<"ip : "<<inet_ntoa(serv_addr.sin_addr)<<"  port : "<<ntohs(serv_addr.sin_port)<<endl;
	cout<<"Waiting for connecting ... "<<endl;
    }
	socklen_t clit_size = 0; //用於accept函數中保存客戶端的地址結構體大小

        //accept成功後，clitfd則指向了這條服務端與客戶端成功連接的”通路“
	if((clitfd = accept(servfd,(sockaddr *)& clit_addr,&clit_size)) == -1)
	{
		cout<<"accept failed : "<<strerror(errno)<<endl;
		return 0;
	}else{
        cout<<"Client access : "<<inet_ntoa(clit_addr.sin_addr)<<"  "<<ntohs(clit_addr.sin_port)<<endl;
    }       
    
   
	while (true) {
        //arm move to ready-to-shot location
        char const* str2 = "MOVP 0 331 171 90 0 180\0";
        cout<<"sending: "<<str2<<endl;
        send(clitfd, str2, strlen(str2) + sizeof(char), 0);
    
	}
	return 0;
    
}