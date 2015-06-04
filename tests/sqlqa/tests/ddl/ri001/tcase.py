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

import time
from ...lib import hpdci
from ...lib import gvars
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


# Testcase Tab002 -- Referential Integrity
# 
# These testcases build on each other and are meant to be run as a whole
# RI dependencies for movie_titles are as such:
#  mv_femalestar relies on f_no in Female_actors, a primary key
#  mv_malestar relies on m_no in Male_actors, a unique column
#  mv_director and mv_movietype rely on d_no and d_speciality in directors,
#    primary key and unique columns respectively
# ***************************************************************************
#testcase A001 Syntax
# ***************************************************************************
def test001(desc="""a01 Syntax"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    stmt = """set schema """ + defs.my_schema + """;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from "_MD_".objects where schema_name='SCH_RI001';"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table Female_actors (
f_no          int not null not droppable,
f_name        varchar(30) not null,
f_realname    varchar(50) default null,
f_birthday    date  constraint md1 check (f_birthday > date '1900-01-01'),
primary key (f_no));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    # add fixed length column, no default
    stmt = """select * from \"_MD_\".objects where schema_name="""+defs.my_schema+""";"""
    output = _dci.cmdexec(stmt)
    
    stmt = """create table Male_actors (
m_no          int not null not droppable,
m_name        varchar(30) not null,
m_realname    varchar(50) default null,
m_birthday    date  constraint md2 check (m_birthday > date '1900-01-01'),
primary key (m_no));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """create table Directors (
d_no          int not null not droppable,
d_name        varchar(30) not null,
"d_specialty" varchar(15) not null unique,
primary key (d_no),
    constraint td1 check ("d_specialty" <> 'Music Video'),
unique (d_no, "d_specialty"));"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    stmt = """Create table Movie_titles (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint ma_fk 
                       references male_actors(m_no) ,
mv_femalestar  int default NULL,
mv_director    int default 0 not null,
mv_yearmade    int check (mv_yearmade > 1901),
mv_star_rating char(4),
mv_movietype   varchar(15),
primary key (mv_no),
    constraint fa_fk foreign key (mv_femalestar) 
           references female_actors ,
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
    _dci.expect_inserted_msg(output, 6)
    
    stmt = """insert into Male_actors values (0, 'No male actor','No male actor', current_date)
                              ,(1111, 'Cary Grant','Archibald Alec Leach',date '1904-01-18')
                              ,(1222, 'Gary Cooper','Frank James Cooper', date '1901-05-07')
                              ,(1333, 'Clint Eastwood','Clinton Eastwood Jr.', date '1930-05-31')
                              ;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 4)
    
    stmt = """insert into Female_actors values (0, 'No female actor','No female actor', current_date),
                                 (6111, 'Grace Kelly', 'Grace Patricia Kelly', date '1929-11-12'),
                                 (6123, 'Katherine Hepburn','Katharine Houghton Hepburn', date '1907-05-12'),
                                 (6124, 'Joan Crawford','Lucille Fay LeSueur', date '1904-03-23'),
                                 (6125, 'Ingrid Bergman', 'Ingrid Bergman', date '1915-08-29');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 5)
    
    stmt = """insert into Movie_titles values 
(1,'To Catch a Thief',1111, 6111, 1234, 1955, '****','Mystery'),
(2,'High Noon',1222, 6111, 1456, 1951, '****','Western'),
(3,'Unforgiven', 1333, 0, 1345, 1990, '***', 'Action'),
(4,'The Women', 0, 6124, 1567, 1939, '****', 'Drama'),
(5,'The Philadelphia Story',1111, 6123,1567, 1940, '****','Drama'),
(6,'Notorious', 1111, 6125, 1234, 1946, '****','Mystery');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 6)  
    
    stmt = """prepare xx from
select mv_name, m_name, f_name, d_name, mv_star_rating from
movie_titles, male_actors, female_actors, directors
where mv_malestar = m_no and
      mv_femalestar = f_no and
      mv_director = d_no
      order by d_name, f_name;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """execute xx;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A001""", 'a1s1')
    
    stmt = """showddl movie_titles, internal;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from movie_titiles;"""
    output = _dci.cmdexec(stmt)
    
    _testmgr.testcase_end(desc)

