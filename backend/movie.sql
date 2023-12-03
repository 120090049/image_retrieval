use csc3170;

-- ALTER TABLE movie DROP FOREIGN KEY DID;
DROP TABLE IF EXISTS `director`;
CREATE TABLE `director` (
  `DID` mediumint(8),
  `name` varchar(255),
  PRIMARY KEY (`DID`)
);


DROP TABLE IF EXISTS `Mtype`;
CREATE TABLE `Mtype` (
  `TID` mediumint(8),
  `typeName` varchar(255),
  PRIMARY KEY (`TID`)
);

DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie` (
  `MID` mediumint(8),
  `name` varchar(255),
  `year` mediumint(4),
  `boxOffice` int(20),
  `country` varchar(255),
  `totalFrame` mediumint(8),
  `frameRate` float(18,10),
  `mark` float(8,7),
  `reviewers` mediumint(10),
  `DID` mediumint(8),
  PRIMARY KEY (`MID`)
--   ,FOREIGN KEY (DID) REFERENCES director(DID)
);

DROP TABLE IF EXISTS `movieType`;
CREATE TABLE `movieType` (
  `MID` mediumint(8),
  `TID` mediumint(8),
  PRIMARY KEY (`MID`, `TID`)
--   ,FOREIGN KEY (MID) REFERENCES movie(MID),
--   FOREIGN KEY (TID) REFERENCES Mtype(TID)
);

DROP TABLE IF EXISTS `cover`;
CREATE TABLE `cover` (
  `MID` mediumint(8),
  `picture` varchar(255),
  PRIMARY KEY (`picture`)
--   ,FOREIGN KEY (MID) REFERENCES movie(MID)
);

DROP TABLE IF EXISTS `frame`;
CREATE TABLE `frame` (
  `MID` mediumint(8),
  `frameNo` mediumint(8),
  `frameExtra` float(8,7),
  `framePic` mediumint(8),
  PRIMARY KEY (`MID`,`frameNo`)
--   ,FOREIGN KEY (MID) REFERENCES movie(MID)
);

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `UID` mediumint(8),
  `permissions` mediumint(1),
  `uname` varchar(10),
  PRIMARY KEY (`UID`)
);


INSERT INTO `movie` (`MID`,`name`,`year`,`boxOffice`,`country`,`totalFrame`,`frameRate`, `mark`, `reviewers`, `DID`)
VALUES
  (1,"The Shawshank Redemption",1994,28767189,"America",720,23.9760239,9.3,2812705,1);
  
INSERT INTO `director` (`DID`,`name`)
VALUES
  (1,"Frank Darabont");
  
INSERT INTO `Mtype` (`TID`,`typeName`)
VALUES
  (1,"Drama");
  
INSERT INTO `movieType` (`TID`,`MID`)
VALUES
  (1,1);
  
INSERT INTO `cover` (`MID`,`picture`)
VALUES
  (1,"https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_SX300.jpg");
  