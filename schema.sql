drop table if exists peopel;
create table people (
  id integer primary key autoincrement,
  nameFirst VARCHAR not null,
  nameLast VARCHAR not null,
  birth date,
  categoryId integer not null,
  pay INTEGER,
  foreign key(categoryId) references category(id)
);

drop table if exists category;
create table category (
  id integer primary key autoincrement,
  name VARCHAR not null,
  laps INTEGER
);

SELECT p.id, p.startNumber, p.nameFirst, p.nameLast, p.bith, c.name as category, p.pay FROM people AS p JOIN category AS c ON p.categoryId = c.id