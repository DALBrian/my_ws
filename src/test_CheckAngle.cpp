#include <iostream>
#include <vector>
using namespace std;


void checkAngle(vector<double> &angle){
    /*20230528 built, haven't test yet*/
    vector<int> exceedAxis;
    for (size_t i = 0; i < angle.size(); i++){
        switch (i){
            case 0:
                if (angle[i] < -30){angle[i] = -29; exceedAxis.push_back(i);}
                else if(angle[i] > 185 ){angle[i] = 184; exceedAxis.push_back(i);}
                break;
            case 1:
                if (angle[i] < -116){angle[i] = -115; exceedAxis.push_back(i);}
                else if(angle[i] > 60 ){angle[i] = 59; exceedAxis.push_back(i);}
                break;
            case 2:
                if (angle[i] < 74.55){angle[i] = 73; exceedAxis.push_back(i);}
                else if(angle[i] > 160 ){angle[i] = 159; exceedAxis.push_back(i);}
                break;
            case 3:
                if (angle[i] < -175){angle[i] = -174; exceedAxis.push_back(i);}
                else if(angle[i] > 175 ){angle[i] = 174; exceedAxis.push_back(i);}
                break;
            case 4:
                if (angle[i] < -125){angle[i] = -124; exceedAxis.push_back(i);}
                else if(angle[i] > 125 ){angle[i] = 124; exceedAxis.push_back(i);}
                break;  
            case 5: 
                if (angle[i] < -350){angle[i] = -349; exceedAxis.push_back(i);}
                else if(angle[i] > 350 ){angle[i] = 349; exceedAxis.push_back(i);} 
                break;  
        }
        
    }
    for (size_t i = 0; i < exceedAxis.size(); i++){
        printf("Axis %i exceed limitation, set to limitation value.\n", exceedAxis[i]);
    }
}

/*Write a test function for checkAngle */
int main(){
    vector<double> angle = {-31, -115, 73, -175, -125, -350};
    checkAngle(angle);
    for (size_t i = 0; i < angle.size(); i++){
        cout << angle[i] << endl;
    }
    return 0;
}