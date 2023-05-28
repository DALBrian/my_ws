#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>
/*
    @author: small brian
    @date: 2023/05/18
    @brief: read pre-build csv path file, prior test.
*/
using std::cout; using std::cerr;
using std::endl; using std::string;
using std::ifstream; using std::ostringstream;
using std::istringstream;

string readFileIntoString(const string& path) {
    auto ss = ostringstream{};
    ifstream input_file(path);
    if (!input_file.is_open()) {
        cerr << "Could not open the file - '"
             << path << "'" << endl;
        exit(EXIT_FAILURE);
    }
    ss << input_file.rdbuf();
    return ss.str();
}

int main()
{
    string filename("/home/dal/my_ws/src/path.csv");
    string file_contents;
    std::map<int, std::vector<string>> csv_contents;
    char delimiter = ',';

    file_contents = readFileIntoString(filename);

    istringstream sstream(file_contents);
    std::vector<string> items;
    string record;

    int counter = 0;
    while (std::getline(sstream, record)) {
        istringstream line(record);
        if (counter == 0){
            std::string label = "time";
        }else if(counter == 1){
            std::string label = "x1";
        }else if(counter == 2){
            std::string label = "x2";
        }
        while (std::getline(line, record, delimiter)) {
            // cout<<"Record: "<<record.c_str()<<endl;
            items.push_back(record);
        }
        csv_contents[counter] = items;
        items.clear();
        cout<<"Counter: "<<counter <<endl;
        counter += 1;
    }
    cout<<"Map size: "<<csv_contents.size()<<endl;
    // cout<<"Map content: "<<csv_contents.first<<endl;
    // for (const auto& element : csv_contents){
    //     cout<<"Element: " << element[1] <<endl;
    // }
    
    std::vector<std::string> result = csv_contents[0];
    cout<<"Result vector element: "<<endl;
    for (const auto& ele : result){
        cout<<ele.c_str()<<endl;
    }
    exit(EXIT_SUCCESS);
}
