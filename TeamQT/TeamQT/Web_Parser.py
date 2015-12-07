import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tkinter import *


class JSON_Parser:
    class JsonObject:
        def __init__(self, d):
            self.__dict__ = d

    def pythonToJson(self, data):
        return json.dump(data, ensure_ascii=False)

    def jsonToPython(self, data):
        return json.loads(data)

    def jsonToPython(self, data):
        return json.loads(data, object_hook=self.JsonObject)

    def request_Melon(self, searchKeyword):
        #http://apis.skplanetx.com/melon/artists?format=json&appKey=1dbcb88b-a238-392a-8bd6-3e44565bbe75&version=1&page=0&count=50&searchKeyword=
        self.version = 1
        self.format = 'json'
        self.appkey1 = '345e9f53-3eae-3fed-988d-6127852f2633'
        self.appkey2 = 'fbb12dba-c982-36f3-8a76-7135acea6510'
        self.page = 0
        self.count = 50

        self.url = 'http://apis.skplanetx.com/melon/artists?format=' + self.format
        self.url += '&appKey=' + self.appkey1
        self.url += '&version=' + str(self.version)
        self.url += '&page=' + str(self.page)
        self.url += '&count=' + str(self.count)
        self.url += '&searchKeyword=' + str(searchKeyword)
        
        try:
            while True:
                self.data = urlopen(self.url)
                self.data = self.data.read().decode(encoding = 'utf-8')
                self.dic = self.jsonToPython(self.data).melon
                #print('Pages : ', self.page)
                #print('totalPages : ', self.dic.totalPages)
                #print('Count : ', self.count)
                #print('totalCount : ', self.dic.totalCount)

                if self.dic.totalCount != self.count or self.dic.totalPages != self.page:
                    self.count = self.dic.totalCount
                    self.page = self.dic.totalPages
                else:
                    break;
        
            list = self.dic.artists.artist
            reList = []
            for item in list:   #artistName, sex, nationalityName, actTypeName, genreNames
                if item.nationalityName == '대한민국':
                    #print('artistName : ', item.artistName)
                    #print('sex : ', item.sex)
                    #print('nationalityName : ', item.nationalityName)
                    #print('actTypeName : ', item.actTypeName)
                    #print('genreNames : ', item.genreNames, '\n')
                    reList.append(item.artistName)
                
        except AttributeError:
            print('AttributeError')
            reList = []
        except UnicodeEncodeError:
            print('UnicodeEncodeError')
            reList = []
        except:
            print('Key limit! Last keyword : ', searchKeyword)
        
        return reList


class URL_Parser:
    def parse_MusicBrain(self):
        self.url = 'http://musicbrainz.org/area/b9f7d640-46e8-313e-b158-ded6d18593b3/artists?page=1'
        self.l = []
        self.data = urlopen(self.url)
        self.soup = BeautifulSoup(self.data.read(), from_encoding = 'utf-8')
    
        for self.link in self.soup('a'):
            if 'href' in dict(self.link.attrs):
                if self.link['href'].find('page=') != -1:
                    self.url, self.t = self.link['href'].split('page=')
                    self.l.append(self.t)
    
        self.page = max(self.l)
        self.l = []
    
        for self.i in range(int(self.page)):
            self.urli = self.url+'page='+str(self.i+1)
            self.data = urlopen(self.urli)
            self.soup = BeautifulSoup(self.data.read(), from_encoding = 'utf-8')
        
            print(self.i+1, '번째 페이지 파싱중')
            for self.link in self.soup('a'):
                if 'href' in dict(self.link.attrs):
                    if 'title' in dict(self.link.attrs):
                        if 'class' not in dict(self.link.attrs):
                            try:
                                print(self.link['title'])
                                self.l.append(self.link['title'])
                            except:
                                print('unicode Exception')  # ô
                                pass
        return self.l