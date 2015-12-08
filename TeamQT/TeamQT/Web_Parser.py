import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib import parse
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

    def parsingToMelon(self, searchKeyword):
        self.version = 1
        self.format = 'json'
        self.appkey1 = '345e9f53-3eae-3fed-988d-6127852f2633'
        self.appkey2 = 'fbb12dba-c982-36f3-8a76-7135acea6510'
        self.page = 0
        self.count = 50

        try:
            while True:     # totalCount와 totalPages로 count와 page를 맞추어 query를 던진다.
                self.url = 'http://apis.skplanetx.com/melon/songs?format=' + self.format
                self.url += '&appKey=' + self.appkey1
                self.url += '&version=' + str(self.version)
                self.url += '&page=' + str(self.page)
                self.url += '&count=' + str(self.count)
                self.url += '&searchKeyword=' + parse.quote(searchKeyword)
                
                self.data = urlopen(self.url)
                self.data = self.data.read().decode(encoding = 'utf-8')
                self.dic = self.jsonToPython(self.data).melon

                if self.dic.totalCount != self.count or self.dic.totalPages != self.page:
                    self.count = self.dic.totalCount
                    self.page = self.dic.totalPages
                else:
                    break;
        
            
            l = self.dic.songs.song
            reList = []
            for i in range(len(l)):
                tList = []
                tList.append(l[i].songName)
                tList.append(l[i].artists.artist[0].artistName)
                tList.append(l[i].albumName)
                reList.append(tList)

        except AttributeError:
            print('AttributeError\n', self.data,'\n',searchKeyword)
            reList = []
        except UnicodeEncodeError:
            print('UnicodeEncodeError')
            reList = []
        except e:
            print('Key limit! Last keyword : ', searchKeyword, e)
        
        return reList

    def matchSongname(self, nameList):
        length = len(nameList)
        name = ''
        names = []
        realSongName = []
        realArtistName = []
        
        for i in range (length):
            for num in range(length-i):
                if name == '':
                    name = nameList[num+i]
                else:
                    name = name + ' ' + nameList[num+i]
                print(name)
                names.append(name)
            name = ''
        
        inNum = 0
        for name in names:
            l = self.parsingToMelon(name)
                
            for i in range(len(l)):
                if l[i][1] in names:
                    #print(l[i][1])
                    realArtistName.append(l[i][1])
                    #break
                try:
                    if l[i][0].index(name):
                        print(l[i][0])
                        realSongName.append(l[i][0])
                        #break
                except ValueError:
                    pass
            try:
                index = realArtistName.index(name)
                artist = realArtistName[index]
            except:
                pass
            try:
                if realSongName[inNum].index(name):
                    song = realSongName[inNum]
                    inNum += 1
                #index = realSongName.index(name)
            except:
                pass

        print(artist)
        print(song)

    def request_Melon(self, searchKeyword):
        #http://apis.skplanetx.com/melon/artists?format=json&appKey=345e9f53-3eae-3fed-988d-6127852f2633&version=1&page=0&count=50&searchKeyword=
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