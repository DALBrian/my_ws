#include <iostream>
#include <string.h>
#include <stdio.h>
#include <sstream>
using namespace std;


void test(double number){
    cout<<"Number: "<<number<<endl;
}

int main(){
     int a[10];
    for (int i = 0; i < 10; ++i)
    {
        a[i] = i + 1;
    }
    cout<<"a: "<<a[1]<<endl;

    test(3.14);
    return 0;
}
