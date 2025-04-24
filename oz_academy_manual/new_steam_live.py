import streamlit as st
import pandas as pd
import random
import time
import json
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="ExamLingo - Gamified Exam Prep",
    page_icon="📚",
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
SUBJECTS = ["Mathematics", "Science", "English", "History"]

# Node connections define the learning path
NODE_CONNECTIONS = {
    "Mathematics": [
        {"id": "node1", "position": (150, 100), "type": "normal", "icon": "📐", "connects_to": ["node2", "node3"], "level": "beginner"},
        {"id": "node2", "position": (100, 200), "type": "normal", "icon": "➕", "connects_to": ["node4"], "level": "beginner"},
        {"id": "node3", "position": (200, 200), "type": "normal", "icon": "✖️", "connects_to": ["node4"], "level": "beginner"},
        {"id": "node4", "position": (150, 300), "type": "special", "icon": "🏆", "connects_to": ["node5", "node6"], "level": "beginner"},
        {"id": "node5", "position": (75, 400), "type": "normal", "icon": "📊", "connects_to": ["node7"], "level": "intermediate"},
        {"id": "node6", "position": (225, 400), "type": "normal", "icon": "📏", "connects_to": ["node7"], "level": "intermediate"},
        {"id": "node7", "position": (150, 500), "type": "special", "icon": "🎯", "connects_to": [], "level": "advanced"}
    ],
    "Science": [
        {"id": "node1", "position": (150, 100), "type": "normal", "icon": "🔬", "connects_to": ["node2", "node3"], "level": "beginner"},
        {"id": "node2", "position": (75, 200), "type": "normal", "icon": "🧪", "connects_to": ["node4"], "level": "beginner"},
        {"id": "node3", "position": (225, 200), "type": "normal", "icon": "🌡️", "connects_to": ["node4"], "level": "beginner"},
        {"id": "node4", "position": (150, 300), "type": "special", "icon": "⚗️", "connects_to": [], "level": "intermediate"}
    ],
    "English": [
        {"id": "node1", "position": (150, 100), "type": "normal", "icon": "📝", "connects_to": ["node2"], "level": "beginner"},
        {"id": "node2", "position": (150, 200), "type": "normal", "icon": "📖", "connects_to": ["node3"], "level": "beginner"},
        {"id": "node3", "position": (150, 300), "type": "special", "icon": "🏆", "connects_to": [], "level": "intermediate"}
    ],
    "History": [
        {"id": "node1", "position": (150, 100), "type": "normal", "icon": "🏛️", "connects_to": ["node2", "node3"], "level": "beginner"},
        {"id": "node2", "position": (100, 200), "type": "normal", "icon": "📜", "connects_to": ["node4"], "level": "beginner"},
        {"id": "node3", "position": (200, 200), "type": "normal", "icon": "⚔️", "connects_to": ["node4"], "level": "beginner"},
        {"id": "node4", "position": (150, 300), "type": "special", "icon": "🌍", "connects_to": [], "level": "intermediate"}
    ]
}

