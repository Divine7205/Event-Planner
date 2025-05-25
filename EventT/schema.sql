DROP TABLE  IF EXISTS Users;
DROP TABLE  IF EXISTS Events;
DROP TABLE  IF EXISTS Attendees;
DROP TABLE  IF EXISTS Tasks;
DROP TABLE  IF EXISTS Budget;


CREATE TABLE Users(
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    PasswordHash TEXT NOT NULL,
    PhoneNumber INTEGER NOT NULL
);

CREATE TABLE Events(
    EventId INTEGER PRIMARY KEY AUTOINCREMENT,
    EventName TEXT NOT NULL,
    Description TEXT NOT NULL,
    Start_date TIMESTAMP NOT NULL,
    End_date TIMESTAMP NOT NULL,
    LocationName Text NOT NULL,
    OrganizerId INTEGER NOT NULL ,
    Status TEXT NOT NULL,
    FOREIGN KEY (OrganizerId) REFERENCES Users(userid)
);


CREATE TABLE Attendees(
    AttendeeId INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT Null,
    Name TEXT NOT NULL,
    EventId INTEGER NOT NULL,
    FOREIGN KEY (EventId) REFERENCES Events(EventId)
);

CREATE TABLE Tasks(
    TaskId INTEGER PRIMARY KEY AUTOINCREMENT,
    EventId INTEGER NOT NULL,
    TaskName TEXT NOT NULL,
    FOREIGN KEY (EventId) REFERENCES Events(EventId)
);

CREATE TABLE Budgets(
    BudgetID INTEGER Primary Key AUTOINCREMENT,
    EventID INTEGER NOT NULL,
    Category TEXT NOT NULL,
    TotalBudget INTEGER,
    AmountSpent INTEGER,
    Foreign Key (EventID) references Events(EventId)
);