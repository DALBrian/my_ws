#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>
using namespace std;
/*
    @author: small brian
    @date: 2023/05/18
    @brief: read pre-build amr&arm csv path file, prior test.
*/
class Readcsv{
public:
    Readcsv();
    string readFileIntoString(const string& path);
    std::map<int, std::vector<string>> process();
};
Readcsv::Readcsv(){
    // process();
}
string Readcsv::readFileIntoString(const string& path){
    auto ss = ostringstream{};
    ifstream input_file(path);
    if (!input_file.is_open()) {
        cerr << "Could not open the file - '"<< path << "'" << endl;
        exit(EXIT_FAILURE);
    }
    ss << input_file.rdbuf();
    return ss.str();
}
std::map<int, std::vector<string>> Readcsv::process(){
    string filename = "/home/dal/my_ws/src/path.csv";
    string file_contents = readFileIntoString(filename);
    istringstream sstream(file_contents);
    std::vector<string> items;
    char delimiter =',';
    string record;
    int counter = 0;
    std::map<int, std::vector<string>> csv_contents;
    while (std::getline(sstream, record)){
        istringstream line(record);
        while (std::getline(line, record, delimiter)) {
            // cout<<"Record: "<<record.c_str()<<endl;
            items.push_back(record);
        }
        csv_contents[counter] = items;
        items.clear();
        cout<<"Counter: "<<counter <<endl;
        counter++;
    }
    std::vector<std::string> result = csv_contents[0];
    cout<<"Result vector element: "<<endl;
    // cout<<"Size: "<<result.size()<<endl; //for debug
    // for (const auto& ele : result){
    //     cout<<ele.c_str()<<endl;
    // }
    return csv_contents;
}

int main(int argc, char** argv){
    Readcsv readcsv;
    std::map<int, std::vector<string>> result;
    result = readcsv.process();
    vector<std::string> result_ = result[0];
    for (const auto& ele : result_){
        cout<<ele.c_str()<<endl;
    }
    return 0;
}