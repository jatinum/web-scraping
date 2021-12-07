
import requests
from bs4 import BeautifulSoup
import textstat
from textblob import TextBlob
import pandas as pd

import pandas as pd
read1 = pd.read_excel('Input-2.xlsx')
all_extracted = []
for x in range(len(read1)):
    url = read1['URL'][x]
    id = int(read1['URL_ID'][x])
    
    try:
        
        
        # --------------------------- url to be extract-----------------------#
        # url = "https://www.insights.blackcoffer.com/how-does-ai-help-to-monitor-retail-shelf-watches/"
        # ---------------------------------------------------------------------

        # --------------------------- bypassing to login as a user -----------------------#
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:60.0)Gecko/20100101 FireFox/60.0'}
        # ---------------------------------------------------------------------

        # -------------------------- requesting for extracting ---------------------
        get_content = requests.get(url,headers=headers)
        # -------------------------- converting extracted data into html view ---------------------
        
        take_in_html = get_content.content
        print(f'url {id} data scraped Successfully')
    except:
            print(f'url {id} data didn\'t scraped')
    # -------------------------- making soup of extracted data to work on it ---------------------
    soup1 = BeautifulSoup(take_in_html,'html.parser')
    # -------------------------- --------------------------------------------

    # -------------------------- Title extracting ---------------------
    title= soup1.find('h1',attrs={'class':'entry-title'}).get_text()
    # print(title)

    # -------------------------- paragraph extracting ---------------------
    para= soup1.find_all('p')
    # -------------------------- converting class to text ---------------------
    paragraph = ''
    for i in para:
        paragraph = paragraph+i.get_text()
        # print (i)
    # -------------------------- ------------------------------------------

    # -------------------------- Extracted data ---------------------
    fetch_text = title+paragraph
    # -------------------------- ------------------------------------------

    # ======Polarity,subjectivity,score
    # -------------------------- using textblob to get polarity ---------------------
    textb_object = TextBlob(fetch_text)
    # print(textb_object.sentiment)
    Polarity = TextBlob(fetch_text).sentiment.polarity
    subjectivity = TextBlob(fetch_text).sentiment.subjectivity
    # -------------------------- ------------------------------------------

    # -------------------------- creating score options ---------------------
    def getscore(score):
        if score<0:
            return 'Negative'
        elif score == 0:
            return 'Nutral'
        else:
            return 'Positive'

    # -------------------------- getting score (positve/neutral/negative) ---------------------
    score1 = getscore(Polarity)
    # print(score1)
    # --------------------------------- ------------------------------------------


    # -------------------------- funtion to calculations ---------------------
    def calculate(text):
        # cleaning text--------
        remove = "!,-@#$%''^""&*()-_+/\[]"
        new = text
        for i in remove:
            new = new.replace(i,"")
        #----------------------------
        b=new.count(' ')
        avg_sen_len = (len(new)-b)/(len(new.split('.')))
        total_sen = len(new.split('.'))
        avg_word_len = (len(new)-b)/(len((' '.join(new.split('.'))).split()))
        word_list = (' '.join(new.split('.'))).split()
        total_words = len((' '.join(new.split('.'))).split())
        filter_data = new
        return avg_sen_len,avg_word_len,total_words,total_sen,filter_data,word_list
    # -------------------------- ------------------------------------------

    # -------------------------- getting required calculation ---------------------
    avg_sen_length = calculate(fetch_text)[0]
    avg_word_length = calculate(fetch_text)[1]
    total_words = calculate(fetch_text)[2]
    total_sen = calculate(fetch_text)[3]
    filter_data = calculate(fetch_text)[4]
    word_list = calculate(fetch_text)[5]
    # -------------------------- ------------------------------------------

    # Percentage of complex words = 
            # missing------ don't know sentax

    # -------------------------- getting FOG index using textstat ---------------------
    Fog_index = textstat.gunning_fog(filter_data)

    #-------------------- avg number of words per sentence
    avg_word_per_sentence = total_words/total_sen
    # complex word Count
        # missing - not found

    #---------------getting syllable using textstat----------
    syllable = (textstat.syllable_count(fetch_text))
    syllable_per_word = round(syllable/total_words,1)
    # print('total syllable',syllable)
    # print('syllable per word',round(syllable_per_word,1))

    # personal pronouns
    prp = ['i','I','we','We','WE','my','My','MY','ours','Ours','OURS','us']
    count = 0
    for i in word_list:
        if i in prp:
            count = count+1
        else: pass
    personal_pronouns = count
    # avg word length
    # avg_word_length
    
    # all_extracted = [[url,Polarity,subjectivity,avg_sen_length,Fog_index,avg_word_per_sentence,total_words,syllable_per_word,personal_pronouns,avg_word_length]]
    all_extracted.insert(total_words,[url,Polarity,subjectivity,avg_sen_length,Fog_index,avg_word_per_sentence,total_words,syllable_per_word,personal_pronouns,avg_word_length])

    df = pd.DataFrame(all_extracted, columns = ['url','Polarity','Subjectivity','Average sentence length','Fog index',' average word per sentence', 'word count', 'syllable per word', 'personal pronoun','average word length'])
# print (df)
df.to_csv('output.csv',index=False)
print('thank you____ created by _ Jatin')

# this is a assignment for done by Jatin on -29-11-2021