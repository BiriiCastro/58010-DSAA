#include <iostream>
#include <numeric>
using namespace std;

//Adding of values inside the array
int arraySum(int arr[], int arr_lenght){
    int initial_sum = 0;
    return accumulate(arr, arr + arr_lenght, initial_sum);
}

int main() {
    int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int arr_lenght = sizeof(arr) / sizeof(int);
    int sum = 0;

    //prints the values inside the array
    for(int i = 0; i < arr_lenght; i++) {
        cout<<"Index:"<<i<<" = "<<arr[i]<<endl;
    }
    //prints the sum of the values in the array
    cout<<"Sum of Array: "<<arraySum(arr, arr_lenght);
    
    return 0;
}