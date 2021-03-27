import psycopg2, difflib, time
from unicodedata import normalize
from auth import dbname,host,password,port,user
from tweetcollector.senticnet_instance import Sentiment
from datetime import datetime
from datetime import date
import os
from config import DEV_CFG, PROD_CFG

class Database:
    def __init__(self):
        self.st = Sentiment()
        try:
            self.connect()
        except Exception as e:
            print("Failure in connection: {}".format(str(e)))
        self.create_table()
        self.all = self.get_all()

    def environment_config(self):
        if os.environ['ENV'] == 'prod':
            return PROD_CFG
        else:
            return DEV_CFG
    
    def connect(self):
        cfg = self.environment_config()
        self.connection = psycopg2.connect(cfg["database_url"], sslmode=cfg["sslmode"])
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_table_command = ("CREATE TABLE IF NOT EXISTS tweets(id serial PRIMARY KEY, id_twitter varchar(50),\
        name varchar(500), content text, image varchar(300), followers integer, location varchar(200),\
        classification varchar(216), query varchar(200), state varchar(200), colected_at TIMESTAMP DEFAULT NOW(), created_at TIMESTAMP);")
        self.cursor.execute(create_table_command)
        create_date_table = ''' CREATE TABLE IF NOT EXISTS search_status(since varchar(50), state varchar(200))'''
        self.cursor.execute(create_date_table)

    def insert(self,id_twitter,name,text,image,followers,location, query, state, created_at):
        print("entrou no insert")
        insert_command = ("INSERT INTO tweets(id_twitter, name, content, image, followers, location, query, state, created_at)\
         VALUES('%s','%s','%s','%s','%d','%s','%s', '%s', '%s')" 
        %(id_twitter, self.str_(name), self.str_(text), image, followers, self.str_(location), query, state, created_at))
        self.cursor.execute(insert_command)

    def get_all(self):
        sql = "SELECT id_twitter,content FROM public.tweets ORDER BY id ASC"
        self.cursor.execute(sql)
        all = [r for r in self.cursor.fetchall()]
        return all

    def get_since_date(self, state):
        sql = "SELECT since from search_status where state = '{}'".format(state)
        self.cursor.execute(sql)
        try:
            return self.cursor.fetchone()[0]
        except:
            return '2021-01-17'  
        
        '''if len(result) == 0 or result[0] == False:
            return '2021-01-17'
        else:
            return date.today().strftime("%Y-%m-%d")'''
    

    def set_since_date(self, date, state):
        sql = "UPDATE search_status SET since = '{}' WHERE state = '{}'".format(date, state)
        self.cursor.execute(sql)

    def get_all_states(self):
        sql = "SELECT DISTINCT state FROM tweets"
        self.cursor.execute(sql)
        return [state for states in self.cursor.fetchall()]

    def get_state_info(self, state):
        sql = "SELECT COUNT(content) AS count_tweet, MAX(created_at) AS last_tweeted, MAX(colected_at) AS last_collected FROM tweets WHERE state = '{}'".format(state)
        self.cursor.execute(sql)
        return [info for infos in self.cursor.fetchall()]

    def main(self, id_twitter, name, text, image, followers, location, query, state, created_at):
        if self.st.sentiment_avg(text):
            diff = self.close_matches(text)
            if diff:
                print("tweet igual")
                pass
            else:
                print("tweet add")
                self.all.append((id_twitter,text))
                self.insert(id_twitter,name,text,image,followers,location, query, state, created_at)
        else:
            print("entrou no else")
    
    def delete(self, id):
        sql = "DELETE FROM public.tweets WHERE id = %s" %id
        self.cursor.execute(sql)

    def close_matches(self, text):
        matches = []
        rage_text = int(len(text)/3)
        for i in self.all:
            count = 0
            for y in range(rage_text):
                try:
                    if i[1][y]==text[y]:
                        count+=1
                except:
                    break
                if y == 0 and count==0:
                    break
            if count == rage_text:
                matches.append(i)
        return matches

    def save(self, result, query, state):
        print("save")
        text = result.content
        '''try:
            text = result.content
        except:
            text = result.full_text'''
        id_twitter = result.id
        name = result.user.displayname
        img = result.user.profileImageUrl
        followers = result.user.followersCount
        location = result.user.location
        created_at = result.date
        self.main(id_twitter,name,text,img,followers,location, query, state, created_at)

    def str_(self,string):
        string = str(string)
        string = string.encode('utf-8').decode('utf-8')
        string = string.replace("'","´")
        string = string.replace('"',"\"")
        return string
