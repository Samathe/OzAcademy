import streamlit as st
import json
import pandas as pd
import random
import os
from datetime import datetime
import requests

# Page configuration
st.set_page_config(
    page_title="ExamLingo - AI Content Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #111b2b;
    }
    
    p, li, label, div {
        color: #ffffff !important;
    }
    
    .stButton button {
        background-color: #58cc02;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 20px;
        border: none;
        box-shadow: 0 4px 0 #46a302;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #61dd00;
        box-shadow: 0 2px 0 #46a302;
        transform: translateY(2px);
    }
    
    .special-button button {
        background-color: #a560ff;
        box-shadow: 0 4px 0 #8548cc;
    }
    
    .output-container {
        background-color: #ffffff10;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border-left: 5px solid #58cc02;
    }
    
    .json-output {
        font-family: monospace;
        white-space: pre-wrap;
        background-color: #1e2a3a;
        padding: 15px;
        border-radius: 5px;
        overflow: auto;
        max-height: 500px;
    }
    
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
</style>
""", unsafe_allow_html=True)

# Load prompt templates
def load_prompt_templates():
    return {
        "math": """
Сгенерируй математическое задание по теме "{тема}" с уровнем сложности {сложность от 1 до 5} для образовательного приложения. 

Требования:
1. Создай задание, которое можно рандомизировать (с параметрами, которые можно менять).
2. Укажи корректный ответ и способ проверки.
3. Предоставь краткое объяснение решения.
4. Задание должно быть в формате {тип_задания: тестовый выбор, числовой ввод, соответствие}.
5. Добавь 2-3 неверных варианта ответа с объяснением, почему они неверны.

Формат ответа должен быть в JSON:
{
  "question": "текст вопроса",
  "type": "тип вопроса",
  "parameters": {
    "param1": {"min": значение, "max": значение, "step": значение},
    ...
  },
  "options": ["вариант1", "вариант2", ...],
  "correctAnswer": "правильный ответ или индекс",
  "explanation": "объяснение решения",
  "wrongAnswersExplanation": {
    "вариант1": "почему неверно",
    ...
  },
  "difficulty": число,
  "tags": ["тег1", "тег2", ...]
}
""",
        "computer_science": """
Сгенерируй задание по информатике по теме "{тема}" с уровнем сложности {сложность от 1 до 5} для образовательного приложения. 

Требования:
1. Задание должно быть в формате {тип_задания: тестовый выбор, написание кода, исправление ошибок, заполнение пропусков}.
2. Если это задание на код, предоставь шаблон начального кода и ожидаемый результат.
3. Укажи критерии проверки и тестовые случаи.
4. Предоставь решение с объяснением.
5. Язык программирования: {язык}.

Формат ответа должен быть в JSON:
{
  "question": "текст вопроса",
  "type": "тип вопроса",
  "programmingLanguage": "язык программирования",
  "initialCode": "начальный код (если применимо)",
  "testCases": [
    {"input": "входные данные", "expectedOutput": "ожидаемый результат"},
    ...
  ],
  "solution": "решение",
  "explanation": "объяснение решения",
  "difficulty": число,
  "tags": ["тег1", "тег2", ...],
  "hints": ["подсказка1", "подсказка2", ...]
}
""",
        "code_analysis": """
Проанализируй следующий код на языке {язык}, написанный пользователем для решения задачи: 

"{текст_задачи}"

Код пользователя:
```
{код_пользователя}
```

Ожидаемое поведение:
{ожидаемое_поведение}

Выполни следующий анализ:
1. Правильность решения (проходит ли тесты).
2. Оценка качества кода (1-10).
3. Выявление потенциальных проблем или ошибок.
4. Предложения по улучшению кода (оптимизация, читаемость, стиль).
5. Персонализированные рекомендации для дальнейшего обучения.

Формат ответа должен быть в JSON:
{
  "isCorrect": true/false,
  "codeQuality": число,
  "issues": [
    {"type": "тип проблемы", "description": "описание", "lineNumber": число, "severity": "критичность"},
    ...
  ],
  "improvements": [
    {"suggestion": "предложение", "reason": "причина", "example": "пример"},
    ...
  ],
  "learning": [
    {"topic": "тема для изучения", "reason": "почему это важно"},
    ...
  ],
  "feedback": "общая обратная связь",
  "nextSteps": "что пользователю следует делать дальше"
}
""",
        "adaptive_assessment": """
