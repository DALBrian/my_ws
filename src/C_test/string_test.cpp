#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <stdio.h>
using namespace std;

int main(){
    printf("Section 1\n");
    string name = "brian";
    cout<<"name: "<<name<<endl;
    string name3 = {"say hi hi "};
    cout<<"name3: "<<name3<<endl;
    cout<<"cells: "<<name3[1]<<endl;
    cout<<"length: "<<name3.length()<<endl;

    printf("Section 2\n");
    char A[1024] = {0};
    cout<<"Enter A: ";cin>>A;cout<<A<<endl;
    cout<<"size of A: "<<sizeof(A)<<endl;
    cout<<"length of A: "<<strlen(A)<<endl;

    printf("Section 3\n");
    string name4 = "cat";
    for(auto ch : name4) {
        cout << ch << endl;
    }

    printf("Section 4\n");
    stringstream name5;
    name5 << name4;
    cout<<"stringstream: name5: "<<name5.str()<<endl;



    return 0;
}