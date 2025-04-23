import streamlit as st
import streamlit.components.v1 as components

# Настройка страницы
st.set_page_config(
    page_title="Образовательная Платформа | Computer Science",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Структура данных для предметов и тем
computer_science_topics = {
    "Основы программирования": {
        "Введение в программирование": ["Что такое программирование?", "Основные понятия алгоритмов", "Блок-схемы"],
        "Основы Python": ["Установка Python", "Переменные и типы данных", "Операторы и выражения"],
        "Управляющие конструкции": ["Условные операторы (if-else)", "Циклы (for, while)", "Функции"],
    },
    "Структуры данных и алгоритмы": {
        "Базовые структуры данных": ["Массивы и списки", "Стеки и очереди", "Деревья и графы"],
        "Алгоритмы сортировки": ["Пузырьковая сортировка", "Сортировка вставками", "Быстрая сортировка"],
        "Алгоритмы поиска": ["Линейный поиск", "Бинарный поиск", "Поиск в ширину и глубину"],
    },
    "Веб-разработка": {
        "Frontend-разработка": ["HTML основы", "CSS основы", "JavaScript основы"],
        "Backend-разработка": ["Введение в серверную разработку", "Python Flask", "REST API"],
        "Базы данных": ["SQL основы", "NoSQL базы данных", "Проектирование баз данных"],
    },
    "Машинное обучение": {
        "Введение в ML": ["Что такое машинное обучение?", "Типы задач ML", "Основные библиотеки"],
        "Обработка данных": ["Основы Pandas", "Визуализация данных", "Предобработка данных"],
        "Модели ML": ["Линейная регрессия", "Классификация", "Основы нейронных сетей"],
    }
}

# Определение цветовой схемы и стилей
primary_color = "#3498db"
secondary_color = "#2ecc71"
bg_color = "#f9f9f9"
text_color = "#333333"

# CSS для стилизации страницы
st.markdown(f"""
<style>
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    .sidebar .sidebar-content {{
        background-color: {primary_color};
    }}
    h1, h2, h3 {{
        color: {primary_color};
    }}
    .topic-card {{
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }}
    .topic-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }}
    .lesson-btn {{
        background-color: {secondary_color};
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
        margin: 5px;
        cursor: pointer;
        text-align: left;
        width: 100%;
    }}
    .lesson-btn:hover {{
        background-color: #27ae60;
    }}
    .header {{
        background-color: {primary_color};
        padding: 20px;
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    .content-area {{
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
</style>
""", unsafe_allow_html=True)

# Функция для отображения контента урока
def show_lesson_content(category, topic, lesson):
    st.markdown(f"<h2>{lesson}</h2>", unsafe_allow_html=True)
    
    # Здесь мы можем добавить фактический контент урока
    # В реальном проекте это может быть загружено из базы данных или файлов
    st.write("Это демонстрационный контент для урока. В настоящей версии здесь будет находиться образовательный материал, видео и интерактивные элементы.")
    
    # Демо-видео (заглушка)
    st.markdown("### Видео-урок")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    # Примеры кода для уроков программирования
    if category == "Основы программирования" or category == "Структуры данных и алгоритмы":
        st.markdown("### Пример кода")
        if "Python" in topic or "программирование" in topic.lower():
            st.code("""
# Пример кода для демонстрации
def hello_world():
    print("Привет, мир!")
    
# Вызов функции
hello_world()
            """, language="python")
    
    # Интерактивные элементы
    st.markdown("### Проверьте свои знания")
    question = st.radio(
        "Выберите правильный ответ:",
        ["Вариант A", "Вариант B", "Вариант C", "Вариант D"]
    )
    
    if st.button("Проверить ответ"):
        if question == "Вариант C":  # Предположим, что это правильный ответ
            st.success("Правильно! Отличная работа!")
        else:
            st.error("Попробуйте еще раз!")
    
    # Добавление практического задания
    st.markdown("### Практическое задание")
    st.text_area("Напишите свое решение здесь:", height=150)
    if st.button("Отправить решение"):
        st.info("Решение отправлено на проверку!")

# Основная функция для отображения
def main():
    # Заголовок сайта
    st.markdown("""
    <div class="header">
        <h1>🎓 Образовательная Платформа</h1>
        <p>Изучайте информатику и программирование онлайн</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Создаем сессионные состояния для отслеживания выбора пользователя
    if 'selected_subject' not in st.session_state:
        st.session_state.selected_subject = "Информатика"
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None
    if 'selected_lesson' not in st.session_state:
        st.session_state.selected_lesson = None
    
    # Боковая панель для навигации
    with st.sidebar:
        st.markdown("<h2 style='color: white;'>Предметы</h2>", unsafe_allow_html=True)
        subjects = ["Информатика", "Математика"]
        
        for subject in subjects:
            if st.button(subject, key=f"subject_{subject}"):
                st.session_state.selected_subject = subject
                st.session_state.selected_category = None
                st.session_state.selected_topic = None
                st.session_state.selected_lesson = None
                st.rerun()
        
        # Если выбран предмет, показываем его категории
        if st.session_state.selected_subject:
            st.markdown(f"<h3 style='color: white;'>Категории {st.session_state.selected_subject}</h3>", unsafe_allow_html=True)
            
            if st.session_state.selected_subject == "Информатика":
                for category in computer_science_topics.keys():
                    if st.button(category, key=f"category_{category}"):
                        st.session_state.selected_category = category
                        st.session_state.selected_topic = None
                        st.session_state.selected_lesson = None
                        st.rerun()
    
    # Основное содержимое
    if st.session_state.selected_subject == "Информатика":
        if st.session_state.selected_category is None:
            # Показываем обзор всех категорий
            st.markdown("<h2>Категории курсов по информатике</h2>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            for i, category in enumerate(computer_science_topics.keys()):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                    <div class="topic-card">
                        <h3>{category}</h3>
                        <p>Изучите основы и продвинутые концепции в данной области.</p>
                        <button class="lesson-btn" onclick="document.getElementById('category_{category.replace(' ', '_')}').click()">Перейти к курсам</button>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Скрытая кнопка для JavaScript
                    st.markdown(f"""
                    <div style="display:none;">
                        <button id="category_{category.replace(' ', '_')}" key="category_{category}"></button>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Перейти к {category}", key=f"cat_btn_{category}", help=f"Просмотреть темы по {category}"):
                        st.session_state.selected_category = category
                        st.rerun()
        
        elif st.session_state.selected_lesson is not None:
            # Показываем содержимое конкретного урока
            st.markdown(f"""
            <div class="content-area">
                <p><a href="#" onclick="javascript:history.back();">← Назад к темам</a></p>
                <h2>{st.session_state.selected_category} > {st.session_state.selected_topic} > {st.session_state.selected_lesson}</h2>
                <hr>
            """, unsafe_allow_html=True)
            
            show_lesson_content(st.session_state.selected_category, st.session_state.selected_topic, st.session_state.selected_lesson)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Навигационные кнопки внизу страницы
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Предыдущий урок"):
                    # Логика для перехода к предыдущему уроку
                    st.info("Переход к предыдущему уроку (функциональность будет добавлена)")
            with col2:
                if st.button("Следующий урок →"):
                    # Логика для перехода к следующему уроку
                    st.info("Переход к следующему уроку (функциональность будет добавлена)")
        
        elif st.session_state.selected_topic is not None:
            # Показываем уроки выбранной темы
            topics = computer_science_topics[st.session_state.selected_category]
            if st.session_state.selected_topic in topics:
                lessons = topics[st.session_state.selected_topic]
                
                st.markdown(f"""
                <div class="content-area">
                    <p><a href="#" onclick="javascript:history.back();">← Назад к темам</a></p>
                    <h2>{st.session_state.selected_category} > {st.session_state.selected_topic}</h2>
                    <p>Выберите урок для изучения:</p>
                    <hr>
                """, unsafe_allow_html=True)
                
                for lesson in lessons:
                    st.markdown(f"""
                    <div class="topic-card">
                        <h3>{lesson}</h3>
                        <p>Продолжительность: ~25 мин | Сложность: ⭐⭐☆☆☆</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Изучить '{lesson}'", key=f"lesson_{lesson}"):
                        st.session_state.selected_lesson = lesson
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        else:
            # Показываем темы выбранной категории
            st.markdown(f"""
            <div class="content-area">
                <p><a href="#" onclick="javascript:history.back();">← Назад к категориям</a></p>
                <h2>Темы в категории: {st.session_state.selected_category}</h2>
                <hr>
                </div>
            """, unsafe_allow_html=True)
            
            topics = computer_science_topics[st.session_state.selected_category]
            col1, col2 = st.columns(2)
            
            for i, topic in enumerate(topics.keys()):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                    <div class="topic-card">
                        <h3>{topic}</h3>
                        <p>Количество уроков: {len(topics[topic])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Открыть '{topic}'", key=f"topic_{topic}"):
                        st.session_state.selected_topic = topic
                        st.rerun()
    
    # Для предмета "Математика" (заглушка для будущего расширения)
    elif st.session_state.selected_subject == "Математика":
        st.markdown("""
        <div class="content-area">
            <h2>Математика</h2>
            <p>Данный раздел находится в разработке. Скоро здесь появятся курсы по математике!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Нижний колонтитул
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; color: #888;">
        <p>© 2025 Образовательная Платформа | Все права защищены</p>
    </div>
    """, unsafe_allow_html=True)

# Запуск приложения
if __name__ == "__main__":
    main()