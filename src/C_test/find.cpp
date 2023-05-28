#include <iostream>
#include <string>
using namespace std;
int main(){
    string s1 = "hello world";
    int loc = s1.find("world", 0);
    cout<<loc<<endl;
    cout<<"s1[6] = "<<s1[6]<<endl;
    cout<<"Length of string: "<<s1.length()<<endl;
    cout<<"Substring: "<<s1.substr(6,5)<<endl;
    return 0;
}