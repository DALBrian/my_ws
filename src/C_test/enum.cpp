#include <stdio.h>
#include <iostream>
#include <string>
using namespace std;

enum arm{
    joint1,
    joint2
};
enum NormalizeStatus {
		Forward,
		Backward
};

int main(){
    string s = "joint1 = 12345, joint2 = 223456", s2 = "sayhihi";
    int loc1 = s.find(joint2, 0);
    int loc2 = s.find("joint2", 0);
    // cout<<loc1<<endl;
    // cout<<loc2<<endl;
    // cout<<Backward<<endl;

    NormalizeStatus A;
    cout<<"A: "<<A<<endl;
    NormalizeStatus B = Forward;
    cout<<"B: "<<B<<endl;
    return 0;
}