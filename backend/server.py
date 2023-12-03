#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
from service import Service

class Server:
   def __init__(self):
      self.status = "stopped"
      self.service = Service()
          
   def movie_info(self, movieName):
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
            print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s" % \
               (MID, name, year, boxOffice, country,mark,reviewers,director,picture))
      except:
         print ("Error: unable to fetch data")
      db.close()
      return (MID, name, year, boxOffice, country,mark,reviewers,director,picture)

   def movie_country(self, country):
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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


   def insert(self,MID,name,year,boxOffice,country,totalFrame,frameRate,mark,reviewers,DID,directorName,Mtypes,cover,mp4):
      # 打开数据库连接
      db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

      # 使用cursor()方法获取操作游标 
      cursor = db.cursor()

      # SQL 插入语句
      sql = "INSERT INTO MOVIE(MID, \
         NAME, YEAR, BOXOFFICE, COUNTRY,TOTALFRAME,FRAMERATE,MARK,REVIEWERS,DID) \
         VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s)" % \
         (MID,"\""+name+"\"",year,boxOffice,"\""+country+"\"",totalFrame,frameRate,mark,reviewers,DID)
   
      try:
         # 执行sql语句
         cursor.execute(sql)
         # 提交到数据库执行
         db.commit()
         print("finish insert movie")
      except:
         # 发生错误时回滚
         db.rollback()
         print("error in movie table")
      #director table  
      sql2 = "INSERT INTO DIRECTOR(DID, \
         NAME) \
         VALUES (%s, %s)" % \
         (DID,"\""+directorName+"\"")
      try:
         # 执行sql语句
         cursor.execute(sql2)
         # 提交到数据库执行
         db.commit()
         print("finish insert director")
      except:
         # 发生错误时回滚
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
         frames = self.service.get_feature_from_video(mp4)
         frameID = 0
         for frame in frames:
            sql8 = "INSERT INTO FRAME(MID, FRAMENO, FRAMEEXTRA) VALUES (%s, %s, %s)" % (MID,frameID,frame)
            try:
            # 执行sql语句
               cursor.execute(sql8)
            # 提交到数据库执行
               db.commit()
               print("finish frame insert" + str(frameID))
            except:
            # 发生错误时回滚
               db.rollback()
               print("error in frame table"+ str(frameID))
            frameID += 1
      # 关闭数据库连接
      db.close()

if __name__=="__main__":
   server = Server()
   # print(server.movie_info("The Shawshank Redemption"))
   # print(server.movie_country("America"))
   # print(server.movie_type("Drama"))
   # print(server.movie_year(1994))
   # print(server.movie_year_country(1994,"America"))
   # print(server.movie_type_country("Drama","America"))
   # print(server.movie_type_year("Drama",1994))
   # print(server.movie_type_country_year("Drama","America",1994))
   # print(server.movie_type_country_year_director("Drama","America",1994,"Frank Darabont"))
   # print(server.movie_type_country_director("Drama","America","Frank Darabont"))
   # print(server.movie_type_year_director("Drama",1994,"Frank Darabont"))
   # print(server.movie_director("Frank Darabont"))
   server.insert(2,"The Godfather",1972,136381073,"America",720,23.9760239,9.2,1962081,2,"Francis Ford Coppola",["Drama","Crime"],"https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",'video.mp4')
   # print(server.movie_info("The Godfather"))
    