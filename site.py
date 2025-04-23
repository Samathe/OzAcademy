import React, { useState, useCallback, useMemo } from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search, ChevronDown, ChevronUp, BookOpen } from 'lucide-react';

// Выносим данные в отдельный файл
const subjects = [
  {
    id: 1,
    name: 'Математическая грамотность',
    icon: '📊',
    sections: [
      {
        id: 101,
        section: 'Количественные рассуждения',
        topics: [
          { id: 1001, title: 'Логические задания с числовыми значениями' },
          { id: 1002, title: 'Текстовые задачи с уравнениями и буквенными выражениями' },
          { id: 1003, title: 'Вычисление процентов и статистические задачи' }
        ]
      },
      {
        id: 102,
        section: 'Неопределенность',
        topics: [
          { id: 1004, title: 'Среднее арифметическое, размах, медиана и мода' },
          { id: 1005, title: 'Статистические таблицы, полигоны и гистограммы' },
          { id: 1006, title: 'Теория множеств, комбинаторика и вероятности' }
        ]
      },
      {
        id: 103,
        section: 'Изменение и зависимости',
        topics: [
          { id: 1007, title: 'Изменение одной величины в зависимости от другой' },
          { id: 1008, title: 'Последовательности и анализ табличных данных' }
        ]
      },
      {
        id: 104,
        section: 'Пространство и форма',
        topics: [
          { id: 1009, title: 'Геометрические и нестандартные задачи' },
          { id: 1010, title: 'Площадь и периметр фигур' },
          { id: 1011, title: 'Площадь поверхности тел' }
        ]
      }
    ]
  },
  {
    id: 2,
    name: 'Информатика',
    icon: '💻',
    sections: [
      {
        id: 201,
        section: 'Компьютерные системы',
        topics: [
          { id: 2001, title: 'Устройства компьютера' },
          { id: 2002, title: 'Компьютерные сети и их организация' }
        ]
      },
      {
        id: 202,
        section: 'Информационные процессы',
        topics: [
          { id: 2003, title: 'Представление и кодирование информации' },
          { id: 2004, title: 'Системы счисления' },
          { id: 2005, title: 'Логические основы компьютера' }
        ]
      },
      {
        id: 203,
        section: 'Компьютерное мышление',
        topics: [
          { id: 2006, title: 'Программирование на Python' },
          { id: 2007, title: 'Функции, рекурсия, строки, файлы, сортировки, графы' }
        ]
      },
      {
        id: 204,
        section: 'Программное обеспечение',
        topics: [
          { id: 2008, title: 'Аппаратное и программное обеспечение' }
        ]
      },
      {
        id: 205,
        section: 'Базы данных и веб',
        topics: [
          { id: 2009, title: 'Реляционные базы данных' },
          { id: 2010, title: 'SQL-запросы' },
          { id: 2011, title: 'Веб-проектирование' }
        ]
      }
    ]
  },
  {
    id: 3,
    name: 'Математика',
    icon: '🧮',
    sections: [
      {
        id: 301,
        section: 'Числа и выражения',
        topics: [
          { id: 3001, title: 'Действия с радикалами и выражениями' },
          { id: 3002, title: 'Абсолютные величины и степени' },
          { id: 3003, title: 'Тригонометрия' }
        ]
      },
      {
        id: 302,
        section: 'Уравнения и неравенства',
        topics: [
          { id: 3004, title: 'Линейные, квадратные и рациональные уравнения' },
          { id: 3005, title: 'Тригонометрические, иррациональные, показательные и логарифмические уравнения' },
          { id: 3006, title: 'Неравенства и системы неравенств' }
        ]
      },
      {
        id: 303,
        section: 'Системы уравнений и прогрессии',
        topics: [
          { id: 3007, title: 'Системы уравнений разных типов' },
          { id: 3008, title: 'Арифметические и геометрические прогрессии' }
        ]
      },
      {
        id: 304,
        section: 'Анализ и геометрия',
        topics: [
          { id: 3009, title: 'Математическое моделирование и анализ' },
          { id: 3010, title: 'Планиметрия' },
          { id: 3011, title: 'Стереометрия и векторы' }
        ]
      }
    ]
  }
];