QUESTIONS = {
    "Mathematics": {
        "beginner": [
            {
                "question": "What is 5 + 7?",
                "options": ["10", "12", "13", "15"],
                "correct": "12",
                "explanation": "Adding 5 and 7 gives us 12."
            },
            {
                "question": "Solve: 8 × 4",
                "options": ["24", "32", "28", "36"],
                "correct": "32",
                "explanation": "Multiplying 8 by 4 gives us 32."
            },
            {
                "question": "What is 20 ÷ 5?",
                "options": ["4", "5", "3", "2"],
                "correct": "4",
                "explanation": "Dividing 20 by 5 gives us 4."
            }
        ],
        "intermediate": [
            {
                "question": "Solve for x: 3x + 5 = 17",
                "options": ["x = 4", "x = 6", "x = 12", "x = 3"],
                "correct": "x = 4",
                "explanation": "3x + 5 = 17\n3x = 12\nx = 4"
            },
            {
                "question": "What is the area of a rectangle with length 8 cm and width 5 cm?",
                "options": ["13 cm²", "26 cm²", "40 cm²", "30 cm²"],
                "correct": "40 cm²",
                "explanation": "Area = length × width = 8 × 5 = 40 cm²"
            }
        ],
        "advanced": [
            {
                "question": "Find the derivative of f(x) = x³ + 2x² - x + 3",
                "options": ["f'(x) = 3x² + 4x - 1", "f'(x) = 3x² + 2x - 1", "f'(x) = 2x² + 4x - 1", "f'(x) = 3x² + 4x + 1"],
                "correct": "f'(x) = 3x² + 4x - 1",
                "explanation": "Taking the derivative term by term:\nf(x) = x³ + 2x² - x + 3\nf'(x) = 3x² + 4x - 1"
            }
        ]
    },
    "Science": {
        "beginner": [
            {
                "question": "Which of the following is NOT a state of matter?",
                "options": ["Solid", "Liquid", "Gas", "Energy"],
                "correct": "Energy",
                "explanation": "The three common states of matter are solid, liquid, and gas. Energy is a form of power, not a state of matter."
            },
            {
                "question": "What is the chemical symbol for water?",
                "options": ["H₂O", "CO₂", "O₂", "NaCl"],
                "correct": "H₂O",
                "explanation": "Water consists of two hydrogen atoms and one oxygen atom, represented as H₂O."
            }
        ],
        "intermediate": [
            {
                "question": "Which of these is NOT a part of a plant cell?",
                "options": ["Cell wall", "Chloroplast", "Cilium", "Mitochondria"],
                "correct": "Cilium",
                "explanation": "Cilia are found in certain animal cells but not in plant cells."
            }
        ],
        "advanced": [
            {
                "question": "What is the approximate speed of light in a vacuum?",
                "options": ["300,000 km/s", "200,000 km/s", "150,000 km/s", "350,000 km/s"],
                "correct": "300,000 km/s",
                "explanation": "The speed of light in a vacuum is approximately 299,792 kilometers per second, often rounded to 300,000 km/s."
            }
        ]
    },
    "English": {
        "beginner": [
            {
                "question": "Which of the following is a proper noun?",
                "options": ["London", "city", "dog", "beautiful"],
                "correct": "London",
                "explanation": "London is a proper noun because it names a specific city."
            }
        ],
        "intermediate": [
            {
                "question": "Identify the correct sentence:",
                "options": [
                    "She don't like ice cream.",
                    "She doesn't likes ice cream.",
                    "She doesn't like ice cream.",
                    "She not like ice cream."
                ],
                "correct": "She doesn't like ice cream.",
                "explanation": "The correct form of the negative present simple for third person singular is 'doesn't like'."
            }
        ],
        "advanced": [
            {
                "question": "Which literary device is used in: 'The wind whispered through the trees'?",
                "options": ["Personification", "Metaphor", "Simile", "Hyperbole"],
                "correct": "Personification",
                "explanation": "Personification attributes human qualities (in this case, the ability to whisper) to non-human things (the wind)."
            }
        ]
    },
    "History": {
        "beginner": [
            {
                "question": "Who was the first President of the United States?",
                "options": ["Thomas Jefferson", "George Washington", "Abraham Lincoln", "John Adams"],
                "correct": "George Washington",
                "explanation": "George Washington was the first President of the United States, serving from 1789 to 1797."
            }
        ],
        "intermediate": [
            {
                "question": "Which event marked the beginning of World War II in Europe?",
                "options": [
                    "The bombing of Pearl Harbor",
                    "Germany's invasion of Poland",
                    "The Russian Revolution",
                    "The Treaty of Versailles"
                ],
                "correct": "Germany's invasion of Poland",
                "explanation": "World War II in Europe began when Nazi Germany invaded Poland on September 1, 1939."
            }
        ],
        "advanced": [
            {
                "question": "What was the significance of the Magna Carta?",
                "options": [
                    "It ended the Cold War",
                    "It established colonies in America",
                    "It limited the power of the English monarchy",
                    "It created the United Nations"
                ],
                "correct": "It limited the power of the English monarchy",
                "explanation": "Signed in 1215, the Magna Carta was a charter that limited the power of the English monarchy and established that everyone, including the king, was subject to the law."
            }
        ]
    }
}

