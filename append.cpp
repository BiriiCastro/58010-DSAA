#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> arr{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    arr.push_back(11); // Append "11" to the array
    
    for (int num : arr) {
        cout << num << " ";
    }
    
    return 0;
}