// Компонент Тема
const Topic = ({ topic }) => (
  <li className="py-1 hover:bg-gray-50 rounded px-2 transition-colors">
    <a href={`/topic/${topic.id}`} className="text-gray-700 hover:text-blue-600 block">
      {topic.title}
    </a>
  </li>
);

// Компонент Раздел
const Section = ({ section, isActive, onToggle }) => {
  return (
    <div className="mb-3 border-l-2 border-gray-200 pl-3">
      <div
        className="flex items-center justify-between cursor-pointer py-2 hover:bg-gray-50 rounded px-2"
        onClick={onToggle}
      >
        <h4 className="font-medium text-gray-800">{section.section}</h4>
        {isActive ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
      </div>
      
      {isActive && (
        <ul className="ml-4 mt-2 space-y-1">
          {section.topics.map(topic => (
            <Topic key={topic.id} topic={topic} />
          ))}
        </ul>
      )}
    </div>
  );
};

// Компонент Предмет
const Subject = ({ subject, isActive, onToggle, activeSection, onSectionToggle }) => {
  return (
    <Card className="rounded-2xl shadow transition-all duration-200 hover:shadow-md overflow-hidden">
      <CardHeader
        className="cursor-pointer hover:bg-gray-50 p-4 flex flex-row items-center justify-between"
        onClick={onToggle}
      >
        <div className="flex items-center">
          <span className="text-2xl mr-3">{subject.icon}</span>
          <h3 className="text-lg font-semibold">{subject.name}</h3>
        </div>
        {isActive ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
      </CardHeader>
      
      {isActive && (
        <CardContent className="p-4 bg-gray-50">
          {subject.sections.map(section => (
            <Section
              key={section.id}
              section={section}
              isActive={activeSection === section.id}
              onToggle={() => onSectionToggle(section.id)}
            />
          ))}
        </CardContent>
      )}
    </Card>
  );
};

// Компонент для поиска
const SearchBar = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState('');
  
  const handleSearch = useCallback(() => {
    onSearch(searchTerm);
  }, [searchTerm, onSearch]);

  return (
    <div className="max-w-xl mx-auto flex items-center gap-2">
      <Input 
        placeholder="Поиск по темам, курсам..." 
        className="flex-grow"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
      />
      <Button 
        variant="outline" 
        className="px-4"
        onClick={handleSearch}
      >
        <Search size={20} />
      </Button>
    </div>
  );
};

// Главный компонент
export default function FreeEduHomePage() {
  const [activeSubject, setActiveSubject] = useState(null);
  const [activeSection, setActiveSection] = useState(null);
  const [filteredSubjects, setFilteredSubjects] = useState(subjects);

  const handleSubjectToggle = useCallback((subjectId) => {
    setActiveSubject(prev => prev === subjectId ? null : subjectId);
    setActiveSection(null);
  }, []);

  const handleSectionToggle = useCallback((sectionId) => {
    setActiveSection(prev => prev === sectionId ? null : sectionId);
  }, []);

  const handleSearch = useCallback((term) => {
    if (!term.trim()) {
      setFilteredSubjects(subjects);
      return;
    }
    
    const lowercasedTerm = term.toLowerCase();
    
    const filtered = subjects.map(subject => {
      // Проверяем, содержит ли название предмета искомый термин
      const matchesSubject = subject.name.toLowerCase().includes(lowercasedTerm);
      
      // Фильтруем разделы и темы, которые содержат искомый термин
      const filteredSections = subject.sections.map(section => {
        const matchesSection = section.section.toLowerCase().includes(lowercasedTerm);
        
        const filteredTopics = section.topics.filter(topic => 
          topic.title.toLowerCase().includes(lowercasedTerm)
        );
        
        // Если раздел содержит термин или в нем есть темы с термином, включаем его
        if (matchesSection || filteredTopics.length > 0) {
          return {
            ...section,
            topics: filteredTopics.length > 0 ? filteredTopics : section.topics
          };
        }
        return null;
      }).filter(Boolean);
      
      // Если предмет содержит термин или в нем есть подходящие разделы, включаем его
      if (matchesSubject || filteredSections.length > 0) {
        return {
          ...subject,
          sections: filteredSections
        };
      }
      return null;
    }).filter(Boolean);
    
    setFilteredSubjects(filtered);
    
    // Если найден только один предмет, автоматически раскрываем его
    if (filtered.length === 1) {
      setActiveSubject(filtered[0].id);
    }
  }, []);

  // Статистика (примерные данные)
  const stats = useMemo(() => ({
    subjects: subjects.length,
    sections: subjects.reduce((acc, subj) => acc + subj.sections.length, 0),
    topics: subjects.reduce((acc, subj) => 
      acc + subj.sections.reduce((secAcc, sec) => secAcc + sec.topics.length, 0), 0)
  }), []);

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Hero section */}
      <div className="bg-gradient-to-r from-blue-500 to-indigo-600 py-16 px-8 text-white">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-5xl font-bold mb-4">LearnFree</h1>
          <p className="text-xl mb-8 max-w-2xl">
            Бесплатные образовательные ресурсы для всех. Изучайте, практикуйтесь и развивайтесь в удобном для вас темпе.
          </p>
          <SearchBar onSearch={handleSearch} />
          
          <div className="flex flex-wrap gap-6 mt-10 text-center">
            <div className="bg-white bg-opacity-20 rounded-lg p-4 flex-1">
              <div className="text-3xl font-bold">{stats.subjects}</div>
              <div>Предметов</div>
            </div>
            <div className="bg-white bg-opacity-20 rounded-lg p-4 flex-1">
              <div className="text-3xl font-bold">{stats.sections}</div>
              <div>Разделов</div>
            </div>
            <div className="bg-white bg-opacity-20 rounded-lg p-4 flex-1">
              <div className="text-3xl font-bold">{stats.topics}</div>
              <div>Тем</div>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-8 py-12">
        <section>
          <div className="flex items-center gap-3 mb-8">
            <BookOpen size={24} className="text-blue-600" />
            <h2 className="text-2xl font-semibold">Доступные предметы</h2>
          </div>
          
          {filteredSubjects.length === 0 ? (
            <div className="text-center py-12 bg-gray-100 rounded-lg">
              <p className="text-gray-600">Ничего не найдено. Попробуйте изменить поисковый запрос.</p>
              <Button 
                variant="outline" 
                className="mt-4"
                onClick={() => {
                  setFilteredSubjects(subjects);
                  // Сбросить поле поиска (предполагается, что вы добавите соответствующий функционал)
                }}
              >
                Сбросить поиск
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredSubjects.map(subject => (
                <Subject 
                  key={subject.id}
                  subject={subject}
                  isActive={activeSubject === subject.id}
                  onToggle={() => handleSubjectToggle(subject.id)}
                  activeSection={activeSection}
                  onSectionToggle={handleSectionToggle}
                />
              ))}
            </div>
          )}
        </section>
        
        {/* Призыв к действию */}
        <section className="mt-16 bg-blue-50 rounded-2xl p-8 text-center">
          <h2 className="text-2xl font-bold mb-4">Готовы начать обучение?</h2>
          <p className="mb-6 max-w-2xl mx-auto">
            Присоединяйтесь к тысячам студентов, которые уже используют нашу платформу для
            получения знаний и развития навыков.
          </p>
          <div className="flex justify-center gap-4">
            <Button className="bg-blue-600 hover:bg-blue-700">
              Начать бесплатно
            </Button>
            <Button variant="outline">
              Узнать больше
            </Button>
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300 py-12 px-8 mt-12">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">LearnFree</h3>
            <p>Бесплатная образовательная платформа, делающая знания доступными для всех.</p>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Ссылки</h4>
            <ul className="space-y-2">
              <li><a href="#" className="hover:text-white">О нас</a></li>
              <li><a href="#" className="hover:text-white">Контакты</a></li>
              <li><a href="#" className="hover:text-white">Блог</a></li>
              <li><a href="#" className="hover:text-white">Политика конфиденциальности</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Подписаться</h4>
            <p className="mb-4">Получайте новости о новых курсах и материалах</p>
            <div className="flex">
              <Input placeholder="Ваш email" className="rounded-r-none" />
              <Button className="rounded-l-none">Подписаться</Button>
            </div>
          </div>
        </div>
        <div className="max-w-6xl mx-auto border-t border-gray-700 mt-8 pt-8 text-center">
           {new Date().getFullYear()} LearnFree. Все права защищены.
        </div>
      </footer>
    </main>
  );
}