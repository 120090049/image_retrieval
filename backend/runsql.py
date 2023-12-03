#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql.connector



def movie_info(movieName):
   # db = mysql.connector.connect("localhost", "root", "Clp20020528!", "movies", charset='utf8')
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
         print ("MID=%s,name=%s,year=%s,boxOffice=%s,country=%s,mark=%s,reviewers=%s,director=%s,picture=%s" % \
             (MID, name, year, boxOffice, country,mark,reviewers,director,picture))
   except:
      print ("Error: unable to fetch data")
   db.close()
   return (MID, name, year, boxOffice, country,mark,reviewers,director,picture)


if __name__=="__main__":
   print(movie_info("The Shawshank Redemption"))
