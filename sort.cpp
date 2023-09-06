#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> arr{5, 4, 3, 2, 1};

    // Sort the array
    sort(arr.begin(), arr.end());

    // Print the sorted array
    for (int num : arr) {
        cout << num << " ";
    }
    cout << endl;

    return 0;
}
