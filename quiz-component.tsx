import React, { useState } from 'react';

const Quiz = () => {
  // Sample quiz questions for Computer Science topics
  const quizQuestions = {
    "Алгоритмы сортировки": [
      {
        question: "Алгоритм сортировки, который меняет местами соседние элементы, если предыдущий элемент больше последующего элемента – это",
        options: [
          "Bubble sort (пузырьковая сортировка)",
          "Insertion sort (сортировка вставкой)",
          "Quick sort (быстрая сортировка)",
          "Selection sort (сортировка выбором)"
        ],
        correctAnswer: 0,
        explanation: "Пузырьковая сортировка (Bubble sort) работает путем многократного прохода по списку, сравнивая соседние элементы и меняя их местами, если они находятся в неправильном порядке."
      },
      {
        question: "Какой алгоритм сортировки имеет наилучшую временную сложность в среднем случае?",
        options: [
          "Bubble sort (пузырьковая сортировка)",
          "Insertion sort (сортировка вставкой)",
          "Quick sort (быстрая сортировка)",
          "Selection sort (сортировка выбором)"
        ],
        correctAnswer: 2,
        explanation: "Быстрая сортировка (Quick sort) имеет среднюю временную сложность O(n log n), что лучше, чем O(n²) у пузырьковой сортировки и сортировки вставками."
      }
    ],
    "Основы Python": [
      {
        question: "Какой тип данных используется для хранения упорядоченной последовательности элементов в Python?",
        options: [
          "Dictionary (словарь)",
          "List (список)",
          "Set (множество)",
          "Tuple (кортеж)"
        ],
        correctAnswer: 1,
        explanation: "Список (List) в Python используется для хранения упорядоченной последовательности элементов, которые могут быть изменены."
      },
      {
        question: "Какой оператор используется для проверки, является ли один объект экземпляром определенного класса в Python?",
        options: [
          "is",
          "in",
          "isinstance()",
          "type()"
        ],
        correctAnswer: 2,
        explanation: "Функция isinstance() используется для проверки, является ли объект экземпляром определенного класса или подкласса."
      }
    ],
    "Базы данных": [
      {
        question: "Какой тип SQL-запроса используется для извлечения данных из базы данных?",
        options: [
          "INSERT",
          "UPDATE",
          "DELETE",
          "SELECT"
        ],
        correctAnswer: 3,
        explanation: "SELECT используется для выборки данных из одной или нескольких таблиц базы данных."
      },
      {
        question: "Какой тип связи в реляционной базе данных подразумевает, что каждая запись в первой таблице может быть связана с множеством записей во второй таблице?",
        options: [
          "Один к одному (One-to-One)",
          "Один ко многим (One-to-Many)",
          "Многие ко многим (Many-to-Many)",
          "Многие к одному (Many-to-One)"
        ],
        correctAnswer: 1,
        explanation: "Связь 'Один ко многим' означает, что одна запись из первой таблицы может быть связана с несколькими записями из второй таблицы."
      }
    ]
  };

  // Get available topics
  const topics = Object.keys(quizQuestions);
  
  // State variables
  const [selectedTopic, setSelectedTopic] = useState(topics[0]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [isAnswerSubmitted, setIsAnswerSubmitted] = useState(false);
  const [score, setScore] = useState(0);
  const [showResults, setShowResults] = useState(false);

  // Get current question
  const currentQuestion = quizQuestions[selectedTopic][currentQuestionIndex];
  
  // Handle topic change
  const handleTopicChange = (topic) => {
    setSelectedTopic(topic);
    setCurrentQuestionIndex(0);
    setSelectedOption(null);
    setIsAnswerSubmitted(false);
    setScore(0);
    setShowResults(false);
  };
  
  // Handle option selection
  const handleOptionSelect = (index) => {
    if (!isAnswerSubmitted) {
      setSelectedOption(index);
    }
  };
  
  // Handle answer submission
  const handleSubmit = () => {
    if (selectedOption !== null && !isAnswerSubmitted) {
      if (selectedOption === currentQuestion.correctAnswer) {
        setScore(score + 1);
      }
      setIsAnswerSubmitted(true);
    }
  };
  
  // Handle next question
  const handleNextQuestion = () => {
    if (currentQuestionIndex < quizQuestions[selectedTopic].length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSelectedOption(null);
      setIsAnswerSubmitted(false);
    } else {
      setShowResults(true);
    }
  };
  
  // Handle restart quiz
  const handleRestartQuiz = () => {
    setCurrentQuestionIndex(0);
    setSelectedOption(null);
    setIsAnswerSubmitted(false);
    setScore(0);
    setShowResults(false);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 max-w-lg mx-auto">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Тестирование по теме</h2>
        
        {/* Topic selector */}
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-2">Выберите тему:</label>
          <select 
            className="w-full border border-gray-300 rounded-md px-3 py-2"
            value={selectedTopic}
            onChange={(e) => handleTopicChange(e.target.value)}
          >
            {topics.map((topic, index) => (
              <option key={index} value={topic}>{topic}</option>
            ))}
          </select>
        </div>
      </div>
      
      {!showResults ? (
        <div>
          {/* Question */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Вопрос {currentQuestionIndex + 1} из {quizQuestions[selectedTopic].length}
            </h3>
            <p className="text-gray-700 mb-4">{currentQuestion.question}</p>
            
            {/* Options */}
            <div className="space-y-2">
              {currentQuestion.options.map((option, index) => (
                <div 
                  key={index}
                  className={`border rounded-md p-3 cursor-pointer transition-colors ${
                    selectedOption === index 
                      ? 'border-blue-500 bg-blue-50' 
                      : 'border-gray-200 hover:bg-gray-50'
                  } ${
                    isAnswerSubmitted && index === currentQuestion.correctAnswer
                      ? 'border-green-500 bg-green-50'
                      : isAnswerSubmitted && index === selectedOption && index !== currentQuestion.correctAnswer
                      ? 'border-red-500 bg-red-50'
                      : ''
                  }`}
                  onClick={() => handleOptionSelect(index)}
                >
                  <div className="flex items-center">
                    <div className={`h-5 w-5 rounded-full flex items-center justify-center mr-3 ${
                      selectedOption === index 
                        ? 'bg-blue-500 text-white' 
                        : 'bg-gray-200'
                    }`}>
                      {String.fromCharCode(65 + index)}
                    </div>
                    <span className="text-gray-700">{option}</span>
                    
                    {isAnswerSubmitted && index === currentQuestion.correctAnswer && (
                      <svg className="h-5 w-5 ml-auto text-green-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M16.707 5.293a1 1 0 00-1.414 0L8 12.586 4.707 9.293a1 1 0 00-1.414 1.414l4 4a1 1 0 001.414 0l8-8a1 1 0 000-1.414z" />
                      </svg>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Explanation */}
          {isAnswerSubmitted && (
            <div className={`p-4 rounded-md mb-6 ${
              selectedOption === currentQuestion.correctAnswer 
                ? 'bg-green-50 border border-green-200' 
                : 'bg-red-50 border border-red-200'
            }`}>
              <h4 className={`font-semibold ${
                selectedOption === currentQuestion.correctAnswer 
                  ? 'text-green-700' 
                  : 'text-red-700'
              }`}>
                {selectedOption === currentQuestion.correctAnswer 
                  ? 'Правильно!' 
                  : 'Неправильно!'
                }
              </h4>
              <p className="text-gray-700 mt-1">{currentQuestion.explanation}</p>
            </div>
          )}
          
          {/* Action buttons */}
          <div className="flex justify-between">
            {!isAnswerSubmitted ? (
              <button
                className={`px-4 py-2 rounded-md ${
                  selectedOption !== null
                    ? 'bg-blue-500 text-white hover:bg-blue-600'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
                onClick={handleSubmit}
                disabled={selectedOption === null}
              >
                Проверить ответ
              </button>
            ) : (
              <button
                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                onClick={handleNextQuestion}
              >
                {currentQuestionIndex < quizQuestions[selectedTopic].length - 1
                  ? 'Следующий вопрос'
                  : 'Посмотреть результаты'
                }
              </button>
            )}
          </div>
        </div>
      ) : (
        // Results screen
        <div className="text-center">
          <div className="mb-6">
            <div className="text-6xl font-bold text-blue-500 mb-2">{score}/{quizQuestions[selectedTopic].length}</div>
            <p className="text-gray-700">
              {score === quizQuestions[selectedTopic].length
                ? 'Отлично! Вы ответили на все вопросы правильно!'
                : score >= quizQuestions[selectedTopic].length / 2
                ? 'Хороший результат! Но есть над чем поработать.'
                : 'Попробуйте еще раз, чтобы улучшить свой результат.'}
            </p>
          </div>
          
          <button
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
            onClick={handleRestartQuiz}
          >
            Пройти тест заново
          </button>
        </div>
      )}
    </div>
  );
};

export default Quiz;
