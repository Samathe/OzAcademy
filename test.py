import streamlit as st
import pandas as pd
import random
import time
import json
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import hashlib
import re

# Set page configuration
st.set_page_config(
    page_title="OZ Academy - Gamified Learning Platform",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling the app
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #111b2b;
    }
    
    /* Text colors for better visibility */
    p, li, label, div {
        color: #ffffff !important;
        font-size: 16px !important;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #58cc02;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 20px;
        border: none;
        box-shadow: 0 4px 0 #46a302;
        width: 100%;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #61dd00;
        box-shadow: 0 2px 0 #46a302;
        transform: translateY(2px);
    }
    
    /* Special buttons */
    .special-button button {
        background-color: #a560ff;
        box-shadow: 0 4px 0 #8548cc;
    }
    .special-button button:hover {
        background-color: #b57aff;
        box-shadow: 0 2px 0 #8548cc;
    }
    
    /* Code editor style */
    .code-editor {
        background-color: #1e1e1e;
        border-radius: 8px;
        border: 1px solid #333;
        padding: 10px;
        font-family: monospace;
    }
    
    /* Answer feedback styling */
    .correct-answer {
        background-color: #d7ffb8;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #58cc02;
        color: #142800 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        animation: glow 2s ease-in-out infinite alternate;
    }
    .incorrect-answer {
        background-color: #ffcfcf;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        color: #580000 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Node styling */
    .node-container {
        position: relative;
        margin: 20px auto;
        text-align: center;
        min-height: 400px;
    }
    .learning-node {
        display: inline-block;
        width: 70px; 
        height: 70px;
        border-radius: 50%;
        background-color: #4b4b4b;
        margin: 10px;
        position: relative;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .learning-node:hover {
        transform: scale(1.1);
    }
    .learning-node.active {
        background-color: #58cc02;
        box-shadow: 0 0 15px #58cc02;
        animation: pulse 2s infinite;
    }
    .learning-node.completed {
        background-color: #58cc02;
    }
    .learning-node.locked {
        background-color: #4b4b4b;
        cursor: not-allowed;
    }
    .special-node {
        background-color: #a560ff;
    }
    .special-node.active {
        background-color: #a560ff;
        box-shadow: 0 0 15px #a560ff;
    }
    .special-node.completed {
        background-color: #a560ff;
    }
    .node-icon {
        font-size: 24px;
        line-height: 70px;
        color: white;
    }
    .node-connector {
        position: absolute;
        background-color: #4b4b4b;
        z-index: -1;
    }
    .node-connector.completed {
        background-color: #58cc02;
    }
    
    /* Character styling */
    .character {
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 100px;
        height: 100px;
        animation: bounce 2s infinite;
    }
    
    /* Progress bar styling */
    .progress-container {
        height: 30px;
        background-color: #e5e5e5;
        border-radius: 15px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #58cc02 0%, #76d639 100%);
        border-radius: 15px;
        transition: width 0.5s ease-in-out;
    }
    .progress-text {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 30px;
        line-height: 30px;
        text-align: center;
        color: white;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    /* Achievement styling */
    .achievement {
        background-color: #ffd900;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        color: #594c00 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    .achievement:hover {
        transform: translateY(-5px);
    }
    
    /* Hearts styling */
    .hearts-container {
        margin: 10px 0;
        font-size: 24px;
    }
    
    /* Animations */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(88, 204, 2, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(88, 204, 2, 0); }
        100% { box-shadow: 0 0 0 0 rgba(88, 204, 2, 0); }
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    @keyframes glow {
        from { box-shadow: 0 0 5px #58cc02; }
        to { box-shadow: 0 0 20px #58cc02; }
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #2b3d5b;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #58cc02;
    }
    
    /* Card styling for welcome screen */
    .welcome-card {
        background-color: #ffffff10;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        text-align: center;
        margin: 0 auto;
        max-width: 500px;
    }
    
    /* Theory section styling */
    .theory-section {
        background-color: #2b3d5b;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Match items styling */
    .match-item {
        background-color: #2b3d5b;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .match-item:hover {
        background-color: #3e5379;
    }
    .match-item.selected {
        background-color: #58cc02;
    }
    
    /* Fix for dark text in Streamlit components */
    .stTextInput label, .stSelectbox label {
        color: white !important;
    }
    .stTextInput input, .stSelectbox select {
        color: white !important;
        background-color: #2b3d5b !important;
        border-color: #3e4c66 !important;
    }
</style>
""", unsafe_allow_html=True)

# Sample data structures
# In a real app, you would store this in a database
SUBJECTS = ["Mathematics", "Computer Science"]

# Node connections define the learning path - 10 levels for each subject
NODE_CONNECTIONS = {
    "Mathematics": [
        {"id": "node1", "position": (150, 100), "type": "normal", "icon": "📐", "connects_to": ["node2"], "level": "beginner", "name": "Basic Arithmetic"},
        {"id": "node2", "position": (100, 180), "type": "normal", "icon": "➕", "connects_to": ["node3"], "level": "beginner", "name": "Algebra Basics"},
        {"id": "node3", "position": (200, 260), "type": "normal", "icon": "✖️", "connects_to": ["node4"], "level": "beginner", "name": "Equations"},
        {"id": "node4", "position": (150, 340), "type": "special", "icon": "🏆", "connects_to": ["node5"], "level": "intermediate", "name": "Functions"},
        {"id": "node5", "position": (75, 420), "type": "normal", "icon": "📊", "connects_to": ["node6"], "level": "intermediate", "name": "Statistics"},
        {"id": "node6", "position": (225, 500), "type": "normal", "icon": "📏", "connects_to": ["node7"], "level": "intermediate", "name": "Geometry"},
        {"id": "node7", "position": (150, 580), "type": "special", "icon": "🎯", "connects_to": ["node8"], "level": "advanced", "name": "Trigonometry"},
        {"id": "node8", "position": (100, 660), "type": "normal", "icon": "📈", "connects_to": ["node9"], "level": "advanced", "name": "Calculus"},
        {"id": "node9", "position": (200, 740), "type": "normal", "icon": "🔢", "connects_to": ["node10"], "level": "expert", "name": "Linear Algebra"},
        {"id": "node10", "position": (150, 820), "type": "special", "icon": "🌟", "connects_to": [], "level": "expert", "name": "Advanced Math"}
    ],
    "Computer Science": [
        {"id": "node1", "position": (150, 100), "type": "normal", "icon": "💻", "connects_to": ["node2"], "level": "beginner", "name": "Intro to Programming"},
        {"id": "node2", "position": (100, 180), "type": "normal", "icon": "🔄", "connects_to": ["node3"], "level": "beginner", "name": "Loops & Conditionals"},
        {"id": "node3", "position": (200, 260), "type": "normal", "icon": "📦", "connects_to": ["node4"], "level": "beginner", "name": "Data Types"},
        {"id": "node4", "position": (150, 340), "type": "special", "icon": "🏆", "connects_to": ["node5"], "level": "intermediate", "name": "Functions & Methods"},
        {"id": "node5", "position": (75, 420), "type": "normal", "icon": "🔍", "connects_to": ["node6"], "level": "intermediate", "name": "Data Structures"},
        {"id": "node6", "position": (225, 500), "type": "normal", "icon": "🔄", "connects_to": ["node7"], "level": "intermediate", "name": "Algorithms"},
        {"id": "node7", "position": (150, 580), "type": "special", "icon": "🎯", "connects_to": ["node8"], "level": "advanced", "name": "OOP Concepts"},
        {"id": "node8", "position": (100, 660), "type": "normal", "icon": "🌐", "connects_to": ["node9"], "level": "advanced", "name": "Web Development"},
        {"id": "node9", "position": (200, 740), "type": "normal", "icon": "🗄️", "connects_to": ["node10"], "level": "expert", "name": "Databases & SQL"},
        {"id": "node10", "position": (150, 820), "type": "special", "icon": "🌟", "connects_to": [], "level": "expert", "name": "Advanced CS Concepts"}
    ]
}

# Theory content for each node
THEORY_CONTENT = {
    "Mathematics": {
        "node1": """
# Basic Arithmetic

Arithmetic is the branch of mathematics dealing with properties of numbers. The basic operations include:

- **Addition (+)**: Combining two numbers to get their sum.
- **Subtraction (-)**: Finding the difference between two numbers.
- **Multiplication (×)**: Adding a number to itself a certain number of times.
- **Division (÷)**: The process of splitting into equal parts.

## Key Concepts:
- Order of operations (BODMAS/PEMDAS)
- Properties of numbers (commutative, associative, distributive)
- Fractions and decimals
        """,
        "node2": """
# Algebra Basics

Algebra introduces variables (letters) to represent unknown numbers. This allows us to:

- Express relationships between quantities
- Write formulas and equations
- Solve for unknown values

## Key Concepts:
- Variables and constants
- Expressions and equations
- Simplifying algebraic expressions
- Solving linear equations
        """,
        "node3": """
# Equations

Equations are mathematical statements that express equality between two expressions. Learning to solve equations is a fundamental skill in mathematics.

## Key Concepts:
- Linear equations (ax + b = c)
- Quadratic equations (ax² + bx + c = 0)
- Systems of equations
- Word problems and applications
        """,
        "node4": """
# Functions

A function is a relation between inputs and outputs where each input is related to exactly one output.

## Key Concepts:
- Function notation f(x)
- Domain and range
- Graphing functions
- Common functions (linear, quadratic, exponential)
        """,
        "node5": """
# Statistics

Statistics is the study of collecting, analyzing, interpreting, and presenting data.

## Key Concepts:
- Measures of central tendency (mean, median, mode)
- Measures of dispersion (range, variance, standard deviation)
- Probability distributions
- Data visualization
        """,
        "node6": """
# Geometry

Geometry is the study of shapes, sizes, properties of space, and the relationships between them.

## Key Concepts:
- Points, lines, angles, and planes
- Polygons and circles
- Area and perimeter
- Volume and surface area
        """,
        "node7": """
# Trigonometry

Trigonometry is the study of relationships between angles and sides of triangles.

## Key Concepts:
- Trigonometric ratios (sine, cosine, tangent)
- The unit circle
- Trigonometric identities
- Applications in physics and engineering
        """,
        "node8": """
# Calculus

Calculus is the mathematical study of continuous change.

## Key Concepts:
- Limits and continuity
- Derivatives (rates of change)
- Integrals (accumulation)
- Fundamental theorem of calculus
        """,
        "node9": """
# Linear Algebra

Linear algebra is the study of linear equations, vector spaces, and matrices.

## Key Concepts:
- Vectors and operations
- Matrices and determinants
- Linear transformations
- Eigenvalues and eigenvectors
        """,
        "node10": """
# Advanced Math

This section covers advanced mathematical concepts that combine knowledge from all previous sections.

## Key Concepts:
- Differential equations
- Complex analysis
- Abstract algebra
- Number theory
        """
    },
    "Computer Science": {
        "node1": """
# Introduction to Programming

Programming is the process of creating instructions for computers to follow. These instructions, called code, tell the computer what tasks to perform.

## Key Concepts:
- What is a program?
- Programming languages (Python, JavaScript, etc.)
- Basic syntax and structure
- Writing your first program

## Hello World in Python:
```python
print("Hello, World!")
```
        """,
        "node2": """
# Loops & Conditionals

Loops and conditionals are control structures that allow us to:
- Make decisions in our code (conditionals)
- Repeat actions (loops)

## Conditional Statements:
```python
if condition:
    # code to execute if condition is True
elif another_condition:
    # code to execute if another_condition is True
else:
    # code to execute if all conditions are False
```

## Loops:
```python
# For loop
for item in sequence:
    # code to repeat for each item

# While loop
while condition:
    # code to repeat while condition is True
```
        """,
        "node3": """
# Data Types

Data types define the kinds of values a variable can hold and the operations that can be performed on them.

## Common Data Types:
- Integers: Whole numbers (e.g., 5, -3, 0)
- Floating-point: Decimal numbers (e.g., 3.14, -0.5)
- Strings: Text (e.g., "Hello", 'World')
- Booleans: True or False values
- Lists/Arrays: Collections of items
- Dictionaries/Objects: Key-value pairs
        """,
        "node4": """
# Functions & Methods

Functions are reusable blocks of code that perform specific tasks. Methods are functions attached to objects.

## Function Structure:
```python
def function_name(parameters):
    # Function body
    # Code to execute
    return result  # Optional
```

## Key Concepts:
- Parameters and arguments
- Return values
- Scope
- Lambda functions
        """,
        "node5": """
# Data Structures

Data structures are specialized formats for organizing, storing, and manipulating data.

## Common Data Structures:
- Arrays/Lists
- Linked Lists
- Stacks (LIFO)
- Queues (FIFO)
- Trees
- Graphs
- Hash Tables/Dictionaries
        """,
        "node6": """
# Algorithms

Algorithms are step-by-step procedures for solving problems or accomplishing tasks.

## Key Concepts:
- Sorting algorithms (bubble, selection, merge, quick)
- Searching algorithms (linear, binary)
- Recursion
- Big O notation
- Greedy algorithms
- Dynamic programming
        """,
        "node7": """
# OOP Concepts

Object-Oriented Programming (OOP) is a programming paradigm based on the concept of "objects".

## Key Concepts:
- Classes and objects
- Inheritance
- Encapsulation
- Polymorphism
- Abstraction
- Composition vs. inheritance
        """,
        "node8": """
# Web Development

Web development involves creating websites and web applications.

## Key Concepts:
- Frontend (HTML, CSS, JavaScript)
- Backend (servers, APIs, databases)
- HTTP protocol
- DOM manipulation
- Responsive design
- Web frameworks
        """,
        "node9": """
# Databases & SQL

Databases store and organize data for easy access and manipulation. SQL (Structured Query Language) is used to interact with relational databases.

## Key Concepts:
- Database design
- Normalization
- SQL queries (SELECT, INSERT, UPDATE, DELETE)
- Joins
- Indexes
- Transactions
        """,
        "node10": """
# Advanced CS Concepts

This section covers advanced computer science concepts that combine knowledge from all previous sections.

## Key Concepts:
- Machine learning
- Artificial intelligence
- System architecture
- Design patterns
- Cybersecurity
- Distributed systems
        """
    }
}

# Initial knowledge test questions
INITIAL_TEST_QUESTIONS = {
    "Mathematics": [
        {
            "question": "Solve: 15 + 7 × 3",
            "options": ["66", "36", "22", "336"],
            "correct": "36",
            "explanation": "Using order of operations (BODMAS/PEMDAS), we multiply first: 7 × 3 = 21, then add: 15 + 21 = 36."
        },
        {
            "question": "Solve for x: 2x - 5 = 11",
            "options": ["x = 8", "x = 3", "x = 7", "x = 9"],
            "correct": "x = 8",
            "explanation": "2x - 5 = 11\n2x = 16\nx = 8"
        },
        {
            "question": "Find the derivative of f(x) = x²",
            "options": ["f'(x) = 2x", "f'(x) = x²", "f'(x) = 2", "f'(x) = x"],
            "correct": "f'(x) = 2x",
            "explanation": "The derivative of x^n is n × x^(n-1). For x², this gives us 2 × x^1 = 2x."
        },
        {
            "question": "Evaluate: sin(30°)",
            "options": ["0.5", "1", "0", "√3/2"],
            "correct": "0.5",
            "explanation": "sin(30°) = 1/2 = 0.5"
        },
        {
            "question": "What is the area of a circle with radius 4 units?",
            "options": ["16π square units", "8π square units", "4π square units", "64π square units"],
            "correct": "16π square units",
            "explanation": "Area of a circle = πr². With r = 4, we get π × 4² = 16π square units."
        }
    ],
    "Computer Science": [
        {
            "question": "What will the following Python code print? x = 5; x += 3; print(x)",
            "options": ["5", "3", "8", "Error"],
            "correct": "8",
            "explanation": "x is initially 5, then we add 3 to it with the += operator, making it 8, which is then printed."
        },
        {
            "question": "Which data structure operates on a LIFO (Last In, First Out) principle?",
            "options": ["Queue", "Stack", "Array", "Linked List"],
            "correct": "Stack",
            "explanation": "A stack follows LIFO - the last element added is the first one to be removed, like a stack of plates."
        },
        {
            "question": "What does SQL stand for?",
            "options": ["Structured Query Language", "Simple Query Language", "Standard Question Language", "System Quality Language"],
            "correct": "Structured Query Language",
            "explanation": "SQL stands for Structured Query Language, used for managing and manipulating relational databases."
        },
        {
            "question": "Which of these is NOT a programming paradigm?",
            "options": ["Object-Oriented", "Functional", "Procedural", "Alphabetical"],
            "correct": "Alphabetical",
            "explanation": "Alphabetical is not a programming paradigm. Common paradigms include Object-Oriented, Functional, and Procedural."
        },
        {
            "question": "What is the time complexity of binary search?",
            "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
            "correct": "O(log n)",
            "explanation": "Binary search has a time complexity of O(log n) because it eliminates half of the remaining elements in each step."
        }
    ]
}

# Questions for each node - different types of questions
QUESTIONS = {
    "Mathematics": {
        "node1": [
            {
                "type": "single_choice",
                "question": "What is 28 + 15?",
                "options": ["43", "42", "44", "41"],
                "correct": "43",
                "explanation": "Adding 28 and 15 gives us 43."
            },
            {
                "type": "single_choice",
                "question": "Evaluate: 56 - 19",
                "options": ["35", "37", "38", "36"],
                "correct": "37",
                "explanation": "Subtracting 19 from 56 gives us 37."
            },
            {
                "type": "single_choice",
                "question": "Calculate: 8 × 7",
                "options": ["54", "56", "58", "55"],
                "correct": "56",
                "explanation": "Multiplying 8 by 7 gives us 56."
            },
            {
                "type": "single_choice",
                "question": "What is 72 ÷ 9?",
                "options": ["9", "8", "7", "6"],
                "correct": "8",
                "explanation": "Dividing 72 by 9 gives us 8."
            },
            {
                "type": "numerical",
                "question": "If you have 45 apples and give away 17, how many do you have left?",
                "correct": 28,
                "explanation": "45 - 17 = 28 apples"
            },
            {
                "type": "multiple_choice",
                "question": "Which of the following are prime numbers?",
                "options": ["11", "21", "17", "15"],
                "correct": ["11", "17"],
                "explanation": "11 and 17 are prime numbers because they are only divisible by 1 and themselves. 21 is divisible by 3 and 7, and 15 is divisible by 3 and 5."
            },
            {
                "type": "match",
                "question": "Match the operation with its result:",
                "pairs": [
                    {"left": "15 + 8", "right": "23"},
                    {"left": "32 - 17", "right": "15"},
                    {"left": "6 × 9", "right": "54"},
                    {"left": "56 ÷ 8", "right": "7"}
                ],
                "explanation": "These are basic arithmetic calculations."
            },
            {
                "type": "numerical",
                "question": "If a book costs $12 and you buy 5 of them, how much will you pay in total?",
                "correct": 60,
                "explanation": "The total cost is 5 × $12 = $60."
            },
            {
                "type": "graph",
                "question": "What is the sum of 25 + 30?",
                "correct": 55,
                "visualization": "bar",
                "explanation": "Adding 25 and 30 gives us 55."
            },
            {
                "type": "single_choice",
                "question": "What is the result of 144 ÷ 12?",
                "options": ["10", "12", "14", "16"],
                "correct": "12",
                "explanation": "Dividing 144 by 12 gives us 12."
            }
        ],
        # Add questions for other nodes as needed
    },
    "Computer Science": {
        "node1": [
            {
                "type": "single_choice",
                "question": "What will the following code print? print('Hello ' + 'World')",
                "options": ["Hello World", "HelloWorld", "Hello + World", "Error"],
                "correct": "Hello World",
                "explanation": "The + operator concatenates strings, so 'Hello ' and 'World' are joined to form 'Hello World'."
            },
            {
                "type": "code",
                "question": "Write a Python function that returns the square of a number.",
                "language": "python",
                "test_cases": [
                    {"input": "5", "expected": "25"},
                    {"input": "0", "expected": "0"},
                    {"input": "-3", "expected": "9"}
                ],
                "solution": """def square(number):
    return number ** 2""",
                "explanation": "The function takes a number as input and returns its square using the ** operator."
            },
            {
                "type": "multiple_choice",
                "question": "Which of the following are valid variable names in Python?",
                "options": ["variable_1", "1variable", "my-variable", "_private"],
                "correct": ["variable_1", "_private"],
                "explanation": "In Python, variable names can't start with a number (so '1variable' is invalid) and can't contain hyphens (so 'my-variable' is invalid)."
            },
            {
                "type": "match",
                "question": "Match each data type with an example of it:",
                "pairs": [
                    {"left": "Integer", "right": "42"},
                    {"left": "Float", "right": "3.14"},
                    {"left": "String", "right": "'Hello'"},
                    {"left": "Boolean", "right": "True"}
                ],
                "explanation": "These are the basic data types in programming and examples of their literal values."
            },
            {
                "type": "code",
                "question": "Write a Python program that prints numbers from 1 to 5 using a for loop.",
                "language": "python",
                "test_cases": [
                    {"input": "", "expected": "1\n2\n3\n4\n5"}
                ],
                "solution": """for i in range(1, 6):
    print(i)""",
                "explanation": "This code uses a for loop with the range function to iterate from 1 to 5 and prints each number."
            },
            {
                "type": "single_choice",
                "question": "What is the output of the following Python code? x = 10; y = 5; print(x * y)",
                "options": ["50", "15", "5", "10"],
                "correct": "50",
                "explanation": "The code multiplies x (10) by y (5), resulting in 50."
            },
            {
                "type": "numerical",
                "question": "If a program takes 3 seconds to process 1 record, how many records can it process in 2 minutes?",
                "correct": 40,
                "explanation": "In 2 minutes (120 seconds), the program can process 120 ÷ 3 = 40 records."
            },
            {
                "type": "single_choice",
                "question": "What symbol is used for comments in Python?",
                "options": ["//", "#", "/* */", "<!-- -->"],
                "correct": "#",
                "explanation": "In Python, the hash symbol (#) is used to indicate a comment. Everything after # on the same line is ignored by the interpreter."
            },
            {
                "type": "code",
                "question": "Write a Python program that prints 'Even' if a number is even and 'Odd' if it's odd.",
                "language": "python",
                "test_cases": [
                    {"input": "4", "expected": "Even"},
                    {"input": "7", "expected": "Odd"}
                ],
                "solution": """def check_even_odd(number):
    if number % 2 == 0:
        return 'Even'
    else:
        return 'Odd'

number = int(input())
print(check_even_odd(number))""",
                "explanation": "This program uses the modulo operator (%) to check if a number is even or odd. If number % 2 equals 0, the number is even; otherwise, it's odd."
            },
            {
                "type": "match",
                "question": "Match the operator with its function in Python:",
                "pairs": [
                    {"left": "+", "right": "Addition"},
                    {"left": "==", "right": "Equality check"},
                    {"left": "%", "right": "Modulo"},
                    {"left": "**", "right": "Exponentiation"}
                ],
                "explanation": "These are common operators in Python and their respective functions."
            }
        ],
        "node2": [
            {
                "type": "single_choice",
                "question": "What will this code print? for i in range(3): print(i)",
                "options": ["0 1 2", "1 2 3", "0 1 2 3", "Error"],
                "correct": "0 1 2",
                "explanation": "The range(3) function generates numbers from 0 to 2 (not including 3), so the loop prints 0, 1, and 2."
            },
            {
                "type": "code",
                "question": "Write a while loop that prints numbers from 5 down to 1.",
                "language": "python",
                "test_cases": [
                    {"input": "", "expected": "5\n4\n3\n2\n1"}
                ],
                "solution": """num = 5
while num >= 1:
    print(num)
    num -= 1""",
                "explanation": "This while loop starts with num = 5 and decrements it until it reaches 1, printing each value."
            },
            {
                "type": "multiple_choice",
                "question": "Which of these are valid loop structures in Python?",
                "options": ["for loop", "do-while loop", "while loop", "repeat-until loop"],
                "correct": ["for loop", "while loop"],
                "explanation": "Python natively supports for loops and while loops. It does not have built-in do-while or repeat-until loop structures."
            },
            {
                "type": "single_choice",
                "question": "What will this code output? if 5 > 3: print('A'); else: print('B')",
                "options": ["A", "B", "A B", "Error"],
                "correct": "A",
                "explanation": "Since 5 is greater than 3, the condition is True, and the code prints 'A'."
            },
            {
                "type": "code",
                "question": "Write a program that prints all even numbers between 1 and 10 using a loop.",
                "language": "python",
                "test_cases": [
                    {"input": "", "expected": "2\n4\n6\n8\n10"}
                ],
                "solution": """for num in range(1, 11):
    if num % 2 == 0:
        print(num)""",
                "explanation": "This program uses a for loop to iterate through numbers 1 to 10 and prints only the even ones using a conditional check."
            }
        ]
    }
}

# Function to create necessary user data files if they don't exist
def initialize_user_data():
    if not os.path.exists("user_data"):
        os.makedirs("user_data")
    
    if not os.path.exists("user_data/users.json"):
        with open("user_data/users.json", "w") as file:
            json.dump({}, file)
    
    if not os.path.exists("user_data/progress.json"):
        with open("user_data/progress.json", "w") as file:
            json.dump({}, file)

# Function to hash password securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to validate if a username is available
def is_username_available(username):
    with open("user_data/users.json", "r") as file:
        users = json.load(file)
    return username not in users

# Function to register a new user
def register_user(username, password, email):
    with open("user_data/users.json", "r") as file:
        users = json.load(file)
    
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open("user_data/users.json", "w") as file:
        json.dump(users, file)
    
    # Initialize progress for new user
    initialize_user_progress(username)
    
    return True

# Function to verify login credentials
def verify_login(username, password):
    with open("user_data/users.json", "r") as file:
        users = json.load(file)
    
    if username in users and users[username]["password"] == hash_password(password):
        return True
    return False

# Function to initialize progress for a new user
def initialize_user_progress(username):
    with open("user_data/progress.json", "r") as file:
        progress = json.load(file)
    
    progress[username] = {
        "Mathematics": {
            "xp": 0,
            "level": 0,
            "completed_nodes": [],
            "hearts": 5,
            "current_node": "node1",
            "test_taken": False,
            "achievements": []
        },
        "Computer Science": {
            "xp": 0,
            "level": 0,
            "completed_nodes": [],
            "hearts": 5,
            "current_node": "node1",
            "test_taken": False,
            "achievements": []
        }
    }
    
    with open("user_data/progress.json", "w") as file:
        json.dump(progress, file)

# Function to update user progress
def update_user_progress(username, subject, field, value):
    with open("user_data/progress.json", "r") as file:
        progress = json.load(file)
    
    if username in progress:
        if field == "xp":
            progress[username][subject]["xp"] += value
            # Check for level up
            if progress[username][subject]["xp"] >= (progress[username][subject]["level"] + 1) * 100:
                progress[username][subject]["level"] += 1
                # Add achievement for level up
                achievement = f"Reached level {progress[username][subject]['level']} in {subject}!"
                if achievement not in progress[username][subject]["achievements"]:
                    progress[username][subject]["achievements"].append(achievement)
        elif field == "completed_nodes":
            if value not in progress[username][subject]["completed_nodes"]:
                progress[username][subject]["completed_nodes"].append(value)
                # Add achievement for completing a node
                node_info = next((node for node in NODE_CONNECTIONS[subject] if node["id"] == value), None)
                if node_info:
                    achievement = f"Completed {node_info['name']} in {subject}!"
                    if achievement not in progress[username][subject]["achievements"]:
                        progress[username][subject]["achievements"].append(achievement)
        elif field == "hearts":
            progress[username][subject]["hearts"] = value
        elif field == "current_node":
            progress[username][subject]["current_node"] = value
        elif field == "test_taken":
            progress[username][subject]["test_taken"] = value
        elif field == "achievements":
            if value not in progress[username][subject]["achievements"]:
                progress[username][subject]["achievements"].append(value)
        
        with open("user_data/progress.json", "w") as file:
            json.dump(progress, file)
        
        return True
    return False

# Function to get user progress
def get_user_progress(username):
    with open("user_data/progress.json", "r") as file:
        progress = json.load(file)
    
    if username in progress:
        return progress[username]
    return None

# Function to get questions for a node
def get_node_questions(subject, node_id, num_questions=10):
    if subject in QUESTIONS and node_id in QUESTIONS[subject]:
        # Get all questions for this node
        all_questions = QUESTIONS[subject][node_id]
        
        # Randomly select questions up to the requested number
        if len(all_questions) <= num_questions:
            return all_questions
        else:
            return random.sample(all_questions, num_questions)
    
    return []

# Function to check if a node is unlocked for a user
def is_node_unlocked(username, subject, node_id):
    progress = get_user_progress(username)
    
    if not progress:
        return False
    
    subject_progress = progress[subject]
    
    # First node is always unlocked
    if node_id == "node1":
        return True
    
    # Get the connecting nodes
    connecting_nodes = []
    for node in NODE_CONNECTIONS[subject]:
        if node_id in node["connects_to"]:
            connecting_nodes.append(node["id"])
    
    # Check if any connecting node is completed
    for connecting_node in connecting_nodes:
        if connecting_node in subject_progress["completed_nodes"]:
            return True
    
    return False

# Function to render learning node map
def render_learning_map(username, subject):
    progress = get_user_progress(username)
    
    if not progress:
        return
    
    subject_progress = progress[subject]
    completed_nodes = subject_progress["completed_nodes"]
    current_node = subject_progress["current_node"]
    
    st.markdown("## Learning Map")
    st.markdown(f"Subject: **{subject}**")
    
    # Create progress bar
    total_nodes = len(NODE_CONNECTIONS[subject])
    completed_count = len(completed_nodes)
    
    st.markdown(f"### Progress: {completed_count}/{total_nodes} nodes completed")
    
    progress_percentage = (completed_count / total_nodes) * 100
    st.markdown(
        f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress_percentage}%;"></div>
            <div class="progress-text">{int(progress_percentage)}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # XP and Level
    st.markdown(f"**Level:** {subject_progress['level']} | **XP:** {subject_progress['xp']}/{(subject_progress['level'] + 1) * 100}")
    
    # Hearts
    st.markdown(
        f"""
        <div class="hearts-container">
            {"❤️" * subject_progress["hearts"]}{"🖤" * (5 - subject_progress["hearts"])}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create a container for the learning map
    st.markdown(
        """
        <div class="node-container" id="learning-map">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Generate node HTML
    node_html = ""
    connector_html = ""
    
    for node in NODE_CONNECTIONS[subject]:
        node_id = node["id"]
        node_type = node["type"]
        pos_x, pos_y = node["position"]
        icon = node["icon"]
        name = node["name"]
        
        # Determine node status
        node_class = "learning-node"
        if node_type == "special":
            node_class += " special-node"
            
        if node_id in completed_nodes:
            node_class += " completed"
        elif node_id == current_node:
            node_class += " active"
        elif not is_node_unlocked(username, subject, node_id):
            node_class += " locked"
        
        # Add node to HTML
        node_html += f"""
        <div 
            class="{node_class}" 
            style="left: {pos_x}px; top: {pos_y}px;"
            onclick="window.location.href='?page=node&subject={subject}&node={node_id}'"
            title="{name}"
        >
            <div class="node-icon">{icon}</div>
        </div>
        """
        
        # Add connectors to HTML
        for connected_node_id in node["connects_to"]:
            # Find the connected node
            connected_node = next((n for n in NODE_CONNECTIONS[subject] if n["id"] == connected_node_id), None)
            
            if connected_node:
                # Calculate connector position and dimensions
                conn_x1, conn_y1 = pos_x + 35, pos_y + 35  # Center of current node
                conn_x2, conn_y2 = connected_node["position"][0] + 35, connected_node["position"][1] + 35  # Center of connected node
                
                # Calculate angle
                angle = np.arctan2(conn_y2 - conn_y1, conn_x2 - conn_x1) * 180 / np.pi
                
                # Calculate length
                length = np.sqrt((conn_x2 - conn_x1)**2 + (conn_y2 - conn_y1)**2)
                
                # Calculate position
                connector_left = min(conn_x1, conn_x2) + abs(conn_x2 - conn_x1) / 2 - length / 2
                connector_top = min(conn_y1, conn_y2) + abs(conn_y2 - conn_y1) / 2 - 2  # 2px height
                
                # Determine connector status
                conn_class = "node-connector"
                if node_id in completed_nodes:
                    conn_class += " completed"
                
                # Add connector to HTML
                connector_html += f"""
                <div 
                    class="{conn_class}" 
                    style="
                        left: {connector_left}px; 
                        top: {connector_top}px;
                        width: {length}px;
                        height: 4px;
                        transform: rotate({angle}deg);
                        transform-origin: center;
                    "
                ></div>
                """
    
    # Combine connectors and nodes
    map_html = connector_html + node_html
    
    # Inject the HTML into the container
    st.markdown(
        f"""
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                document.getElementById('learning-map').innerHTML = `{map_html}`;
            }});
        </script>
        """,
        unsafe_allow_html=True
    )

# Main application
def main():
    # Initialize user data on first run
    initialize_user_data()
    
    # Session state setup
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    if "current_subject" not in st.session_state:
        st.session_state.current_subject = None
    if "current_node" not in st.session_state:
        st.session_state.current_node = None
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "feedback" not in st.session_state:
        st.session_state.feedback = None
    if "show_explanation" not in st.session_state:
        st.session_state.show_explanation = False
        
    # Get query parameters
    query_params = st.experimental_get_query_params()
    
    # Check if there are page parameters
    if "page" in query_params:
        st.session_state.current_page = query_params["page"][0]
    if "subject" in query_params:
        st.session_state.current_subject = query_params["subject"][0]
    if "node" in query_params:
        st.session_state.current_node = query_params["node"][0]
    
    # Sidebar for navigation once logged in
    if st.session_state.logged_in:
        with st.sidebar:
            st.title("OZ Academy")
            st.markdown(f"Welcome, **{st.session_state.username}**!")
            
            # Profile button
            if st.button("My Profile"):
                st.session_state.current_page = "profile"
                st.experimental_set_query_params(page="profile")
                st.rerun()
            
            # Subject selection
            if st.button("Select Subject"):
                st.session_state.current_page = "subjects"
                st.experimental_set_query_params(page="subjects")
                st.rerun()
            
            # Logout button
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.current_page = "login"
                st.experimental_set_query_params()
                st.rerun()
    
    # Page router
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.current_page == "subjects":
            subjects_page()
        elif st.session_state.current_page == "test":
            test_page()
        elif st.session_state.current_page == "map":
            map_page()
        elif st.session_state.current_page == "node":
            node_page()
        elif st.session_state.current_page == "theory":
            theory_page()
        elif st.session_state.current_page == "quiz":
            quiz_page()
        elif st.session_state.current_page == "profile":
            profile_page()
        else:
            subjects_page()  # Default to subjects page if page is unknown

# Login/Registration page
def login_page():
    st.title("OZ Academy")
    
    # Welcome container with animation
    st.markdown(
        """
        <div class="welcome-card">
            <h2>🧠 Welcome to OZ Academy</h2>
            <p>A gamified learning platform for Mathematics and Computer Science</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Login/Register tabs
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.header("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_button"):
            if username and password:
                if verify_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.current_page = "subjects"
                    st.experimental_set_query_params(page="subjects")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")
    
    with tab2:
        st.header("Register")
        new_username = st.text_input("Choose a Username", key="reg_username")
        new_password = st.text_input("Choose a Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        email = st.text_input("Email Address", key="reg_email")
        
        if st.button("Register", key="register_button"):
            if new_username and new_password and confirm_password and email:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif not is_username_available(new_username):
                    st.error("Username already taken")
                elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error("Invalid email address")
                else:
                    if register_user(new_username, new_password, email):
                        st.success("Registration successful! You can now login.")
                        st.session_state.current_page = "login"
                        st.rerun()
                    else:
                        st.error("Registration failed. Please try again.")
            else:
                st.warning("Please fill in all fields")

# Subjects selection page
def subjects_page():
    st.title("Select a Subject")
    
    # Create a container for subject cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div style="background-color: #2b3d5b; border-radius: 15px; padding: 20px; text-align: center; height: 250px;">
                <h2>📐 Mathematics</h2>
                <p>Learn various mathematical concepts from basic arithmetic to advanced calculus.</p>
                <br>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Select Mathematics", key="math_button"):
            # Check if the user has taken the initial test
            progress = get_user_progress(st.session_state.username)
            if progress and not progress["Mathematics"]["test_taken"]:
                st.session_state.current_subject = "Mathematics"
                st.session_state.current_page = "test"
                st.experimental_set_query_params(page="test", subject="Mathematics")
                st.rerun()
            else:
                st.session_state.current_subject = "Mathematics"
                st.session_state.current_page = "map"
                st.experimental_set_query_params(page="map", subject="Mathematics")
                st.rerun()
    
    with col2:
        st.markdown(
            """
            <div style="background-color: #2b3d5b; border-radius: 15px; padding: 20px; text-align: center; height: 250px;">
                <h2>💻 Computer Science</h2>
                <p>Explore programming, algorithms, data structures, and more.</p>
                <br>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Select Computer Science", key="cs_button"):
            # Check if the user has taken the initial test
            progress = get_user_progress(st.session_state.username)
            if progress and not progress["Computer Science"]["test_taken"]:
                st.session_state.current_subject = "Computer Science"
                st.session_state.current_page = "test"
                st.experimental_set_query_params(page="test", subject="Computer Science")
                st.rerun()
            else:
                st.session_state.current_subject = "Computer Science"
                st.session_state.current_page = "map"
                st.experimental_set_query_params(page="map", subject="Computer Science")
                st.rerun()

# Initial knowledge test page
def test_page():
    subject = st.session_state.current_subject
    
    st.title(f"Knowledge Test: {subject}")
    st.markdown("Let's test your current knowledge level to personalize your learning path.")
    
    # Initialize test questions if not already done
    if "test_questions" not in st.session_state or st.session_state.current_subject != st.session_state.get("test_subject"):
        st.session_state.test_questions = INITIAL_TEST_QUESTIONS[subject]
        st.session_state.test_subject = subject
        st.session_state.test_question_idx = 0
        st.session_state.test_score = 0
        st.session_state.test_answers = []
    
    # Display current question
    if st.session_state.test_question_idx < len(st.session_state.test_questions):
        current_q = st.session_state.test_questions[st.session_state.test_question_idx]
        
        st.markdown(f"### Question {st.session_state.test_question_idx + 1} of {len(st.session_state.test_questions)}")
        st.markdown(f"**{current_q['question']}**")
        
        # Create radio buttons for options
        answer = st.radio("Select your answer:", current_q["options"], key=f"test_q_{st.session_state.test_question_idx}")
        
        # Navigation buttons
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Next", key="test_next"):
                # Record the answer
                st.session_state.test_answers.append(answer)
                
                # Check if the answer is correct
                if answer == current_q["correct"]:
                    st.session_state.test_score += 1
                
                # Move to next question
                st.session_state.test_question_idx += 1
                st.rerun()
    else:
        # Test completed - show results and set up learning path
        st.markdown("## Test Complete!")
        
        score_percentage = (st.session_state.test_score / len(st.session_state.test_questions)) * 100
        st.markdown(f"Your score: **{st.session_state.test_score}/{len(st.session_state.test_questions)}** ({score_percentage:.1f}%)")
        
        # Determine the starting level based on the score
        starting_level = 0
        if score_percentage >= 80:
            starting_level = 2  # Advanced
            st.markdown("Great job! You have advanced knowledge in this subject.")
        elif score_percentage >= 40:
            starting_level = 1  # Intermediate
            st.markdown("You have a good foundation in this subject.")
        else:
            starting_level = 0  # Beginner
            st.markdown("Let's start with the basics to build a strong foundation.")
        
        # Set initial XP based on test score
        initial_xp = int(score_percentage)
        
        # Update user progress
        update_user_progress(st.session_state.username, subject, "xp", initial_xp)
        update_user_progress(st.session_state.username, subject, "level", starting_level)
        update_user_progress(st.session_state.username, subject, "test_taken", True)
        
        # Show button to continue to the learning map
        if st.button("Start Learning"):
            st.session_state.current_page = "map"
            st.experimental_set_query_params(page="map", subject=subject)
            st.rerun()

# Learning map page
def map_page():
    subject = st.session_state.current_subject
    
    st.title(f"{subject} Learning Map")
    st.markdown("Navigate through the learning nodes to master the subject.")
    
    # Render the interactive learning map
    render_learning_map(st.session_state.username, subject)

# Node page - entry point for each learning node
def node_page():
    subject = st.session_state.current_subject
    node_id = st.session_state.current_node
    
    # Get node details
    node_info = next((node for node in NODE_CONNECTIONS[subject] if node["id"] == node_id), None)
    
    if not node_info:
        st.error("Node not found")
        return
    
    st.title(f"{node_info['name']}")
    st.markdown(f"Level: **{node_info['level'].capitalize()}**")
    
    # Check if node is unlocked
    if not is_node_unlocked(st.session_state.username, subject, node_id):
        st.warning("This node is locked. Complete the previous nodes to unlock it.")
        
        if st.button("Back to Map"):
            st.session_state.current_page = "map"
            st.experimental_set_query_params(page="map", subject=subject)
            st.rerun()
        return
    
    # Create tabs for Theory and Practice
    tab1, tab2 = st.tabs(["Theory", "Practice"])
    
    with tab1:
        # Theory content
        st.markdown("## Theory")
        st.markdown("Review the theoretical concepts before testing your knowledge.")
        
        if st.button("Start Learning", key="start_theory"):
            st.session_state.current_page = "theory"
            st.experimental_set_query_params(page="theory", subject=subject, node=node_id)
            st.rerun()
    
    with tab2:
        # Practice quizzes
        st.markdown("## Practice")
        st.markdown("Test your knowledge with interactive questions.")
        
        if st.button("Start Quiz", key="start_quiz"):
            # Set up quiz questions
            st.session_state.quiz_questions = get_node_questions(subject, node_id)
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.feedback = None
            st.session_state.show_explanation = False
            
            st.session_state.current_page = "quiz"
            st.experimental_set_query_params(page="quiz", subject=subject, node=node_id)
            st.rerun()
    
    # Back to map button
    if st.button("Back to Map"):
        st.session_state.current_page = "map"
        st.experimental_set_query_params(page="map", subject=subject)
        st.rerun()

# Theory page - shows theoretical content for a node
def theory_page():
    subject = st.session_state.current_subject
    node_id = st.session_state.current_node
    
    # Get node details
    # Get node details
    node_info = next((node for node in NODE_CONNECTIONS[subject] if node["id"] == node_id), None)
    
    if not node_info:
        st.error("Node not found")
        return
    
    st.title(f"{node_info['name']} - Theory")
    
    # Display the theory content
    if subject in THEORY_CONTENT and node_id in THEORY_CONTENT[subject]:
        st.markdown(THEORY_CONTENT[subject][node_id], unsafe_allow_html=True)
    else:
        st.warning("Theory content for this node is not available yet.")
    
    # Button to start practicing
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Start Practice"):
            # Set up quiz questions
            st.session_state.quiz_questions = get_node_questions(subject, node_id)
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.feedback = None
            st.session_state.show_explanation = False
            
            st.session_state.current_page = "quiz"
            st.experimental_set_query_params(page="quiz", subject=subject, node=node_id)
            st.rerun()
    
    with col2:
        if st.button("Back to Node"):
            st.session_state.current_page = "node"
            st.experimental_set_query_params(page="node", subject=subject, node=node_id)
            st.rerun()

# Quiz page - interactive quiz for a node
def quiz_page():
    subject = st.session_state.current_subject
    node_id = st.session_state.current_node
    
    # Get node details
    node_info = next((node for node in NODE_CONNECTIONS[subject] if node["id"] == node_id), None)
    
    if not node_info:
        st.error("Node not found")
        return
    
    st.title(f"{node_info['name']} - Practice")
    
    # Check if there are questions
    if not st.session_state.quiz_questions:
        st.warning("No questions available for this node.")
        if st.button("Back to Node"):
            st.session_state.current_page = "node"
            st.experimental_set_query_params(page="node", subject=subject, node=node_id)
            st.rerun()
        return
    
    # Display progress
    progress_percentage = ((st.session_state.current_question) / len(st.session_state.quiz_questions)) * 100
    st.markdown(
        f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress_percentage}%;"></div>
            <div class="progress-text">Question {st.session_state.current_question + 1}/{len(st.session_state.quiz_questions)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display hearts
    progress = get_user_progress(st.session_state.username)
    hearts = progress[subject]["hearts"]
    
    st.markdown(
        f"""
        <div class="hearts-container">
            {"❤️" * hearts}{"🖤" * (5 - hearts)}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Check if quiz completed
    if st.session_state.current_question >= len(st.session_state.quiz_questions):
        quiz_completed()
        return
    
    # Get current question
    current_q = st.session_state.quiz_questions[st.session_state.current_question]
    
    # Display question
    st.markdown(f"### {current_q['question']}")
    
    # Handle different question types
    if current_q['type'] == 'single_choice':
        handle_single_choice_question(current_q)
    elif current_q['type'] == 'multiple_choice':
        handle_multiple_choice_question(current_q)
    elif current_q['type'] == 'numerical':
        handle_numerical_question(current_q)
    elif current_q['type'] == 'match':
        handle_match_question(current_q)
    elif current_q['type'] == 'code':
        handle_code_question(current_q)
    elif current_q['type'] == 'graph':
        handle_graph_question(current_q)
    
    # Display feedback if available
    if st.session_state.feedback:
        st.markdown(f"""
        <div class="{st.session_state.feedback['class']}">
            {st.session_state.feedback['message']}
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.show_explanation and 'explanation' in current_q:
            st.markdown("### Explanation")
            st.markdown(current_q['explanation'])
        
        # Button to continue
        st.button("Continue", on_click=next_question)

# Handler functions for different question types
def handle_single_choice_question(question):
    # If feedback is being shown, don't allow new answers
    if st.session_state.feedback:
        return
    
    # Create a placeholder for the user's selection
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = None
    
    # Create radio buttons for options
    answer = st.radio("Select your answer:", question["options"], key=f"q_{st.session_state.current_question}")
    
    # Check answer button
    if st.button("Check Answer"):
        st.session_state.user_answer = answer
        check_answer(question, answer)

def handle_multiple_choice_question(question):
    # If feedback is being shown, don't allow new answers
    if st.session_state.feedback:
        return
    
    # Create checkboxes for options
    selected_options = []
    for option in question["options"]:
        if st.checkbox(option, key=f"opt_{option}_{st.session_state.current_question}"):
            selected_options.append(option)
    
    # Check answer button
    if st.button("Check Answer"):
        check_answer(question, selected_options)

def handle_numerical_question(question):
    # If feedback is being shown, don't allow new answers
    if st.session_state.feedback:
        return
    
    # Create a number input
    answer = st.number_input("Enter your answer:", key=f"num_{st.session_state.current_question}")
    
    # Check answer button
    if st.button("Check Answer"):
        check_answer(question, answer)

def handle_match_question(question):
    # If feedback is being shown, don't allow new answers
    if st.session_state.feedback:
        return
    
    st.markdown("Match the items by selecting the same number for pairs that go together.")
    
    # Create a dictionary to store the user's matches
    if 'match_selections' not in st.session_state:
        st.session_state.match_selections = {}
    
    # Display all items on the left
    for idx, pair in enumerate(question["pairs"]):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"**{pair['left']}**")
        
        with col2:
            options = list(range(1, len(question["pairs"]) + 1))
            selected = st.selectbox(f"Match {idx+1}", options, key=f"match_left_{idx}")
            st.session_state.match_selections[pair['left']] = selected
    
    # Display all items on the right with their numbers
    st.markdown("### Match with:")
    for idx, pair in enumerate(question["pairs"]):
        st.markdown(f"{idx+1}. **{pair['right']}**")
    
    # Check answer button
    if st.button("Check Answer"):
        # Create user's matches based on selections
        user_matches = []
        correct_matches = []
        
        for idx, pair in enumerate(question["pairs"]):
            selected_idx = st.session_state.match_selections[pair['left']] - 1
            if selected_idx < len(question["pairs"]):
                user_matches.append((pair['left'], question["pairs"][selected_idx]['right']))
            else:
                user_matches.append((pair['left'], ""))
            correct_matches.append((pair['left'], pair['right']))
        
        check_answer(question, user_matches, correct_matches)

def handle_code_question(question):
    # If feedback is being shown, don't allow new answers
    if st.session_state.feedback:
        return
    
    st.markdown(f"Language: **{question['language']}**")
    
    # Create a code editor
    code = st.text_area("Write your code here:", height=300, key=f"code_{st.session_state.current_question}", 
                        help="Write your solution here and click 'Run Code' to test it.")
    
    # Run code button
    if st.button("Run Code"):
        run_and_check_code(question, code)

def handle_graph_question(question):
    # If feedback is being shown, don't allow new answers
    if st.session_state.feedback:
        return
    
    # For graph questions, we'll use a numerical input
    answer = st.number_input("Enter your answer:", key=f"graph_{st.session_state.current_question}")
    
    # If visualization is available
    if 'visualization' in question:
        if question['visualization'] == 'bar':
            # Create sample visualization (this would be customized based on the problem)
            st.markdown("### Visualization")
            
            # Create sample data for the bar chart
            data = {'A': 25, 'B': 30}
            fig, ax = plt.subplots()
            ax.bar(data.keys(), data.values())
            ax.set_ylabel('Value')
            ax.set_title('Sample Visualization')
            
            # Display the chart
            st.pyplot(fig)
    
    # Check answer button
    if st.button("Check Answer"):
        check_answer(question, answer)

# Function to check answers
def check_answer(question, user_answer, correct_answer=None):
    # Get the correct answer
    if correct_answer is None:
        correct_answer = question["correct"]
    
    # Check if the answer is correct
    is_correct = False
    
    if question['type'] == 'single_choice':
        is_correct = user_answer == correct_answer
    elif question['type'] == 'multiple_choice':
        # For multiple choice, check if the selections match exactly
        is_correct = sorted(user_answer) == sorted(correct_answer)
    elif question['type'] == 'numerical' or question['type'] == 'graph':
        # For numerical questions, allow a small tolerance
        is_correct = abs(user_answer - correct_answer) < 0.0001
    elif question['type'] == 'match':
        # For matching, check if all pairs match
        is_correct = sorted(user_answer) == sorted(correct_answer)
    
    # Prepare feedback
    if is_correct:
        st.session_state.feedback = {
            "class": "correct-answer",
            "message": "✅ Correct! Well done."
        }
        st.session_state.score += 1
        # Award XP
        update_user_progress(st.session_state.username, st.session_state.current_subject, "xp", 10)
    else:
        st.session_state.feedback = {
            "class": "incorrect-answer",
            "message": "❌ Incorrect. Try to understand why."
        }
        # Lose a heart
        progress = get_user_progress(st.session_state.username)
        hearts = progress[st.session_state.current_subject]["hearts"]
        if hearts > 0:
            update_user_progress(st.session_state.username, st.session_state.current_subject, "hearts", hearts - 1)
    
    st.session_state.show_explanation = True
    st.rerun()

# Function to run and check code
def run_and_check_code(question, code):
    # In a real application, this would execute the code in a sandbox
    # For demo purposes, we'll just check if it has some expected content
    
    # Check if the code is not empty
    if not code:
        st.session_state.feedback = {
            "class": "incorrect-answer",
            "message": "❌ Please write some code before submitting."
        }
        st.rerun()
        return
    
    # Simple pattern matching (this would be more sophisticated in a real app)
    all_tests_pass = True
    test_results = []
    
    for test_case in question['test_cases']:
        input_val = test_case['input']
        expected = test_case['expected']
        
        # Very basic check (in a real app, this would execute the code with the input)
        if question['language'] == 'python':
            # Check if code contains function call pattern
            if 'def ' in code and 'return' in code:
                # For demonstration purposes, just check if certain keywords are present
                # In a real app, this would actually run the code with test cases
                test_pass = True
            else:
                test_pass = False
        else:
            # For other languages
            test_pass = True  # Simplified for demo
        
        test_results.append({
            "input": input_val,
            "expected": expected,
            "pass": test_pass
        })
        
        if not test_pass:
            all_tests_pass = False
    
    # Prepare feedback based on test results
    if all_tests_pass:
        st.session_state.feedback = {
            "class": "correct-answer",
            "message": "✅ All tests passed! Well done."
        }
        st.session_state.score += 1
        # Award XP
        update_user_progress(st.session_state.username, st.session_state.current_subject, "xp", 15)  # More XP for code
    else:
        st.session_state.feedback = {
            "class": "incorrect-answer",
            "message": "❌ Some tests failed. Check your code and try again."
        }
        # Lose a heart
        progress = get_user_progress(st.session_state.username)
        hearts = progress[st.session_state.current_subject]["hearts"]
        if hearts > 0:
            update_user_progress(st.session_state.username, st.session_state.current_subject, "hearts", hearts - 1)
    
    # Display test results
    st.markdown("### Test Results")
    for idx, test in enumerate(test_results):
        status = "✅ Passed" if test["pass"] else "❌ Failed"
        st.markdown(f"Test {idx+1}: Input: `{test['input']}` | Expected: `{test['expected']}` | **{status}**")
    
    st.session_state.show_explanation = True
    st.rerun()

# Function to move to the next question
def next_question():
    st.session_state.current_question += 1
    st.session_state.feedback = None
    st.session_state.show_explanation = False
    
    # If all questions are answered, check if the node is completed
    if st.session_state.current_question >= len(st.session_state.quiz_questions):
        # Update user progress
        progress = get_user_progress(st.session_state.username)
        hearts = progress[st.session_state.current_subject]["hearts"]
        
        # Check if user has hearts left and score is sufficient
        if hearts > 0 and st.session_state.score >= len(st.session_state.quiz_questions) * 0.7:
            # Mark node as completed if not already
            if st.session_state.current_node not in progress[st.session_state.current_subject]["completed_nodes"]:
                update_user_progress(
                    st.session_state.username, 
                    st.session_state.current_subject, 
                    "completed_nodes", 
                    st.session_state.current_node
                )
                
                # Award bonus XP for completing node
                update_user_progress(st.session_state.username, st.session_state.current_subject, "xp", 50)
                
                # If this is a special node, award an achievement
                node_info = next((node for node in NODE_CONNECTIONS[st.session_state.current_subject] 
                                  if node["id"] == st.session_state.current_node), None)
                if node_info and node_info["type"] == "special":
                    achievement = f"Mastered {node_info['name']}!"
                    update_user_progress(
                        st.session_state.username, 
                        st.session_state.current_subject, 
                        "achievements", 
                        achievement
                    )
            
            # Unlock next node if available
            for node in NODE_CONNECTIONS[st.session_state.current_subject]:
                if st.session_state.current_node in node["connects_to"]:
                    update_user_progress(
                        st.session_state.username, 
                        st.session_state.current_subject, 
                        "current_node", 
                        node["id"]
                    )
                    break

# Function to handle quiz completion
def quiz_completed():
    st.markdown("## Quiz Completed!")
    
    # Calculate score percentage
    score_percentage = (st.session_state.score / len(st.session_state.quiz_questions)) * 100
    
    # Display results
    st.markdown(f"Your score: **{st.session_state.score}/{len(st.session_state.quiz_questions)}** ({score_percentage:.1f}%)")
    
    # Get user progress
    progress = get_user_progress(st.session_state.username)
    hearts = progress[st.session_state.current_subject]["hearts"]
    
    if hearts > 0 and score_percentage >= 70:
        st.markdown(
            """
            <div class="correct-answer">
                Congratulations! You've successfully completed this node.
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Check if a new achievement was earned
        node_info = next((node for node in NODE_CONNECTIONS[st.session_state.current_subject] 
                          if node["id"] == st.session_state.current_node), None)
        if node_info and node_info["type"] == "special":
            st.markdown(
                """
                <div class="achievement">
                    🏆 New Achievement Unlocked: Special node mastered!
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            """
            <div class="incorrect-answer">
                You need to score at least 70% and have hearts remaining to complete this node.
                Try again after reviewing the theory.
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Buttons for navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Try Again"):
            # Reset quiz state
            st.session_state.quiz_questions = get_node_questions(
                st.session_state.current_subject, 
                st.session_state.current_node
            )
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.feedback = None
            st.session_state.show_explanation = False
            st.rerun()
    
    with col2:
        if st.button("Back to Map"):
            st.session_state.current_page = "map"
            st.experimental_set_query_params(
                page="map", 
                subject=st.session_state.current_subject
            )
            st.rerun()

# Profile page - shows user stats and achievements
def profile_page():
    st.title(f"Profile: {st.session_state.username}")
    
    # Get user progress
    progress = get_user_progress(st.session_state.username)
    
    if not progress:
        st.error("User progress not found")
        return
    
    # Create tabs for each subject
    tabs = st.tabs(SUBJECTS)
    
    for idx, subject in enumerate(SUBJECTS):
        with tabs[idx]:
            subject_progress = progress[subject]
            
            # Display XP and level
            st.markdown(f"## {subject} Stats")
            st.markdown(f"**Level:** {subject_progress['level']}")
            st.markdown(f"**XP:** {subject_progress['xp']}/{(subject_progress['level'] + 1) * 100}")
            
            # Display progress
            completed_nodes = len(subject_progress['completed_nodes'])
            total_nodes = len(NODE_CONNECTIONS[subject])
            
            st.markdown(f"**Progress:** {completed_nodes}/{total_nodes} nodes completed")
            
            progress_percentage = (completed_nodes / total_nodes) * 100
            st.markdown(
                f"""
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress_percentage}%;"></div>
                    <div class="progress-text">{int(progress_percentage)}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Display achievements
            st.markdown("## Achievements")
            
            if subject_progress['achievements']:
                for achievement in subject_progress['achievements']:
                    st.markdown(
                        f"""
                        <div class="achievement">
                            🏆 {achievement}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No achievements yet. Keep learning to earn them!")
            
            # Button to go to subject map
            if st.button(f"Go to {subject} Map", key=f"map_{subject}"):
                st.session_state.current_subject = subject
                st.session_state.current_page = "map"
                st.experimental_set_query_params(page="map", subject=subject)
                st.rerun()

# Run the app
if __name__ == "__main__":
    main()