LEVELS = {
    "beginner": {"xp_reward": 10, "hearts": 3, "unlock_xp": 0},
    "intermediate": {"xp_reward": 20, "hearts": 3, "unlock_xp": 50},
    "advanced": {"xp_reward": 40, "hearts": 3, "unlock_xp": 150}
}

ACHIEVEMENTS = [
    {"name": "First Steps", "description": "Complete your first lesson", "xp_threshold": 10, "icon": "🌱"},
    {"name": "Quick Learner", "description": "Earn 50 XP", "xp_threshold": 50, "icon": "⚡"},
    {"name": "Knowledge Seeker", "description": "Earn 150 XP", "xp_threshold": 150, "icon": "📚"},
    {"name": "Master Scholar", "description": "Earn 300 XP", "xp_threshold": 300, "icon": "🎓"},
    {"name": "Perfect Run", "description": "Complete a lesson without losing hearts", "xp_threshold": 0, "icon": "❤️"},
    {"name": "Streak Master", "description": "Maintain a 5-day streak", "xp_threshold": 0, "icon": "🔥"}
]

# Helper functions for rendering various UI components
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
        <div class="progress-text">{text if text else f"{value}/{max_value}"}</div>
    </div>
    """, unsafe_allow_html=True)

def render_hearts(count):
    """Renders the hearts display"""
    st.markdown(f"""
    <div class="hearts-container">
        {"❤️" * count}{"🖤" * (3 - count)}
    </div>
    """, unsafe_allow_html=True)

def render_learning_path(subject, completed_nodes=None):
    """Renders the non-linear learning path with nodes and connections"""
    if completed_nodes is None:
        completed_nodes = []
    
    # Check if the subject has a defined path
    if subject not in NODE_CONNECTIONS:
        st.warning(f"No learning path defined for {subject}")
        return
    
    nodes = NODE_CONNECTIONS[subject]
    
    # Prepare SVG dimensions based on node positions
    max_x = max([node["position"][0] for node in nodes]) + 100
    max_y = max([node["position"][1] for node in nodes]) + 100
    
    # Start SVG container
    svg = f'<svg width="{max_x}" height="{max_y}" xmlns="http://www.w3.org/2000/svg">'
    
    # Draw connections first (so they are behind nodes)
    for node in nodes:
        from_x, from_y = node["position"]
        node_center_x = from_x + 35
        node_center_y = from_y + 35
        
        # Draw connections to other nodes
        for target_id in node["connects_to"]:
            # Find target node
            target_node = next((n for n in nodes if n["id"] == target_id), None)
            if target_node:
                to_x, to_y = target_node["position"]
                to_center_x = to_x + 35
                to_center_y = to_y + 35
                
                # Determine if this connection is completed
                connection_completed = node["id"] in completed_nodes and target_id in completed_nodes
                connection_color = "#58cc02" if connection_completed else "#4b4b4b"
                
                # Draw the line
                svg += f'<line x1="{node_center_x}" y1="{node_center_y}" x2="{to_center_x}" y2="{to_center_y}" stroke="{connection_color}" stroke-width="8" />'
    
    # Draw nodes
    for node in nodes:
        x, y = node["position"]
        node_id = node["id"]
        node_type = node["type"]
        icon = node["icon"]
        
        # Determine node status
        is_completed = node_id in completed_nodes
        is_active = False
        is_locked = False
        
        # A node is active if all its prerequisites are completed
        # For simplicity, we'll consider the first node always active if not completed
        # and other nodes active if at least one of their incoming connections is from a completed node
        if node_id == "node1" and not is_completed:
            is_active = True
        else:
            # Check if any node that connects to this one is completed
            for other_node in nodes:
                if node_id in other_node["connects_to"] and other_node["id"] in completed_nodes:
                    is_active = True
                    break
        
        # A node is locked if it's not active and not completed
        is_locked = not is_active and not is_completed
        
        # Set node style based on status
        node_class = "completed" if is_completed else "active" if is_active else "locked"
        
        # Set node color based on type
        type_class = "special-node" if node_type == "special" else ""
        
        # Draw the node with its status
      # Modify the SVG node drawing code to ensure valid element creation
        svg += f'''
        <g transform="translate({x}, {y})">
            <circle cx="35" cy="35" r="35" fill="{get_node_color(is_completed, is_active, is_locked, node_type)}" />
            <text x="35" y="45" text-anchor="middle" fill="white" font-size="24">{icon}</text>
        </g>
        '''
    
    # End SVG container
    svg += '</svg>'
    
    # Render the SVG
    st.markdown(f"""
    <div class="node-container">
        {svg}
    </div>
    """, unsafe_allow_html=True)
    
    return nodes

def get_node_color(is_completed, is_active, is_locked, node_type):
    """Returns the appropriate color for a node based on its status"""
    if node_type == "special":
        if is_completed:
            return "#a560ff"
        elif is_active:
            return "#b57aff"
        else:
            return "#4b4b4b"
    else:
        if is_completed:
            return "#58cc02"
        elif is_active:
            return "#76d639"
        else:
            return "#4b4b4b"

# Initialize session state variables
def init_session_state():
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            "username": "",
            "xp": 0,
            "current_subject": "",
            "current_level": "",
            "current_node": "",
            "lessons_completed": 0,
            "achievements": [],
            "streak_days": 1,
            "last_active": None,
            "completed_nodes": {subject: [] for subject in SUBJECTS},
            "subjects_progress": {subject: {"beginner": 0, "intermediate": 0, "advanced": 0} for subject in SUBJECTS}
        }

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

    if 'hearts' not in st.session_state:
        st.session_state.hearts = 3

    if 'lesson_complete' not in st.session_state:
        st.session_state.lesson_complete = False

    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0

    if 'perfect_run' not in st.session_state:
        st.session_state.perfect_run = True

    if 'page' not in st.session_state:
        st.session_state.page = "welcome"

# Game mechanics functions
def start_lesson(subject, node_id):
    """Start a lesson for a specific node"""
    # Find the node data
    node_data = next((node for node in NODE_CONNECTIONS[subject] if node["id"] == node_id), None)
    
    if node_data:
        level = node_data["level"]
        st.session_state.user_data["current_subject"] = subject
        st.session_state.user_data["current_level"] = level
        st.session_state.user_data["current_node"] = node_id
        st.session_state.current_question_index = 0
        st.session_state.hearts = LEVELS[level]["hearts"]
        st.session_state.lesson_complete = False
        st.session_state.correct_answers = 0
        st.session_state.perfect_run = True
        st.session_state.page = "lesson"

def check_answer(selected_option, correct_option):
    """Check if the answer is correct and update hearts accordingly"""
    if selected_option == correct_option:
        st.session_state.correct_answers += 1
        return True
    else:
        st.session_state.hearts -= 1
        st.session_state.perfect_run = False
        return False

def complete_lesson():
    """Mark a lesson as complete and award XP"""
    subject = st.session_state.user_data["current_subject"]
    level = st.session_state.user_data["current_level"]
    node_id = st.session_state.user_data["current_node"]
    
    # Award XP
    xp_reward = LEVELS[level]["xp_reward"]
    st.session_state.user_data["xp"] += xp_reward
    
    # Update progress
    st.session_state.user_data["subjects_progress"][subject][level] += 1
    st.session_state.user_data["lessons_completed"] += 1
    
    # Mark node as completed
    if node_id not in st.session_state.user_data["completed_nodes"][subject]:
        st.session_state.user_data["completed_nodes"][subject].append(node_id)
    
    # Check for achievements
    check_achievements()
    
    # Update streak (in a real app, you'd check the date)
    st.session_state.user_data["streak_days"] += 1
    
    st.session_state.lesson_complete = True
    st.session_state.page = "lesson_complete"

def check_achievements():
    """Check if any new achievements have been unlocked"""
    current_xp = st.session_state.user_data["xp"]
    
    for achievement in ACHIEVEMENTS:
        if achievement["name"] == "Perfect Run" and st.session_state.perfect_run:
            if achievement["name"] not in st.session_state.user_data["achievements"]:
                st.session_state.user_data["achievements"].append(achievement["name"])
        elif achievement["name"] == "Streak Master" and st.session_state.user_data["streak_days"] >= 5:
            if achievement["name"] not in st.session_state.user_data["achievements"]:
                st.session_state.user_data["achievements"].append(achievement["name"])
        elif achievement["xp_threshold"] > 0 and current_xp >= achievement["xp_threshold"]:
            if achievement["name"] not in st.session_state.user_data["achievements"]:
                st.session_state.user_data["achievements"].append(achievement["name"])

def can_access_level(level):
    """Check if the user has enough XP to access a specific level"""
    return st.session_state.user_data["xp"] >= LEVELS[level]["unlock_xp"]

# Main application logic
def main():
    # Initialize session state
    init_session_state()
    
    # Render the character mascot
    render_character()
    
    # Navigation based on current page
    if st.session_state.page == "welcome":
        show_welcome_page()
    elif st.session_state.page == "dashboard":
        show_dashboard()
    elif st.session_state.page == "lesson":
        show_lesson()
    elif st.session_state.page == "lesson_complete":
        show_lesson_complete()
    elif st.session_state.page == "profile":
        show_profile()

def show_welcome_page():
    """Display the welcome page with login/sign up options"""
    st.markdown("""
    <div class="welcome-card">
        <h1 style="color: white; font-size: 42px;">Welcome to ExamLingo</h1>
        <p style="color: #d7d7d7; font-size: 18px;">The fun and engaging way to prepare for exams</p>
        <div style="font-size: 80px; margin: 30px 0;">📚✨</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Enter your username", key="username_input")
        st.session_state.user_data["username"] = username
    
    with col2:
        if st.button("Start Learning", key="start_button"):
            if st.session_state.user_data["username"]:
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Please enter a username to continue.")

