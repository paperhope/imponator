drop table if exists entries;
create table stuffdone(
       Who text,
       What text,
       Why text,
       Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
       ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
);
