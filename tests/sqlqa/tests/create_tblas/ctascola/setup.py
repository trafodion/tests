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

#import b2uwl02_ddl
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
			m_no          int not null not droppable,
			m_name        varchar(30) not null,
			m_realname    varchar(50) default null,
			m_birthday    date  constraint md2b check (m_birthday > date '1900-01-01'),
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
			mv_malestar    int default NULL constraint """ + defs.w_catalog + """.""" + defs.w_schema + """.ma_fk 
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
			(6,'Notorious', 1111, 6125, 1234, 1946, '****','Mystery')
			;"""
	output = _dci.cmdexec(stmt)

	#following table is used by CTAS013 and CTAS016
	#create table to select from
	stmt = """Create Table b2uwl02
   (
     char0_n10           Character(2)
                        default 'AD' heading 'char0_n10 with default AD',
     sbin0_uniq          Smallint                   not null,
     sdec0_n500          Decimal(18)                        ,
     date0_uniq          Date                          no default not null,
     int0_yTOm_nuniq     Interval year(5) to month              no default,


     int1_hTOs_1000      Interval hour(2) to second(0)   not null,
     date1_n4            Date                               ,
     real1_uniq          Real                          no default not null,
     ubin1_n2            Numeric(4) unsigned                    no default,
     udec1_100           Decimal(2) unsigned        not null,

     char2_2             Character(2)               not null,
     sbin2_nuniq         Largeint                           ,
     sdec2_500           Decimal(9) signed             no default not null,
     date2_uniq          Date                       not null,
     int2_dTOf6_n2       Interval day to second(6)            no default,
     real2_500           Real                       not null,

     real3_n1000         Real                               ,
     int3_yTOm_4         Interval year(1) to month     no default not null,
     date3_n2000         Date                                   no default,
     udec3_n100          Decimal(9) unsigned                ,
     ubin3_n2000         Numeric(4) unsigned                ,
     char3_4             Character(8)                  no default not null,

     sdec4_n20           Decimal(4)                             no default,
     int4_yTOm_uniq      Interval year(5) to month   not null,
     sbin4_n1000         Smallint                           ,
     time4_1000          Time                          no default not null,
     char4_n10           Character(8)                           no default,
     real4_2000          Real                       not null,

     char5_n20           Character(8)                       ,
     sdec5_10            Decimal(9) signed             no default not null,
     ubin5_n500          Numeric(9) unsigned                    no default,
     real5_uniq          Real                       not null,
     dt5_yTOmin_n500     Timestamp(0)            ,
     int5_hTOs_500       Interval hour to second(0)       no default not null,

     int6_dTOf6_nuniq    Interval day to second(6)            no default,
     sbin6_nuniq         Largeint                               no default,
     double6_n2          Float(23)                          ,
     sdec6_4             Decimal(4) signed             no default not null,
     char6_n100          Character(8)                           no default,
     date6_100           Date                       not null,

     time7_uniq          Time                       not null,
     sbin7_n20           Smallint                               no default,
     char7_500           Character(8)                  no default not null,
     int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
     udec7_n10           Decimal(4) unsigned                ,
     real7_n4            Real                               ,

     ubin8_10            Numeric(4) unsigned        not null,
     int8_y_n1000        Interval year(3)                   ,
     date8_10            Date                          no default not null,
     char8_n1000         Character(8)                           no default,
     double8_n10         Double Precision                       no default,
     sdec8_4             Decimal(9) unsigned        not null,

     sdec9_uniq          Decimal(18) signed            no default not null,
     real9_n20           Real                               ,
     time9_n4            Time                               ,
     char9_100           Character(2)                  no default not null,
     int9_dTOf6_2000     Interval day to second(6)   no default not null,
     ubin9_n4            Numeric(9) unsigned                    no default,

     ubin10_n2           Numeric(4) unsigned                    no default,
     char10_nuniq        Character(8)                       ,
     int10_d_uniq        Interval day(6)            not null,
     ts10_n2             Timestamp                          ,
     real10_100          Real                       not null,
     udec10_uniq         Decimal(9) unsigned           no default not null,

     udec11_2000         Decimal(9) unsigned           no default not null,
     int11_h_n10         Interval hour(1)                       no default,
     sbin11_100          Integer                    not null,
     time11_20           Time                       not null,
     char11_uniq         Character(8)               not null,
     double11_n100       Double Precision                   ,

     real12_n20          Real                               ,
     ubin12_2            Numeric(4) unsigned           no default not null,
     dt12_mTOh_1000      Timestamp(0)        no default not null,
     sdec12_n1000        Decimal(18) signed                     no default,
     char12_n2000        Character(8)                           no default,
     int12_yTOm_100      Interval year to month     not null,

     int13_yTOm_n1000    Interval year to month             ,
     udec13_500          Decimal(9) unsigned           no default not null,
     sbin13_n100         PIC S9(9)V9 COMP                       no default,
     ts13_uniq           Timestamp                  not null,
     char13_1000         Character(8)               not null,
     real13_n1000        Real                               ,
     sbin14_1000         Integer                       no default not null,
     double14_nuniq      Float(23)                              no default,
     udec14_100          Decimal(4) unsigned        not null,
     char14_n500         Character(8)                       ,
     int14_d_500         Interval day(3)               no default not null,
     ts14_n100           Timestamp                              no default,

     dt15_mTOh_n100      Timestamp(0)                 no default,
     double15_uniq       Double Precision           not null,
     sbinneg15_nuniq     Largeint                           ,
     sdecneg15_100       Decimal(9) signed             no default not null,
     int15_dTOf6_n100    Interval day to second(6)            no default,
     char15_100          Character(8)               not null,

     dt16_m_n10          date                     ,
     int16_h_20          Interval hour                 no default not null,
     ubin16_n10          Numeric(4) unsigned                    no default,
     sdec16_uniq         Decimal(18) signed         not null,
     char16_n20          Character(5)        ,   -- len = 2,4
     real16_10           Real                          no default not null,

     int17_y_n10         Interval year(1)                       no default,
     dt17_yTOmin_uniq    Timestamp(0)    not null,
     real17_n100         Real                               ,
     sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
     sdec17_nuniq        Decimal(18)                            no default,
     char17_2            Character(8)               not null

  )
   store by ( sbin0_uniq )
--   attributes audit
;"""
	output = _dci.cmdexec(stmt)   

	stmt = """INSERT INTO b2uwl02
			(SELECT * FROM TRAFODION.g_sqldopt.b2uwl02);"""
	output = _dci.cmdexec(stmt)
