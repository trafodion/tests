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
	_dci.setup_schema(defs.my_schema)

	#I am making sure that the below cqd is 'system' meaning it issues a 1302 warning
	stmt = """control query default REF_CONSTRAINT_NO_ACTION_LIKE_RESTRICT 'SYSTEM';"""
	output = _dci.cmdexec(stmt)
	
	#create tables that will be used to select from
	stmt = """create table Female_actors (
			f_no          int not null not droppable,
			f_name        varchar(30) not null,
			f_realname    varchar(50) default null,
			f_birthday    date  constraint md1 check (f_birthday > date '1900-01-01'),
			primary key (f_no)
			);"""
	output = _dci.cmdexec(stmt)

	stmt = """create table Male_actors (
			m_no          int not null not droppable ,
			m_name        varchar(30) not null,
			m_realname    varchar(50) default null,
			m_birthday    date  constraint md2 check (m_birthday > date '1900-01-01'),
			primary key (m_no) 
			);"""
	output = _dci.cmdexec(stmt)

	stmt = """create table Directors (
			d_no          int not null not droppable,
			d_name        varchar(30) not null,
			"d_specialty" varchar(15) not null unique,
			primary key (d_no),
			constraint td1 check ("d_specialty" <> 'Music Video'),
			unique (d_no, "d_specialty")
			);"""
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
			constraint fa_fk foreign key (mv_femalestar) references female_actors,
			constraint d_fk foreign key (mv_director, mv_movietype) references directors (d_no, "d_specialty")
			);"""
	output = _dci.cmdexec(stmt)

	#Populate tables that will be used to select
	stmt = """insert into directors values (0, 'No director named','Unknown')
                            ,(1234, 'Alfred Hitchcock', 'Mystery')
                            ,(1345, 'Clint Eastwood','Action')
                            ,(1456, 'Fred Zinneman', 'Western')
                            ,(1567, 'George Cukor', 'Drama')
                            ,(1789, 'Roger Corman','Scary')
                            ;"""
	output = _dci.cmdexec(stmt)
	
	stmt = """insert into Male_actors values (0, 'No male actor','No male actor', current_date)
                              ,(1111, 'Cary Grant','Archibald Alec Leach',date '1904-01-18')
                              ,(1222, 'Gary Cooper','Frank James Cooper', date '1901-05-07')
                              ,(1333, 'Clint Eastwood','Clinton Eastwood Jr.', date '1930-05-31')
                              ;"""
	output = _dci.cmdexec(stmt)

	stmt = """insert into Female_actors values (0, 'No female actor','No female actor', current_date),
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
			(6,'Notorious', 1111, 6125, 1234, 1946, '****','Mystery');"""
	output = _dci.cmdexec(stmt)
