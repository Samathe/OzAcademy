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
        # More theory content for other nodes
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
        # More theory content for other nodes
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
        # More questions for other nodes
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
                "question": "What is the output of the following code? print(len('programming'))",
                "options": ["11", "10", "9", "12"],
                "correct": "11",
                "explanation": "The string 'programming' has 11 characters, so len('programming') returns 11."
            },
            {
                "type": "single_choice",
                "question": "Which symbol is used for comments in Python?",
                "options": ["//", "/* */", "#", "<!--"],
                "correct": "#",
                "explanation": "In Python, the # symbol is used to denote a comment."
            },
            {
                "type": "single_choice",
                "question": "What is the correct way to create a function in Python?",
                "options": [
                    "function myFunc():", 
                    "def myFunc():", 
                    "create myFunc():", 
                    "function: myFunc()"
                ],
                "correct": "def myFunc():",
                "explanation": "In Python, we use the 'def' keyword to define a function."
            },
            {
                "type": "code",
                "question": "Write a Python program that checks if a number is even or odd.",
                "language": "python",
                "test_cases": [
                    {"input": "4", "expected": "Even"},
                    {"input": "7", "expected": "Odd"}
                ],
                "solution": """number = int(input())
if number % 2 == 0:
    print("Even")
else:
    print("Odd")""",
                "explanation": "This program takes a number as input, checks if it's divisible by 2 using the modulo operator (%), and prints 'Even' or 'Odd' accordingly."
            },
            {
                "type": "multiple_choice",
                "question": "Which of these are Python data structures?",
                "options": ["List", "Dictionary", "Tuple", "Engine"],
                "correct": ["List", "Dictionary", "Tuple"],
                "explanation": "Lists, dictionaries, and tuples are built-in data structures in Python. 'Engine' is not a Python data structure."
            }
        ],
        # More questions for other nodes
    }
}

# Define level requirements
LEVELS = {
    "beginner": {"xp_reward": 10, "hearts": 5, "unlock_xp": 0},
    "intermediate": {"xp_reward": 20, "hearts": 4, "unlock_xp": 50},
    "advanced": {"xp_reward": 30, "hearts": 3, "unlock_xp": 150},
    "expert": {"xp_reward": 50, "hearts": 3, "unlock_xp": 300}
}

# Define achievements
ACHIEVEMENTS = [
    {"name": "First Steps", "description": "Complete your first lesson", "xp_threshold": 10, "icon": "🌱"},
    {"name": "Quick Learner", "description": "Earn 50 XP", "xp_threshold": 50, "icon": "⚡"},
    {"name": "Knowledge Seeker", "description": "Earn 150 XP", "xp_threshold": 150, "icon": "📚"},
    {"name": "Master Scholar", "description": "Earn 300 XP", "xp_threshold": 300, "icon": "🎓"},
    {"name": "Perfect Run", "description": "Complete a lesson without losing hearts", "xp_threshold": 0, "icon": "❤️"},
    {"name": "Streak Master", "description": "Maintain a 5-day streak", "xp_threshold": 0, "icon": "🔥"},
    {"name": "Code Ninja", "description": "Complete 3 coding challenges successfully", "xp_threshold": 0, "icon": "👨‍💻"},
    {"name": "Math Wizard", "description": "Solve 5 difficult math problems", "xp_threshold": 0, "icon": "🧙‍♂️"},
    {"name": "All-rounder", "description": "Complete at least one level in each subject", "xp_threshold": 0, "icon": "🌠"}
]

# Helper functions for rendering UI components
def render_character(character_type="owl"):
    """Renders the mascot character"""
    if character_type == "owl":
        st.markdown("""
        <div style="position: fixed; bottom: 10px; right: 10px; width: 100px; height: 100px; text-align: center;">
            <div style="font-size: 70px; animation: bounce 2s infinite;">🦉</div>
        </div>
        """, unsafe_allow_html=True)

def render_progress_bar(value, max_value, text=""):
    """Renders a custom progress bar"""
    percentage = min(100, int((value / max_value) * 100)) if max_value > 0 else 0
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {percentage}%;"></div>