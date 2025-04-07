Question = dict()

Question["2"] = """
'Floating point compare text'
Problem description:
This program tests the special floating point compare script accompanying CMS.
The problem input consists of first a line with a single integer, then that many lines,
with on each line a floating point number (possibly also ± inf or nan). For each floating
point number, a line should be written containing the reciprocal of the number, within
10−6 precision.
Sample input/output:
Sample input and output for this problem:
Input
8
+0
1.0
2E0
3
4.0000000000000
5.0000000000001
Inf
nan
Output
inf
1.0
0.50000000001
3.333333333E-1
0.25
2E-1
0
NaN
"""

Question["1"] = """
Problem description:
You are to write the most basic program; it should just output Hello world!” on a single line, no matter what the input.

Sample input/output:
 Input
 1
 Output
 Hello world!
"""

Question["3"] = """
‘Boolean switch search’
Problem description:
We have a very long array of boolean values, where the first value is known to be true and the last
value false. You are tasked with finding the position in the array where a true value is immediately
followed by false.
The input format is as follows:
The first line contains a single integer representing the number of test cases.
For each test case, a number n (2 ≤ n ≤ 10^9) is provided, representing the length of the zero-indexed
array.
The input will then proceed interactively based on your program's output. When your program outputs
a single line in the format READ x, where x is an integer between 0 and n − 1, the system will return
either true or false, indicating the value at position x in the array.
Once you find a position where a true value is immediately followed by false, your program should
output a line in the format OUTPUT x, where x is the index of that position. The system will then
move to the next test case.
Sample input/output:
The input box contains the input, but additionally, after the array length, there is a line containing all
values of the array, with booleans represented by 0 and 1. The input (and output) after that is a sample
interactive session.
Input
1
5
1 1010
false
true
Output
READ 2
READ 1
OUTPUT 1
"""