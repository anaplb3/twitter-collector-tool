from senticnet.babelsenticnet import BabelSenticNet
import codecs
from auth import sentiment_boolean
import csv

class Sentiment():
    def sentiment_avg(self, text):
        if sentiment_boolean == False:
            return True
        sn = BabelSenticNet('pt')
        list_polarity = []
        qtd_words = len(text)
        temp = text.split()
        avg_n = 0
        for i in range(len(temp)):
            try:
                polarity_value = sn.polarity_value(self.treatment_string(temp[i]))
                list_polarity.append(polarity_value)
            except:
                qtd_words-=1
                i+=1

        avg_n = self.avg(list_polarity, qtd_words)
        if avg_n > 0.003 or avg_n < -0.003:
            return True
        else:
            return False
            
    def avg(self,lst, size):
        return sum(lst) / size

    def treatment_string(self,string):
        string = string.lower()
        sign = ['.',',','!','?','(',')','´','*','#','@',';',':']
        for i in sign:
            try:
                string = string.replace(i,'')
                return string
            except:
                pass

    def adjectives(self):
        dir_ = 'tweetcollector/data.json'
        data = codecs.open(dir_,'r','utf8')
        list = data.readline()
        data.close()
        return json.loads(json_string)
        #return list.split(',')

    def getData(self):
        data = []
        with open("tweetcollector/data3.csv", 'r') as file:
            next(file)
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data