def test002(desc="""A002 Insert into/Delete from/Update RI tables"""):
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
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into movie_titles values (7,'Austin Powers',1444, 6126, 1678, 1999, '***','Comedy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')

    stmt = """insert into male_actors values (1444, 'Mike Myers','Mike Myers',date '1963-05-23');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)    

    stmt = """insert into movie_titles values (7,'Austin Powers',1444, 6126, 1678, 1999, '***','Comedy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    # this is a two-part constraint, add each separately
    stmt = """insert into directors values (1678,'Jay Roach','Funny');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 

    stmt = """insert into movie_titles values (7,'Austin Powers',1444, 6126, 1678, 1999, '***','Comedy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')

    stmt = """update directors set "d_specialty" = 'Comedy' where d_no = 1678;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """insert into movie_titles values (7,'Austin Powers',1444, 6126, 1678, 1999, '***','Comedy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 

    stmt = """select * from movie_titles;"""
    output = _dci.cmdexec(stmt)

    # update part of two-part foreign key
    # A002.2 unused director
    stmt = """update directors set "d_specialty" = 'Really Bad' where d_name like 'Rog%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # A002.3 used director
    stmt = """select * from directors;"""
    output = _dci.cmdexec(stmt)

    stmt = """update directors set "d_specialty" = 'Kung Fu' where d_name like '%Hitch%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    stmt = """select * from directors;"""
    output = _dci.cmdexec(stmt)
    
    # A002.4 delete unused director
    stmt = """delete from directors where d_name like 'Rog%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,1)
    
    # A002.5 delete used director
    stmt = """delete from directors where d_name like 'Cli%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    stmt = """select * from movie_titles;"""
    output = _dci.cmdexec(stmt)
    
    # A002.6 Update column in child to conflict with RI values
    stmt = """Update movie_titles set mv_movietype = 'Cartoon' where mv_no = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
    
    stmt = """select * from directors;"""
    output = _dci.cmdexec(stmt)

    stmt = """select * from movie_titles;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)

def test003(desc="""A003 Alter Table Referential Integrity tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return

    #  A003.1 add column with reference
    stmt = """alter table movie_titles
  add column mv_subspecialty varchar(15) 
             default 'Unknown'
             references directors("d_specialty");"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """invoke movie_titles;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from movie_titles;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from female_actors;"""
    output = _dci.cmdexec(stmt)
    stmt = """showddl movie_titles, internal;"""
    output = _dci.cmdexec(stmt)
    
    #  A003.2 drop RI constraint with restrict option
    stmt = """alter table movie_titles
  drop constraint fa_fk restrict;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    #  A003.3 add RI constraint using explicit column reference
    stmt = """alter table movie_titles add constraint fa_fk foreign key (mv_femalestar)
references female_actors(f_no);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output) 
    
    #  A003.4 drop RI constraint using cascade option
    stmt = """alter table movie_titles
  drop constraint fa_fk cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  check that constraint really dropped by updated table with invalid f_no
    stmt = """update movie_titles set mv_femalestar = 27 where mv_no = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)

    stmt = """select mv_name, mv_femalestar, f_name from
movie_titles left join female_actors
on mv_femalestar = f_no;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_file(output, defs.test_dir + """/A001""", 'a3s3')
    
    #  a003.5 Try to add constraint to table with conflicting data
    stmt = """alter table movie_titles add constraint fa_fk foreign key (mv_femalestar)
references female_actors(f_no);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '1143')
    
    #  restore table data
    stmt = """update movie_titles set mv_femalestar = 6111 where mv_no = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    #  A003.6 add RI constraint without explicit column reference
    #  it's not supposed to be necessary since key is PK
    stmt = """alter table movie_titles add constraint fa_fk foreign key (mv_femalestar)
references female_actors;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    #  check with update failure
    stmt = """update movie_titles set mv_femalestar = 27 where mv_no = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')
        
    _testmgr.testcase_end(desc)

def test004(desc="""A004 'Utility' Referential Integrity tests"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  A004.1 CREATE LIKE doesn't copy RI constraints
    stmt = """create table movie_titles_clone like movie_titles
  with constraints;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    stmt = """showddl movie_titles_clone, internal;"""
    output = _dci.cmdexec(stmt)
    _dci.unexpect_any_substr(output,'FOREIGN')
    
    #  A004.2 import good data into table
    stmt = """insert into male_actors values (6555,'Jimmy Stewart','James Maitland Stewart',
date '1908-05-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 
    
    stmt = """insert into female_actors values (6127,'Constance Bennett',
    'Constance Campbell Bennett',date '1904-10-22');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 
    
    stmt = """insert into female_actors values (6128,'Eva Marie Saint','Eva Marie Saint',
    date '1924-07-04');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 
    
    stmt = """insert into female_actors values (6130,'Irene Dunne','Irene Marie Dunne',
    date '1898-12-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8101')
    
    #  we'll make her a little younger
    stmt = """insert into female_actors values (6130,'Irene Dunne','Irene Marie Dunne',
    date '1900-12-20');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 
    
    stmt = """insert into directors values (1799,'Norman MacLoud','Comedy1');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 
    
    stmt = """insert into directors values (1890,'Garson Kanin','Comedy2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 
    
    stmt = """select * from directors;"""
    output = _dci.cmdexec(stmt)
    
    stmt = """select * from female_actors;"""
    output = _dci.cmdexec(stmt)
    
    # #expectfile $testdir/A004 a4s1
    # #expect any *Exit Status: 0*
    # #sh import ${testcat}.${testsch}.movie_titles -I $testdir/gooddata
    stmt = """insert into """+  defs.my_schema + """.movie_titles values (20,'Topper',1111,6127,1890,1937,'****','Comedy2','Comedy2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 
    
    stmt = """insert into """+  defs.my_schema + """.movie_titles values (21,'Dial M for Murder',1222,6111,1234,1954,'****','Mystery','Mystery');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 
    
    stmt = """select * from """+  defs.my_schema + """.movie_titles;"""
    output = _dci.cmdexec(stmt)
    
    # #expectfile $testdir/A004 a4s2
    # #sh import ${testcat}.${testsch}.movie_titles -I $testdir/baddata
    stmt = """insert into """+  defs.my_schema + """.movie_titles values (13,'North By Northwest',1111,6128,1234,1959,'****','Mystery','Mystery');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 
    
    stmt = """insert into """+  defs.my_schema + """.movie_titles values (16,'My Favorite Wife',1111,6130,1890,1942,'***','Drama','Drama');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_error_msg(output, '8103')

    stmt = """insert into """+  defs.my_schema + """.movie_titles values (15,'My Favorite Wife',1111,6130,1890,1942,'***','Comedy2','Comedy2');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 

    stmt = """delete from movie_titles where mv_no in (13,14,15,20,21);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 4)

    stmt = """delete from female_actors where f_no in (6127,6128,6130);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 3)

    stmt = """delete from male_actors where m_no = 6555;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output, 1)  
    #expect any *2 row(s) deleted*
    # #expect any *ERROR[8103]*
    # #expect any*** ERROR[8103] The operation is prevented by referential integrity constraint ${testcat}.SCH.D_FK on # table ${testcat}.SCH.DIRECTORS.*

    stmt = """delete from directors where d_no in (1799,1890);"""
    output = _dci.cmdexec(stmt)
    
    stmt = """drop table movie_titles_clone cascade;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)
    
    _testmgr.testcase_end(desc)

    # *******************************************************************************
def test005(desc="""Negative Referential Integrity tests not enforced"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist): return
    
    #  declare constraint not enforced
    stmt = """Create table Movie_titles1 (
mv_no          int not null not droppable,
mv_name        varchar (40) not null,
mv_malestar    int default NULL constraint ma_fk1 
                       references male_actors(m_no) not enforced,
mv_femalestar  int default NULL,
mv_director    int default 0 not null,
mv_yearmade    int check (mv_yearmade > 1901),
mv_star_rating char(4),
mv_movietype   varchar(15),
primary key (mv_no),
    constraint fa_fk1 foreign key (mv_femalestar) 
           references female_actors not enforced,
    constraint d_fk1 foreign key (mv_director, mv_movietype) 
           references directors (d_no, "d_specialty") not enforced
);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_warning_msg(output, '1313')

    stmt = """select * from movie_titles1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from female_actors;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from directors;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from male_actors;"""
    output = _dci.cmdexec(stmt)

    # A002.1 insert row with invalid male, female and director
    stmt = """insert into Movie_titles1 values (7,'Austin Powers',1555, 6126, 1789, 1999, '***','Comedy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    # add necessary rows until successful
    stmt = """insert into female_actors values (6127, 'Liz Hurley','Elizabeth Jane Hurley', date '1965-06-10');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """insert into male_actors values (1555, 'Mike Myers','Mike Myers',date '1963-05-23');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)    

    # this is a two-part constraint, add each separately
    stmt = """insert into directors values (1789,'Ching','Funny');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1) 

    stmt = """insert into directors values (9999,'test','JusetTest');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)
    # insert row with valid male, female and director
    stmt = """insert into Movie_titles1 values (8,'Austin Powers2',1666, 6127, 1901, 1999, '***','Comedy');"""
    output = _dci.cmdexec(stmt)
    _dci.expect_inserted_msg(output, 1)

    stmt = """select * from movie_titles1;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from movie_titles;"""
    output = _dci.cmdexec(stmt)
    # update part of two-part foreign key
    # unused director
    stmt = """update directors set "d_specialty" = 'Really Bad' where d_name like 'test';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    # used director
    stmt = """select * from directors;"""
    output = _dci.cmdexec(stmt)

    stmt = """update directors set "d_specialty" = 'Kung Fu' where d_name like 'Ching';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from directors;"""
    output = _dci.cmdexec(stmt)
    
    # delete unused director
    stmt = """delete from directors where d_name like 'test';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,1)
    
    # delete used director
    stmt = """delete from directors where d_name like 'Ching%';"""
    output = _dci.cmdexec(stmt)
    _dci.expect_deleted_msg(output,1)
    
    stmt = """select * from movie_titles1;"""
    output = _dci.cmdexec(stmt)
    
    # Update column in child to conflict with RI values
    stmt = """Update movie_titles1 set mv_movietype = 'Cartoon' where mv_no = 7;"""
    output = _dci.cmdexec(stmt)
    _dci.expect_updated_msg(output, 1)
    
    stmt = """select * from directors;"""
    output = _dci.cmdexec(stmt)
    stmt = """select * from movie_titles1;"""
    output = _dci.cmdexec(stmt)

    stmt = """drop table movie_titles1 cascade;"""
    output = _dci.cmdexec(stmt)

    _testmgr.testcase_end(desc)    





