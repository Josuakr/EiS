#include <iostream> // io (print to console)

using namespace std; // include all std-lib names

int main() {
    int i=10; // declare variable
    while (i>0) { // while loop (for simplicity)j
        cout << i << "\n"; // print number and "return" 
        if (i == 8) {
            cout << "ignition sequence start\n";
        }
        i = i - 1; 
    }
    cout << "liftoff!\n";
    return 0; // 0 == Programm endet fehlerfrei 
}