На основе ответов пользователя на предыдущие вопросы, оцени текущий уровень понимания темы "{тема}" и выбери следующий вопрос.

История ответов:
{
  "questions": [
    {
      "id": "идентификатор",
      "difficulty": число,
      "topic": "тема",
      "subtopic": "подтема",
      "userAnswer": "ответ пользователя",
      "isCorrect": true/false,
      "timeSpent": число_секунд
    },
    ...
  ]
}

Требования:
1. Оцени текущий уровень знаний по подтемам (1-5).
2. Определи области, требующие улучшения.
3. Выбери оптимальный следующий вопрос (ID из доступных вопросов).
4. Предложи стратегию для улучшения слабых мест.

Формат ответа должен быть в JSON:
{
  "skillAssessment": {
    "тема1": число,
    "тема2": число,
    ...
  },
  "weakAreas": ["область1", "область2", ...],
  "nextQuestionId": "идентификатор следующего вопроса",
  "nextQuestionDifficulty": число,
  "nextQuestionTopic": "тема",
  "improvement": [
    {"area": "область", "suggestion": "предложение"},
    ...
  ],
  "confidence": число,
  "explanation": "объяснение выбора следующего вопроса"
}
""",
        "personalized_recommendations": """
На основе профиля пользователя и его прогресса в обучении, сгенерируй персонализированные рекомендации для более эффективного изучения темы "{тема}".

Профиль пользователя:
{
  "skills": {
    "тема1": число,
    "тема2": число,
    ...
  },
  "learningStyle": "стиль обучения",
  "completedLevels": ["уровень1", "уровень2", ...],
  "struggles": ["проблема1", "проблема2", ...],
  "averageTimePerQuestion": число_секунд,
  "strengths": ["сильная_сторона1", "сильная_сторона2", ...],
  "preferences": ["предпочтение1", "предпочтение2", ...]
}

Требования:
1. Предложи 3-5 конкретных рекомендаций для улучшения.
2. Учитывай стиль обучения и предпочтения пользователя.
3. Основывай рекомендации на выявленных слабых местах.
4. Предложи оптимальный порядок изучения последующих тем.
5. Добавь мотивационный элемент.

Формат ответа должен быть в JSON:
{
  "recommendations": [
    {
      "title": "название рекомендации",
      "description": "подробное описание",
      "reason": "обоснование",
      "priority": число,
      "actionItem": "конкретное действие"
    },
    ...
  ],
  "learningPath": [
    {"topic": "тема", "reason": "причина"},
    ...
  ],
  "motivation": "мотивационное сообщение",
  "estimatedImprovementTime": "оценка времени для улучшения",
  "potentialOutcome": "ожидаемый результат при следовании рекомендациям"
}
""",
        "performance_prediction": """
На основе истории обучения пользователя, сделай прогноз его успеваемости на ближайшие {период} дней в изучении темы "{тема}".

История обучения:
{
  "dailyProgress": [
    {"date": "дата", "completedTasks": число, "correctAnswers": число, "timeSpent": число_минут},
    ...
  ],
  "skillGrowth": [
    {"skill": "навык", "initialLevel": число, "currentLevel": число, "daysToAchieve": число},
    ...
  ],
  "consistency": число,
  "currentStreak": число_дней,
  "averageSessionLength": число_минут
}

Требования:
1. Спрогнозируй ожидаемый прогресс на каждый день указанного периода.
2. Оцени вероятность достижения следующего уровня.
3. Выяви потенциальные риски и препятствия.
4. Предложи корректирующие действия для оптимизации обучения.

Формат ответа должен быть в JSON:
{
  "dailyPredictions": [
    {"day": число, "expectedTasks": число, "expectedCorrectRate": число, "skillLevel": число},
    ...
  ],
  "levelUpPrediction": {
    "probability": число,
    "estimatedDays": число,
    "confidence": число
  },
  "risks": [
    {"risk": "описание риска", "probability": число, "impact": число, "mitigation": "способ смягчения"},
    ...
  ],
  "optimizationSuggestions": [
    {"suggestion": "предложение", "expectedImpact": число, "effort": число},
    ...
  ],
  "confidenceScore": число,
  "predictionMethod": "описание метода прогнозирования"
}
""",
        "hints_generator": """