def show_dashboard():
    """Display the main dashboard with subject selection and learning paths"""
    # Header with user info
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(f"Welcome, {st.session_state.user_data['username']}! 👋")
        st.subheader(f"XP: {st.session_state.user_data['xp']} | Streak: {st.session_state.user_data['streak_days']} days 🔥")
    
    with col2:
        if st.button("My Profile"):
            st.session_state.page = "profile"
            st.rerun()
    
    # Subject selection
    st.header("Choose a Subject")
    
    tab_labels = SUBJECTS
    tabs = st.tabs(tab_labels)
    
    for i, tab in enumerate(tabs):
        with tab:
            subject = SUBJECTS[i]
            st.subheader(f"{subject} Learning Path")
            
            # Render subject learning path
            nodes = render_learning_path(subject, st.session_state.user_data["completed_nodes"][subject])
            
            # Show available nodes
            if nodes:
                st.subheader("Available Lessons")
                
                for node in nodes:
                    node_id = node["id"]
                    node_type = node["type"]
                    level = node["level"]
                    icon = node["icon"]
                    
                    # Check if node is accessible
                    is_completed = node_id in st.session_state.user_data["completed_nodes"][subject]
                    can_access = False
                    
                    # First node is always accessible
                    if node_id == "node1":
                        can_access = True
                    else:
                        # Check if any prerequisite node is completed
                        for other_node in nodes:
                            if node_id in other_node["connects_to"] and other_node["id"] in st.session_state.user_data["completed_nodes"][subject]:
                                can_access = True
                                break
                    
                    # Check if user has enough XP for this level
                    level_accessible = can_access_level(level)
                    can_access = can_access and level_accessible
                    
                    # Display node information
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        title_style = ""
                        if not can_access:
                            title_style = "color: gray;"
                        elif is_completed:
                            title_style = "color: #58cc02;"
                        
                        st.markdown(f"<h4 style='{title_style}'>{icon} {level.capitalize()} {subject} {node_id.replace('node', 'Lesson ')}</h4>", unsafe_allow_html=True)
                        
                        if not level_accessible:
                            st.markdown(f"<p style='color: #ff4b4b;'>🔒 Need {LEVELS[level]['unlock_xp']} XP to unlock</p>", unsafe_allow_html=True)
                        elif is_completed:
                            st.markdown("✅ Completed", unsafe_allow_html=True)
                    
                    with col2:
                        if node_type == "special":
                            button_class = "special-button"
                        else:
                            button_class = ""
                        
                        if can_access and not is_completed:
                            if st.button(f"Start", key=f"start_{subject}_{node_id}", disabled=not can_access):
                                start_lesson(subject, node_id)
                                st.rerun()
                        elif can_access and is_completed:
                            if st.button(f"Review", key=f"review_{subject}_{node_id}"):
                                start_lesson(subject, node_id)
                                st.rerun()

