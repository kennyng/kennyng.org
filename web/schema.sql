drop table if exists books;
create table books (
  id integer primary key autoincrement,
  year integer not null,
  title text not null,
  image text not null,
  url text not null
);


