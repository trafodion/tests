# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2014-2015 Hewlett-Packard Development Company, L.P.
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
from ...lib import gvars
import defs

_testmgr = None
_testlist = []
_dci = None

# Testcase Tab002 -- Referential Integrity
#
# These testcases build on each other and are meant to be run as a whole
# RI dependencies for movie_titles are as such:
#  mv_femalestar relies on f_no in Female_actors, a primary key
#  mv_malestar relies on m_no in Male_actors, a unique column
#  mv_director and mv_movietype rely on d_no and d_speciality in directors,
#    primary key and unique columns respectively
def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci
    
    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()
    
def test001(desc="""Syntax"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """create table Female_actors (
f_no          int not null not droppable,
f_name        varchar(30) not null,
f_realname    varchar(50) default null,
f_birthday    date  constraint md1 check (f_birthday > date '1900-01-01'),
primary key (f_no)
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table Male_actors (
m_no          int not null not droppable unique,
m_name        varchar(30) not null,
m_realname    varchar(50) default null,
m_birthday    date  constraint md2 check (m_birthday > date '1900-01-01')
) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table Directors (
d_no          int not null not droppable,
d_name        varchar(30) not null,
"d_specialty" varchar(15) not null unique,
primary key (d_no),
constraint td1 check ("d_specialty" <> 'Music Video'),
unique (d_no, "d_specialty")
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """Create table Movie_titles (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint """ + defs.my_schema + """.ma_fk
references male_actors(m_no),
mv_femalestar  int default NULL,
mv_director    int default 0 not null,
mv_yearmade    int check (mv_yearmade > 1901),
mv_star_rating char(4),
mv_movietype   varchar(15),
primary key (mv_no),
constraint fa_fk foreign key (mv_femalestar)
references female_actors,
constraint d_fk foreign key (mv_director, mv_movietype)
references directors (d_no, "d_specialty")
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into directors values (0, 'No director named','Unknown')
,(1234, 'Alfred Hitchcock', 'Mystery')
,(1345, 'Clint Eastwood','Action')
,(1456, 'Fred Zinneman', 'Western')
,(1567, 'George Cukor', 'Drama')
,(1789, 'Roger Corman','Scary')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into Male_actors values (0, 'No male actor','No male actor', current_date)
,(1111, 'Cary Grant','Archibald Alec Leach',date '1904-01-18')
,(1222, 'Gary Cooper','Frank James Cooper', date '1901-05-07')
,(1333, 'Clint Eastwood','Clinton Eastwood Jr.', date '1930-05-31')
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into Female_actors values (0, 'No female actor','No female actor', current_date),
(6111, 'Grace Kelly', 'Grace Patricia Kelly', date '1929-11-12'),
(6123, 'Katherine Hepburn','Katharine Houghton Hepburn', date '1907-05-12'),
(6124, 'Joan Crawford','Lucille Fay LeSueur', date '1904-03-23'),
(6125, 'Ingrid Bergman', 'Ingrid Bergman', date '1915-08-29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into Movie_titles values
(1,'To Catch a Thief',1111, 6111, 1234, 1955, '****','Mystery'),
(2,'High Noon',1222, 6111, 1456, 1951, '****','Western'),
(3,'Unforgiven', 1333, 0, 1345, 1990, '***', 'Action'),
(4,'The Women', 0, 6124, 1567, 1939, '****', 'Drama'),
(5,'The Philadelphia Story',1111, 6123,1567, 1940, '****','Drama'),
(6,'Notorious', 1111, 6125, 1234, 1946, '****','Mystery');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select mv_name, m_name, f_name, d_name, mv_star_rating from
movie_titles, male_actors, female_actors, directors
where mv_malestar = m_no and
mv_femalestar = f_no and
mv_director = d_no
order by d_name, f_name;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """a1s1""")
    
    stmt = """showddl movie_titles, internal;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test002(desc="""Insert into/Delete from/Update RI tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # A002.1 insert row with invalid male, female and director
    stmt = """insert into movie_titles values (7,'Austin Powers',1444, 6126, 1678, 1999, '***','Comedy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    # add necessary rows until successful
    stmt = """insert into female_actors values (6126, 'Liz Hurley','Elizabeth Jane Hurley', date '1965-06-10');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into movie_titles values (7,'Austin Powers',1444, 6126, 1678, 1999, '***','Comedy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    stmt = """insert into male_actors values (1444, 'Mike Myers','Mike Myers',date '1963-05-23');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into movie_titles values (7,'Austin Powers',1444, 6126, 1678, 1999, '***','Comedy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    # this is a two-part constraint, add each separately
    stmt = """insert into directors values (1678,'Jay Roach','Funny');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into movie_titles values (7,'Austin Powers',1444, 6126, 1678, 1999, '***','Comedy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    stmt = """update directors set "d_specialty" = 'Comedy' where d_no = 1678;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    stmt = """insert into movie_titles values (7,'Austin Powers',1444, 6126, 1678, 1999, '***','Comedy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    #update part of two-part foreign key
    # A002.2 unused director
    stmt = """update directors set "d_specialty" = 'Really Bad' where d_name like 'Rog%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    # A002.3 used director
    stmt = """update directors set "d_specialty" = 'Kung Fu' where d_name like '%Hitch%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    # A002.4 delete unused director
    stmt = """delete from directors where d_name like 'Rog%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    # A002.5 delete used director
    stmt = """delete from directors where d_name like 'Cli%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    # A002.6 Update column in child to conflict with RI values
    stmt = """Update movie_titles set mv_movietype = 'Cartoon' where mv_no = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    _testmgr.testcase_end(desc)

def test003(desc="""Alter Table Referential Integrity tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # A003.1 add column with reference
    
    stmt = """alter table movie_titles
add column mv_subspecialty varchar(15)
default 'Unknown'
references directors("d_specialty");"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """invoke movie_titles;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl movie_titles, internal;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # A003.2 drop RI constraint with restrict option
    
    stmt = """alter table movie_titles
drop constraint fa_fk restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # A003.3 add RI constraint using explicit column reference
    stmt = """alter table movie_titles add constraint fa_fk foreign key (mv_femalestar)
references female_actors(f_no);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # A003.4 drop RI constraint using cascade option
    stmt = """alter table movie_titles
drop constraint fa_fk cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    # check that constraint really dropped by updated table with invalid f_no
    stmt = """update movie_titles set mv_femalestar = 27 where mv_no = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    stmt = """select mv_name, mv_femalestar, f_name from
movie_titles left join female_actors
on mv_femalestar = f_no;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/a001.exp""", """a3s3""")
    
    # a003.5 Try to add constraint to table with conflicting data
    stmt = """alter table movie_titles add constraint fa_fk foreign key (mv_femalestar)
references female_actors(f_no);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1143')
    
    # restore table data
    stmt = """update movie_titles set mv_femalestar = 6111 where mv_no = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output)
    
    # A003.6 add RI constraint without explicit column reference
    # it's not supposed to be necessary since key is PK
    stmt = """alter table movie_titles add constraint fa_fk foreign key (mv_femalestar)
references female_actors;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # check with update failure
    stmt = """update movie_titles set mv_femalestar = 27 where mv_no = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    _testmgr.testcase_end(desc)

def test004(desc="""'Utility' Referential Integrity tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    # A004.1 CREATE LIKE doesn't copy RI constraints
    
    stmt = """create table movie_titles_clone like movie_titles
with constraints;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl movie_titles_clone, internal;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output, """FOREIGN""")
    
    # A004.2 import good data into table
    stmt = """insert into male_actors values (6555,'Jimmy Stewart','James Maitland Stewart',
date '1908-05-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into female_actors values (6127,'Constance Bennett',
'Constance Campbell Bennett',date '1904-10-22');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into female_actors values (6128,'Eva Marie Saint','Eva Marie Saint',
date '1924-07-04');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into female_actors values (6130,'Irene Dunne','Irene Marie Dunne',
date '1898-12-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    # we'll make her a little younger
    stmt = """insert into female_actors values (6130,'Irene Dunne','Irene Marie Dunne',
date '1900-12-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into directors values (1799,'Norman MacLoud','Comedy1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    stmt = """insert into directors values (1890,'Garson Kanin','Comedy2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """select * from directors;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from female_actors;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/A004 a4s1
    ##expect any *Exit Status: 0*
    ##sh import ${w_catalog}.sch.movie_titles -I $test_dir/gooddata
    stmt = """insert into """ + defs.my_schema + """.movie_titles values (20,'Topper',1111,6127,1890,1937,'****','Comedy2','Comedy2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    stmt = """insert into """ + defs.my_schema + """.movie_titles values (21,'Dial M for Murder',1222,6111,1234,1954,'****','Mystery','Mystery');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    
    stmt = """select * from """ + defs.my_schema + """.movie_titles;"""
    output = _dci.cmdexec(stmt)
    
    ##expectfile $test_dir/A004 a4s2
    ##sh import ${w_catalog}.sch.movie_titles -I $test_dir/baddata
    stmt = """insert into """ + defs.my_schema + """.movie_titles values (13,'North By Northwest',1111,6128,1234,1959,'****','Mystery','Mystery');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """insert into """ + defs.w_schema + """.movie_titles values (16,'My Favorite Wife',1111,6130,1890,1942,'***','Drama','Drama');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    stmt = """insert into """ + defs.my_schema + """.movie_titles values (15,'My Favorite Wife',1111,6130,1890,1942,'***','Comedy2','Comedy2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """delete from movie_titles where mv_no in (13,14,15,20,21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from female_actors where f_no in (6127,6128,6130);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """delete from male_actors where m_no = 6555;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    
    stmt = """delete from directors where d_no in (1799,1890);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output)
    stmt = """drop table movie_titles_clone;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test005(desc="""Negative Referential Integrity tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    # N001.1 declare constraint twice
    stmt = """Create table Movie_titles1 (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint ma_fk1 references male_actors(m_no),
mv_femalestar  int default NULL,
mv_director    int default 0 constraint d_fk1 references directors(d_no),
--mv_yearmade    datetime year,
mv_yearmade    interval year,
mv_star_rating char(4),
mv_movietype   varchar(15),
primary key (mv_no),
constraint fa_fk1 foreign key (mv_femalestar) references female_actors,
constraint d_fk1 foreign key (mv_director, mv_movietype) references directors (d_no, "d_specialty")
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # N001.2 create child table before parent
    stmt = """Create table Movie_titles2 (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint ma_fk2 references male_actors(m_no),
mv_femalestar  int default NULL,
mv_director    int default 0 not null,
--mv_yearmade    datetime year,
mv_yearmade    interval year,
mv_star_rating char(4),
mv_movietype   varchar(15),
primary key (mv_no),
constraint fa_fk2 foreign key (mv_femalestar) references female_actresses,
constraint d_fk2 foreign key (mv_director, mv_movietype) references directors (d_no, "d_specialty")
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # N001.3 Create child table with different datatype
    stmt = """Create table Movie_titles3 (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint ma_fk3 references male_actors(m_no),
mv_femalestar  int default NULL,
mv_director    int default 0 not null,
--mv_yearmade    datetime year,
mv_yearmade    interval year,
mv_star_rating char(4),
mv_movietype   char(15),
primary key (mv_no),
constraint fa_fk3 foreign key (mv_femalestar) references female_actors,
constraint d_fk3 foreign key (mv_director, mv_movietype) references directors (d_no, "d_specialty")
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # N001.4 Create child table with different data length
    stmt = """Create table Movie_titles4 (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint ma_fk4 references male_actors(m_no),
mv_femalestar  int default NULL,
mv_director    int default 0 not null,
--mv_yearmade    datetime year,
mv_yearmade    interval year,
mv_star_rating char(4),
mv_movietype   varchar(12),
primary key (mv_no),
constraint fa_fk4 foreign key (mv_femalestar) references female_actors,
constraint d_fk4 foreign key (mv_director, mv_movietype) references directors (d_no, "d_specialty")
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # N001.5 Create parent table with unique on columns, but not on multi-columns
    stmt = """create table Directors1 (
d_no          int not null not droppable,
d_name        varchar(30) not null,
d_specialty   varchar(15) not null unique,
primary key (d_no),
constraint td2 check (d_specialty <> 'Music Video')
);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """Create table Movie_titles5 (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint ma_fk5 references male_actors(m_no),
mv_femalestar  int default NULL,
mv_director    int default 0 not null unique,
--mv_yearmade    datetime year,
mv_yearmade    interval year,
mv_star_rating char(4),
mv_movietype   varchar(12),
primary key (mv_no),
constraint fa_fk5 foreign key (mv_femalestar)
references female_actors,
constraint d_fk5 foreign key (mv_director, mv_movietype)
references directors1 (d_no, d_specialty)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """drop table directors1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # N001.6 Child table same as referenced table
    stmt = """Create table Movie_titles6 (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint ma_fk6 references movie_titles6,
mv_femalestar  int default NULL,
mv_director    int default 0 not null unique,
--mv_yearmade    datetime year,
mv_yearmade    interval year,
mv_star_rating char(4),
mv_movietype   varchar(12),
primary key (mv_no),
constraint fa_fk6 foreign key (mv_femalestar)
references female_actors,
constraint d_fk6 foreign key (mv_director, mv_movietype)
references directors (d_no, "d_specialty")
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #N001.7 Order of keys in constraint much match
    stmt = """Create table Movie_titles7 (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL,
mv_femalestar  int default NULL,
mv_director    int default 0 not null unique,
--mv_yearmade    datetime year,
mv_yearmade    interval year,
mv_star_rating char(4),
mv_movietype   varchar(12),
primary key (mv_no),
constraint fa_fk7 foreign key (mv_femalestar)
references female_actors,
constraint d_fk7 foreign key (mv_movietype,mv_director)
references directors (d_no, "d_specialty")
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    # N001.8 ON DELETE SET NULL not yet implemeted
    stmt = """Create table Movie_titles8 (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint ma_fk8 references male_actors(m_no),
mv_femalestar  int default NULL,
mv_director    int default 0 constraint d_fk8 references directors(d_no)
on delete set NULL,
--mv_yearmade    datetime year,
mv_yearmade    interval year,
mv_star_rating char(4),
primary key (mv_no),
constraint fa_fk8 foreign key (mv_femalestar) references female_actors
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3029')
    
    # N001.9 ON DELETE SET DEFAULT not yet supported
    stmt = """Create table Movie_titles9 (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint ma_fk9 references male_actors(m_no),
mv_femalestar  int default NULL,
mv_director    int default 0 constraint d_fk9 references directors(d_no)
on delete set default,
--mv_yearmade    datetime year,
mv_yearmade    interval year,
mv_star_rating char(4),
primary key (mv_no),
constraint fa_fk9 foreign key (mv_femalestar) references female_actors
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3029')
    
    # N001.10 Drop parent table before child
    stmt = """drop table directors;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1059')
    
    # N001.11 Reference View
    
    stmt = """create view mtitles as select mv_no, mv_star_rating, mv_name from movie_titles;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """create table newmovies (
n_no int not null references mtitles(mv_no),
n_stars  char(4)) no partition;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    stmt = """drop view mtitles;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # N001.12 RI constraint in different catalog
    stmt = """create table newmovies (
n_no int not null,
n_starts char(4),
primary key (n_no),
--  constraint sqldpops.sch.cs1 foreign key (n_no)
constraint ddl.sqldpops.cs1 foreign key (n_no)
references movies_titles(mv_no)
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '3050')
    
    # N001.13 Create table with not enforced RI (not in EAP)
    ##expect any *ERROR[15001]*
    stmt = """Create table Movie_titles5 (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint mz_fk4 references male_actors(m_no) not enforced,
mv_femalestar  int default NULL,
mv_director    int default 0 not null,
--mv_yearmade    datetime year,
mv_yearmade    interval year,
mv_star_rating char(4),
mv_movietype   varchar(15),
primary key (mv_no),
constraint fz_fk4 foreign key (mv_femalestar) references female_actors,
constraint dz_fk4 foreign key (mv_director, mv_movietype) references directors (d_no, "d_specialty")
);"""
    output = _dci.cmdexec(stmt)
    # _dci.expect_warning_msg(output, '1313')
    _dci.unexpect_error_msg(output)
    
    # N001.14 Drop RI referenced constraint
    stmt = """CREATE TABLE MALE_ACTORS77
(
M_NO                             INT NO DEFAULT  NOT NULL NOT DROPPABLE
, M_NAME                           VARCHAR(30) CHARACTER SET ISO88591 COLLATE
DEFAULT NO DEFAULT NOT NULL NOT DROPPABLE
, M_REALNAME                       VARCHAR(50) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, M_BIRTHDAY                       DATE DEFAULT NULL
, CONSTRAINT mno_UNIQ UNIQUE (M_NO) DROPPABLE
, CONSTRAINT MDX CHECK (M_BIRTHDAY > DATE
'1900-01-01') DROPPABLE
) no partition
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE Male_TITLES
(
MV_NO                            INT NO DEFAULT NOT NULL NOT DROPPABLE
, MV_NAME                          VARCHAR(40) CHARACTER SET ISO88591 COLLATE
DEFAULT NO DEFAULT  NOT NULL NOT DROPPABLE
, MV_MALESTAR                      INT DEFAULT NULL
, MV_FEMALESTAR                    INT DEFAULT NULL
, MV_DIRECTOR                      INT DEFAULT 0 NOT NULL NOT DROPPABLE
, MV_YEARMADE                      INT DEFAULT NULL
, MV_STAR_RATING                   CHAR(4) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, MV_MOVIETYPE                     VARCHAR(15) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, MV_SUBSPECIALTY                  VARCHAR(15) CHARACTER SET ISO88591 COLLATE
DEFAULT DEFAULT NULL
, PRIMARY KEY (MV_NO) NOT DROPPABLE
, CONSTRAINT MAX_FK FOREIGN KEY (MV_MALESTAR) REFERENCES
MALE_ACTORS77(M_NO) DROPPABLE)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table male_actors77 drop constraint mno_uniq;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1050')
    
    #N001.15 RI key references PK in same table
    stmt = """create table latest_movies (mv_no int not null primary key,
mv_title char(23),
mv_dno int not null
references latest_movies(mv_no));"""
    output = _dci.cmdexec(stmt)
    # TRAF has relaxed the rules.  Self-referencial foreign keys are now
    # allowed.
    if hpdci.tgtSQ():
        _dci.expect_error_msg(output, '1090')
    elif hpdci.tgtTR():
        _dci.expect_complete_msg(output)

    #N001.16 RI key added to table with data conflict
    stmt = """create table new_dirs (nd_no int not null ,
nd_name char(15),
primary key (nd_no));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into new_dirs values (43, 'capra'),(44, 'scorcese'),(45,'robbins');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """create table new_movies (nm_no int not null, nm_dir int,primary key (nm_no));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """insert into new_movies values (56,44),(57,43),(58,90);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output)
    
    stmt = """alter table new_movies add foreign key (nm_no) references new_dirs(nd_no);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1143')
    
    # N001.17 RI key added for column already referenced
    stmt = """CREATE TABLE NEW_DIRS1
(
ND_NO                            INT NO DEFAULT NOT NULL NOT DROPPABLE
, ND_NAME                          CHAR(15)
, PRIMARY KEY (ND_NO) NOT DROPPABLE
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """CREATE TABLE NEW_MOVIES1
(
NM_NO                            INT NO DEFAULT  NOT NULL NOT DROPPABLE
, NM_DIR                           INT DEFAULT NULL
, PRIMARY KEY (NM_NO) NOT DROPPABLE
, FOREIGN KEY (NM_NO) REFERENCES NEW_DIRS1(ND_NO) DROPPABLE
)
;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """alter table new_movies1 add foreign key (nm_no) references new_dirs1(nd_no);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
 
    stmt = """showddl new_movies1, internal;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_any_substr(output, """FOREIGN KEY""")

    stmt = """alter table new_dirs1 add foreign key (nd_no) references new_movies1(nm_no);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1188')
    
    # cleanup
    stmt = """drop table male_titles;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table male_actors77;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table new_movies;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table new_dirs;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table new_movies1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    stmt = """drop table new_dirs1;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

def test006(desc="""Negative Referential Integrity tests_2"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #(precision,scale)
    stmt = """create table n002_t10 (
a int,
b numeric (5,3) unique not null not droppable,
c decimal (6,2) unique not null not droppable,
Primary key (b,c));"""
    output = _dci.cmdexec(stmt)
    
    #N002.1 create child table with different scale
    stmt = """create table n002_t11 (
aa int,
bb numeric (5,2) unique not null not droppable,
cc decimal (6,2) unique not null not droppable,
Primary key (bb,cc),
constraint t2_c1 foreign key (bb,cc)
references n002_t10(b,c) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #N002.2 create child table with different precision
    stmt = """create table n002_t12 (
aa int,
bb numeric (5,3) unique not null not droppable,
cc decimal (7,2) unique not null not droppable,
Primary key (bb,cc),
constraint t3_c1 foreign key (bb,cc)
references n002_t10(b,c) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    #N002.3 columns in constraint doesn't exist
    stmt = """create table n002_t13 (
aa int,
bb numeric (5,3) unique not null not droppable,
cc decimal (6,2) unique not null not droppable,
Primary key (bb,cc),
constraint t4_c1 foreign key (b,cc)
references n002_t10(b,c) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1009')
    
    #N002.4 reference non-unique, non-primary key column
    stmt = """create table n002_t13 (
aa int,
bb numeric (5,3) unique not null not droppable,
cc decimal (6,2) unique not null not droppable,
Primary key (aa),
constraint t4_c1 foreign key (aa)
references n002_t10(a) );"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output)
    
    _testmgr.testcase_end(desc)