Пользователь пытается решить задачу, но испытывает трудности. Сгенерируй серию постепенных подсказок, не раскрывающих сразу полное решение.

Задача:
"{текст_задачи}"

Текущий прогресс пользователя:
"{действия_пользователя}"

Сложность: {1-5}
Количество предыдущих подсказок: {число}

Требования:
1. Создай 3 уровня подсказок возрастающей детализации.
2. Первая подсказка должна направлять мышление, не давая конкретного решения.
3. Вторая подсказка должна указывать на ключевой метод или формулу.
4. Третья подсказка должна содержать частичное решение.
5. Адаптируй уровень подсказок к текущему прогрессу и количеству предыдущих подсказок.

Формат ответа должен быть в JSON:
{
  "hints": [
    {
      "level": 1,
      "text": "легкая подсказка",
      "reveals": "что раскрывает подсказка"
    },
    {
      "level": 2,
      "text": "средняя подсказка",
      "reveals": "что раскрывает подсказка"
    },
    {
      "level": 3,
      "text": "детальная подсказка",
      "reveals": "что раскрывает подсказка"
    }
  ],
  "recommendedHintLevel": число,
  "conceptsToReview": ["концепция1", "концепция2", ...],
  "encouragement": "мотивационное сообщение"
}
""",
        "error_patterns": """
Проанализируй историю ошибок пользователя в задачах по теме "{тема}" и определи системные паттерны, которые могут указывать на фундаментальные пробелы в понимании.

История ошибок:
{
  "errors": [
    {
      "questionId": "идентификатор",
      "topic": "тема",
      "subtopic": "подтема",
      "userAnswer": "ответ пользователя",
      "correctAnswer": "правильный ответ",
      "errorType": "тип ошибки",
      "timestamp": "время"
    },
    ...
  ]
}

Требования:
1. Выяви повторяющиеся типы ошибок.
2. Определи возможные концептуальные пробелы.
3. Предложи целевые упражнения для устранения пробелов.
4. Оцени общий уровень понимания темы.

