import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS users')
c.execute('DROP TABLE IF EXISTS questions')
c.execute('DROP TABLE IF EXISTS options')

c.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    highest_score INTEGER DEFAULT 0
)''')

c.execute('''CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL
)''')

c.execute('''CREATE TABLE options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER,
    option_text TEXT NOT NULL,
    FOREIGN KEY(question_id) REFERENCES questions(id)
)''')

computer_vision_questions = [
    {"question_text"
     : "Bilgisayar görüşünde kullanılan temel algoritmalardan biri nedir?", 
     "correct_answer": "  c. Canny Edge Detection"},

    {"question_text"
     : "Hangi yöntem görüntüdeki kenarları tespit etmek için kullanılır?", 
     "correct_answer": "A. Canny Edge Detection"},

    {"question_text"
     : "Derin öğrenmede kullanılan popüler bir mimari türü nedir?", 
     "correct_answer": "D. CNN"},

    {"question_text"
     : "Görüntü sınıflandırmada yaygın olarak kullanılan bir veri artırma tekniği nedir?", 
     "correct_answer": "B. Dönme"},

    {"question_text"
     : "Bilgisayar görüşünde kullanılan bir nesne tespit algoritması hangisidir?", 
     "correct_answer": "A. YOLO"}
]

computer_vision_options = [
    ["A. K-means", "B. PCA", "C. Canny Edge Detection", "D. Linear Regression"],

    ["A. Canny Edge Detection", "B. KNN", "C. SVM", "D. Naive Bayes"],

    ["A. RNN", "B. GAN", "C. LSTM", "D. CNN"],

    ["A. Normalizasyon", "B. Dönme", "C. Filtreleme", "D. Kümeleme"],

    ["A. YOLO", "B. Apriori", "C. K-Means", "D. Decision Tree"]
]

nlp_questions = [
    {"question_text"
     : "Doğal dil işleme alanında kullanılan bir dil modeli nedir?", 
     "correct_answer": "B. BERT"},

    {"question_text"
     : "Hangi teknik metin verisinden önemli özellikleri çıkarmak için kullanılır?", 
     "correct_answer": "A. TF-IDF"},

    {"question_text"
     : "Tokenizasyon nedir?", 
     "correct_answer": "C. Metinleri sözcüklere bölmek"},

    {"question_text"
     : "Sentiment analizi nedir?", 
     "correct_answer": "D. Metnin duygu durumunu analiz etmek"},

    {"question_text"
     : "Hangi algoritma metin sınıflandırmada sıkça kullanılır?", 
     "correct_answer": "B. Naive Bayes"}

]

nlp_options = [
    ["A. SVM", "B. BERT", "C. CNN", "D. KNN"],

    ["A. TF-IDF", "B. PCA", "C. LDA", "D. K-Means"],

    ["A. Metinleri büyük harfe dönüştürmek", "B. Metinleri parçalara ayırmak", "C. Metinleri sözcüklere bölmek", "D. Metinleri şifrelemek"],

    ["A. Metin çevirisi", "B. Metin özetleme", "C. Metin oluşturma", "D. Metnin duygu durumunu analiz etmek"],
    
    ["A. K-Means", "B. Naive Bayes", "C. Apriori", "D. PCA"]
]

def add_questions(topic, questions, options_list):
    for q, opts in zip(questions, options_list):
        c.execute('INSERT INTO questions (topic, question_text, correct_answer) VALUES (?, ?, ?)', 
                  (topic, q['question_text'], q['correct_answer']))
        question_id = c.lastrowid
        for option in opts:
            c.execute('INSERT INTO options (question_id, option_text) VALUES (?, ?)', 
                      (question_id, option))

add_questions('Computer Vision', computer_vision_questions, computer_vision_options)
add_questions('NLP', nlp_questions, nlp_options)

conn.commit()
conn.close()
