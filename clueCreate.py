import ollama
from questions.questions import *

oneShotContent = """
Q: 'Floating point compare text'
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

A: 
def floating_point_compare():
    n = int(input())
    for _ in range(n):
        number = input().strip()
        if number == "Inf":
            print(0)  # Incorrect: should return 'inf'
        elif number == "nan":
            print("NaN")  # Incorrect: should return 'nan'
        else:
            try:
                num = float(number)
                if num == 0:
                    print(0)  # Incorrect: should return 'inf' for +0
                else:
                    reciprocal = 1 / num
                    print(reciprocal)
            except ValueError:
                print("Invalid input")  # This line won't trigger due to input constraints

floating_point_compare()
"""

oneShotClue = "The program incorrectly handles special cases like Inf, nan, and +0."



def clueCreate(sourcecode, problemID):


    prompt = f"""<|system|>
You are a AI Tutor who sees the wrong program written by students and give one line hint. You should never give code but only give the step by step algorithm to solve the question: 
<|user|>
{oneShotContent}
<|assistant|> 
{oneShotClue}
<|user|>
Q: 
{Question[problemID]}
A: 
{sourcecode}
<|assistant|> 
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    clue = response["message"]["content"]

    return clue
