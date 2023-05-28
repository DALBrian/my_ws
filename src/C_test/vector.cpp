#include <iostream>
#include <string.h>
#include <stdio.h>
#include <vector>

using namespace std;
void test(vector<double> &number){
    number.push_back(10);
    number.push_back(20);
}



int main(){
   vector<double> v1, v2;
   v1.push_back(10);
//    cout<<"v1: "<<v1[0]<<endl;
    test(v2);
    for (auto& v : v2){
        cout<<"V: "<<v;
    }
    cout<<"v2"<<v2[0]<<" "<<v2[1]<<endl;
    cout<<endl;
    return 0;
}
