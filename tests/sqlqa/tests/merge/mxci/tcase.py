# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@

from ...lib import hpdci
import defs

_testmgr = None
_testlist = []
_dci = None

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc='a01'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #    Test updates multiple columns in one SET statement using scalar values
    #      update table set (a,b,c) = (1,2,3) where
    
    stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    #create table and data for merge
    stmt = """create table Female_actors (
f_no          int not null not droppable,
f_name        varchar(30) not null,
f_realname    varchar(50) default null,
f_birthday    date  constraint md1 check (f_birthday > date '1900-01-01'),
primary key (f_no)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into Female_actors values
(0, 'No female actor','No female actor',current_date),
(6111, 'Grace Kelly', 'Grace Patricia Kelly', date '1929-11-12'),
(6123, 'Katherine Hepburn','Katharine Houghton Hepburn', date '1907-05-12'),
(6124, 'Joan Crawford','Lucille Fay LeSueur', date '1904-03-23'),
(6125, 'Ingrid Bergman', 'Ingrid Bergman', date '1915-08-29');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select f_no,f_name,f_realname,f_birthday from female_actors where (f_no = 6124);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg01""", 's01')
    
    stmt = """update female_actors set (f_name,f_realname,f_birthday) = ('Joan Bette Crawford',
'Lucy May LeSueur',date '1908-05-12') where (f_no=6124);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select f_no,f_name,f_realname,f_birthday from female_actors where (f_no = 6124);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg01""", 's03')
    
    stmt = """drop table Female_actors;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc='a02'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # Tests update multiple columns in a Set statement using a subquery
    #  update table set (a,b) = (select r,t from t1) where...
    
    stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    #create tables and data for merge
    
    stmt = """create table mychar (col1 largeint not null,
col2  char(10),
col3  char(5),
col4  char(20),
primary key(col1));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into mychar values(1,'AAAAAAAAAA','BBBBB','my longish string'),
(2,'bbbbbbbbbb','ccccc','my second string');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from mychar order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg02""", 's01')
    
    stmt = """create table mychar2 (a   largeint not null,
b char(10),
c char(5),
d char(20),
primary key (a));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into mychar2 values (10,'ZZZZZZZZZZ','XXXXX','this is it');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from mychar2 order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg02""", 's02')
    
    stmt = """update mychar set (col3,col4)=(select c,d from mychar2) where (col1=1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    stmt = """select * from mychar order by col1;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table mychar;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table mychar2;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test003(desc='a03'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  tests merge into table on x when matched then update when not then insert
    
    stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    #--create tables and data for merge
    
    stmt = """create table anchar (col1 largeint not null,
col2  char(10),
col3  char(5),
col4  char(20),
primary key(col1));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into anchar values(1,'AAAAAAAAAA','BBBBB','my longish string'),
(2,'bbbbbbbbbb','ccccc','my second string');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from anchar order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg03""", 's01')
    
    stmt = """create table anchar2 (a   largeint not null,
b char(10),
c char(5),
d char(20),
primary key (a));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into anchar2 values (10,'ZZZZZZZZZZ','XXXXX','this is it');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from anchar2 order by a;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg03""", 's02')
    
    #expect col2=('YYYYYYYYYY') after merge
    stmt = """merge into anchar on (col1) =2
when matched then update set (col2)=('YYYYYYYYYY')
when not matched then insert (col1,col2,col3,col4) values
(10,'YYYYYYYYYY','yyyyy','this is string3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from anchar order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg03""", 's04')
    
    #expect new row of (10,'YYYYYYYYYY','yyyyy','this is string3'); after merge
    stmt = """merge into anchar on (col1) =10
when matched then update set (col2)=('YYYYYYYYYY')
when not matched then insert (col1,col2,col3,col4) values
(10,'YYYYYYYYYY','yyyyy','this is string3');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from anchar order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg03""", 's06')
    
    #expect col4 of row where col1 =10 to change to 'drums bang'
    stmt = """merge into anchar on (col1) =10
when matched then update set (col4)=('drums bang');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from anchar order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg03""", 's08')
    
    #expect row added
    
    stmt = """merge into anchar on (col1) =12
when not matched then insert values (12,'x','yy','violins squeal');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from anchar order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg03""", 's10')
    
    stmt = """drop table anchar;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table anchar2;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test004(desc='a04'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # upsert
    # Merge into table on col1=val1 when matched then update set...
    #    when not matched then insert values ....
    
    stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    #--create tables and data for merge
    
    stmt = """create table TTF (
sky largeint not null not droppable
, vch7 varchar(7)
, nint smallint
, ch3 char(3)
, nnum9 numeric(9,2)
, ch4 char(4)
, nnum5 numeric(5,1)
, vch5 varchar(5)
, nsint smallint signed
, primary key(sky)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into TTF (sky,vch7,nint,ch3,nnum9,ch4,nnum5,vch5,nsint) values
(1,'a',      1,'a'  ,0.9,       NULL,NULL  ,NULL,0)
, (2,'cc'     ,2,'cc' ,2.00,      'cc',2.0   ,'cc',2)
, (3,'abcdefg',3,'cc' ,0.09,    'alph',2     ,'cc',1)
, (4,'b',      4,'c'  ,1234567.89,'e' ,1234.5,'c' ,12345)
, (5,'abcdefg',5,'cc' ,0.09,      'cc',2     ,'cc',2)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from TTF order by sky;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg04""", 's01')
    
    #expect 4 updated
    stmt = """merge into TTF on (sky) =4
when matched then update set (nnum9,nnum5,nsint)=(12,13,14)
when not matched then insert (sky,vch7,nint,ch3,nnum9,ch4,nnum5,vch5,nsint) values
(10,'ab',10,'YYY',12,'zzzz',12,'banjo',12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select nnum9,nnum5,nsint from ttf where (sky=4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg04""", 's03')
    
    stmt = """merge into TTF on (sky) =10
when matched then update set (nnum9,nnum5,nsint)=(12,13,14)
when not matched then insert (sky,vch7,nint,ch3,nnum9,ch4,nnum5,vch5,nsint) values
(10,'ab',10,'YYY',12,'zzzz',12,'banjo',12);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #--should be 6 selected.
    stmt = """select * from TTF order by sky;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg04""", 's05')
    
    stmt = """drop table TTF;"""
    output = _dci.cmdexec(stmt)
    #end of merge04
    
    _testmgr.testcase_end(desc)

def test005(desc='a05'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    #  Merge into table using (select ....
    # on col1 = x.col1 when matched then update set....
    #  when not matched then insert....
    
    stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    #create tables and data for merge
    
    stmt = """create table TTF1 (
sky largeint not null not droppable
, vch7 varchar(7)
, nint smallint
, ch3 char(3)
, nnum9 numeric(9,2)
, ch4 char(4)
, nnum5 numeric(5,1)
, vch5 varchar(5)
, nsint smallint signed
, primary key(sky)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into TTF1 (sky,vch7,nint,ch3,nnum9,ch4,nnum5,vch5,nsint) values
(1,'a',      1,'a'  ,0.9,       NULL,NULL  ,NULL,0)
, (2,'cc'     ,2,'cc' ,2.00,      'cc',2.0   ,'cc',2)
, (3,'abcdefg',3,'cc' ,0.09,    'alph',2     ,'cc',1)
, (4,'b',      4,'c'  ,1234567.89,'e' ,1234.5,'c' ,12345)
, (5,'abcdefg',5,'cc' ,0.09,      'cc',2     ,'cc',2)
;"""
    output = _dci.cmdexec(stmt)
    #selected 5
    
    stmt = """select * from TTF1 order by sky;"""
    output = _dci.cmdexec(stmt)
    stmt = """create table TTF2(
sk largeint not null not droppable
, v1   varchar(7)
, n2   smallint
, c3   char(3)
, n4   numeric(9,2)
, c5   char(4)
, n6   numeric(5,1)
, v7   varchar(5)
, n8   smallint
, primary key (sk)) ;"""
    output = _dci.cmdexec(stmt)
    
    #expect all rows from TTF1 to be added to TTF2
    stmt = """merge into ttf2
using (select * from ttf1) as z
on sk=z.sky
when matched then update set (v1,n2,c3)=(z.vch7,z.nint,z.ch3)
when not matched then insert (sk,v1,n2,c3,n4,c5,n6,v7,n8) values
(z.sky,z.vch7,z.nint,z.ch3,z.nnum9,z.ch4,z.nnum5,z.vch5,z.nsint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from ttf2 order by sk;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg05""", 's02')
    
    stmt = """insert into ttf1 values(10,'bambi  ',32,'CHA',9.9,'chin',5.2,'chooo',-6),
(11,'thumper',34,'cha',8.9,'CHIN',5.1,'chugg',-4);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into ttf1 values(100,'bilboa  ',32,'CHA',9.9,'chin',5.2,'chooo',-6),
(110,'sam    ',34,'cha',8.9,'CHIN',5.1,'chugg',-4);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """merge into ttf2
using (select * from ttf1) as z
on sk=z.sky
when not matched then insert (sk,v1,n2,c3,n4,c5,n6,v7,n8) values
(z.sky,z.vch7,z.nint,z.ch3,z.nnum9,z.ch4,z.nnum5,z.vch5,z.nsint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from ttf2 where (v1 in ('bambi','thumper')) order by 1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg05""", 's04')
    
    stmt = """drop table TTF1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TTF2;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test006(desc='a06'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # merge from one table into another
    
    stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    #create tables and data for merge
    
    stmt = """create table Fem_actors (
f_no          int not null not droppable,
f_name        varchar(30) not null,
f_realname    varchar(50) default null,
f_birthday    date  constraint mdf1 check (f_birthday > date '1900-01-01'),
primary key (f_no)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table Male_actors (
m_no          int not null not droppable,
m_name        varchar(30) not null,
m_realname    varchar(50) default null,
m_birthday    date  constraint md2 check (m_birthday > date '1900-01-01'),
primary key (m_no)
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table Directors (
d_no          int not null not droppable,
d_name        varchar(30) not null,
"d_specialty" varchar(15) not null unique,
primary key (d_no),
constraint td1 check ("d_specialty" <> 'Music Video'),
unique (d_no, "d_specialty")
)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create table Movie_titles (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint """ + defs.w_catalog + """.""" + defs.w_schema + """.ma_fk references male_actors(m_no),
mv_femalestar  int default NULL,
mv_director    int default 0 not null,
mv_yearmade    int check (mv_yearmade > 1901),
mv_star_rating char(4),
mv_movietype   varchar(15),
primary key (mv_no),
constraint fa_fk foreign key (mv_femalestar)
references fem_actors,
constraint d_fk foreign key (mv_director, mv_movietype)
references directors (d_no, "d_specialty")
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into directors values (0, 'No director named','Unknown')
,(1234, 'Alfred Hitchcock', 'Mystery')
,(1345, 'Clint Eastwood','Action')
,(1456, 'Fred Zinneman', 'Western')
,(1567, 'George Cukor', 'Drama')
,(1789, 'Roger Corman','Scary')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)
    
    stmt = """insert into Male_actors values (0, 'No male actor','No male actor', current_date)
,(1111, 'Cary Grant','Archibald Alec Leach',date '1904-01-18')
,(1222, 'Gary Cooper','Frank James Cooper', date '1901-05-07')
,(1333, 'Clint Eastwood','Clinton Eastwood Jr.', date '1930-05-31')
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into Fem_actors values (0, 'No female actor','No female actor', current_date),
(6111, 'Grace Kelly', 'Grace Patricia Kelly', date '1929-11-12'),
(6123, 'Katherine Hepburn','Katharine Houghton Hepburn', date '1907-05-12'),
(6124, 'Joan Crawford','Lucille Fay LeSueur', date '1904-03-23'),
(6125, 'Ingrid Bergman', 'Ingrid Bergman', date '1915-08-29')
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into Movie_titles values
(1,'To Catch a Thief',1111, 6111, 1234, 1955, '****','Mystery'),
(2,'High Noon',1222, 6111, 1456, 1951, '****','Western'),
(3,'Unforgiven', 1333, 0, 1345, 1990, '***', 'Action'),
(4,'The Women', 0, 6124, 1567, 1939, '****', 'Drama'),
(5,'The Philadelphia Story',1111, 6123,1567, 1940, '****','Drama'),
(6,'Notorious', 1111, 6125, 1234, 1946, '****','Mystery')
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table port (
f_no          int not null not droppable,
f_name        varchar(30) not null,
f_realname    varchar(50) default null,
mv_name        varchar (40) not null,
primary key(f_no));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into port values  (6111, 'Grace Kelly', 'Grace Patricia Kelly', ''),
(6123, 'Katherine Hepburn','Katharine Houghton Hepburn',''),
(6124, 'Joan Crawford','Lucille Fay LeSueur', ''),
(6125, 'Ingrid Bergman', 'Ingrid Bergman', '');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select f_no,f_name,f_realname,f_birthday from fem_actors order by f_no;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg06""", 's01')
    stmt = """select mv_no,mv_name,mv_malestar,mv_femalestar,mv_director,mv_yearmade,mv_star_rating,mv_movietype from movie_titles order by mv_no;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg06""", 's02')
    stmt = """select m_no,m_name,m_realname,m_birthday from male_actors order by m_no;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg06""", 's03')
    stmt = """select * from directors order by d_no;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg06""", 's04')
    
    stmt = """select * from port order by f_no;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg06""", 's05')
    
    stmt = """merge into port
using (select fem_actors.f_no,fem_actors.f_name,fem_actors.f_realname,movie_titles.mv_name from
fem_actors,movie_titles where (fem_actors.f_no = movie_titles.mv_femalestar)) as X
on port.f_no = x.f_no
when matched then update set mv_name = x.mv_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from port order by f_no;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg06""", 's07')
    
    stmt = """insert into fem_actors values (7125, 'Marilyn Monroe', 'Jean Pateau', date '1934-04-24');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into movie_titles values (7,'Naked City', 1111, 7125, 1234, 1946, '****','Mystery');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """merge into port
using (select fem_actors.f_no,fem_actors.f_name,fem_actors.f_realname,movie_titles.mv_name from
fem_actors,movie_titles where (fem_actors.f_no = movie_titles.mv_femalestar)) as X
on port.f_no = x.f_no
when matched then update set mv_name = x.mv_name
when not matched then insert (f_no,f_name,f_realname,mv_name) values (x.f_no,x.f_name,x.f_realname,x.mv_name);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """select * from port order by f_no;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg06""", 's09')
    
    stmt = """drop table Fem_actors cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table Male_actors cascade;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table Directors cascade;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table port;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test007(desc='n07'):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # restrictions and error cases
    # # of columns on left side of assignment needs to match select list on right
    # on multi-column update when right side contains a subquery, only one element
    #   the subquery is allowed.
    # using multi-column syntax, only one subquery is allowed.
    # if a subquery is used, it must return atmost one row
    
    stmt = """set schema """ + defs.w_catalog + """.""" + defs.w_schema + """;"""
    output = _dci.cmdexec(stmt)
    #create tables and data for merge
    stmt = """create table mychar (col1 largeint not null,
col2  char(10),
col3  char(5),
col4  char(20),
primary key(col1));"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into mychar values(1,'AAAAAAAAAA','BBBBB','my longish string'),
(2,'bbbbbbbbbb','ccccc','my second string');"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from mychar order by col1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg07""", 's01')
    stmt = """create table TTF1 (
sky largeint not null not droppable
, vch7 varchar(7)
, nint smallint
, ch3 char(3)
, nnum9 numeric(9,2)
, ch4 char(4)
, nnum5 numeric(5,1)
, vch5 varchar(5)
, nsint smallint signed
, primary key(sky)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into TTF1 (sky,vch7,nint,ch3,nnum9,ch4,nnum5,vch5,nsint) values
(1,'a',      1,'a'  ,0.9,       NULL,NULL  ,NULL,0)
, (2,'cc'     ,2,'cc' ,2.00,      'cc',2.0   ,'cc',2)
, (3,'abcdefg',3,'cc' ,0.09,    'alph',2     ,'cc',1)
, (4,'b',      4,'c'  ,1234567.89,'e' ,1234.5,'c' ,12345)
, (5,'abcdefg',5,'cc' ,0.09,      'cc',2     ,'cc',2)
;"""
    output = _dci.cmdexec(stmt)
    #selected 5
    
    stmt = """select * from TTF1 order by sky;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg07""", 's02')
    
    stmt = """create table TTF (
sky largeint not null not droppable
, vch7 varchar(7)
, nint smallint
, ch3 char(3)
, nnum9 numeric(9,2)
, ch4 char(4)
, nnum5 numeric(5,1)
, vch5 varchar(5)
, nsint smallint signed
, primary key(sky)
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """insert into TTF (sky,vch7,nint,ch3,nnum9,ch4,nnum5,vch5,nsint) values
(1,'a',      1,'a'  ,0.9,       NULL,NULL  ,NULL,0)
, (2,'cc'     ,2,'cc' ,2.00,      'cc',2.0   ,'cc',2)
, (3,'abcdefg',3,'cc' ,0.09,    'alph',2     ,'cc',1)
, (4,'b',      4,'c'  ,1234567.89,'e' ,1234.5,'c' ,12345)
, (5,'abcdefg',5,'cc' ,0.09,      'cc',2     ,'cc',2)
;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from TTF order by sky;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/mrg07""", 's03')
    stmt = """create table TTF2(
sk largeint not null not droppable
, v1   varchar(7)
, n2   smallint
, c3   char(3)
, n4   numeric(9,2)
, c5   char(4)
, n6   numeric(5,1)
, v7   varchar(5)
, n8   smallint
, primary key (sk)) ;"""
    output = _dci.cmdexec(stmt)
    
    #expect any *** ERROR[4023] The degree of each row value constructor*
    stmt = """update ttf1 set (vch7,nint)=('abcdefg',49,54) where ch4='cc';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #using query
    #expect any *** ERROR[4023] The degree of each row value constructor*
    stmt = """update ttf1 set (vch7,vch5)=(select col1,col2,col3 from mychar) where (vch7=1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    ##expect any *** ERROR[3242] This statement is not supported. Reason:  Multiple elements or m
    #ultiple subqueries are not allowed in this SET clause.
    stmt = """update ttf1 set (vch7,vch5)=('abcdef',(select col3 from mychar)) where (vch7=1);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    ##expect any *** ERROR[3242] This statement is not supported. Reason:  Multiple elements or m
    #multiple subqueries are not allowed in this SET clause.
    stmt = """update ttf1 set (vch7,vch5)=(select col1,col3 from mychar),(nint,ch4)=(select nsint,ch3 from ttf);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    ##expect any *** ERROR[8401] A row subquery or SELECT...INTO statement cannot return more tha
    #n one row.
    stmt = """update ttf1 set (vch7,vch5)=(select col1,col2 from mychar) where (ch3='cc');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    ##expect any *** ERROR[3241] This MERGE statement is not supported. Reason:  Non-unique ON cl
    #ause not allowed.
    stmt = """merge into ttf2
using (select * from ttf1) as z
on sk > 0
when matched then update set (v1,n2,c3)=(z.vch7,z.nint,z.ch3)
when not matched then insert (sk,v1,n2,c3,n4,c5,n6,v7,n8) values
(z.sky,z.vch7,z.nint,z.ch3,z.nnum9,z.ch4,z.nnum5,z.vch5,z.nsint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """merge into mychar on col1=2 when matched then update set (col1,col2)=(20,'a');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
 
    ##expect any *** ERROR[3241] This MERGE statement is not supported. Reason:  Non-unique ON cl
    #ause not allowed.
    ##expectfile ${test_dir}/mrg07 s11
    stmt = """merge into mychar on col2='AAAAAAAAAA' when matched then update set (col2,col3
)=('BBBBBBBBBB','eeeee');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    ##expect any *** ERROR[3241] This MERGE statement is not supported. Reason:  Subquery in ON c
    #lause not allowed.
    stmt = """merge into mychar on col1=(select sky from ttf) when matched then update set (col2,col3)=(ttf.ch3,ttf.ch4);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
 
    ##expect any *** ERROR[3241] This MERGE statement is not supported. Reason:  Subquery in INSE
    #RT clause not allowed.
    stmt = """merge into ttf1 on sky=1 when not matched then insert (v1) values ((select vch7 from ttf2));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
 
    #*** ERROR[8595] Key values specified in the INSERT part of a MERGE statement mus
    #t be the same as those specified in the ON clause.
    stmt = """merge into ttf2
using (select * from ttf1) as z
on sk = 1
when matched then update set (v1,n2,c3)=(z.vch7,z.nint,z.ch3)
when not matched then insert (sk,v1,n2,c3,n4,c5,n6,v7,n8) values
(2,z.vch7,z.nint,z.ch3,z.nnum9,z.ch4,z.nnum5,z.vch5,z.nsint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #expect any *** ERROR[4022] Target column N2 was specified more than once.
    #*** ERROR[8822] The statement was not prepared.
    
    stmt = """merge into ttf2
using (select * from ttf1) as z
on sk = 1
when matched then update set (v1,n2,c3)=(z.vch7,z.nint,z.ch3)
when not matched then insert (n2,v1,n2,c3,n4,c5,n6,v7,n8) values
(z.sky,z.vch7,z.nint,z.ch3,z.nnum9,z.ch4,z.nnum5,z.vch5,z.nsint);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
 
    #empty table to begin with

    stmt = """merge into TTF2 on sk = 1 when matched then update set sk = 2
when not matched then insert values (1,'a',      1,'a'  ,0.9,       NULL,NULL  ,NULL,0 );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    stmt = """select * from TTF2 order by sk;"""
    output = _dci.cmdexec(stmt)
    
    #put something in table first
    stmt = """insert into TTF2 values
(1,'a',      1,'a'  ,0.9,       NULL,NULL  ,NULL,0)
, (2,'cc'     ,2,'cc' ,2.00,      'cc',2.0   ,'cc',2)
, (3,'abcdefg',3,'cc' ,0.09,    'alph',2     ,'cc',1)
, (4,'b',      4,'c'  ,1234567.89,'e' ,1234.5,'c' ,12345)
, (5,'abcdefg',5,'cc' ,0.09,      'cc',2     ,'cc',2)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """select * from TTF2 order by sk;"""
    output = _dci.cmdexec(stmt)

    stmt = """merge into TTF2 on sk = 1 when matched then update set sk =2 when not matched then insert
values (1,'a',      1,'a'  ,0.9,       NULL,NULL  ,NULL,0);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)

    stmt = """drop table TTF1;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TTF2;"""
    output = _dci.cmdexec(stmt)
    stmt = """drop table TTF;"""
    output = _dci.cmdexec(stmt)
    
    ##expect any *** ERROR[3241] This MERGE statement is not supported. Reason:  Non-unique ON cl
    #ause not allowed.
    ##expectfile ${test_dir}/mrg07 s11 -fixed in r2.4
    stmt = """merge into mychar on col2='AAAAAAAAAA' when matched then update set (col2,col3
)=('BBBBBBBBBB','eeeee');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """drop table mychar;"""
    output = _dci.cmdexec(stmt)
    #restrictions for the first release of Merge inlcude
    #  1. a subquery cannot be used in the on, update, or insert clauses
    #  2. merge is not allowed with set on rollback,pub-sub, embedded update/delete, or stream
    #  3. merge is not allowed if table has triggers or RI constraints
    #  4. dp2 savepoints are not enabled with merge statement
    #  5. merged table cannot be a view.
    
    _testmgr.testcase_end(desc)

