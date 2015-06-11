-- @@@ START COPYRIGHT @@@
--
-- (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
--
--  Licensed under the Apache License, Version 2.0 (the "License");
--  you may not use this file except in compliance with the License.
--  You may obtain a copy of the License at
--
--      http://www.apache.org/licenses/LICENSE-2.0
--
--  Unless required by applicable law or agreed to in writing, software
--  distributed under the License is distributed on an "AS IS" BASIS,
--  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--  See the License for the specific language governing permissions and
--  limitations under the License.
--
-- @@@ END COPYRIGHT @@@

?section create_table
----------------------------------------------------------------------------------
create schema a28schema1;
set schema a28schema1;
create table a28tab_up(c1 int not null primary key, c2 int);
insert into a28tab_up values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7);
select * from a28tab_up;

create table a28tab_me(c1 int not null primary key, c2 int);
insert into a28tab_me values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7);
select * from a28tab_me;
   
create table a28tab_cas(c1 int not null primary key, c2 int);
insert into a28tab_cas values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7);
select * from a28tab_cas;

create table a28tab_load1(c1 int not null primary key, c2 int);
insert into a28tab_load1 values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7);
select * from a28tab_load1;

create table a28tab_load2(c1 int not null primary key, c2 int);
insert into a28tab_load2 values (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7);
select * from a28tab_load2;

create table a28tab_index(c1 int not null primary key, c2 int);
create index a28index on a28tab_index(c2 desc);
insert into a28tab_index values (1,1),(3,3),(5,5), (6,6), (7,7),(2,2),(4,4);
select * from a28tab_index;



            


