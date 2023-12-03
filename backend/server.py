#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql.connector
from service import Service
import cv2
import numpy as np

class Server:
   def __init__(self):
      self.status = "stopped"
      self.service = Service()
   
   def test(self):
      print("test")
      
   # name -> index
   def movie_info(self, movieName):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID`\
            WHERE MOVIE.`NAME` = \"" + movieName + "\""
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            #打印结果
            # print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s" % \
            #    (MID, name, year, boxOffice, country,mark,reviewers,director,picture))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture)

   def movie_country(self, country):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID`\
            WHERE MOVIE.`COUNTRY` = \"" + country + "\""
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture)

   def movie_type(self, type):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID` LEFT JOIN MOVIETYPE on MOVIE.`MID` = MOVIETYPE.`MID` LEFT JOIN MTYPE ON MOVIETYPE.`TID` = MTYPE.`TID` \
            WHERE MTYPE.`TYPENAME` = \"" + type + "\""
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            typeName = row[17]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s,typeName =%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName)

   def movie_year(self, year):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID`\
            WHERE MOVIE.`YEAR` = " +str(year)
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture)

   def movie_year_country(self, year,country):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID`\
            WHERE MOVIE.`YEAR` = " +str(year) + " AND MOVIE.`COUNTRY` = \"" + country + "\""
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture)

   def movie_type_country(self, type,country):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID` LEFT JOIN MOVIETYPE on MOVIE.`MID` = MOVIETYPE.`MID` LEFT JOIN MTYPE ON MOVIETYPE.`TID` = MTYPE.`TID` \
            WHERE MTYPE.`TYPENAME` = \"" + type + "\"" + " AND MOVIE.`COUNTRY` = \"" + country + "\""
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            typeName = row[17]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s,typeName =%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName)

   def movie_type_year(self, type,year):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID` LEFT JOIN MOVIETYPE on MOVIE.`MID` = MOVIETYPE.`MID` LEFT JOIN MTYPE ON MOVIETYPE.`TID` = MTYPE.`TID` \
            WHERE MTYPE.`TYPENAME` = \"" + type + "\"" + " AND MOVIE.`YEAR` = " + str(year)
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            typeName = row[17]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s,typeName =%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName)

   def movie_type_country_year(self, type,country,year):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID` LEFT JOIN MOVIETYPE on MOVIE.`MID` = MOVIETYPE.`MID` LEFT JOIN MTYPE ON MOVIETYPE.`TID` = MTYPE.`TID` \
            WHERE MTYPE.`TYPENAME` = \"" + type + "\"" + " AND MOVIE.`COUNTRY` = \"" + country + "\"" + " AND MOVIE.`YEAR` = " + str(year)
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            typeName = row[17]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s,typeName =%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName)

   def movie_type_country_year_director(self, type,country,year,director):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID` LEFT JOIN MOVIETYPE on MOVIE.`MID` = MOVIETYPE.`MID` LEFT JOIN MTYPE ON MOVIETYPE.`TID` = MTYPE.`TID` \
            WHERE MTYPE.`TYPENAME` = \"" + type + "\"" + " AND MOVIE.`COUNTRY` = \"" + country + "\"" + " AND MOVIE.`YEAR` = " + str(year) + " AND DIRECTOR.`NAME` = \"" + director + "\""
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            typeName = row[17]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s,typeName =%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName)

   def movie_type_country_director(self, type,country,director):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID` LEFT JOIN MOVIETYPE on MOVIE.`MID` = MOVIETYPE.`MID` LEFT JOIN MTYPE ON MOVIETYPE.`TID` = MTYPE.`TID` \
            WHERE MTYPE.`TYPENAME` = \"" + type + "\"" + " AND MOVIE.`COUNTRY` = \"" + country + "\"" " AND DIRECTOR.`NAME` = \"" + director + "\""
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            typeName = row[17]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s,typeName =%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName)

   def movie_type_year_director(self,type,year,director):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID` LEFT JOIN MOVIETYPE on MOVIE.`MID` = MOVIETYPE.`MID` LEFT JOIN MTYPE ON MOVIETYPE.`TID` = MTYPE.`TID` \
            WHERE MTYPE.`TYPENAME` = \"" + type + "\"" + " AND MOVIE.`YEAR` = " + str(year) + " AND DIRECTOR.`NAME` = \"" + director + "\""
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            typeName = row[17]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s,typeName =%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName)

   def movie_year_director(self,year,director):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID` LEFT JOIN MOVIETYPE on MOVIE.`MID` = MOVIETYPE.`MID` LEFT JOIN MTYPE ON MOVIETYPE.`TID` = MTYPE.`TID` \
            WHERE MOVIE.`YEAR` = " + str(year) + " AND DIRECTOR.`NAME` = \"" + director + "\""
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            typeName = row[17]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s,typeName =%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName)

   def movie_director(self,director):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN DIRECTOR ON MOVIE.`DID` = DIRECTOR.`DID` LEFT JOIN COVER ON MOVIE.`MID` = COVER.`MID` LEFT JOIN MOVIETYPE on MOVIE.`MID` = MOVIETYPE.`MID` LEFT JOIN MTYPE ON MOVIETYPE.`TID` = MTYPE.`TID` \
            WHERE DIRECTOR.`NAME` = \"" + director + "\""
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         for row in results:
            MID = row[0]
            name = row[1]
            year = row[2]
            boxOffice = row[3]
            country = row[4]
            mark = row[7]
            reviewers = row[8]
            director = row[11]
            picture = row[13]
            typeName = row[17]
            #打印结果
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s,typeName =%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture,typeName)

   def insert(self,name,year,movie_dir,country,boxOffice = 100000,totalFrame = 10,frameRate = 10,mark= 9.2,reviewers = 10000,DID = 2,totalTime = 10,directorName = "MAGG",Mtypes = ["Drama"],cover = '1111',MID = 0):
      # 打开数据库连接
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()
      
      cursor.execute('SELECT COUNT(*) FROM MOVIE')
      result = cursor.fetchall()
      MID = result[0][0] + 1 #change the MID
      
      #need to update the totalTime and totalFrame before insert
      
      cap = cv2.VideoCapture(movie_dir)
      totalFrame = cap.get(cv2.CAP_PROP_FRAME_COUNT) # 获取帧数
      frameRate = cap.get(cv2.CAP_PROP_FPS) # 获取帧速
      print("帧速：", frameRate)
      totalTime = totalFrame / frameRate
      print("帧数 =", totalFrame)
      
      # SQL 插入语句
      sql = "INSERT INTO MOVIE(MID, \
         NAME, YEAR, BOXOFFICE, COUNTRY,TOTALFRAME,FRAMERATE,MARK,REVIEWERS,DID,TOTALTIME) \
         VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)" % \
         (MID,"\""+name+"\"",year,boxOffice,"\""+country+"\"",totalFrame,frameRate,mark,reviewers,DID,totalTime)

      try:
         cursor.execute(sql)
         db.commit()
         print("finish insert movie")
      except:
         db.rollback()
         print("error in movie table")

      sql2 = "INSERT INTO DIRECTOR(DID, \
         NAME) \
         VALUES (%s, %s)" % \
         (DID,"\""+directorName+"\"")
      try:
         cursor.execute(sql2)
         db.commit()
         print("finish insert director")
      except:
         db.rollback()
         print("error in director table")
      #cover table  
      sql3 = "INSERT INTO COVER(MID, \
         PICTURE) \
         VALUES (%s, %s)" % \
         (MID,"\""+cover+"\"")
      try:
         # 执行sql语句
         cursor.execute(sql3)
         # 提交到数据库执行
         db.commit()
         print("finish insert cover")
      except:
         # 发生错误时回滚
         db.rollback()
         print("error in cover table")
      #movie type table
      for type in Mtypes:
         sql14 = "SELECT TID from MTYPE WHERE TYPENAME = %s limit 1" % ("\""+type+"\"")
         sql15 = "SELECT COUNT(*) FROM MTYPE"
         try:#先获取Movie这个type存不存在
         # 执行SQL语句
            cursor.execute(sql14)
         # 获取所有记录列表
            results = cursor.fetchall()
         # print(results)
            if len(results) == 0:
               print("no exist type")
               try:
                  cursor.execute(sql15)
                  result = cursor.fetchall()
                  # print(result)
                  TID = result[0][0] + 1
               except:
                  TID = 99 * MID * DID
               sql6 = "INSERT INTO MTYPE(TID, \
               TYPENAME) \
               VALUES (%s, %s)" % \
               (TID,"\""+type+"\"")
               try:
               # 执行sql语句
                  cursor.execute(sql6)
                  # 提交到数据库执行
                  db.commit()
                  print("finish insert Mtype; current TID: " + str(TID))
               except:
               # 发生错误时回滚
                  db.rollback()
                  print("error in Mtype table") 
            else:
               TID = results[0][0]
               print ("current TID: "+str(TID))
         except:
            print ("Error: unable to fetch data")
         #获得TID以后把MID和TID都存进去 MOVIE TYPE这个多对多的表
         sql7 = "INSERT INTO MOVIETYPE(MID, TID) VALUES (%s, %s)" % (MID,TID)
         try:
         # 执行sql语句
            cursor.execute(sql7)
         # 提交到数据库执行
            db.commit()
            print("finish movie_type insert")
         except:
         # 发生错误时回滚
            db.rollback()
            print("error in movie_type table")
         
         #存frame那边的数据
         frames = self.service.get_feature_from_video(movie_dir) #记得改这里，函数封装以后
         frameID = 0
         for frame in frames:
            try:
               bytes_feature = frame.tobytes()
               cursor.execute('insert into frame values(%s,%s,%s)',([MID,frameID,bytes_feature]))
            except:
               print("error in frame table"+ str(frameID))
            frameID += 1
           
      # 关闭数据库连接
      db.close()
   
   def movie_features(self, movieName):
      db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 查询语句
      
      sql = "SELECT * FROM MOVIE LEFT JOIN FRAME ON MOVIE.`MID` = FRAME.`MID`\
            WHERE MOVIE.`NAME` = \"" + movieName + "\""
      try:
         # 执行SQL语句
         cursor.execute(sql)
         # 获取所有记录列表
         results = cursor.fetchall()
         # print(results)
         if len(results) == 0:
            print("no result")
            return
         
         row = results[0]
         totalFrame = row[5]
         totalTime = row[10]
         featuresInDB = np.empty((0, 1))
         for row in results:
            MID = row[0]
            frameNo = row[12]
            frameExtra = row[13]
            featuresInDB = np.append(featuresInDB, np.array([[frameExtra]]), axis=0)
            #打印结果
            print ("MID=%s,totalFrame=%s,totalTime=%s,frameNo=%s,frameExtra=%s" % \
               (MID, totalFrame, totalTime, frameNo, frameExtra))
      except:
         print ("Error: unable to fetch data")
      db.close()

      return (featuresInDB, totalFrame, totalTime)
   
   def retrieve_img(self, movie_name, img):
      (featuresInDB, totalFrame, totalTime) = self.movie_features(movie_name)
      img_feature = self.service.get_feature_from_img(img)
      print(img_feature.shape)
      print(featuresInDB.shape)
      print(totalFrame)
      print(totalTime)
      index, metaRes = self.service.feature_cmp(img_feature, featuresInDB, totalFrame, totalTime)
      print(metaRes)
      return metaRes


if __name__=="__main__":
   # server = Server()
   # print(server.movie_info("The Shawshank Redemption"))
   db = mysql.connector.connect(host="localhost", user="root", password="Clp20020528!", database="movies", charset='utf8')
   db.close()
   
   