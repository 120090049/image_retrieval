USE CSC3170_HW2;

DROP TABLE IF EXISTS `Designer`;
CREATE TABLE Designer(
	Designer_Identifier mediumint(8),
    Designer_SSN varchar(50) ,
    first_name varchar(250),
    last_name varchar(250),
    PRIMARY KEY (Designer_Identifier)
);

DROP TABLE IF EXISTS `Customer`;
CREATE TABLE Customer(
	Customer_Identifier INT(50),
    name varchar(50),
    primary key (Customer_Identifier)
);

DROP TABLE IF EXISTS `Customer_phone`;
CREATE TABLE Customer_phone(
	Customer_Identifier mediumint(50),
    phone_number varchar(250),
    primary key(phone_number)
);

DROP TABLE IF EXISTS `Tailoring_technician`;
CREATE TABLE Tailoring_technician(
	Tailoring_SSN mediumint(8),
    first_name varchar(250),
    last_name varchar(250),
    primary key(Tailoring_SSN)
);

DROP TABLE IF EXISTS `Outfit`;
CREATE TABLE Outfit(
	Outfit_Identifier mediumint(50),
    Planned_Date Date,
    price varchar (250),
    Designer_Identifier mediumint(8),
    Customer_Identifier mediumint(50),
    primary key(Outfit_Identifier)
);

DROP TABLE IF EXISTS `Fashion_show`;
 CREATE TABLE Fashion_show(
	Fashion_show_Identifier  mediumint(8),
    show_Date varchar(250),
    Location varchar(50),
    primary key(Fashion_show_Identifier)
);


DROP TABLE IF EXISTS `Work_relationship`;
CREATE TABLE Work_relationship(
	Outfit_Identifier mediumint(8),
    Tailoring_SSN mediumint(8),
    start_date varchar(250),
    
    primary key(Outfit_Identifier,Tailoring_SSN)
);

DROP TABLE IF EXISTS `Participate_relationship`;
CREATE TABLE Participate_relationship(
	Fashion_show_Identifier mediumint(8),
    designer_Identifier mediumint(8),
    primary key(Fashion_show_Identifier,designer_Identifier)
);


INSERT INTO `Designer` (`Designer_Identifier`, `Designer_SSN`, `first_name`, `last_name`)
VALUES 
(1, "SSN001", "John", "Doe"),
(2, "SSN002", "Jane", "Smith"),
(3, "SSN003", "Alice", "Johnson");


INSERT INTO `Customer` (`Customer_Identifier`, `name`)
VALUES 
(1, "Tom"),
(2, "Jerry"),
(3, "Mike");


INSERT INTO `Customer_phone` (`Customer_Identifier`, `phone_number`)
VALUES 
(1, "1234567890"),
(2, "0987654321"),
(3, "1122334455");


INSERT INTO `Tailoring_technician` (`Tailoring_SSN`, `first_name`, `last_name`)
VALUES 
(1, "Bob", "Williams"),
(2, "Eve", "Brown"),
(3, "Charlie", "Davis");


INSERT INTO `Outfit` (`Outfit_Identifier`, `Planned_Date`, `price`, `Designer_Identifier`, `Customer_Identifier`)
VALUES 
(1, "2023-11-01", "100", 1, 1),
(2, "2023-12-01", "200", 2, 2),
(3, "2024-01-01", "300", 3, 3);


INSERT INTO `Fashion_show` (`Fashion_show_Identifier`, `show_Date`, `Location`)
VALUES 
(1, "2023-11-15", "New York"),
(2, "2023-12-15", "Paris"),
(3, "2024-01-15", "London");


INSERT INTO `Work_relationship` (`Outfit_Identifier`, `Tailoring_SSN`, `start_date`)
VALUES 
(1, 1, "2023-11-01"),
(2, 2, "2023-12-01"),
(3, 3, "2024-01-01");


INSERT INTO `Participate_relationship` (`Fashion_show_Identifier`, `designer_Identifier`)
VALUES 
(1, 1),
(2, 2),
(3, 3);


select * from Tailoring_technician;
select * from Designer;
select * from Customer;
select * from Fashion_show;
select * from Customer_phone;
select * from Outfit;
select * from Work_relationship;
select * from Participate_relationship;
