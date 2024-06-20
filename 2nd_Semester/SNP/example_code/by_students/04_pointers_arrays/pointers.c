#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
	/*
	* ----------------------------------------------------------------------------
	* Pointer
	* ----------------------------------------------------------------------------
	 */
	//Arrays are essentially just a pointer pointing to the first element.
	//Most Arrays terminate with a null character '\0' also known as null
	int arr[] = {1, 2, 3, 4, 5};
	int* p = arr; // p points to the first element of arr
	
	//you can do addition and subtraction with pointers you cannot multiply or divide
	p = p + 3; // p now points to the fourth element of arr
	
	//if you want retrieve the value stored at a possition you can use the dereference operator * 
	int x = *p; // x is now 4 if you see * without a datatype it is the dereference operator
	//int* p means p is a pointer to an integer *p means the value at the address p points to
	
	// & is the address of operator
	int y = 3;
	int* addr = &x; // addr is a pointer to x
	
	/*
	* ----------------------------------------------------------------------------
	* Arrays
	* ----------------------------------------------------------------------------
	 */
	//Intializing arrays is done as follows:
	int arr2[5]; // arr2 is an array of 5 integers
	//You can initialize arrays with values as follows:
	int arr3[5] = {1, 2, 3, 4, 5}; // arr3 is an array of 5 integers with the values 1, 2, 3, 4, 5
	
	//accessing elements of an array is done as follows:
	arr2[0] = 7; // the first element of arr2 is now 7
	x = arr3[2]; // x is now 3
	//technically you can also access the same value with
	x = 2[arr3]; //because under the hood c adds 2 to the pointer arr3 and then dereferences it and addition is commutative
	
	//Strings are essentially just arrays of characters so everything that applies to arrays also applies to strings
	
	/*
	* ----------------------------------------------------------------------------
	* Multidimensional Arrays
	* ----------------------------------------------------------------------------
	*/
	int arr4[2][3]; // arr4 is a 2x3 matrix
	//You can initialize multidimensional arrays as follows:
	int arr5[2][3] = {{1, 2, 3}, {4, 5, 6}}; // arr5 is a 2x3 matrix with the values 1, 2, 3, 4, 5, 6
	// Accessing elements of a multidimensional array is done as follows:
	x = arr5[1][2]; // x is now 6
	return EXIT_SUCCESS;
}
