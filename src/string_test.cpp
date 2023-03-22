#include <iostream>
#include <string>
#include <cstring>
using namespace std;

int main(){
    string name = "brian";
    cout<<"name: "<<name<<endl;
    // string name2;
    // printf("Enter your name: ");
    // cin >> name2;
    // cout<<"name2: "<<name2<<endl;
    string name3 = {"say hi hi "};
    cout<<"name3: "<<name3<<endl;
    cout<<"cells: "<<name3[1]<<endl;
    cout<<"length: "<<name3.length()<<endl;


    char A[1024] = {0};
    cout<<"Enter A: ";
    cin>>A;
    cout<<A<<endl;
    cout<<"size of A: "<<sizeof(A)<<endl;
    cout<<"length of A: "<<strlen(A)<<endl;

    string name4 = "caterpillar";

    for(auto ch : name4) {
        cout << ch << endl;
    }
    return 0;
}