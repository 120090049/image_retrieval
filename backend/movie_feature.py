import MySQLdb
import numpy as np

def movie_features(movieName):
   db = MySQLdb.connect("localhost", "root", "123456", "movies", charset='utf8' )

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