def show_lesson():
    """Display the active lesson with questions"""
    subject = st.session_state.user_data["current_subject"]
    level = st.session_state.user_data["current_level"]
    node_id = st.session_state.user_data["current_node"]
    
    # Header with lesson info
    st.title(f"{subject} - {level.capitalize()} {node_id.replace('node', 'Lesson ')}")
    
    # Show hearts
    render_hearts(st.session_state.hearts)
    
    # Get questions for this level
    questions = QUESTIONS[subject][level]
    
    if st.session_state.current_question_index < len(questions):
        # Still have questions to answer
        current_question = questions[st.session_state.current_question_index]
        
        # Display progress
        progress_text = f"Question {st.session_state.current_question_index + 1}/{len(questions)}"
        render_progress_bar(st.session_state.current_question_index + 1, len(questions), progress_text)
        
        # Display question
        st.subheader(current_question["question"])
        
        # Check if user has already selected an answer for this question
        if 'selected_option' not in st.session_state:
            # Show options as buttons
            for option in current_question["options"]:
                if st.button(option, key=f"option_{option}"):
                    st.session_state.selected_option = option
                    st.rerun()
        else:
            # User has selected an answer, check it
            is_correct = check_answer(st.session_state.selected_option, current_question["correct"])
            
            # Display correct/incorrect feedback
            if is_correct:
                st.markdown(f"""
                <div class="correct-answer">
                    <h3>✅ Correct!</h3>
                    <p>{current_question["explanation"]}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="incorrect-answer">
                    <h3>❌ Incorrect</h3>
                    <p>The correct answer is: <strong>{current_question["correct"]}</strong></p>
                    <p>{current_question["explanation"]}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Continue button
            if st.button("Continue"):
                # Check if out of hearts
                if st.session_state.hearts <= 0:
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    # Move to next question
                    st.session_state.current_question_index += 1
                    if st.session_state.current_question_index >= len(questions):
                        complete_lesson()
                    # Clear selected option for next question
                    if 'selected_option' in st.session_state:
                        del st.session_state.selected_option
                    st.rerun()
    else:
        # All questions have been answered
        complete_lesson()
        st.rerun()

def show_lesson_complete():
    """Display the lesson complete screen"""
    subject = st.session_state.user_data["current_subject"]
    level = st.session_state.user_data["current_level"]
    xp_reward = LEVELS[level]["xp_reward"]
    
    # Show celebration message
    st.balloons()
    st.title("🎉 Lesson Complete! 🎉")
    
    # Show stats
    st.markdown(f"""
    <div style="background-color: #ffffff10; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h2 style="color: #58cc02;">+{xp_reward} XP earned!</h2>
        <p>Correct answers: {st.session_state.correct_answers}</p>
        <p>Hearts remaining: {st.session_state.hearts}/3</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for achievements
    new_achievements = [ach for ach in st.session_state.user_data["achievements"] 
                        if ach not in ["First Steps", "Quick Learner", "Knowledge Seeker", "Master Scholar"]]
    
    if new_achievements:
        st.subheader("🏆 Achievements Unlocked!")
        for ach_name in new_achievements:
            ach = next((a for a in ACHIEVEMENTS if a["name"] == ach_name), None)
            if ach:
                st.markdown(f"""
                <div class="achievement">
                    <h3>{ach["icon"]} {ach["name"]}</h3>
                    <p>{ach["description"]}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Continue button
    if st.button("Continue to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

def show_profile():
    """Display user profile page with stats and achievements"""
    st.title(f"{st.session_state.user_data['username']}'s Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Stats")
        st.markdown(f"""
        <div style="background-color: #ffffff10; padding: 20px; border-radius: 10px;">
            <p>📊 Total XP: <strong>{st.session_state.user_data['xp']}</strong></p>
            <p>🔥 Streak: <strong>{st.session_state.user_data['streak_days']} days</strong></p>
            <p>✅ Lessons completed: <strong>{st.session_state.user_data['lessons_completed']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Subject Progress")
        for subject in SUBJECTS:
            beginner_progress = st.session_state.user_data["subjects_progress"][subject]["beginner"]
            intermediate_progress = st.session_state.user_data["subjects_progress"][subject]["intermediate"]
            advanced_progress = st.session_state.user_data["subjects_progress"][subject]["advanced"]
            
            total_nodes = sum(1 for node in NODE_CONNECTIONS[subject] if node["level"] == "beginner")
            if total_nodes > 0:
                beginner_percentage = int((beginner_progress / total_nodes) * 100)
            else:
                beginner_percentage = 0
                
            total_nodes = sum(1 for node in NODE_CONNECTIONS[subject] if node["level"] == "intermediate") 
            if total_nodes > 0:
                intermediate_percentage = int((intermediate_progress / total_nodes) * 100)
            else:
                intermediate_percentage = 0
                
            total_nodes = sum(1 for node in NODE_CONNECTIONS[subject] if node["level"] == "advanced")
            if total_nodes > 0:
                advanced_percentage = int((advanced_progress / total_nodes) * 100)
            else:
                advanced_percentage = 0
            
            st.markdown(f"### {subject}")
            st.markdown(f"Beginner: {beginner_percentage}%")
            render_progress_bar(beginner_progress, total_nodes)
            
            st.markdown(f"Intermediate: {intermediate_percentage}%")
            render_progress_bar(intermediate_progress, total_nodes if total_nodes > 0 else 1)
            
            st.markdown(f"Advanced: {advanced_percentage}%")
            render_progress_bar(advanced_progress, total_nodes if total_nodes > 0 else 1)
    
    with col2:
        st.subheader("Achievements")
        if st.session_state.user_data["achievements"]:
            for ach_name in st.session_state.user_data["achievements"]:
                ach = next((a for a in ACHIEVEMENTS if a["name"] == ach_name), None)
                if ach:
                    st.markdown(f"""
                    <div class="achievement">
                        <h3>{ach["icon"]} {ach["name"]}</h3>
                        <p>{ach["description"]}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Complete lessons to earn achievements!")
        
        # Locked achievements
        st.subheader("Locked Achievements")
        locked_achs = [a for a in ACHIEVEMENTS if a["name"] not in st.session_state.user_data["achievements"]]
        for ach in locked_achs:
            st.markdown(f"""
            <div style="background-color: #ffffff10; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h3 style="color: gray;">🔒 {ach["name"]}</h3>
                <p>{ach["description"]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Back button
    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

# Run the app
if __name__ == "__main__":
    main()