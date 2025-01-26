import re
import nltk
from bs4 import BeautifulSoup
import requests
import csv
import xlsxwriter

GenericLong = {}
Auditor = {}
Currencies = {}
DatesAndNumbers = {}
Generic = {}
Geographic = {}
Names = {}
positive = {}
negative = {}
punctuations = {'!': 1,
                '?': 1,
                ',': 1,
                '.': 1
                }
P_pronoun = {'I': 1,
             'i': 1,
             'WE': 1,
             'we': 1,
             'MY': 1,
             'my': 1,
             'OUR': 1,
             'our': 1,
             'us': 1}

positive_score = 0
negative_score = 0
polarity_score = 0
subjectivity_score = 0
avg_sentence_length = 0
percentage_of_complex_words = 0
fog_index = 0
average_number_of_words_per_sentence = 0
complex_word_count = 0
syllable_per_word = 0
personal_pronoun = 0
avg_word_length = 0
words_after_cleaning = 0
words = 0
sentences = 0
characters = 0
url_id = 36

urls = []
link = open('url.csv', "r", encoding="utf-8")
csv_reader = csv.DictReader(link)

workbook = xlsxwriter.Workbook('Output Data Structure.xlsx')
worksheet = workbook.add_worksheet()
rows = 0
col = 0
worksheet.write('A1', 'URL_ID')
worksheet.write('B1', 'URL')
worksheet.write('C1', 'POSITIVE SCORE')
worksheet.write('D1', 'NEGATIVE SCORE')
worksheet.write('E1', 'POLARITY SCORE')
worksheet.write('F1', 'SUBJECTIVITY SCORE')
worksheet.write('G1', 'AVG SENTENCE LENGTH')
worksheet.write('H1', 'PERCENTAGE OF COMPLEX WORDS')
worksheet.write('I1', 'FOG INDEX')
worksheet.write('J1', 'AVG NUMBER OF WORDS PER SENTENCE')
worksheet.write('K1', 'COMPLEX WORD COUNT')
worksheet.write('L1', 'WORD COUNT')
worksheet.write('M1', 'SYLLABLE PER WORD')
worksheet.write('N1', 'PERSONAL PRONOUNS')
worksheet.write('O1', 'AVG WORD LENGTH')



# FUNCTION TO COUNT SYLLABLES
def count_syllables(word):
    z = len(
        re.findall('(?!e$)[aeiouy]+', word, re.I) +
        re.findall('^[^aeiouy]*e$', word, re.I)
    )
    if len(word) > 2 and word[-1] == 's' and word[-2] == 'e':
        z -= 1
    elif len(word) > 2 and word[-1] == 'd' and word[-2] == 'e':
        z -= 1
    return z


# CONVERTS THE TEXT FILE TO DICTIONARY
def Convert_Into_Dict(text_file, dictionary):
    with open(text_file, encoding='latin-1') as topo_file:
        for line in topo_file:
            line = line.strip()
            dictionary[line] = 1


Convert_Into_Dict('StopWords_Auditor.txt', Auditor)
Convert_Into_Dict('StopWords_Currencies.txt', Currencies)
Convert_Into_Dict('StopWords_DatesandNumbers.txt', DatesAndNumbers)
Convert_Into_Dict('StopWords_Generic.txt', Generic)
Convert_Into_Dict('StopWords_GenericLong.txt', GenericLong)
Convert_Into_Dict('StopWords_Geographic.txt', Geographic)
Convert_Into_Dict('StopWords_Names.txt', Names)
Convert_Into_Dict('positive-words.txt', positive)
Convert_Into_Dict('negative-words.txt', negative)

for row in csv_reader:
    rows += 1
    url_id += 1
    print(row['URL'])
    url = row['URL']
    headers = {
        'user-agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.14.1) Presto/2.12.388 Version/12.16'
    }
    # GETS THE RESPONSE
    response = requests.get(url, headers=headers)
    # CONVERTS THE RESPONSE IN A READABLE TEXT
    soup = BeautifulSoup(response.text, 'lxml')
    # IGNORING UNREACHABLE WEBPAGES
    if soup.title.text != 'Page not found - Blackcoffer Insights':
        # STORES THE TITLE OF THE WEBPAGE TO X
        x = soup.title.text
        # STORES THE CONTENT OF THE WEBPAGE TO Y
        y = soup.findAll(attrs={'class': 'td-post-content'})[0].text
        # CREATING THE TEXT FILE
        f = open(x, "w")
        f.write(y)
        # CONVERTS THE PARAGRAPH INTO SENTENCES
        sentence = nltk.sent_tokenize(y)
        sentences = len(sentence)
        # CONVERTS INTO WORDS
        y = y.split()

        for i in y:
            # Total words
            words += 1
            # COUNTS THE NUMBER OF SYLLABLES
            syllable_per_word = count_syllables(i)
            # CLEAN WORDS
            if i not in Auditor or Currencies or DatesAndNumbers or Generic or GenericLong or Geographic or Names or punctuations:
                words_after_cleaning += 1

            if i in positive:
                positive_score += 1

            if i in negative:
                negative_score += 1

            if syllable_per_word > 2:
                complex_word_count += 1

            if i in P_pronoun:
                personal_pronoun += 1

            for character in i:
                characters += 1

        # print(positive_score)
        # print(negative_score)
        # print(personal_pronoun)
        # print(complex_word_count)
        # print(words_after_cleaning)
        # print(syllable_per_word)
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        # print(polarity_score)
        subjectivity_score = (positive_score + negative_score) / (words_after_cleaning + 0.000001)
        # print(subjectivity_score)
        avg_sentence_length = words / sentences
        # print(avg_sentence_length)
        percentage_of_complex_words = complex_word_count / words
        # print(percentage_of_complex_words)
        fog_index = 0.4 * (avg_sentence_length + percentage_of_complex_words)
        # print(fog_index)
        average_number_of_words_per_sentence = words / sentences
        # print(average_number_of_words_per_sentence)
        avg_word_length = characters / words
        # print(avg_word_length)
        worksheet.write(rows, col, url_id)
        worksheet.write(rows, col + 1, url)
        worksheet.write(rows, col + 2, positive_score)
        worksheet.write(rows, col + 3, negative_score)
        worksheet.write(rows, col + 4, polarity_score)
        worksheet.write(rows, col + 5, subjectivity_score)
        worksheet.write(rows, col + 6, avg_sentence_length)
        worksheet.write(rows, col + 7, percentage_of_complex_words)
        worksheet.write(rows, col + 8, fog_index)
        worksheet.write(rows, col + 9, average_number_of_words_per_sentence)
        worksheet.write(rows, col + 10, complex_word_count)
        worksheet.write(rows, col + 11, words_after_cleaning)
        worksheet.write(rows, col + 12, syllable_per_word)
        worksheet.write(rows, col + 13, personal_pronoun)
        worksheet.write(rows, col + 14, avg_word_length)

workbook.close()