Формат ответа должен быть в JSON:
{
  "errorPatterns": [
    {
      "pattern": "описание паттерна",
      "frequency": число,
      "subtopics": ["подтема1", "подтема2", ...],
      "examples": ["пример1", "пример2", ...]
    },
    ...
  ],
  "conceptualGaps": [
    {
      "concept": "концепция",
      "description": "описание пробела",
      "confidence": число,
      "relatedErrors": ["ошибка1", "ошибка2", ...]
    },
    ...
  ],
  "targetedExercises": [
    {
      "title": "название упражнения",
      "description": "описание",
      "targetGap": "целевой пробел",
      "difficulty": число
    },
    ...
  ],
  "overallAssessment": {
    "understanding": число,
    "strengths": ["сильная_сторона1", "сильная_сторона2", ...],
    "priorityGaps": ["приоритетный_пробел1", "приоритетный_пробел2", ...]
  },
  "recommendedAction": "рекомендуемое действие"
}
"""
    }

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = ""

if 'prompt_template' not in st.session_state:
    st.session_state.prompt_template = ""

if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

if 'history' not in st.session_state:
    st.session_state.history = []

# Simulate AI API call
def generate_ai_content(prompt, api_key):
    # This is a mock function - in a real app, you would call an actual AI API here
    # For demonstration purposes, we'll just return a sample response
    
    if "математическое задание" in prompt:
        return json.dumps({
            "question": "Решите уравнение: ax² + bx + c = 0, где a = 2, b = -5, c = 3",
            "type": "тестовый выбор",
            "parameters": {
                "a": {"min": 1, "max": 5, "step": 1},
                "b": {"min": -10, "max": 10, "step": 1},
                "c": {"min": -5, "max": 5, "step": 1}
            },
            "options": ["x₁ = 1, x₂ = 1.5", "x₁ = 0.5, x₂ = 3", "x₁ = 2, x₂ = 0.75", "x₁ = 1.5, x₂ = 1"],
            "correctAnswer": "x₁ = 1.5, x₂ = 1",
            "explanation": "Используем формулу дискриминанта D = b² - 4ac = (-5)² - 4·2·3 = 25 - 24 = 1.\nЗатем находим корни: x₁ = (-b + √D)/2a = (5 + 1)/4 = 1.5, x₂ = (-b - √D)/2a = (5 - 1)/4 = 1",
            "wrongAnswersExplanation": {
                "x₁ = 1, x₂ = 1.5": "Неверно применена формула для нахождения корней квадратного уравнения",
                "x₁ = 0.5, x₂ = 3": "Неверный расчет при вычислении корней",
                "x₁ = 2, x₂ = 0.75": "Ошибка в вычислении дискриминанта"
            },
            "difficulty": 3,
            "tags": ["квадратные уравнения", "алгебра", "дискриминант"]
        }, indent=2, ensure_ascii=False)
    elif "информатике" in prompt:
        return json.dumps({
            "question": "Напишите функцию на Python, которая найдет все простые числа в диапазоне от 1 до n с использованием решета Эратосфена",
            "type": "написание кода",
            "programmingLanguage": "Python",
            "initialCode": "def sieve_of_eratosthenes(n):\n    # Ваш код здесь\n    pass\n\n# Пример использования\nprint(sieve_of_eratosthenes(30))",
            "testCases": [
                {"input": "10", "expectedOutput": "[2, 3, 5, 7]"},
                {"input": "20", "expectedOutput": "[2, 3, 5, 7, 11, 13, 17, 19]"},
                {"input": "30", "expectedOutput": "[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]"}
            ],
            "solution": "def sieve_of_eratosthenes(n):\n    primes = []\n    sieve = [True] * (n + 1)\n    for p in range(2, n + 1):\n        if sieve[p]:\n            primes.append(p)\n            for i in range(p * p, n + 1, p):\n                sieve[i] = False\n    return primes",
            "explanation": "Алгоритм Эратосфена работает путем итеративного отметания чисел, которые являются кратными простым числам. Мы создаем булев массив sieve размером n+1, где sieve[i] обозначает, является ли i простым числом. Изначально предполагаем, что все числа простые (True). Затем для каждого числа p от 2 до n, если оно остается отмеченным как простое, мы добавляем его в список primes и отмечаем все его кратные как составные (False).",
            "difficulty": 4,
            "tags": ["алгоритмы", "простые числа", "решето Эратосфена", "оптимизация"],
            "hints": [
                "Создайте массив булевых значений для отметки простых чисел",
                "Начните с первого простого числа (2) и отметьте все его кратные как составные",
                "Для оптимизации достаточно начать отметку с p*p, так как все меньшие кратные уже отмечены"
            ]
        }, indent=2, ensure_ascii=False)
    else:
        # Generic response for other prompt types
        return json.dumps({
            "message": "Это примерный ответ от ИИ. В реальном приложении здесь будет настоящий ответ от API.",
            "prompt_received": prompt,
            "timestamp": datetime.now().isoformat()
        }, indent=2, ensure_ascii=False)

# Main app function
def main():
    st.title("🤖 ExamLingo - AI Content Generator")
    st.markdown("### Генератор контента для обучающей платформы")
    
    # Sidebar for API settings
    with st.sidebar:
        st.header("Настройки")
        api_key = st.text_input("API Ключ (не обязательно для демо)", type="password")
        st.session_state.api_key = api_key
        
        st.header("История генераций")
        if st.session_state.history:
            for idx, item in enumerate(st.session_state.history[-5:]):
                if st.button(f"{item['type']} - {item['timestamp']}", key=f"history_{idx}"):
                    st.session_state.generated_content = item["content"]
                    st.session_state.prompt_template = item["template"]
        
        st.markdown("---")
        st.markdown("© 2025 ExamLingo")
    
    # Main content area
    templates = load_prompt_templates()
    
    # Tabs for different prompt types
    tabs = st.tabs([
        "🧮 Математика", 
        "💻 Информатика", 
        "🔍 Анализ кода", 
        "📊 Адаптивная оценка",
        "🎯 Рекомендации",
        "📈 Прогноз успеваемости",
        "💡 Подсказки",
        "❌ Анализ ошибок"
    ])
    
    with tabs[0]:  # Math tab
        st.header("Генератор математических заданий")
        math_topic = st.text_input("Тема задания", value="Квадратные уравнения", key="math_topic")
        math_difficulty = st.slider("Сложность", 1, 5, 3, key="math_difficulty")
        
        if st.button("Сгенерировать задание", key="generate_math"):
            prompt = templates["math"].replace("{тема}", math_topic).replace("{сложность от 1 до 5}", str(math_difficulty))
            st.session_state.prompt_template = prompt
            
            with st.spinner("Генерация задания..."):
                response = generate_ai_content(prompt, st.session_state.api_key)
                st.session_state.generated_content = response
                
                # Add to history
                st.session_state.history.append({
                    "type": "Математика",
                    "template": prompt,
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
    with tabs[1]:  # Computer Science tab
        st.header("Генератор заданий по информатике")
        cs_topic = st.text_input("Тема задания", value="Алгоритмы сортировки", key="cs_topic")
        cs_difficulty = st.slider("Сложность", 1, 5, 3, key="cs_difficulty")
        cs_language = st.selectbox("Язык программирования", ["Python", "JavaScript", "Java", "C++", "C#"], key="cs_language")
        
        if st.button("Сгенерировать задание", key="generate_cs"):
            prompt = templates["computer_science"]\
                .replace("{тема}", cs_topic)\
                .replace("{сложность от 1 до 5}", str(cs_difficulty))\
                .replace("{язык}", cs_language)
            st.session_state.prompt_template = prompt
            
            with st.spinner("Генерация задания..."):
                response = generate_ai_content(prompt, st.session_state.api_key)
                st.session_state.generated_content = response
                
                # Add to history
                st.session_state.history.append({
                    "type": "Информатика",
                    "template": prompt,
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
    
    with tabs[2]:  # Code Analysis tab
        st.header("Анализ кода")
        ca_language = st.selectbox("Язык программирования", ["Python", "JavaScript", "Java", "C++", "C#"], key="ca_language")
        ca_task = st.text_area("Текст задачи", value="Напишите функцию, которая находит наибольший общий делитель двух чисел", key="ca_task")
        ca_code = st.text_area("Код пользователя", value="def gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a", key="ca_code", height=200)
        ca_expected = st.text_area("Ожидаемое поведение", value="Функция должна возвращать НОД двух чисел", key="ca_expected")
        
        if st.button("Проанализировать код", key="analyze_code"):
            prompt = templates["code_analysis"]\
                .replace("{язык}", ca_language)\
                .replace("{текст_задачи}", ca_task)\
                .replace("{код_пользователя}", ca_code)\
                .replace("{ожидаемое_поведение}", ca_expected)
            st.session_state.prompt_template = prompt
            
            with st.spinner("Анализ кода..."):
                response = generate_ai_content(prompt, st.session_state.api_key)
                st.session_state.generated_content = response
                
                # Add to history
                st.session_state.history.append({
                    "type": "Анализ кода",
                    "template": prompt,
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
    
    # Display output
    if st.session_state.generated_content:
        st.markdown("---")
        st.header("Сгенерированный контент")
        
        try:
            # Try to parse as JSON for pretty formatting
            parsed = json.loads(st.session_state.generated_content)
            st.markdown('<div class="output-container">', unsafe_allow_html=True)
            st.json(parsed)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Export options
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Копировать JSON"):
                    # In a real app, this would use JavaScript to copy to clipboard
                    st.success("JSON скопирован в буфер обмена")
            with col2:
                if st.download_button(
                    label="Скачать JSON",
                    data=st.session_state.generated_content,
                    file_name=f"examlingo_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                ):
                    pass
                    
        except json.JSONDecodeError:
            # If not valid JSON, display as text
            st.markdown('<div class="output-container">', unsafe_allow_html=True)
            st.markdown('<div class="json-output">' + st.session_state.generated_content + '</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Display used prompt template (collapsible)
    if st.session_state.prompt_template:
        with st.expander("