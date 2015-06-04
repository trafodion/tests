# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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

def _init(hptestmgr, testlist=[]):
    global _testmgr
    global _testlist
    global _dci

    _testmgr = hptestmgr
    _testlist = testlist
    # default hpdci was created using 'SQL' as the proc name.
    # this default instance shows 'SQL>' as the prompt in the log file.
    _dci = _testmgr.get_default_dci_proc()

def test001(desc="""create tables"""):
    global _testmgr
    global _testlist
    global _dci
    if not _testmgr.testcase_begin(_testlist):
        return

    stmt = """create table s32(a varchar(4015)) attributes EXTENT (1064, 1064), MAXEXTENTS 755 no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table testtab( e_name varchar(20) not null, e_num int not null , e_city char(15),
        e_title varchar(20), e_salary numeric(11,2), e_code smallint, e_date date,
        e_time time,  e_tstamp timestamp, e_long largeint , e_float float,  e_real real,
        e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),
        e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))   attributes extent (1064, 1064), maxextents 755 no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table  T1
        (
        A                                INT DEFAULT NULL
        , B                                INT DEFAULT NULL
        ) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table T2
        (
        A                                CHAR(10) CHARACTER SET ISO88591 COLLATE
        DEFAULT DEFAULT NULL
        , B                                CHAR(10) CHARACTER SET ISO88591 COLLATE
        DEFAULT DEFAULT NULL
        , C                                VARCHAR(10) CHARACTER SET ISO88591 COLLATE
        DEFAULT DEFAULT NULL
        )   no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table b2pns01
        (
        char0_n10           Character(2)
        default 'AD' heading 'char0_n10 with default AD',
        sbin0_uniq          Smallint                       not null,
        sdec0_n500          Decimal(18)                    ,
        date0_uniq          Date                     no default not null,
        int0_yTOm_nuniq     Interval year(5) to month      no default,
        int1_hTOs_1000      Interval hour(2) to second     not null,
        date1_n4            Date                           ,
        real1_uniq          Real                    no default not null,
        ubin1_n2            Numeric(4) unsigned            no default,
        udec1_100           Decimal(2) unsigned            not null
        ) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table d4 (
        i1 SMALLINT
        , i2 DECIMAL (7,0) NOT NULL
        , i3 DOUBLE PRECISION NO DEFAULT NOT NULL
        , G0 DECIMAL (9,0) NOT NULL
        , G1 VARCHAR (23) NOT NULL
        , G2 CHAR (792)
        , G3 DEC     (18, 16) NOT NULL
        , G4 VARCHAR (5) NOT NULL
        , G5 DOUBLE PRECISION
        , G6 NUMERIC (18)
        , G7 VARCHAR (910) NOT NULL
        , primary key (i2,G4)
        )  no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table d3 (
        i1 DOUBLE PRECISION NO HEADING
        , i2 REAL NOT NULL NOT DROPPABLE
        , i3 DECIMAL (7,0) NOT NULL NOT DROPPABLE PRIMARY KEY DROPPABLE
        , s0 NUMERIC (18, 7) DEFAULT 70 CONSTRAINT s003903b0H4WtYY NOT NULL
        , s1 DEC     (18, 7) CONSTRAINT s103904XfXhhML8 CHECK (s1 < 2530466427.7281775)
        , s2 NUMERIC (4,0) HEADING 'X)-xg''T?T"'
        , s3 VarChar (11) DEFAULT '9C4CG528'
        , s4 DECIMAL (4,0)
        , s5 FLOAT (54)
        , s6 FLOAT (54) DEFAULT 13 NOT NULL NOT DROPPABLE
        , s7 VarChar (12) DEFAULT 'MLQSCF8R' NOT NULL
        , s8 DECIMAL (4,0) DEFAULT 38
        , s9 PIC S9(4) CONSTRAINT s903905PUGC1oaG NOT NULL
        , s10 DOUBLE PRECISION DEFAULT 32 NO HEADING  CONSTRAINT s1003906CXMvEviI NOT NULL NOT DROPPABLE
        , s11 DECIMAL (7,0) DEFAULT 40 CONSTRAINT s1103907VHdNSteM NOT NULL
        , s12 DECIMAL (7,0) DEFAULT 67 NOT NULL NOT DROPPABLE
        , s13 REAL DEFAULT 88 CONSTRAINT s1303908K56BUbbW NOT NULL
        , s14 NUMERIC (18) CONSTRAINT s1403909P8kGcI2p NOT NULL NOT DROPPABLE
        )
        STORE BY (i3)
        no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table d1 (
        i3 INTEGER DEFAULT 956
        , i1 LARGEINT DEFAULT -572 NO HEADING  NOT NULL NOT DROPPABLE
        , i2 LARGEINT
        )
        ATTRIBUTE  EXTENT 138  MAXEXTENTS 2 CLEARONPURGE AUDITCOMPRESS
        STORE BY (i1) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table coffees (cof_name  varchar(32)  not null not droppable primary key,sup_id int, price float(54),sales int, total int) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table ntab (cof_name  varchar(32)  ,sup_id int, price float(54),sales int, total int) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table SUPPLIERS
        (
        SUP_ID                           INT DEFAULT NULL
        , SUP_NAME                         VARCHAR(40) CHARACTER SET ISO88591 COLLATE
        DEFAULT DEFAULT NULL
        , STREET                           VARCHAR(40) CHARACTER SET ISO88591 COLLATE
        DEFAULT DEFAULT NULL
        , CITY                             VARCHAR(20) CHARACTER SET ISO88591 COLLATE
        DEFAULT DEFAULT NULL
        , STATE                            CHAR(2) CHARACTER SET ISO88591 COLLATE
        DEFAULT DEFAULT NULL
        , ZIP                              CHAR(5) CHARACTER SET ISO88591 COLLATE
        DEFAULT DEFAULT NULL
        ) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table TrN (
        N5 DOUBLE PRECISION DEFAULT 81
        , N3 DOUBLE PRECISION DEFAULT 33
        , N2 DOUBLE PRECISION DEFAULT 11
        , s1 FLOAT (54) DEFAULT 50 NOT NULL
        , s0 DECIMAL (9,0) DEFAULT 31 NOT NULL
        , N6 DOUBLE PRECISION DEFAULT 54
        , N1 DOUBLE PRECISION DEFAULT 52
        , s2 DOUBLE PRECISION DEFAULT 94
        , s3 DOUBLE PRECISION DEFAULT 64 NOT NULL
        , N4 DOUBLE PRECISION DEFAULT 89
        )  no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table TrS (
        St1 VarChar (117) DEFAULT 'B8YNT80Y'
        , St2 Char (105) DEFAULT 'EA6L0UJH'
        , St3 Char (106) DEFAULT 'DNIF7GJH'
        , St4 Char (120) DEFAULT 'J17RQ4WH'
        , St5 Char (113) DEFAULT 'J8N9E0A2'
        , St6 Char (102) DEFAULT '4MGI4DH1'
        , s0 NUMERIC (9, 2) DEFAULT 22
        , s1 DECIMAL (9, 2) DEFAULT 9 NOT NULL
        )  no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table bigb
        (
        int0_yTOm_uniq      Interval year(5) to month     no default not null,
        sbin0_1000          Largeint                      no default not null,
        sdec0_nuniq         Decimal(18)                          default null,
        ts0_uniq            Timestamp                  not null,
        char0_uniq          Character(8)               not null,
        udec1_n2            Decimal(4) unsigned                ,
        time1_n100          Time                               ,
        double1_uniq        Double Precision              no default not null,
        ubin1_1000          Numeric(4) unsigned           no default not null,
        int1_dTOf6_n10      Interval day to second(6)            no default,
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
        dt16_m_n10          Date                     ,
        int16_h_20          Interval hour                 no default not null,
        ubin16_n10          Numeric(4) unsigned                    no default,
        sdec16_uniq         Decimal(18) signed         not null,
        char16_n20          Character(5)        ,
        real16_10           Real                          no default not null,
        int17_y_n10         Interval year(1)                       no default,
        dt17_yTOmin_uniq    Timestamp(0)    not null,
        real17_n100         Real                               ,
        sbin17_uniq         Largeint  no default not null,
        sdec17_nuniq        Decimal(18)                            no default,
        char17_2            Character(8)               not null,
        primary key  (  int0_yTOm_uniq ) not droppable
        ) store by primary key;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table movies (
        title              CHARACTER VARYING (100) not null not droppable,
        director           CHARACTER VARYING (50),
        year_introduced    CHARACTER (4),
        runs               INTEGER CHECK (runs BETWEEN 0 AND 480),
        PRIMARY KEY (title)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table awards (
        award              CHARACTER VARYING (20),
        person             CHARACTER VARYING (60),
        title              CHARACTER VARYING (100) REFERENCES movies,
        award_year         CHARACTER (4)
        ) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table votes (
        title             CHAR VARYING (100) REFERENCES movies,
        voter             CHAR VARYING (10),
        vote              INT
        ) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table movies_in_stock (
        title             CHARACTER VARYING (100) REFERENCES movies not null  not droppable,
        quantity          INTEGER,
        sale_price        DECIMAL(4,2),
        YearToDateSales   DECIMAL(6,2),
        PRIMARY KEY (title)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table movie_stars (
        title CHARACTER VARYING (100) not null  not droppable,
        star_first_name   CHARACTER VARYING (25) not null  not droppable,
        star_last_name    CHARACTER VARYING (25) not null  not droppable,
        PRIMARY KEY (title, star_first_name, star_last_name),
        FOREIGN KEY (title) REFERENCES movies
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table sample (c1 char(20), c2 smallint, c3 integer, c4 largeint, c5 varchar(120), c6 numeric(10,2),
        c7 decimal(10,2),c8 date, c9 time, c10 timestamp, c11 float, c12 double precision) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create table empl (empl_id  int, dept_id int, name varchar(30), date_of_birth  date, date_of_hire  date, monthly_salary numeric(15,2), position1 varchar(100),extension  int, office_location  varchar(100)) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table dept (dept_id int,name varchar(100), location varchar(100)) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table n1 (cof_name  varchar(32)  ,sup_id int, price float(54),sales int, total int) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table n2 (cof_name  varchar(32)  ,sup_id char(45), price float(54),sales decimal(9,4)) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table n3 (cof_name  nchar(32)  ,sup_id largeint, price smallint,sales decimal(9,4),tot numeric(8,3)) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table n4 (cof_name  nchar(32)  ,sup_id date, price time,sales timestamp, rel real) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table n5 (sup_id date, price time,sales timestamp) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table s2(a nchar(25)) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table TSTTBL021
        (
        C0                               CHAR(2) CHARACTER SET ISO88591 COLLATE
        DEFAULT DEFAULT NULL
        , C1                               SMALLINT DEFAULT NULL
        , C2                               SMALLINT UNSIGNED DEFAULT NULL
        , C3                               INT DEFAULT NULL
        , C4                               INT UNSIGNED DEFAULT NULL
        , C5                               LARGEINT DEFAULT NULL
        , C6                               REAL DEFAULT NULL
        , C7                               FLOAT(54) DEFAULT NULL
        , C8                               DOUBLE PRECISION DEFAULT NULL
        , C9                               DECIMAL(18, 2) DEFAULT NULL
        , C10                              NUMERIC(18, 2) DEFAULT NULL
        , C11                              NUMERIC(15, 6) DEFAULT NULL
        , C12                              NUMERIC(10, 0) DEFAULT NULL
        , C13                              NUMERIC(9, 2) DEFAULT NULL
        , C14                              NUMERIC(4, 1) DEFAULT NULL
        , C15                              CHAR(25) CHARACTER SET ISO88591 COLLATE
        DEFAULT DEFAULT NULL
        , C16                              VARCHAR(35) CHARACTER SET ISO88591 COLLATE
        DEFAULT DEFAULT NULL
        , C17                              VARCHAR(150) CHARACTER SET ISO88591
        COLLATE DEFAULT DEFAULT NULL
        , C18                              DATE DEFAULT NULL
        , C19                              TIME(0) DEFAULT NULL
        , C20                              TIMESTAMP(6) DEFAULT NULL
        , c21                               nchar(25)
        )  no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table lv_char(a long varchar(2000)) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table str_num (
        char_up         char(12)         UPSHIFT not null,
        varchars        varchar(7)       default 'DEFAULT',
        varchar_up      varchar(9)       UPSHIFT default 'default',
        picx            pic xxx          default 'DEF',
        picx_up         pic xxxxxxxxxxxx UPSHIFT default 'DEfauLT',
        picx_dis        pic x(12)        DISPLAY default 'DEFAULT',
        picx_updis      pic xxxxxxxxxxxx DISPLAY UPSHIFT default 'defaULT',
        char_vary       char varying (5) default 'DEFAU',
        char_vary_up    char varying (10)   UPSHIFT default 'default',
        num_s           numeric(7, 3)  signed not null,
        num_s2          numeric(7, 3)  signed default 0.0,
        num_us          numeric(9, 0)  unsigned default 0,
        smallint_s      smallint       signed default 0,
        smallint_us     smallint       unsigned default 0,
        integer_s       integer        signed default 0,
        integer_us      integer        unsigned default 0,
        large_int       largeint       default 0,
        decimal_s       decimal(8,7)   signed default 0.0,
        decimal_us      decimal(5,2)   unsigned default 0.0,
        pic_scomp       pic s9999999999  comp default 0,
        pic_uscomp      pic 9(2)        comp default 0,
        pic_s           pic s9(6)       default 0,
        pic_us          pic 99999       default 0,
        pic_vscomp      pic s9999999v99 comp default 0.0,
        pic_vuscomp     pic 9(2)v999    comp default 0.0,
        pic_vs          pic s9(6)v99999 display sign is leading default 0.0,
        pic_vus         pic 99999v9(2)  default 0.0,
        real_col        real           default 0.0,
        float_col       float(54)      default 0.0,
        double_preci    double precision  default 0.0,
        primary key (char_up, num_s)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table datetime_interval (
        date_key        date not null,
        date_col        date default date '0001-01-01',
        time_col        time default time '00:00:00',
        timestamp_col   timestamp
        default timestamp '0001-01-01:00:00:00.000000',
        interval_year   interval year default interval '00' year,
        yr2_to_mo       interval year to month
        default interval '00-00' year to month,
        yr6_to_mo       interval year(6) to month
        default interval '000000-00' year(6) to month,
        yr16_to_mo      interval year(16) to month default
        interval '0000000000000000-00' year(16) to month,
        year18          interval year(18) default
        interval '000000000000000000' year(18),
        day2            interval day default interval '00' day,
        day18           interval day(18)
        default interval '000000000000000000' day(18),
        day16_to_hr     interval day(16) to hour
        default interval '0000000000000000:00' day(16) to hour,
        day14_to_min    interval day(14) to minute default
        interval '00000000000000:00:00' day(14) to minute,
        day5_to_second6 interval day(5) to second(6) default
        interval '00000:00:00:00.000000' day(5) to second(6),
        hour2           interval hour default interval '00' hour,
        hour18          interval hour(18)
        default interval '000000000000000000' hour(18),
        hour16_to_min   interval hour(16) to minute default
        interval '0000000000000000:00' hour(16) to minute,
        hour14_to_ss0   interval hour(14) to second(0) default
        interval '00000000000000:00:00' hour(14) to second(0),
        hour10_to_second4        interval hour(10) to second(4) default
        interval '0000000000:00:00.0000' hour(10) to second(4),
        min2            interval minute default interval '00' minute,
        min18           interval minute(18) default
        interval '000000000000000000' minute(18),
        min13_s3        interval minute(13) to second(3) default
        interval '0000000000000:00.000' minute(13) to second(3),
        min16_s0        interval minute(16) to second(0) default
        interval '0000000000000000:00' minute(16) to second(0),
        seconds         interval second default interval '00' second,
        seconds5        interval second(5) default interval '00000' second(5),
        seconds18       interval second(18,0) default
        interval '000000000000000000' second(18,0),
        seconds15       interval second(15,3) default
        interval '000000000000000.000' second(15,3),
        primary key (date_key)
        ) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table tab2000
        (
        col0  char(143) not null,
        col1  smallint unsigned,
        col2  double precision,
        col3  real,
        col4  largeint,
        col5  time,
        col6  date,
        col7  timestamp,
        col8  smallint,
        col9  timestamp,
        col10  real,
        col11  integer,
        col12  numeric(2, 0) unsigned,
        col13  interval day(2),
        col14  char(2),
        col15  largeint,
        col16  real,
        col17  double precision,
        col18  double precision,
        col19  double precision,
        col20  smallint unsigned,
        col21  float(19),
        col22  char(154),
        col23  date,
        col24  date,
        col25  real,
        col26  integer,
        col27  timestamp,
        col28  interval minute(9),
        col29  numeric(4, 3),
        col30  smallint,
        col31  date,
        col32  interval minute(11),
        col33  float(14),
        col34  integer,
        col35  char(95),
        col36  numeric(1, 0) unsigned,
        col37  time,
        col38  integer unsigned,
        col39  double precision,
        col40  decimal(9, 0) unsigned,
        col41  timestamp,
        col42  real,
        col43  smallint unsigned,
        col44  real,
        col45  float(51),
        col46  timestamp,
        col47  numeric(6, 4),
        col48  double precision,
        col49  double precision,
        col50  largeint,
        col51  numeric(7, 5) unsigned,
        col52  real,
        col53  interval minute(6),
        col54  smallint unsigned,
        col55  real,
        col56  char(178),
        col57  real,
        col58  numeric(2, 1),
        col59  timestamp,
        col60  integer,
        col61  char(246),
        col62  decimal(10, 0),
        col63  time,
        col64  date,
        col65  double precision,
        col66  smallint,
        col67  date,
        col68  real,
        col69  smallint unsigned,
        col70  timestamp,
        col71  float(15),
        col72  double precision,
        col73  decimal(10, 0),
        col74  timestamp,
        col75  real,
        col76  numeric(15, 0),
        col77  real,
        col78  decimal(9, 0) unsigned,
        col79  numeric(16, 8),
        col80  largeint,
        col81  real,
        col82  largeint,
        col83  time,
        col84  largeint,
        col85  float(14),
        col86  interval month(13),
        col87  double precision,
        col88  smallint unsigned,
        col89  date,
        col90  float(27),
        col91  time,
        col92  char(253),
        col93  double precision,
        col94  char(135),
        col95  smallint unsigned,
        col96  decimal(9, 0) unsigned,
        col97  smallint,
        col98  numeric(13, 4),
        col99  interval month(6),
        col100  numeric(15, 10),
        col101  double precision,
        col102  timestamp,
        col103  integer unsigned,
        col104  char(15),
        col105  date,
        col106  time,
        col107  smallint unsigned,
        col108  double precision,
        col109  char(29),
        col110  float(40),
        col111  decimal(10, 0),
        col112  char(111),
        col113  smallint,
        col114  integer,
        col115  integer,
        col116  real,
        col117  decimal(10, 0),
        col118  real,
        col119  interval minute(16),
        col120  smallint unsigned,
        col121  smallint,
        col122  float(53),
        col123  numeric(1, 0),
        col124  interval year(16),
        col125  integer unsigned,
        col126  timestamp,
        col127  float(10),
        col128  decimal(9, 0) unsigned,
        col129  float(25),
        col130  double precision,
        col131  decimal(10, 0),
        col132  date,
        col133  decimal(9, 0) unsigned,
        col134  double precision,
        col135  largeint,
        col136  smallint,
        col137  double precision,
        col138  time,
        col139  integer,
        col140  double precision,
        col141  timestamp,
        col142  double precision,
        col143  largeint,
        col144  real,
        col145  numeric(11, 6),
        col146  decimal(9, 0) unsigned,
        col147  numeric(15, 13),
        col148  double precision,
        col149  timestamp,
        col150  char(170),
        col151  interval month(10),
        col152  integer,
        col153  numeric(15, 11),
        col154  smallint unsigned,
        col155  numeric(11, 9),
        col156  double precision,
        col157  float(22),
        col158  integer,
        col159  real,
        col160  numeric(13, 4),
        col161  date,
        col162  interval minute(13),
        col163  integer unsigned,
        col164  numeric(14, 7),
        col165  double precision,
        col166  interval year(15),
        col167  decimal(10, 0),
        col168  numeric(4, 1),
        col169  time,
        col170  double precision,
        col171  decimal(10, 0),
        col172  real,
        col173  largeint,
        col174  real,
        col175  date,
        col176  real,
        col177  largeint,
        col178  decimal(10, 0),
        col179  double precision,
        col180  float(1),
        col181  timestamp,
        col182  numeric(15, 7),
        col183  timestamp,
        col184  real,
        col185  largeint,
        col186  date,
        col187  double precision,
        col188  largeint,
        col189  interval hour(3),
        col190  largeint,
        col191  numeric(17, 10),
        col192  char(84),
        col193  char(127),
        col194  numeric(15, 8),
        col195  timestamp,
        col196  time,
        col197  char(32),
        col198  timestamp,
        col199  decimal(10, 0),
        col200  char(43),
        col201  decimal(10, 0),
        col202  largeint,
        col203  largeint,
        col204  decimal(9, 0) unsigned,
        col205  date,
        col206  real,
        col207  double precision,
        col208  date,
        col209  time,
        col210  numeric(7, 1),
        col211  numeric(1, 0) unsigned,
        col212  double precision,
        col213  integer unsigned,
        col214  smallint unsigned,
        col215  numeric(2, 0),
        col216  date,
        col217  time,
        col218  date,
        col219  timestamp,
        col220  double precision,
        col221  largeint,
        col222  time,
        col223  smallint,
        col224  smallint,
        col225  double precision,
        col226  interval year(1),
        col227  real,
        col228  float(5),
        col229  integer,
        col230  integer unsigned,
        col231  numeric(1, 0),
        col232  char(85),
        col233  time,
        col234  float(23),
        col235  interval minute(9),
        col236  date,
        col237  timestamp,
        col238  float(13),
        col239  char(134),
        col240  interval day(4),
        col241  double precision,
        col242  integer,
        col243  interval day(16),
        col244  char(90),
        primary key  (col0) not droppable
        )
        store by primary key;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table t5
        (
        Int_1            INT SIGNED not null,
        Large_2          LARGEINT not null,
        Flt_1            FLOAT,
        Ch_1             CHAR(10),
        primary key( Int_1)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table t6
        (
        Ch_1             CHAR(10) not null,
        Dec_1            DECIMAL(9, 0) SIGNED,
        IntvlYr_Mn_1     INTERVAL YEAR(2) TO MONTH,
        IntvlHr_Mi_2     INTERVAL HOUR(2) TO MINUTE,
        Int_1            INT ,
        Int_2            INT ,
        primary key( Ch_1)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table i3(
        col_int         integer   default 2147483647 not null
        , col_i64         largeint  default 9.223E18
        , col_u64         largeint  default 0
        , col_float       float     default 1.7272337e-76 not null
        , col_float4      float(4)  default -1.7272337e-76
        , col_float21     float(21) default 1.1579208e77
        , col_float22     float(22) default -1.1579208e77
        , col_float23     float(23) default +1.7272337110188889e-76
        , col_float52     float(52) default -1.7272337110188889e-76 not null
        , col_float53     float(53) default 1.1579208E77
        , col_float54     float(54) default -1.15792089237316189e77 not null
        , col_real        real      default -1.1579208e38
        , col_doublep     double precision  default -1.15792089237316189e77
        , primary key (col_int));"""
    output = _dci.cmdexec(stmt)

    stmt = """create table i4(
        col_int         integer   default 2147483647 not null
        , col_i64         largeint  default 9.223E18 not null
        , col_u64         largeint  default 0
        , col_float       float     default 2.2250738585072014e-308
        , col_float4      float(4)  default -2.2250738585072014e-308
        , col_float21     float(21) default 1.7976931348623157e+308
        , col_float22     float(22) default -1.7976931348623157e+308
        , col_float23     float(23) default 1.15792089237316192e77
        , col_float52     float(52) default -2.2250738585072014e-308
        , col_float53     float(53) default 2.2250738585072014e-308
        , col_float54     float(54) default -1.7976931348623157e+308
        , col_real        real      default -1.17549435e-38
        , col_doublep     double precision  default -2.2250738585072014e-308
        , primary key (col_int, col_i64));"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table b2
        (
        char0_100           Character(9)                  no default not null,
        sbin0_100           Integer                       no default not null,
        int0_dTOf6_n100     Interval day to second(6)            no default,
        sdec0_nuniq         Decimal(9)                             no default,
        date0_100           Date                       not null,
        time1_1000          Time                       not null,
        int1_yTOm_uniq      Interval year(5) to month  not null,
        udec1_2             Decimal(9) unsigned        not null,
        ubin1_uniq          Numeric(9) unsigned        not null,
        real1_uniq          Real                          no default not null,
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
        dt16_m_n10          Date                     ,
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
        char17_2            Character(8)               not null,
        primary key  (  date0_100, time1_1000 DESC, int1_yTOm_uniq) not droppable
        )
        store by primary key;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table b3 (
        ordering            smallint   not null
        , alwaysnull          smallint                default null
        , char_1              char(1)                 default null
        , pic_x_8             pic x(8)                default null
        , var_char_2          varchar(2)              default null
        , var_char_3          varchar(3)              default null
        , binary_signed       numeric (4) signed      default null
        , binary_32_u         numeric (9,2) unsigned  default null
        , binary_64_s         numeric (18,3) signed   default null
        , pic_comp_1          pic s9(10) comp         default null
        , pic_comp_2          pic sv9(2) comp         default null
        , pic_comp_3          pic s9(3)v9(5) comp     default null
        , small_int           smallint                default null
        , medium_int          integer unsigned        default null
        , large_int           largeint signed         default null
        , decimal_1           decimal (1)             default null
        , decimal_2_signed    decimal (2,2) signed    default null
        , decimal_3_unsigned  decimal (3,0) unsigned  default null
        , pic_decimal_1       pic s9(1)v9(1)          default null
        , pic_decimal_2       picture v999 display    default null
        , pic_decimal_3       pic s9                  default null
        , float_basic         float (4)               default null
        , float_real          real                    default null
        , float_double_p      double precision        default null
        , y_to_d              date                    default null
        , y_to_d_2            date                    default null
        , h_to_f              time                 default null
        , time1               time                    default null
        , iy_to_mo            interval year(4) to month  default null
        , ih_to_s             interval hour to second default null
        , primary key (ordering)
        )
        ;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table b32
        (
        "char0_100"           Character(8)               not null,
        "sbin0_uniq"          Integer                    not null,
        "sdec0_n10"           Decimal(4)                              default 9,
        "int0_yTOm_uniq"      Interval year(5) to month     no default not null,
        "date0_nuniq"         Date                                   no default,
        "double1_uniq"        Double Precision           not null,
        "ts1_n100"            Timestamp                          ,
        "ubin1_500"           Numeric(4) unsigned           no default not null,
        "int1_dTOf6_100"      Interval day to second(6)   no default not null,
        "udec1_n2000"         PIC 9(8)V9                         ,
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
        "dt16_m_n10"          Date                     ,
        "int16_h_20"          Interval hour                 no default not null,
        "ubin16_n10"          Numeric(4) unsigned                    no default,
        "sdec16_uniq"         Decimal(18) signed         not null,
        "char16_n20"          Character(5)        ,   -- len = 2,4
        "real16_10"           Real                          no default not null,
        "int17_y_n10"         Interval year(1)                       no default,
        "dt17_yTOmin_uniq"    Timestamp(0)    not null,
        "real17_n100"         Real                               ,
        "sbin17_uniq"         Largeint  no default not null,  -- range: 0-149999
        "sdec17_nuniq"        Decimal(18)                            no default,
        "char17_2"            Character(8)               not null,
        primary key  (  "int0_yTOm_uniq", "int1_dTOf6_100" DESC) not droppable
        )
        store by primary key  ;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table big210
        (
        char0_n10           Character(2)
        default 'AD' heading 'char0_n10 with default AD',
        sbin0_uniq          int                    not null,
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
        dt16_m_n10          Date                     ,
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
        ) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table B212 (
        Y           INTERVAL    YEAR(4),
        Y_to_MO     INTERVAL    YEAR(4) TO MONTH,
        MO          INTERVAL    MONTH,
        D           INTERVAL    DAY,
        D_to_H      INTERVAL    DAY TO HOUR,
        D_to_MI     INTERVAL    DAY TO MINUTE,
        D_to_S      INTERVAL    DAY TO SECOND(0),
        D_to_F      INTERVAL    DAY TO SECOND(3),
        H           INTERVAL    HOUR,
        H_to_MI     INTERVAL    HOUR TO MINUTE,
        H_to_S      INTERVAL    HOUR TO SECOND(0),
        H_to_F      INTERVAL    HOUR TO SECOND(3),
        MI          INTERVAL    MINUTE,
        MI_to_S     INTERVAL    MINUTE TO SECOND(0),
        MI_to_F     INTERVAL    MINUTE TO SECOND(3),
        S           INTERVAL    SECOND(2,0),
        S_to_F      INTERVAL    SECOND(2,3)
        ) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO b212 VALUES
        ( interval '10' year(2),
        interval '10-01' year(2) TO MONTH,
        interval '01' month,
        interval '15' day,
        interval '15:12' day TO HOUR,
        interval '16:13:15' day TO MINUTE,
        interval '17:14:16:01' DAY TO SECOND(0),
        interval '18:15:17:02.123' DAY TO SECOND(3),
        interval '16' hour,
        interval '17:18' hour TO MINUTE,
        interval '18:19:03' HOUR TO SECOND(0),
        interval '19:20:04.345' HOUR TO SECOND(3),
        interval '21' minute,
        interval '21:05' MINUTE TO SECOND(0),
        interval '22:06.444' MINUTE TO SECOND(3),
        interval '07' SECOND(2,0),
        interval '08.555' SECOND(2,3)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO b212 VALUES
        ( interval '9999' year(4),
        interval '9999-11' year(4) TO MONTH,
        interval '11' month,
        interval '31' day,
        interval '30:01' day TO HOUR,
        interval '29:02:59' day TO MINUTE,
        interval '28:03:58:59' DAY TO SECOND(0),
        interval '27:04:57:58.999' DAY TO SECOND(3),
        interval '23' hour,
        interval '22:56' hour TO MINUTE,
        interval '21:55:57' HOUR TO SECOND(0),
        interval '20:54:56.888' HOUR TO SECOND(3),
        interval '59' minute,
        interval '58:59' MINUTE TO SECOND(0),
        interval '57:58.777' MINUTE TO SECOND(3),
        interval '59' SECOND(2,0),
        interval '58.666' SECOND(2,3)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO b212 VALUES
        ( interval '1' year(4),
        interval '1-1' year(4)  TO MONTH,
        interval '1' month,
        interval '1' day,
        interval '1:1' day TO HOUR,
        interval '1:1:1' day TO MINUTE,
        interval '1:1:1:1' DAY TO SECOND(0),
        interval '1:1:1:1.1' DAY TO SECOND(3),
        interval '1' hour,
        interval '1:1' hour TO MINUTE,
        interval '1:1:1' HOUR TO SECOND(0),
        interval '1:1:1.1' HOUR TO SECOND(3),
        interval '1' minute,
        interval '1:1' MINUTE TO SECOND(0),
        interval '1:1.1' MINUTE TO SECOND(3),
        interval '1' SECOND(2,0),
        interval '1.1' SECOND(2,3)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO b212 VALUES
        ( interval '1' year(2),
        interval '1-1' year(2) TO MONTH,
        interval '1' month,
        interval '1' day,
        interval '0:0' day TO HOUR,
        interval '0:0:0' day TO MINUTE,
        interval '0:0:0:0' DAY TO SECOND(0),
        interval '0:0:0:0.0' DAY TO SECOND(3),
        interval '0' hour,
        interval '0:0' hour TO MINUTE,
        interval '0:0:0' HOUR TO SECOND(0),
        interval '0:0:0.0' HOUR TO SECOND(3),
        interval '0' minute,
        interval '0:0' MINUTE TO SECOND(0),
        interval '0:0.0' MINUTE TO SECOND(3),
        interval '0' SECOND(2,0),
        interval '0.0' SECOND(2,3)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO b212 VALUES
        ( interval '1444' year(4),
        interval '1445-09' year(4) TO MONTH,
        interval '8' month,
        interval '22' day,
        interval '23:10' day TO HOUR,
        interval '24:10:10' day TO MINUTE,
        interval '25:10:10:10' DAY TO SECOND(0),
        interval '26:9:09:09.009' DAY TO SECOND(3),
        interval '11' hour,
        interval '11:12' hour TO MINUTE,
        interval '11:12:13' HOUR TO SECOND(0),
        interval '11:12:13.444' HOUR TO SECOND(3),
        interval '14' minute,
        interval '14:14' MINUTE TO SECOND(0),
        interval '14:14.444' MINUTE TO SECOND(3),
        interval '35' SECOND(2,0),
        interval '35.333' SECOND(2,3)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into coffees values('Colombian', 101, 7.99, 0, 0);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into coffees values('Colombian_Decaf', 101, 8.99, 0, 0);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into coffees values('French_Roast_Decaf', 49, 9.99, 0, 0);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into coffees values('Espresso', 150, 9.99, 0, 00);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into coffees values('French_Roast', 49, 8.99, 0, 0);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into coffees values('Indian_Assam_Coffee', 68, 10.99, 0, 0);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into coffees values('Assam_Coffee',123,7.88,0,0);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into coffees values('Andhra_Tea',142,10.98,0,0);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into ntab values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into ntab values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into ntab values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into ntab values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into ntab values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into ntab values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into ntab values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into SUPPLIERS values(49, 'Superior Coffee', '1 Party Place', 'Mendocino', 'CA', '95460');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into SUPPLIERS values(101, 'Acme, Inc.', '99 Market Street', 'Groundsville', 'CA', '95199');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into SUPPLIERS values(150, 'The High Ground', '100 Coffee Lane', 'Meadows', 'CA', '93966');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into sample values('Moe', 100, 12345678, 123456789012, 'Moe', 100.12, 100.12, {d '2000-05-16'}, {t '10:11:12'},
        {ts '2000-05-06 10:11:12.0'}, 100.12, 100.12);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into sample values('Larry', -100, -12345678, -123456789012, 'Larry', -100.12, -100.12, {d '2000-05-16'}, {t '10:11:12'},
        {ts '2000-05-06 10:11:12'}, -100.12, -100.12);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into sample values('Curly', 100, -12345678, 123456789012, 'Curly', -100.12, 100.12, {d '2000-05-16'}, {t '10:11:12'},
        {ts '2000-05-06 10:11:12'}, -100.12, 100.12);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into sample values('Smith', 125, -987654321, 987654321233, 'Smith', -125.99, 125.32, {d '2005-10-20'}, {t '12:10:10'},
        {ts '2005-10-20 12:45:45'}, -125.32, 124.98);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (100 , 'ACCOUNTING'          , 'BUTLER, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (101 , 'RESEARCH'            , 'DALLAS, TX');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (102 , 'SALES'               , 'CHICAGO, IL');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (103 , 'OPERATIONS'          , 'BOSTON, MA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (104 , 'IT'                  , 'PITTSBURGH, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (105 , 'ENGINEERING'         , 'WEXFORD, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (106 , 'QA'                  , 'WEXFORD, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (107 , 'PROCESSING'          , 'NEW YORK, NY');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (108 , 'CUSTOMER SUPPORT'    , 'TRANSFER, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (109 , 'HQ'                  , 'WEXFORD, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (110 , 'PRODUCTION SUPPORT'  , 'MONTEREY, CA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (111 , 'DOCUMENTATION'       , 'WEXFORD, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (112 , 'HELP DESK'           , 'GREENVILLE, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (113 , 'AFTER HOURS SUPPORT' , 'SAN JOSE, CA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (114 , 'APPLICATION SUPPORT' , 'WEXFORD, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (115 , 'MARKETING'           , 'SEASIDE, CA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (116 , 'NETWORKING'          , 'WEXFORD, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (117 , 'DIRECTORS OFFICE'    , 'WEXFORD, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (118 , 'ASSISTANTS'          , 'WEXFORD, PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (119 , 'COMMUNICATIONS'      , 'SEATTLE, WA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into dept values (120 , 'REGIONAL SUPPORT'    , 'PORTLAND, OR');"""
    output = _dci.cmdexec(stmt)

    stmt = """Insert into empl values (1001,105,'Jeff Hunter', date '1967-10-24',date '1994-07-28',8700.00,
        'Sr.Software Engineer',8007,'Butler,PA');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n1 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n1 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n1 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n2 values(null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n2 values(null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n2 values(null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n2 values(null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n2 values(null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n2 values(null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n3 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n3 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n3 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n4 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n4 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n4 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n4 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n4 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n4 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n4 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n4 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n4 values(null,null,null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n5 values(null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into n5 values(null,null,null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into s2 values(_ucs2'AAA Computers'),(_ucs2'131324353'),(_ucs2'#^$%&%^*^'),(_ucs2'"double Quotes"'),(_ucs2'               '),(_ucs2'heWlEtT pAcKArD');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into str_num
        (char_up, varchars, varchar_up, picx, picx_up,
        picx_dis, picx_updis, char_vary, char_vary_up, num_s)
        values
        ('char UPSHIFT', 'Varchar', 'xxxxxxxxx', 'piC', 'pic DISPLAY ',
        'picUpDisP   ', 'Picx12      ', 'varyc', 'varychup', 4444.333);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into str_num
        (char_up, varchars, varchar_up, picx, picx_up,
        picx_dis, picx_updis, char_vary, char_vary_up, num_s)
        values
        ('3rd row     ', '7vArcH', '9ArcH', '3pP', 'still x(12) ',
        '3rd DISPLAY ', 'Oh, char    ', '5var', '10 vary', 9210.945);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into str_num
        (char_up, varchars, varchar_up, picx, picx_up,
        picx_dis, picx_updis, char_vary, char_vary_up, num_s)
        values
        ('2nd charUP  ', 'varcha7', 'varChA9', '33p', 'col pix only',
        'col33333    ', '2nd cold    ', NULL, 'changeV', 923.10);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into str_num
        (char_up, num_s, num_s2, num_us, smallint_s, smallint_us,
        integer_s, integer_us, large_int, decimal_s, decimal_us)
        values
        ('c11111111111', 1234.98, -1234.98, 987651234, -32768, null,
        -2147483648, 4294967295, 92231234567, 1.1111117, 133.11);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into str_num
        (char_up, num_s, num_s2, num_us, smallint_s, smallint_us,
        integer_s, integer_us, large_int, decimal_s, decimal_us)
        values
        ('c22222222222', 5678.28, -5678.28, null, 32767, 65535,
        -2147483647, 7295, 3457, -2.2222227, 23.21);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into str_num
        (char_up, num_s, num_s2, num_us, smallint_s, smallint_us,
        integer_s, integer_us, large_int, decimal_s, decimal_us)
        values
        ('c33333333333', -3482.73, 3482.73, 4376, -7431, 65124,
        4836, 9672, -457, 3.3333337, 333.13);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into str_num
        (char_up, num_s, pic_scomp, pic_uscomp,
        pic_s, pic_us, pic_vscomp, pic_vuscomp, pic_vs, pic_vus,
        real_col, float_col, double_preci)
        values
        ('N11111a1111n', 1111.111, 1234567891, 11, 654321, 12345,
        7654321.11, 12.111, 654321.11111, 15432.11,
        1.157911e+38, 1.7272337E-76, -1.7272337E-76);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into str_num
        (char_up, num_s, pic_scomp, pic_uscomp,
        pic_s, pic_us, pic_vscomp, pic_vuscomp, pic_vs, pic_vus,
        real_col, float_col, double_preci)
        values
        ('N22222a2222n', 2233.212, 2134567892, 28, 254322, 54321,
        2654322.12, 29.282, 254322.29832, 25732.22,
        -1.1579108E38, -1.7272337E-76, -1.7272337E-76);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into str_num
        (char_up, num_s, pic_scomp, pic_uscomp,
        pic_s, pic_us, pic_vscomp, pic_vuscomp, pic_vs, pic_vus,
        real_col, float_col, double_preci)
        values
        ('N33333a3333n', 3233.393, 3134567333, 31, 35622, 011,
        3928333.32, 39.375, 382930.33923, 34632.33,
        1.1579108E38, -1.7272337E-76, -1.7272337E-76);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into str_num
        (char_up, num_s, num_us, smallint_s, smallint_us,
        integer_s, integer_us, large_int, decimal_s, decimal_us)
        values
        ('c11111111111', 9999.99, null, null, null,
        null, null, null, null, null);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into str_num
        (char_up, num_s, num_us, smallint_s, smallint_us,
        integer_s, integer_us, large_int, decimal_s, decimal_us)
        values
        ('c33333333333', -3480.73, 65124, -4376, 7431,
        4836, 9672, -457, 3.3333337, 333.13);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into datetime_interval
        (date_key, date_col, time_col, timestamp_col,
        interval_year, yr2_to_mo, yr6_to_mo, yr16_to_mo, year18)
        values
        (date '0011-12-30', date '1239-01-01', time '01:01:01',
        timestamp '0091-10-10 10:10:10.111111', - interval '11' year,
        interval '11-11' year to month,
        interval '111111-11' year(6) to month,
        interval '1111111111111111-11' year(16) to month,
        interval '111111111111111111' year(18));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into datetime_interval
        (date_key, date_col, time_col, timestamp_col,
        interval_year, yr2_to_mo, yr6_to_mo, yr16_to_mo, year18)
        values
        (date '2999-12-30', date '2999-12-12', time '09:59:59',
        timestamp '9992-02-21 10:59:59.666666', interval '22' year,
        interval '22-02' year to month,
        interval '222222-02' year(6) to month,
        interval '1234567890123456-09' year(16) to month,
        interval '123456789012345678' year(18));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into datetime_interval
        (date_key, day2, day18, day16_to_hr, day14_to_min, day5_to_second6,
        hour2, hour18, hour16_to_min, hour14_to_ss0, hour10_to_second4)
        values
        (date '8011-12-30', interval '18' day,
        interval '987654321012345678' day(18),
        interval '5678901234123456:11' day(16) to hour,
        interval  '12345678904321:11:59' day(14) to minute,
        interval '54321:11:59:59' day(5) to second(6),
        interval '22' hour,
        interval '999999999999999999' hour(18),
        interval  '9999999999999999:59' hour(16) to minute,
        interval '99999999999999:59:59' hour(14) to second(0),
        interval  '9999999999:11:59.1234' hour(10) to second(4));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into datetime_interval
        (date_key, day2, day18, day16_to_hr, day14_to_min, day5_to_second6,
        hour2, hour18, hour16_to_min, hour14_to_ss0, hour10_to_second4)
        values
        (date '4011-10-03', interval '98' day,
        interval '00321012345678' day(18),
        interval '000000123456:11' day(16) to hour,
        interval '32100000000:11:59' day(14) to minute,
        interval '99999:01:09:39' day(5) to second(6),
        interval '99' hour,
        interval '123456789012345678' hour(18),
        interval '1234567890123456:01' hour(16) to minute,
        interval '12345678901234:59:45' hour(14) to second(0),
        interval '1234567890:05:29.9999' hour(10) to second(4));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into datetime_interval
        (date_key, day2, day18, day16_to_hr, day14_to_min, day5_to_second6,
        hour2, hour18, hour16_to_min, hour14_to_ss0, hour10_to_second4)
        values
        (date '1011-07-18', interval '95' day,
        interval '123456789012345678' day(18),
        interval '6:01' day(16) to hour,
        interval '1:01:09' day(14) to minute,
        interval '1:01:01:01' day(5) to second(6),
        interval '77' hour,
        interval '12345678' hour(18),
        interval '123456:16' hour(16) to minute,
        interval '1234:45:10' hour(14) to second(0),
        interval '1:01:50.0000' hour(10) to second(4));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into datetime_interval
        (date_key, min2, min18, min13_s3, min16_s0, seconds,
        seconds5, seconds18, seconds15)
        values
        (date '0009-02-01',
        interval  '99' minute,
        interval  '999999999999999999' minute(18),
        interval  '9999999999999:59.999' minute(13) to second(3),
        interval  '9999999999999999:59' minute(16) to second(0),
        interval  '99' second,
        interval  '99999' second(5),
        interval  '999999999999999999' second(18,0),
        interval  '999999999999999.999' second(15,3));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into datetime_interval
        (date_key, min2, min18, min13_s3, min16_s0, seconds,
        seconds5, seconds18, seconds15)
        values
        (date '5009-02-01',
        interval '01' minute,
        interval '000000000000000001' minute(18),
        interval  '01:01.001' minute(13) to second(3),
        interval '00001:01' minute(16) to second(0),
        interval  '01' second,
        interval '00001' second(5),
        interval  '000000000000000001' second(18,0),
        interval '000000000000001.001' second(15,3));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into datetime_interval
        (date_key, min2, min18, min13_s3, min16_s0, seconds,
        seconds5, seconds18, seconds15)
        values
        (date '7009-02-01',
        interval '11' minute,
        interval  '123456789012345678' minute(18),
        interval '1234567890123:12.000' minute(13) to second(3),
        interval  '1234567890123456:56' minute(16) to second(0),
        interval '76' second,
        interval '12345' second(5),
        interval  '123456789012345678' second(18,0),
        interval '123456789012345.783' second(15,3));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tab2000 values ('0', 11598, -9999999999999999999.999999,
        -4084864663.308103723, -4155107703233106935, time '14:58:03', date '4090-05-09',
        timestamp '2082-01-18 08:01:01.26', -6192, timestamp '3126-06-17 13:33:48.39',
        -0232637165.815979197, 2046207240, 16, interval '4' day(2), 'Y', 2850649416109126779,
        6102675372.622920710, -35333046357450423.899541, -73105600367110308.594237,
        -45086146865586252.2695954, 54672,0544081501.633644261,
        'FXAavxhZT4NOFTT8Cwg5YCg2Vcz7eknhKhMJQT5PsYx0VmkylKm8lxshmcVV3aBAXCEUoIf642cEN',
        date '3741-09-07', date '4229-09-05', 0476064877.334060772, 802577871,
        timestamp '2105-06-26 01:05:08.08', INTERVAL '8' MINUTE(9), -3.808,
        -4680, date '3327-01-05', INTERVAL '1' MINUTE(11), -4185484688.881321977, 839291124,
        'bVBaozj5FpU5nbVoIX1uH02OoYxwcIyhu4m7h14BnNIMAb2iqsQI8LWAYTiGbaUu4CVcNbQ9FRqYOLq1CUvaD',
        5, time '09:22:01.17', 1011950181, 32407278512572267.2148509, 052112480,
        timestamp '1663-04-08 11:28:24.54', 2438477757.392971741, 21610, 2787240003.741217105,
        -801578.088356429975211, timestamp '2731-06-10 05:28:40.55', 82.5284,
        -45331754556566.8147040, 20284551504.7302685, -1503861117887224534, 20.22472,
        3610533682.839622352, INTERVAL '1' MINUTE(6), 43456, -5678752714.639140621,
        'l2VcDc8fJ8J3zyzOZ7raMcOA8LmzvMYagyrtZ1tmJ', -8333357338.546701203, -5.3,
        timestamp '1662-07-04 06:48:25.58', -563167928,
        'GnsDtzV1yASTffU1NwDfzlv5otjvlqmkueF8YB5lDDRp7rsYYNXaqr82GRp6EfZerxNFAi9ea5zUlgAQGZZqE2j9Hnemmlm8KTsQW661qgc5j4w8xuQ4xAPqDGXXUEZIrvc5Vwrnuc3pzi3LWmCVANXku8Rm2cUcifIJHnesczipYFq05hrRDsvGYGeZIgF7SDB5Iw3OhFgrHXw2UCwBKxNIDZlagcn',
        -363147718, time '07:08:35.00', date '4366-06-11', -278426453815.1211684, -23788,
        date '2684-08-19', -7706327725.117421523, 15055, timestamp '1834-05-08 22:13:15.36',
        5263606516.358540653, 16667652126841.8634939, -551845056, timestamp '1704-08-06 05:43:58.44',
        4875661613.678803644, 535360080303324, -2587432863.766862157, 504488620,
        -45031860.06977166, -7004660654890357284, 2157674856.087983122, -2281873799006071216,
        time '08:32:37.55', 860576169358079549, -6200141572.869124771, INTERVAL '3' MONTH(13),
        -7844663623076.4202673, 5018, date '3277-07-10', 358.927599602272239, time '18:14:19.13',
        'p6YgJoxlW4tcUSIHwgeVbttiGuTLJ6OSKesaV0JsDiFlIxFPSRMh8TcoEi9CWLWL1r02ujg89KheuyATXK3I5molBtnZW2yB7cWsGnPrk3D15KjBQY98FfcJ2KLJrWy3h9czvwatnWEc4yJBRJKLmxW5IYX7VmNF1ZTQMy39HpLQN7IqFm3kjSQIM00LFGcZ4Ipa6Ygi1xVeubewaoJUvBhZyt6LI3KotoMOOVEFkAD03befyt6Z',
        650046126.3359998,
        '7Qt0A7LEkScuFnajHs1HvahrIaVe5XmxBW35HNpMNS8Jiv2WT7Xghb7BmNmuVO8jNlAeyUVZQzENf',
        22110, 531312102, -28845, -453068303.8195, INTERVAL '6' MONTH(6), -50255.6856593062,
        8626012401.5348041, timestamp '3016-04-11 03:21:29.18', 3194344946, 'Z4RA',
        date '3615-04-14', time '04:27:19.24', 50880, 230440715731762.0024,
        'AnJ5HLmNCXtJGP8iscayilMb5V2', -45326.942184603199580, 763566275,
        'O3IikvN5vBOamH5YoWNqnpHUZcW8ia2PxzWf6w1YWmOWNUEyT', -26539, -493878499, 1706217988,
        1341032348.743763011, -130674417, -4877442360.600162984, INTERVAL '4' MINUTE(16),
        51695, 30415, -158.285486616536, 8, INTERVAL '8' YEAR(16), 103862278,
        timestamp '2160-08-27 15:29:21.48', -6860268130.214956254, 607843045, 6433101205655706581,
        -515774378057621047e55, 843730557, date '2456-11-09', 622243242, 3665808543355.4016210,
        -7311150180122707628, 19133, 6105736430.5549327, time '08:19:32.58', 681042263,
        -826384556.5289081, timestamp '2489-02-18 15:37:47.51', 780083.7511785,
        2354207472840603401, 3161876125.153887630, 72663.960413, 474163010, 41.7500628990172,
        -80675877.1983007, timestamp '2752-10-30 07:52:49.01',
        'bKafvYc3mcvCq4cArMT4YFCLzmmVRxl9tKxmChsjITHbJtv6xnn8cwuziWBW1UovBjPULrqG2TlbtBKwqOxuz72GZZwRMxoWIkAur0c6L3aFC',
        INTERVAL '4' MONTH(10), 2112352316, -7636.49368304743, 46447, -76.444655118,
        8885.3445159, 3206807338.998862344, 2004874172, 0704487871.815076797, 355311678.3280,
        date '1590-08-01', INTERVAL '0' MINUTE(13), 4238287909, -1127603.6837745, 265742.8573274,
        INTERVAL '0' YEAR(15), -308475712, -704.0, time '08:42:39.29', -22266216822.1157294,
        -028162474, 6401524085.767945548, -7174566589668409133, 1160453342.009317841,
        date '2004-07-19', 6170056271.882876400, 3339660809692154547, -775828551,
        104.5909229, 8101382855.937084123, timestamp '1846-10-15 02:32:10.26', -33422812.2018507,
        timestamp '2175-08-27 13:41:11.16', -1157174145.175157793, -5232775974148383384,
        date '2255-06-18', -73288231372.4733990, -747742967858968982, INTERVAL '6' HOUR(3), -4200330505619237033,
        -3723010.9510756331, '65jNGjWTT2M1HfMUfM',
        'MTzMYSccIEFeX9bNLWcbtLMxV9X9YDIiHL6MqFCK3DjUEWTZ3NyqcOaY7V',
        3702163.56405965, timestamp '3199-10-14 01:08:40.53', time '02:23:00.38',
        '0uC6XpzMYKkvXMU1Jm6xB2IFqApRUHE', timestamp '2877-05-17 12:00:56.05',
        816024145, 'Mgwubp9aINED7L7eENcBarPmoLGYZKh8XNuowRnm38e', -068532668,
        -4724518552171639913, -1240752503883112656, 253508550, date '1757-08-17',
        0238860278.241067575, 666013345822.9757039, date '3842-11-28', time '04:47:37.02',
        076666.7, 1, 81285844780600.1360227, 69892995, 60943, -64, date '3466-06-14',
        time '22:41:17.19', date '2924-09-04', timestamp '2979-09-03 16:30:47.20',
        -5713484.0397789, 2915004435460583200, time '14:52:13.54', 3270, -10431,
        2242251835.3361529, INTERVAL '7' YEAR(1), -4854638218.948388932, 2030848352.359236819,
        -225048903, 2645426975, -6, 'zNgRbTmDDchSVE5USL', time '09:44:29.16',
        -85744728532.27835713, INTERVAL '6' MINUTE(9), date '2899-06-27',
        timestamp '3541-08-20 19:58:39.49', 6864117861.488590543,
        '7D7cBpjHAzTQphTbZUuYFt9RWrPcgGO9a8kiVOX9g47u88XHXxSSKbaj4cp4ncci3oBP7pU5ctf17rKwAuinI58ycMWPeR6JlO0te5K385R4CEjKO',
        INTERVAL '0' DAY(4), 101582384801.7570416, -1486445201, INTERVAL '0' DAY(16),
        'DRn2FXaNeX1GfjJvG7i515K5MOWk');"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( 4.942827519712582E26, -3.1309435524155164E38, 7.594749387433122E13, 1.947974892549734E9,
        2175,            null, 1.9773025819571992E60,       9.03,   -3580.41,
        -2.8055469090990334E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN (N5, N3, N2, s1, s0, N6, N1, s2, s3, N4)  VALUES (
        5.007896699313307E25, -1.6187509032816747E38, 7.594749682273267E13, 1.798301806201026E8,        32206,
        5.720461176103054E19, 1.743765668960615E60,       1.37,    -613.34, 3.2323660295253167E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( 4.875861976385449E26,       null, 7.59475751341826E13, 2.880917621956657E8,
        6896, 5.720404263321621E19, 4.258079875018589E60,        6.9,   -1769.25,
        null) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES (       null, -2.907587572074583E38, 7.594748871091198E13, 7.02651917024814E8,
        2246, 5.720559482609924E19, 2.11195312321434E60,      -7.71,    -3301.0,
        1.6343409861670025E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( -1.405034579407558E26, 6.821274823686944E37, 7.594751800345695E13, 2.072142055028277E9,
        9579, 5.720669225499993E19, 4.674560002342868E60,      14.97,   -1463.94,
        2.501401722376738E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( 9.212283208272503E26, 1.0450166683529358E38, 7.594732521107677E13, 1.399418106121844E9,
        33643, 5.720378698019163E19, 4.208209083100687E60,      -3.95,    2438.42,
        -2.1639229968100792E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( 8.821929368604119E26, -3.4210686348481095E37, 7.594758522175428E13, 1.567478029353561E9,
        62498, 5.720573650076573E19,            null,      -4.54,    2730.05,
        -2.873808166354463E37) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( 7.653664928885494E26, 2.5400231249663133E38, 7.594737337268548E13, 1.114387785178059E9,
        59860, 5.720399002433927E19, 7.496566770957052E59,       2.88,    -573.76,
        null) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES (       null, -2.1600546534406616E38,            null, 3.925190009986142E8,
        48594,            null, 1.234826930785855E60,       4.94,    3300.27,
        4.468011345170713E37) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( -3.2016849327473334E26, 2.581671918639232E37, 7.594761837627564E13, 1.629533663784055E9,
        1376, 5.720601106826706E19, 4.753418704996284E60,       null,    -321.45,
        -2.3282837882262257E37) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( 1.5203439838939815E26, -1.4321401787868914E38,            null, 1.722368278078835E9,
        46704, 5.720610824298581E19, 4.551584758803844E60,      -3.33,   -2051.87,
        3.262053083976856E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN (N5, N3, N2, s1, s0, N6, N1, s2, s3, N4)  VALUES (
        1.010896869654167E27, 2.8182385004675907E38, 7.59474299826989E13, 1.233678403273567E9,        41949,
        5.720655732023512E19, 1.8307947577804464E60,       5.84,   -1964.21, -2.1215405322094574E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( 8.655355699463032E26, -1.3169968724531086E38, 7.594759670172764E13, 1.93552181235432E9,
        22092, 5.720440773776165E19, 1.500899424592097E60,       0.23,    -560.32,
        -2.411060560880588E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( -8.440958360990383E26,       null, 7.594753320791722E13, 9.705187018764105E8,
        18053, 5.72043959181655E19,            null,       9.78,    3269.08,
        null) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( 8.78852956792509E26, -2.08910672707099E38, 7.594732927891966E13, 1.915054633352672E9,
        13944, 5.720450305727807E19, 4.242560777731846E60,      16.23,    -340.89,
        -1.811618427620466E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( -2.8713449582670357E26, -2.02570621838354E38, 7.594748252701334E13, 1.772275680075427E9,
        3196,            null,            null,       5.18,     601.85,
        -2.181283842597737E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( -6.746661928664186E26, -2.237064903415018E38, 7.594758864632602E13, 1.031549591517858E8,
        35158, 5.72044977655708E19, 1.817393435439062E60,       0.49,     430.64,
        -3.099298512522107E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( 5.434931663303015E26, 5.285716392424701E37, 7.594738736924048E13, 2.114533190109132E9,
        13457, 5.72067828368245E19, 3.561915860385377E60,      -7.41,   -2240.39,
        9.052783505265789E37) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrN VALUES ( 2.292962078194277E25,       null, 7.594738557348898E13, 6.498921475318679E8,
        44064, 5.720659080477625E19, 2.1373236961385414E59,      14.51,   -4526.37,
        -2.8280626403870254E38) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (s1, St1, St2, St3, St4, St5, St6, s0)  VALUES (
        708.13,
        '-275427.08804271324 192 -817608.8332214953 ',
        'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW4M6L0UJH KM6L0UJH 1M6L0UJH 8M6L0UJH WM6L0UJH 2M6L0UJH NM6L0UJH ',
        '                          CMIF7GJH 2MIF7GJH several HMIF7GJH 699141.592691117 923846.5980633064 Emma flew ',
        '225 quite a few 437RQ close to sprinted F37RQ  637RQ beneath K37RQ 598498.3059382555 cats lots of P37RQ4WH              ',
        '                              8QN9E 6QN9E GQN9E0A2 EQN9E UQN9E Mike OQN9E0A2 Louise many -985737.648297855 Susan ',
        null,
        78812.7) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (s0, St6, St5, St4, St3, St2, St1, s1)  VALUES (
        78824.81,
        ' Adam and Biff skedaddled cautiously under all bike. An indian scampered through one of the penguins. ',
        null,
        'X37RQ4WH 237RQ4WH birds turtles J37RQ Y37RQ  G37RQ4WH 216 -504810.576637059 -416 A37RQ4WH flew a few -86 zzzzzzzzzzzzzzz',
        '         His father got out cheerfully. Edward jumped leisurely! lots of car Susan DMIF7GJH TMIF7GJH 363  ',
        null,
        ' 931892.7636158853 -768587.3458396954 -826255.5447646142 482 -4 367 -399 -51 -33 -463 ',
        -368.42) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (s1, St6, St1, St3, St5, St2, s0, St4)  VALUES (
        -857.54,
        'Fred and Iola hotfooted rapidly near those train. Jessie scampered near one of the goats! 666666666666',
        ' -759576.5143965881 435 456460.6925244583 -827993.8170541001 -103 -9 -408215.319955618 ',
        'Ed drove under lots of sharks? -178987.14391873404 240 -439 QMIF7GJH  The tigers wormed beneath Callie. ::',
        '9QN9E0A2 -395 4QN9E0A2 crows around towards 145 door                                                             ',
        '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''CM6L0UJH XM6L0UJH GM6L0UJH PM6L0UJH LM6L0UJH 7M6L0UJH ',
        78826.67,
        '                                     V37RQ4WH 837RQ4WH over 166 961698.8053130626 T37RQ M37RQ4WH 037RQ4WH drove beneath ') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (s1, St4, s0, St2, St5, St3, St1, St6)  VALUES (
        -2139.88,
        'rarely beside got out Z37RQ U37RQ 775350.6878337655 racoons  ___________________________________________________________',
        78811.7,
        'W06L0UJH 206L0UJH N06L0UJH 006L0UJH H06L0UJH Y06L0UJH S06L0UJH CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
        '-217616.10925354494 book mom 1QN9E 420 Fred RQN9E0A2 an Indian VQN9E0A2 lots of 7QN9E0A2 245417.75250266492 roof ',
        'WMIF7GJH VMIF7GJH RMIF7GJH  IMIF7GJH 119379.26586303813 several 5MIF7 bike rose 185                       ',
        '276 325229.5125800434 185 492426.48290554667 273 285 80665.79990977538 ',
        'Michelle flew through the lions. Sue hopped beside those mice. A few tigers ran near dad. ''''''''''''''''''''''''') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St5, St2, St1, St3, s1, s0, St6, St4)  VALUES (
        null,
        '906L0UJH 606L0UJH Q06L0UJH Z06L0UJH 506L0UJH T06L0UJH 306L0UJH F06L0UJH U06L0UJH E06L0UJH                ',
        '55151.25289719622 -955742.1651839486 361 ',
        '99999999999999999999999999999999999999999999MIF7GJH XMIF7GJH EMIF7GJH OMIF7GJH MMIF7GJH BMIF7GJH LMIF7GJH ',
        -265.11,   78812.92,
        'Bob ran carefully! Callie ran boldly. Mike and an American dashed gracefully beneath all book! +++++++',
        '                          B37RQ4WH -318992.24878756003 around around some 737RQ4WH beneath slide those C37RQ L37RQ -205 ') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St4, St3, St1, St5, s1, s0, St2, St6)  VALUES (
        '                                                      -239 937RQ4WH 137RQ I37RQ4WH 213 4T7RQ -556143.2745420365 through ',
        '0MIF7GJH 4MIF7GJH C1IF7GJH 21IF7GJH H1IF7GJH D1IF7GJH T1IF7GJH Q1IF7GJH 71IF7GJH                          ',
        '0 -420 -264 -617292.4096839062 -519029.90705979214 592350.3848925123 799811.1278238832 ',
        '                                   crows 2QN9E0A2 Edward across BQN9E several 258 blue birds an Englishman SQN9E ',
        -1213.71,   78810.39,
        '                                          4R6L0UJH KR6L0UJH 1R6L0UJH 8R6L0UJH WR6L0UJH 2R6L0UJH NR6L0UJH ',
        '5555555An englishman and Mike ambled promptly over many desk. Derek skedaddled beside one of the elk! ') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St1, s1, s0, St6, St3, St5, St4, St2)  VALUES (
        '-148455.8532120384 965745.24351121 100727.95775494468 -121 -158 322 16355.978317754227 139 308 ',
        871.51,   78822.28,
        '                                         Edward hightailed rapidly. an Englishman sprinted leisurely. ',
        '                              Those snails rushed close to Bill. Jessie split boldly. Mike walked neatly! ',
        'chair CQN9E0A2 over QQN9E HQN9E crane mom a few lovingly rapidly 276                                             ',
        null,
        '               PR6L0UJH LR6L0UJH 7R6L0UJH IR6L0UJH 9R6L0UJH 6R6L0UJH QR6L0UJH ZR6L0UJH 5R6L0UJH TR6L0UJH ') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St1, St3, St6, s1, St5, s0, St4, St2)  VALUES (
        '118 -26 260 -713252.336519578 -207 295491.31063330686 181 64 286148.5571356034 -132034.97260540526 ',
        '//////////////////////////////////////////////////////////////walked hightailed truck over J1IF7GJH 11IF7 ',
        'EEEEEEEEEEEEEEEEEEEEEEEEEEEESheep and chickens and wolves. Oh My! Sharks and cows and racoons. Oh My! ',
        705.51,
        '6HN9E tree quite a few ambled GHN9E0A2 EHN9E over UHN9E crawled those close to OHN9E ----------------------------',
        78817.34,
        'PT7RQ DT7RQ 165 blue birds rambled car wolves OT7RQ faithfully quickly flew 554744.6734571252 thoughtfully RRRRRRRRRRRRR',
        '                                          OR6L0UJH RR6L0UJH VR6L0UJH BR6L0UJH MR6L0UJH JR6L0UJH DR6L0UJH ') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St3, St6, s1, St5, s0, St4, St2, St1)  VALUES (
        'N1IF7GJH  -210997.36128240812 hopped A1IF7GJH W1IF7GJH V1IF7GJH R1IF7GJH I1IF7GJH 51IF7GJH 91IF7GJH       ',
        'Vince and Madelyn ambled solemnly through many crane.                                                 ',
        -1406.25,
        '               KHN9E 0HN9E0A2 door -37987.09257293248 Janine YHN9E0A2 NHN9E0A2 -260 THN9E0A2 drove -291 415 Adam ',
        78818.05,
        '479 347445.28046879056 -419 2T7RQ -316 JT7RQ luckily YT7RQ4WH GT7RQ4WH AT7RQ4WH ST7RQ4WH 343 ooooooooooooooooooooooooooo',
        '266L0UJH N66L0UJH 066L0UJH H66L0UJH Y66L0UJH S66L0UJH A66L0UJH C66L0UJH X66L0UJH G66L0UJH P66L0UJH       ',
        ' 471 136 -179011.2171844471 -777131.489735976 -419 971635.211366469 297 -508333.4497396581 615007.1042519333 113 ') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St2, s0, St4, St1, St5, St6, s1, St3)  VALUES (
        '566L0UJH T66L0UJH 366L0UJH F66L0UJH U66L0UJH E66L0UJH O66L0UJH R66L0UJH V66L0UJH ssssssssssssssssssssssss',
        78813.07,
        '                                                 one of the a few rushed Claire MT7RQ4WH Jessie 542014.0635171654 0T7RQ ',
        '425760.15470613725 245 11 -456 402 879377.8048802435 293 46 -476 ',
        'WHN9E0A2 boldly carefully his father sprang across 1HN9E crane                                                   ',
        '>>>>>>>>>>>>Callie and Louise ran carefully around lots of chair??? Tigers and goats and eels! Oh My! ',
        1271.22,
        '      -18 466 484 -28361.52569006465 F1IF7 81IF7 Z1IF7GJH over P1IF7 01IF7GJH -156284.6630732055 41IF7GJH ') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St2, St6, St4, St1, St3, s0, St5, s1)  VALUES (
        'D66L0UJH 476L0UJH K76L0UJH 176L0UJH 876L0UJH W76L0UJH 276L0UJH N76L0UJH WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
        '        Frank ran excitedly. Michael crawled gracefully! Ben hightailed across quite a few turtles??? ',
        '6666666666666666666666ZT7RQ beneath UT7RQ RT7RQ 610827.488916235 quickly -636872.9262176658 mice  3T7RQ WT7RQ ET7RQ4WH  ',
        null,
        '                                          close to lots of string C4IF7 Seals and pigs and snails? Oh My! ',
        78814.04,
        '3HN9E0A2 across carelessly 2HN9E0A2 BHN9E SHN9E0A2 MHN9E goats ZHN9E0A2  split PHN9E CHN9E                       ',
        2128.55) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St3, St1, s1, St4, St5, s0, St6, St2)  VALUES (
        'Vince crawled near several turtles. 24IF7GJH H4IF7GJH D4IF7GJH T4IF7GJH Q4IF7GJH 74IF7GJH zzzzzzzzzzzzzzzz',
        '569164.3278538533 -340 -426388.9477655649 -383 968913.7428815416 -384 401 -395508.60896345717 ',
        1687.9,
        '      eagles LT7RQ4WH -843075.1189519993 steadily QT7RQ4WH -239 tree lots of beneath quite a few -288106.2820658566 all ',
        '                                   -886664.8693634879 96770.9638168125 whales IHN9E sadly Chet 52 DHN9E0A2 Derek ',
        78812.48,
        null,
        'G76L0UJH P76L0UJH L76L0UJH 776L0UJH I76L0UJH 976L0UJH 676L0UJH Q76L0UJH Z76L0UJH 576L0UJH T76L0UJH zzzzzz') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St3, St5, s1, St6, St2, s0, St1, St4)  VALUES (
        '                   J4IF7GJH 14IF7GJH Biff scampered towards many snails. Goats and tigers and elk. Oh My! ',
        '8JN9E0A2 whales -49 Vince sauntered Frank 6JN9E0A2 GJN9E EJN9E UJN9E -116 -481 OJN9E0A2 -304                     ',
        668.57,
        null,
        'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBV76L0UJH B76L0UJH M76L0UJH J76L0UJH D76L0UJH 4B6L0UJH KB6L0UJH ',
        null,
        '467',
        '++++++++++++++++++++++++++564501.5257413525 1T7RQ IT7RQ rushed sharks -123 477RQ F77RQ 677RQ K77RQ4WH P77RQ4WH D77RQ4WH ') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St2, s1, St1, St3, St5, St6, St4, s0)  VALUES (
        '0B6L0UJH HB6L0UJH YB6L0UJH SB6L0UJH AB6L0UJH ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''',
        2031.3,
        '-368342.0467070817 -228796.40308067773 -387 -59 664722.0474792717 ',
        null,
        '               train KJN9E 0JN9E0A2 hill YJN9E0A2 NJN9E TJN9E0A2 AJN9E Alexandra rug 907064.2059836178 a sibling ',
        'Claire and a German sprinted sloppily beneath those slide? 7777777777777777777777777777777777777777777',
        ' -974207.5309979279 277RQ 694846.08313824 J77RQ sharks many Y77RQ G77RQ4WH string A77RQ eagles 612998.4532842508        ',
        78814.85) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St6, St5, St2, St4, s1, St1, St3, s0)  VALUES (
        '                            Those rats sauntered beside Diane! An englishman drove around a few cats? ',
        '    slide sauntered FJN9E0A2 -72128.73344324785 5JN9E0A2 JJN9E0A2 house 208935.09596802224 birds several quickly ',
        '9B6L0UJH  6B6L0UJH QB6L0UJH ZB6L0UJH 5B6L0UJH TB6L0UJH 3B6L0UJH                                          ',
        'EE877RQ -173465.8192189642 steadily under rolled T77RQ4WH -855338.6560968377 M77RQ 077RQ4WH near -10 407987.41936755716 ',
        -2011.08,
        '797608.5315068637 321755.82934379973 -36571.08337854664 385 215 -147 -180 -118 ',
        'around Joe wormed nervously. Chet crawled loudly. MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM',
        78826.63) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (s0, St3, St1, s1, St4, St2, St5, St6)  VALUES (
        78812.61,
        'Fish and chickens and chickens. Oh My! Eels and pigs and seals? Oh My! aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        '-499921.94203564734 -485 291 -292 -248342.07594328106 -74 -867989.3137775805 ',
        -359.02,
        'the U77RQ several R77RQ -453338.4103997275 penguins 89 377RQ4WH W77RQ4WH 206 -16                                        ',
        'VB6L0UJH BB6L0UJH MB6L0UJH JB6L0UJH DB6L0UJH 446L0UJH K46L0UJH 146L0UJH                                  ',
        '1JN9E several RJN9E VJN9E 7JN9E0A2 -406 35 -340984.2044201357 sauntered 3JN9E0A2 many plane a few 2JN9E0A2       ',
        '                                 Mom ambled near several lions? Some cows scampered around an Indian. ') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St6, St1, St2, s0, s1, St5, St3, St4)  VALUES (
        'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMHenry and a sibling jumped badly through lots of ball! ',
        '474 -613675.2721482445 -20 490246.3083130957 935288.6247624084 -55 -519435.94790965156 -251 ',
        'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbH46L0UJH Y46L0UJH S46L0UJH A46L0UJH C46L0UJH ',
        78814.19,     758.51,
        null,
        'Callie close to several -100 rarely R4IF7GJH 368  -174 I4IF7GJH 54IF7GJH 94IF7GJH X4IF7GJH E4IF7GJH BBBBBB',
        ' under C77RQ4WH computer swiftly Ben wolves lots of -118 L77RQ4WH sprang -30090.798366051167 Q77RQ4WH 12 several        ') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (s0, St4, St2, St5, St6, s1, St3, St1)  VALUES (
        78816.04,
        '-636794.8283216909 -459 dolphins Claire hightailed quite a few Ben 177RQ4WH pppppppppppppppppppppppppppppppppppppppppppp',
        '                        Q46L0UJH Z46L0UJH 546L0UJH T46L0UJH 346L0UJH F46L0UJH U46L0UJH E46L0UJH O46L0UJH ',
        '                                               crows Genelle PJN9E CJN9E0A2 scampered 483 all fish rats QJN9E0A2 ',
        'llllllllHis father slide around several whales! An indian skipped boldly. Vince rambled thoughtfully. ',
        -1061.45,
        'RRRRRRRRRRJessie happily hill excitedly O4IF7GJH M4IF7GJH some B4IF7GJH L4IF7GJH U4IF7GJH eagles K4IF7GJH ',
        '-357 -204 891384.8590732787 -398 -321284.47770295665 420 ') ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (St3, St6, St1, St5, s1, St2, St4, s0)  VALUES (
        'Sue and Iola sprinted promptly beneath some beach? Fred sprinted near lots of blue birds. ++++++++++++++++',
        'iiiiiiiiiiiiiiiiiiiiiFrank sprinted sadly. Callie danced sloppily. Some mice scampered close to Iola. ',
        null,
        'LJN9E0A2 536629.3848650944 one of the IJN9E0A2 DJN9E some 88N9E0A2 438 11 68N9E0A2 G8N9E0A2 -170019.6378408461 ,,',
        -1550.44,
        ' 8A6L0UJH WA6L0UJH 2A6L0UJH NA6L0UJH 0A6L0UJH HA6L0UJH YA6L0UJH SA6L0UJH AA6L0UJH CA6L0UJH               ',
        '                                                   617RQ4WH K17RQ4WH a few Frank P17RQ4WH rarely 282166.129903249 D17RQ ',
        78815.43) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (s0, St3, St6, St1, St5, s1, St2, St4)  VALUES (
        78819.53,
        '890217.540824526 CNIF7GJH 2NIF7GJH HNIF7GJH My mother and Fred jumped promptly close to some bike?        ',
        'All eagles flew across Janine. Those mice jumped beside Derek. &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&',
        '-259313.14669021394 546043.3078223432 848151.3278231663 -145 -177722.87439805595 -97 440 16 ',
        '98N9E0A2 69888.00851253932 -427588.2297418694 48N9E0A2 K8N9E0A2 08N9E Y8N9E0A2 N8N9E -481 Ed T8N9E \\\\\\\\\\\\\\',
        -200.82,
        'LA6L0UJH 7A6L0UJH IA6L0UJH 9A6L0UJH 6A6L0UJH QA6L0UJH                                                    ',
        null) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO TrS (s0, St3, St6, St1, St5, s1, St2, St4)  VALUES (
        78819.53,
        '890217.540824526 CNIF7GJH 2NIF7GJH HNIF7GJH My mother and Fred jumped promptly close to some bike?        ',
        'All eagles flew across Janine. Those mice jumped beside Derek. &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&',
        '-259313.14669021394 546043.3078223432 848151.3278231663 -145 -177722.87439805595 -97 440 16 ',
        '98N9E0A2 69888.00851253932 -427588.2297418694 48N9E0A2 K8N9E0A2 08N9E Y8N9E0A2 N8N9E -481 Ed T8N9E \\\\\\\\\\\\\\',
        -200.82,
        'LA6L0UJH 7A6L0UJH IA6L0UJH 9A6L0UJH 6A6L0UJH QA6L0UJH                                                    ',
        null) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3 (ordering , pic_comp_2 ,
        pic_comp_3 , char_1 , pic_x_8 , var_char_2, var_char_3
        , small_int , large_int , decimal_2_signed
        , decimal_1
        )
        values ( 1, .1, 1
        , 'a' , 'Abcdefgh' , 'aB' , 'AbC'
        , NULL , 1 , .1
        , 1
        ) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3 (ordering , pic_comp_2 ,
        pic_comp_3 , var_char_2, var_char_3
        , small_int , large_int , decimal_2_signed
        , decimal_1
        )
        values ( 2, null, 2
        , 'az' , 'zz'
        , NULL , NULL , .2
        , 1
        ) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3 (ordering , pic_comp_2 ,
        pic_comp_3 , var_char_2, var_char_3
        , small_int , large_int , decimal_2_signed
        )
        values ( 3, null, 2
        , 'zy' , 'zy'
        , NULL , 10 , NULL
        ) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3
        values ( 4, NULL
        ,'C' ,'maureen' ,'E' ,'rum'
        ,3000 ,80 ,2000 ,500
        ,0.50 ,100.7
        ,9000 ,1000 ,2000 ,8 ,.97 ,150
        ,7.1 ,0.7 ,7
        ,1.2 ,0.0001 ,0.0002
        ,date '1975-01-01'
        ,date '1980-01-01'
        ,time '15:00:00'
        ,time '13:11:59'
        ,interval '1900-01' year(4) to month
        ,interval '1:2:3' hour to second
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3 (ordering , pic_comp_2 ,
        pic_comp_3 , large_int , decimal_1 , decimal_2_signed
        )
        values ( 5, .3, null
        , 2 , 0 , NULL
        ) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3 (ordering , pic_comp_2 ,
        pic_comp_3 , large_int , decimal_1 , decimal_2_signed
        )
        values ( 6, .3, null
        , 2 , NULL , .1
        ) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3 (ordering , pic_comp_2 ,
        pic_comp_3 , large_int , decimal_1 , decimal_2_signed
        )
        values ( 7, null, null
        , 2 , NULL , NULL
        ) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3 (ordering ) values ( 8 ) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3
        (ordering, char_1, var_char_2, decimal_1,
        pic_comp_3, time1, iy_to_mo)
        values (11111, 'a', 'aa', 3, 5.8, time '13:40:05',
        interval '1999-10' year(4) to month);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3
        (ordering, char_1, var_char_2, decimal_1,
        pic_comp_3, time1, iy_to_mo)
        values (22222, 'a', 'aa', 3, 4.0, time '10:46:15',
        interval '1999-08' year(4) to month);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3
        (ordering, char_1, var_char_2, decimal_1,
        pic_comp_3, time1, iy_to_mo)
        values (31111, 'a', 'aa', 5, 2.7, time '13:00:05',
        interval '1999-01' year(4) to month);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into b3
        (ordering, char_1, var_char_2, decimal_1,
        pic_comp_3, time1, iy_to_mo)
        values (32111, 'a', 'aa', 5, 2.7, time '13:00:05',
        interval '1998-01' year(4) to month);"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d3 VALUES ( 9292497.946062302, 5.726006E11,           10, 3.4149506658174787E9,
        2225.6347732,    null,  'UC4CG528',     426, -7.4562720920063552E17, 4.89347329936429E15,
        'RLQSCF8R',      -1,      15, 8.484265719E9,        95075,        83619, 1.214297E13,
        46934280) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d3 (i1, i2, i3, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14)  VALUES (
        1.0074399321376462E7, 5.726021E11,           17, 4.044375689500143E9,   26412.9934317,       9,
        'NC4CG528',     431, -7.4562720920063552E17, 4.89331272203828E15,    'towards',       4,      17,
        8.484728052E9,        95078,       318348, 1.214298E13,     46934287) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d3 VALUES ( 9793464.726473104, 5.726034E11,           24, 4.389640383599992E8,
        29511.121122,      11,  '7C4CG528',     423, -7.4562720920063552E17, 4.893224925054353E15,
        'quickly',       3,      28, 8.485883884E9,        95081,       342586,  1.2143E13,
        46934294) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d3 VALUES ( 9604527.05587021, 5.726047E11,           31, 3.075786923042454E8,
        32829.8609676,      13,  'HC4CG528',     420, -7.4562720920063552E17, 4.893495804895335E15,
        '2LQSCF8R',       8,      48, 8.487733214E9,        95077,       310332, 1.214301E13,
        46934301) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( G7, i1, i2, i3, G0, G1, G2, G3, G4, G5, G6 )  VALUES (
        'RKA7K85L TKA7K85L 8KA7K85L 4KA7K85L KKA7K85L 0KA7K85L UKA7K85L 5KA7K85L QKA7K85L DKA7K85L AKA7K85L YKA7K85L ZKA7K85L GKA7K85L BKA7K85L 1KA7K85L WKA7K85L LKA7K85L FKA7K85L CKA7K85L 3KA7K85L  XKA7K85L 7KA7K85L EKA7K85L VKA7K85L 9KA7K85L SKA7K85L IKA7K85L 2KA7K85L 6KA7K85L MKA7K85L OKA7K85L HKA7K85L PKA7K85L JKA7K85L NKA7K85L R4A7K85L T4A7K85L 84A7K85L  44A7K85L K4A7K85L 04A7K85L U4A7K85L 54A7K85L Q4A7K85L D4A7K85L A4A7K85L Y4A7K85L Z4A7K85L G4A7K85L B4A7K85L 14A7K85L W4A7K85L L4A7K85L F4A7K85L C4A7K85L 34A7K85L  X4A7K85L 74A7K85L E4A7K85L V4A7K85L 94A7K85L S4A7K85L I4A7K85L 24A7K85L 64A7K85L M4A7K85L O4A7K85L H4A7K85L P4A7K85L J4A7K85L N4A7K85L RCA7K85L TCA7K85L 8CA7K85L  4CA7K85L KCA7K85L 0CA7K85L UCA7K85L  5CA7K85L QCA7K85L DCA7K85L ACA7K85L YCA7K85L ZCA7K85L GCA7K85L BCA7K85L 1CA7K85L WCA7K85L LCA7K85L FCA7K85L CCA7K85L 3CA7K85L XCA7K85L 7CA7K85L ECA7K85L VCA7K85L 9CA7K85L SCA7K85L ICA7K85L ',
        158,       4, 1.5376132033228447E13, 1155072,              'DNKQKMFU',
        '             A guy from Silicon Valley and mom wormed cheerfully across lots of crane? Quite a few sharks danced across Emma! Bob rolled over many turtles. Mike and Violet ambled softly near all wood. Crows and lions and snails??? Oh My! Edward rushed happily. Joe crawled thoughtfully. Racoons and fish and worms! Oh My! Michael and Violet jumped quietly through lots of train. A few cows ran towards Joe. Issac skedaddled beside the seals. Sharks and cats and fish? Oh My! Iola rambled steadily. Janine sauntered loudly. Derek and Louise skedaddled loudly beside quite a few string. A sibling and Biff ran kindly close to one of the store. Madelyn and Mike crawled softly beside quite a few swing. Vince and Callie got out faithfully close to a few car??? Henry sprang through many horses. ',
        4.832490599599329, 'OD4U1', 1.921363458757037E12, -5942807);"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( i2, i3, G0, G3, G5, G2, G7, G6, G4, G1, i1 )  VALUES (
        14, 1.5376132762557064E13, 1811564, -2.0358477047693344, 1.92136407311277E12,
        'Quite a few tigers walked over Joe. Tony sauntered kindly. Tony jumped carefully. Genelle and Violet danced rapidly under one of the computer! Chet and Genelle flew luckily around all bike. Vince leaped under lots of whales??? Jessie rambled close to those seals??? Lots of tigers split beneath a sibling. Fred split solemnly??? Biff sauntered softly? Iola slide under the cats. Michael hightailed cheerfully! a guy from Silicon Valley scampered lovingly! Emma and Tony ran happily through some ball. Mike and Jessie hotfooted kindly through a few ball! Emma and Biff hightailed angrily over some beach. Many eagles sauntered across Adam. Those sharks ambled near mom. Derek ran quickly. Diane scampered leisurely??? Ed and Chet rolled swiftly towards those crane!                            ',
        'TAA7K85L 8AA7K85L 4AA7K85L KAA7K85L 0AA7K85L UAA7K85L 5AA7K85L QAA7K85L DAA7K85L AAA7K85L YAA7K85L ZAA7K85L GAA7K85L BAA7K85L 1AA7K85L WAA7K85L LAA7K85L FAA7K85L CAA7K85L 3AA7K85L XAA7K85L 7AA7K85L EAA7K85L VAA7K85L 9AA7K85L SAA7K85L IAA7K85L 2AA7K85L 6AA7K85L MAA7K85L OAA7K85L HAA7K85L PAA7K85L JAA7K85L NAA7K85L R5A7K85L T5A7K85L 85A7K85L 45A7K85L K5A7K85L 05A7K85L U5A7K85L 55A7K85L Q5A7K85L D5A7K85L A5A7K85L Y5A7K85L Z5A7K85L G5A7K85L B5A7K85L 15A7K85L W5A7K85L L5A7K85L F5A7K85L C5A7K85L 35A7K85L X5A7K85L 75A7K85L E5A7K85L V5A7K85L 95A7K85L S5A7K85L I5A7K85L 25A7K85L 65A7K85L M5A7K85L O5A7K85L H5A7K85L P5A7K85L J5A7K85L N5A7K85L R0A7K85L T0A7K85L 80A7K85L 40A7K85L K0A7K85L 00A7K85L U0A7K85L 50A7K85L Q0A7K85L D0A7K85L A0A7K85L Y0A7K85L Z0A7K85L G0A7K85L B0A7K85L 10A7K85L W0A7K85L L0A7K85L F0A7K85L C0A7K85L 30A7K85L X0A7K85L 70A7K85L E0A7K85L V0A7K85L 90A7K85L S0A7K85L ',
        -5942806, 'HD4U1',              'SNKQKMFU',     -53);"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 VALUES (      42,      13, 1.5376133491885682E13, 1172100,              'ANKQKMFU',
        '                         Lots of turtles wormed through Joe? Michelle walked under some whales. Mom and Fred hotfooted carelessly near some string. Biff ran near those bears. Those birds skipped over Joe! Eels and worms and eels. Oh My! Eagles and chickens and sheep! Oh My! Blue birds and mice and mice. Oh My! A few cats flew through Joseph??? A guy from Silicon Valley crawled towards several sharks. Callie rushed slowly. Emma ambled softly. Henry hotfooted steadily. Vince drove leisurely. Tigers and bears and turtles! Oh My! Turtles and mice and crows. Oh My! Racoons and sharks and mice. Oh My! A guy from Silicon Valley skipped close to all bears! Eagles and mice and wolves??? Oh My! Sue and Vince scampered swiftly under quite a few tree. Bob flew happily! Janine split carefully. ',
        1.5753313665799018, 'SD4U1', 1.9213646874685034E12, -5942804,
        'H0A7K85L P0A7K85L J0A7K85L N0A7K85L RXA7K85L TXA7K85L 8XA7K85L 4XA7K85L KXA7K85L 0XA7K85L UXA7K85L 5XA7K85L QXA7K85L DXA7K85L AXA7K85L YXA7K85L ZXA7K85L GXA7K85L BXA7K85L 1XA7K85L WXA7K85L LXA7K85L FXA7K85L CXA7K85L 3XA7K85L XXA7K85L 7XA7K85L EXA7K85L VXA7K85L 9XA7K85L SXA7K85L IXA7K85L 2XA7K85L 6XA7K85L MXA7K85L OXA7K85L HXA7K85L PXA7K85L JXA7K85L NXA7K85L REA7K85L TEA7K85L 8EA7K85L 4EA7K85L KEA7K85L 0EA7K85L UEA7K85L 5EA7K85L QEA7K85L DEA7K85L AEA7K85L YEA7K85L ZEA7K85L GEA7K85L BEA7K85L 1EA7K85L WEA7K85L LEA7K85L FEA7K85L CEA7K85L 3EA7K85L XEA7K85L 7EA7K85L EEA7K85L VEA7K85L 9EA7K85L SEA7K85L IEA7K85L 2EA7K85L 6EA7K85L MEA7K85L OEA7K85L HEA7K85L PEA7K85L JEA7K85L NEA7K85L RYA7K85L TYA7K85L 8YA7K85L 4YA7K85L KYA7K85L 0YA7K85L UYA7K85L 5YA7K85L QYA7K85L  DYA7K85L AYA7K85L YYA7K85L ZYA7K85L GYA7K85L BYA7K85L 1YA7K85L WYA7K85L LYA7K85L FYA7K85L CYA7K85L 3YA7K85L XYA7K85L 7YA7K85L ');"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( i2, i3, G0, G3, G5, G2, G7, G6, G4, G1, i1 )  VALUES (
        23, 1.53761342212143E13, -587812, 4.819733028231306, 1.9213653018242368E12,
        null,
        ' 6YA7K85L MYA7K85L OYA7K85L HYA7K85L PYA7K85L JYA7K85L NYA7K85L RHA7K85L THA7K85L 8HA7K85L 4HA7K85L KHA7K85L 0HA7K85L UHA7K85L 5HA7K85L QHA7K85L DHA7K85L AHA7K85L YHA7K85L ZHA7K85L GHA7K85L BHA7K85L 1HA7K85L WHA7K85L LHA7K85L FHA7K85L CHA7K85L 3HA7K85L XHA7K85L 7HA7K85L EHA7K85L VHA7K85L 9HA7K85L SHA7K85L IHA7K85L 2HA7K85L 6HA7K85L MHA7K85L OHA7K85L HHA7K85L PHA7K85L JHA7K85L NHA7K85L RMA7K85L TMA7K85L 8MA7K85L 4MA7K85L KMA7K85L 0MA7K85L UMA7K85L 5MA7K85L QMA7K85L DMA7K85L AMA7K85L YMA7K85L ZMA7K85L GMA7K85L BMA7K85L 1MA7K85L WMA7K85L LMA7K85L FMA7K85L CMA7K85L 3MA7K85L XMA7K85L 7MA7K85L EMA7K85L VMA7K85L 9MA7K85L SMA7K85L IMA7K85L  2MA7K85L 6MA7K85L MMA7K85L OMA7K85L HMA7K85L PMA7K85L JMA7K85L NMA7K85L RFA7K85L TFA7K85L 8FA7K85L 4FA7K85L KFA7K85L 0FA7K85L UFA7K85L 5FA7K85L QFA7K85L DFA7K85L AFA7K85L YFA7K85L ZFA7K85L GFA7K85L BFA7K85L 1FA7K85L WFA7K85L LFA7K85L FFA7K85L CFA7K85L 3FA7K85L ',
        -5942801, '1D4U1',              'FNKQKMFU',     163);"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( G5, G2, G1, i1, G4, G0, i3, G7, G6, G3, i2 )  VALUES (
        1.9213659161799697E12,
        'Tony and Vince sprang rarely towards many book. Dad drove rarely. Madelyn ran faithfully. Sue scampered cheerfully. Violet got out quickly??? All snails strolled around Violet. Derek dashed near many birds. Joe ran sloppily! Emma ran carelessly??? Bill jumped happily. an Indian sprang quietly. Michael skipped around several mice! Mike scampered through some worms. The pigs split under Frank! Henry and Biff rambled angrily near one of the computer. Susan rolled luckily! Sue rambled badly. An Indian and an Indian rambled softly over a few store. Some tigers danced over Bill? One of the cats scampered across Jessie. Vince dashed luckily. Joseph sprinted sloppily??? One of the eagles hightailed around a sibling. Several whales hopped close to Frank.                                     ',
        'PNKQKMFU',    null, '4D4U1', 1811445, 1.537613495054292E13,
        '6FA7K85L MFA7K85L OFA7K85L HFA7K85L PFA7K85L JFA7K85L NFA7K85L RTA7K85L TTA7K85L 8TA7K85L 4TA7K85L KTA7K85L 0TA7K85L UTA7K85L 5TA7K85L QTA7K85L DTA7K85L ATA7K85L YTA7K85L ZTA7K85L GTA7K85L BTA7K85L 1TA7K85L WTA7K85L LTA7K85L FTA7K85L CTA7K85L 3TA7K85L XTA7K85L 7TA7K85L ETA7K85L VTA7K85L 9TA7K85L STA7K85L ITA7K85L 2TA7K85L 6TA7K85L MTA7K85L OTA7K85L HTA7K85L PTA7K85L  JTA7K85L NTA7K85L RLA7K85L TLA7K85L 8LA7K85L 4LA7K85L KLA7K85L 0LA7K85L ULA7K85L 5LA7K85L QLA7K85L DLA7K85L ALA7K85L YLA7K85L ZLA7K85L GLA7K85L BLA7K85L  1LA7K85L WLA7K85L LLA7K85L FLA7K85L CLA7K85L 3LA7K85L XLA7K85L 7LA7K85L ELA7K85L VLA7K85L 9LA7K85L SLA7K85L ILA7K85L 2LA7K85L 6LA7K85L MLA7K85L OLA7K85L HLA7K85L PLA7K85L JLA7K85L NLA7K85L RPA7K85L TPA7K85L 8PA7K85L 4PA7K85L KPA7K85L 0PA7K85L UPA7K85L 5PA7K85L QPA7K85L DPA7K85L APA7K85L YPA7K85L ZPA7K85L GPA7K85L BPA7K85L 1PA7K85L WPA7K85L LPA7K85L FPA7K85L CPA7K85L ',
        -5942797, 2.608202563819594,      22);"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 VALUES (      -8,      32, 1.5376135679871533E13,  675976,              'UNKQKMFU',
        'Several horses drove around Frank. Mice and bears and tigers??? Oh My! My mother walked through several cows! Adam flew leisurely! Edward hotfooted excitedly! Issac sprinted close to many worms. Claire rushed steadily. an Indian sauntered lovingly! Joe drove through many fish! A sibling sprinted towards some mice? Michael dashed under a few penguins. Bill scampered excitedly. Iola got out angrily. Ed flew quietly? Bob flew promptly. Lots of cats got out over an Indian. Those blue birds rambled across dad. A German dashed near some whales! Adam and Genelle sauntered softly across quite a few door. Dad split loudly? an Indian drove leisurely. Several tigers drove across Henry. Joseph and Joe ran steadily close to many truck??? An Englishman hopped over those snails??? QQQQQQQQQQQQQQQ',
        1.0112428712638701, '3D4U1', 1.921366530535703E12,    null,
        '9PA7K85L SPA7K85L IPA7K85L  2PA7K85L 6PA7K85L MPA7K85L OPA7K85L HPA7K85L PPA7K85L JPA7K85L NPA7K85L RUA7K85L TUA7K85L 8UA7K85L 4UA7K85L KUA7K85L 0UA7K85L UUA7K85L 5UA7K85L QUA7K85L DUA7K85L AUA7K85L YUA7K85L ZUA7K85L GUA7K85L BUA7K85L 1UA7K85L WUA7K85L LUA7K85L FUA7K85L CUA7K85L 3UA7K85L XUA7K85L 7UA7K85L EUA7K85L VUA7K85L 9UA7K85L SUA7K85L IUA7K85L 2UA7K85L 6UA7K85L MUA7K85L OUA7K85L HUA7K85L PUA7K85L JUA7K85L NUA7K85L R7A7K85L T7A7K85L 87A7K85L 47A7K85L K7A7K85L 07A7K85L U7A7K85L 57A7K85L Q7A7K85L D7A7K85L A7A7K85L Y7A7K85L Z7A7K85L G7A7K85L B7A7K85L 17A7K85L W7A7K85L L7A7K85L F7A7K85L C7A7K85L 37A7K85L X7A7K85L 77A7K85L E7A7K85L V7A7K85L 97A7K85L S7A7K85L I7A7K85L 27A7K85L 67A7K85L M7A7K85L O7A7K85L H7A7K85L P7A7K85L J7A7K85L N7A7K85L  RVA7K85L TVA7K85L 8VA7K85L 4VA7K85L KVA7K85L 0VA7K85L UVA7K85L 5VA7K85L QVA7K85L DVA7K85L AVA7K85L YVA7K85L ZVA7K85L GVA7K85L BVA7K85L 1VA7K85L WVA7K85L ');"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 VALUES (      89,      31, 1.5376136409200154E13, -1253256,              '0NKQKMFU',
        'His father and Janine hotfooted quietly through some swing! Biff ran luckily. Biff dashed excitedly! Madelyn and Sue hopped rapidly through lots of tree! An American rushed faithfully! Vince ambled steadily! Genelle leaped beneath the snails. All eels ambled across Janine! Michael drove beneath several worms. Genelle and Joe scampered sloppily towards a few door. A sibling flew close to the tigers. Sue ran close to many sheep! Those eagles rushed around an Englishman. His father sauntered cheerfully. Michael danced promptly! His father and Chet hightailed neatly beside several store! A guy from Silicon Valley and my mother sprang angrily over quite a few truck. Rats and sharks and crows? Oh My! Sue strolled angrily? Madelyn walked happily??? Snails and eels and seals. Oh My! cccccc',
        4.5030374872223105, 'WD4U1', 1.921367144891436E12, -5942792,
        'FVA7K85L CVA7K85L 3VA7K85L  XVA7K85L 7VA7K85L EVA7K85L VVA7K85L 9VA7K85L SVA7K85L IVA7K85L 2VA7K85L 6VA7K85L MVA7K85L OVA7K85L HVA7K85L PVA7K85L JVA7K85L NVA7K85L RSA7K85L TSA7K85L 8SA7K85L 4SA7K85L KSA7K85L 0SA7K85L USA7K85L 5SA7K85L QSA7K85L DSA7K85L ASA7K85L YSA7K85L ZSA7K85L GSA7K85L BSA7K85L 1SA7K85L WSA7K85L LSA7K85L FSA7K85L CSA7K85L 3SA7K85L XSA7K85L 7SA7K85L ESA7K85L VSA7K85L 9SA7K85L SSA7K85L ISA7K85L 2SA7K85L 6SA7K85L MSA7K85L OSA7K85L HSA7K85L PSA7K85L JSA7K85L NSA7K85L R8A7K85L T8A7K85L 88A7K85L 48A7K85L K8A7K85L 08A7K85L U8A7K85L 58A7K85L Q8A7K85L D8A7K85L A8A7K85L Y8A7K85L Z8A7K85L G8A7K85L B8A7K85L 18A7K85L W8A7K85L L8A7K85L F8A7K85L C8A7K85L 38A7K85L X8A7K85L 78A7K85L E8A7K85L V8A7K85L  98A7K85L S8A7K85L I8A7K85L 28A7K85L 68A7K85L M8A7K85L O8A7K85L H8A7K85L P8A7K85L J8A7K85L N8A7K85L RQA7K85L TQA7K85L 8QA7K85L 4QA7K85L KQA7K85L 0QA7K85L UQA7K85L ');"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( i2, G5, G7, G2, G1, G3, i1, G4, G0, G6, i3 )  VALUES (
        41, 1.9213677592471692E12,
        ' GQA7K85L BQA7K85L 1QA7K85L WQA7K85L LQA7K85L FQA7K85L CQA7K85L  3QA7K85L XQA7K85L 7QA7K85L EQA7K85L VQA7K85L 9QA7K85L SQA7K85L IQA7K85L 2QA7K85L 6QA7K85L MQA7K85L OQA7K85L HQA7K85L PQA7K85L JQA7K85L NQA7K85L R3A7K85L T3A7K85L 83A7K85L 43A7K85L K3A7K85L 03A7K85L U3A7K85L 53A7K85L Q3A7K85L D3A7K85L A3A7K85L Y3A7K85L Z3A7K85L G3A7K85L B3A7K85L 13A7K85L W3A7K85L L3A7K85L F3A7K85L C3A7K85L 33A7K85L X3A7K85L 73A7K85L E3A7K85L V3A7K85L 93A7K85L S3A7K85L I3A7K85L 23A7K85L 63A7K85L M3A7K85L O3A7K85L H3A7K85L P3A7K85L J3A7K85L N3A7K85L ROA7K85L TOA7K85L 8OA7K85L 4OA7K85L KOA7K85L 0OA7K85L UOA7K85L 5OA7K85L QOA7K85L DOA7K85L AOA7K85L YOA7K85L ZOA7K85L GOA7K85L BOA7K85L 1OA7K85L WOA7K85L LOA7K85L FOA7K85L COA7K85L 3OA7K85L XOA7K85L 7OA7K85L EOA7K85L VOA7K85L 9OA7K85L SOA7K85L IOA7K85L 2OA7K85L 6OA7K85L MOA7K85L OOA7K85L HOA7K85L POA7K85L ',
        'Joe drove towards all seals??? Ben and Biff hopped neatly across several car. Michelle slide rarely. Henry scampered nervously! Whales and turtles and dogs. Oh My! Mike rambled nervously. Janine rolled kindly. Vince sprang luckily? Sue scampered promptly! Derek and Derek hotfooted nervously beneath those tree. Edward and his father strolled sloppily around several door. Those whales hopped over Susan. A sibling skipped angrily. Bill hotfooted slowly. Claire and a German slide promptly under a few plane! A guy from Silicon Valley and an Indian crawled solemnly towards all house??? Quite a few wolves hotfooted beneath Henry??? Tigers and seals and blue birds? Oh My! Those cows crawled across Bill! Frank wormed sadly? Michael scampered leisurely. pppppppppppppppppppppppppppppppppppppp',
        '6NKQKMFU', 1.4158064711816776,    -133, 'AD4U1',   55085, -5942786,
        1.5376137138528771E13);"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( i3, i2, G5, G7, G2, G1, G3, i1, G4, G0, G6 )  VALUES (
        1.537613786785739E13,      40, 1.9213683736029023E12,
        '5RA7K85L QRA7K85L DRA7K85L ARA7K85L YRA7K85L ZRA7K85L GRA7K85L BRA7K85L 1RA7K85L WRA7K85L LRA7K85L FRA7K85L CRA7K85L 3RA7K85L XRA7K85L 7RA7K85L ERA7K85L VRA7K85L 9RA7K85L SRA7K85L IRA7K85L 2RA7K85L 6RA7K85L MRA7K85L ORA7K85L HRA7K85L PRA7K85L JRA7K85L NRA7K85L RGA7K85L TGA7K85L 8GA7K85L 4GA7K85L KGA7K85L 0GA7K85L  UGA7K85L 5GA7K85L QGA7K85L DGA7K85L AGA7K85L YGA7K85L ZGA7K85L GGA7K85L BGA7K85L 1GA7K85L WGA7K85L LGA7K85L FGA7K85L CGA7K85L 3GA7K85L XGA7K85L 7GA7K85L EGA7K85L VGA7K85L 9GA7K85L SGA7K85L IGA7K85L 2GA7K85L 6GA7K85L MGA7K85L OGA7K85L HGA7K85L  PGA7K85L JGA7K85L NGA7K85L RBA7K85L TBA7K85L 8BA7K85L 4BA7K85L KBA7K85L 0BA7K85L UBA7K85L 5BA7K85L QBA7K85L DBA7K85L ABA7K85L YBA7K85L ZBA7K85L GBA7K85L BBA7K85L 1BA7K85L WBA7K85L LBA7K85L FBA7K85L CBA7K85L 3BA7K85L XBA7K85L 7BA7K85L EBA7K85L VBA7K85L 9BA7K85L SBA7K85L IBA7K85L 2BA7K85L ',
        'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyChet split quietly. Jessie split happily. Ben scampered luckily! dad hopped carefully! All fish strolled under Susan? Those bears scampered beneath Joe??? Derek hopped rapidly. an Indian drove leisurely. Mike skipped towards all racoons. Those birds hotfooted near Sue! Joseph sauntered close to one of the dolphins? A few eagles crawled over Henry! Derek danced angrily. Chet walked softly! Frank and Iola scampered cheerfully near some table. A sibling wormed through lots of goats! Mice and blue birds and crows??? Oh My! One of the tigers rolled beneath Derek! Bob and Louise flew nervously across many car??? Bob and Madelyn got out angrily through all chair! Joe sprinted around all sharks. Biff ambled sloppily! Genelle jumped leisurely! ',
        'JNKQKMFU', -2.024040339377417,     198, 'RD4U1', 1195656, -5942779);"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( G7, G1, G4, G0, G2, G3, i1, G6, i3, G5, i2 )  VALUES (
        '8NA7K85L 4NA7K85L KNA7K85L 0NA7K85L UNA7K85L 5NA7K85L QNA7K85L DNA7K85L ANA7K85L YNA7K85L ZNA7K85L GNA7K85L BNA7K85L 1NA7K85L WNA7K85L LNA7K85L FNA7K85L CNA7K85L 3NA7K85L   XNA7K85L 7NA7K85L ENA7K85L VNA7K85L 9NA7K85L SNA7K85L INA7K85L 2NA7K85L 6NA7K85L MNA7K85L ONA7K85L HNA7K85L PNA7K85L JNA7K85L NNA7K85L R9A7K85L T9A7K85L 89A7K85L 49A7K85L K9A7K85L 09A7K85L U9A7K85L 59A7K85L Q9A7K85L D9A7K85L A9A7K85L Y9A7K85L Z9A7K85L G9A7K85L B9A7K85L 19A7K85L W9A7K85L L9A7K85L F9A7K85L C9A7K85L 39A7K85L X9A7K85L 79A7K85L E9A7K85L V9A7K85L 99A7K85L S9A7K85L I9A7K85L 29A7K85L 69A7K85L M9A7K85L O9A7K85L H9A7K85L P9A7K85L J9A7K85L N9A7K85L RWA7K85L TWA7K85L 8WA7K85L 4WA7K85L KWA7K85L 0WA7K85L UWA7K85L 5WA7K85L QWA7K85L DWA7K85L AWA7K85L YWA7K85L ZWA7K85L GWA7K85L BWA7K85L 1WA7K85L WWA7K85L LWA7K85L FWA7K85L CWA7K85L 3WA7K85L XWA7K85L 7WA7K85L EWA7K85L VWA7K85L 9WA7K85L SWA7K85L IWA7K85L 2WA7K85L 6WA7K85L ',
        'ONKQKMFU', 'YD4U1', -1598438,
        'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHJessie jumped gracefully! Claire flew quickly. Edward hightailed beside some chickens. Edward and Louise dashed solemnly beneath many swing. Bill and Bill rushed steadily close to quite a few chair. Many racoons scampered towards a sibling??? Frank ambled beneath lots of rats! An American flew beneath the penguins. Henry sprinted close to some snails! Derek hopped quickly. mom split sadly. Some whales rolled close to Fred. Michael sprinted softly! Ed got out carelessly? Ed and Vince scampered carelessly towards quite a few book. Claire hightailed near the fish! Joseph ran swiftly! an Englishman walked luckily. Mike got out sadly! my mother sauntered carelessly. Lots of racoons danced around a guy from Silicon Valley. Susan danced near all fish! ',
        6.104582975212968,    -126, -5942771, 1.537613859718601E13, 1.9213689879586355E12,      50);"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( i2, G7, G1, G4, G0, G2, G3, i1, G6, i3, G5 )  VALUES (
        49,
        '8JA7K85L 4JA7K85L KJA7K85L  0JA7K85L    UJA7K85L 5JA7K85L QJA7K85L DJA7K85L AJA7K85L YJA7K85L ZJA7K85L GJA7K85L BJA7K85L 1JA7K85L WJA7K85L LJA7K85L FJA7K85L CJA7K85L 3JA7K85L XJA7K85L 7JA7K85L EJA7K85L VJA7K85L 9JA7K85L SJA7K85L IJA7K85L 2JA7K85L 6JA7K85L MJA7K85L OJA7K85L HJA7K85L PJA7K85L JJA7K85L NJA7K85L RZA7K85L TZA7K85L 8ZA7K85L 4ZA7K85L KZA7K85L 0ZA7K85L UZA7K85L 5ZA7K85L QZA7K85L DZA7K85L AZA7K85L YZA7K85L ZZA7K85L GZA7K85L BZA7K85L 1ZA7K85L WZA7K85L LZA7K85L FZA7K85L CZA7K85L 3ZA7K85L XZA7K85L 7ZA7K85L EZA7K85L VZA7K85L 9ZA7K85L SZA7K85L IZA7K85L 2ZA7K85L 6ZA7K85L MZA7K85L OZA7K85L HZA7K85L PZA7K85L JZA7K85L NZA7K85L RIA7K85L TIA7K85L 8IA7K85L 4IA7K85L KIA7K85L 0IA7K85L UIA7K85L 5IA7K85L QIA7K85L DIA7K85L AIA7K85L YIA7K85L ZIA7K85L GIA7K85L BIA7K85L 1IA7K85L WIA7K85L LIA7K85L FIA7K85L CIA7K85L 3IA7K85L  XIA7K85L 7IA7K85L EIA7K85L VIA7K85L 9IA7K85L SIA7K85L IIA7K85L 2IA7K85L ',
        'ENKQKMFU', 'ID4U1',  528695,
        'Those cows crawled near Fred. Elk and lions and birds. Oh My! Diane scampered rapidly. my mother slide cheerfully??? Claire skipped around quite a few racoons. Edward and Fred slide neatly near some crane. All birds flew towards a guy from Silicon Valley. Whales and tigers and sheep. Oh My! Many tigers wormed around dad. Diane leaped close to the eels. Sheep and chickens and pigs? Oh My! Horses and seals and birds! Oh My! Dad and a guy from Silicon Valley slide carelessly towards many rug! Sharks and wolves and tigers. Oh My! Issac and Louise scampered steadily under lots of car. Violet skipped boldly. Ben walked sadly. Henry rolled towards lots of elk. Joseph scampered luckily. Michelle leaped lovingly. His father rushed swiftly! an Englishman sprinted cheerfully.                 ',
        2.172216200811401,     -75, -5942762, 1.5376139326514623E13, 1.9213696023143687E12);"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( i1, i2, i3, G0, G1, G2, G3, G4, G5, G6, G7 )  VALUES (
        null,      59, 1.5376140055843244E13,  604177,              'GNKQKMFU',
        'Several mice hotfooted beneath his father. Violet sprang solemnly. Michelle sprinted sloppily. Wolves and crows and cows. Oh My! Diane and Issac got out rarely beneath a few train. Ben ran quietly? Joe walked sloppily. Adam and a German drove cheerfully close to a few rug! Edward hopped around those worms. Emma hotfooted softly. Vince scampered nervously. Sue and Henry sprinted badly near quite a few rug. Elk and dogs and blue birds??? Oh My! His father and Ben ran softly beside all wood. Violet and Biff rolled quickly around many book. Horses and snails and whales. Oh My! All horses hopped under my mother? Seals and fish and rats. Oh My! Louise sprang beneath many mice! An Indian scampered over a few sheep. Horses and seals and racoons. Oh My! All lions rolled near Susan. ))))))))',
        3.9132186545542416, 'FD4U1', 1.9213702166701018E12, -5942752,
        '81A7K85L 41A7K85L K1A7K85L 01A7K85L U1A7K85L 51A7K85L Q1A7K85L D1A7K85L A1A7K85L Y1A7K85L Z1A7K85L G1A7K85L B1A7K85L 11A7K85L W1A7K85L L1A7K85L F1A7K85L C1A7K85L 31A7K85L X1A7K85L 71A7K85L E1A7K85L V1A7K85L 91A7K85L S1A7K85L I1A7K85L 21A7K85L 61A7K85L M1A7K85L O1A7K85L H1A7K85L P1A7K85L J1A7K85L N1A7K85L R6A7K85L T6A7K85L 86A7K85L 46A7K85L K6A7K85L 06A7K85L U6A7K85L 56A7K85L Q6A7K85L D6A7K85L A6A7K85L Y6A7K85L Z6A7K85L G6A7K85L B6A7K85L 16A7K85L W6A7K85L L6A7K85L F6A7K85L C6A7K85L 36A7K85L X6A7K85L 76A7K85L E6A7K85L V6A7K85L 96A7K85L S6A7K85L I6A7K85L 26A7K85L 66A7K85L M6A7K85L O6A7K85L H6A7K85L P6A7K85L J6A7K85L N6A7K85L RDA7K85L TDA7K85L 8DA7K85L 4DA7K85L KDA7K85L 0DA7K85L UDA7K85L 5DA7K85L QDA7K85L DDA7K85L ADA7K85L YDA7K85L ZDA7K85L GDA7K85L BDA7K85L 1DA7K85L WDA7K85L LDA7K85L FDA7K85L CDA7K85L 3DA7K85L XDA7K85L 7DA7K85L EDA7K85L VDA7K85L 9DA7K85L SDA7K85L IDA7K85L 2DA7K85L ');"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( G4, i2, G7, G2, i3, G5, i1, G0, G1, G3, G6 )  VALUES (
        'UD4U1',      58,
        ' T2A7K85L 82A7K85L 42A7K85L K2A7K85L 02A7K85L U2A7K85L 52A7K85L Q2A7K85L D2A7K85L A2A7K85L Y2A7K85L Z2A7K85L G2A7K85L B2A7K85L 12A7K85L W2A7K85L L2A7K85L F2A7K85L C2A7K85L 32A7K85L X2A7K85L 72A7K85L E2A7K85L V2A7K85L 92A7K85L S2A7K85L I2A7K85L 22A7K85L 62A7K85L M2A7K85L O2A7K85L H2A7K85L P2A7K85L J2A7K85L N2A7K85L RKD7K85L TKD7K85L 8KD7K85L 4KD7K85L KKD7K85L 0KD7K85L UKD7K85L 5KD7K85L QKD7K85L DKD7K85L AKD7K85L YKD7K85L ZKD7K85L GKD7K85L BKD7K85L 1KD7K85L WKD7K85L LKD7K85L FKD7K85L CKD7K85L 3KD7K85L XKD7K85L 7KD7K85L  EKD7K85L VKD7K85L 9KD7K85L SKD7K85L IKD7K85L 2KD7K85L 6KD7K85L MKD7K85L OKD7K85L HKD7K85L PKD7K85L JKD7K85L NKD7K85L R4D7K85L T4D7K85L 84D7K85L 44D7K85L K4D7K85L 04D7K85L U4D7K85L 54D7K85L Q4D7K85L D4D7K85L A4D7K85L Y4D7K85L Z4D7K85L G4D7K85L B4D7K85L 14D7K85L W4D7K85L L4D7K85L F4D7K85L C4D7K85L 34D7K85L ',
        '                                        Jessie ambled across all fish??? One of the elk slide over Bob. Dad ambled around one of the cats. Edward and Derek rolled cautiously through many roof. Susan ran excitedly. Joe skipped sloppily. Dad and Vince sprang faithfully towards the roof. Joe danced rarely. Edward rolled quickly. Madelyn leaped leisurely! Issac rolled luckily. Mom hopped faithfully. my mother rolled softly! Those fish got out through Henry. Adam rushed lovingly??? an Englishman danced faithfully. Chickens and cows and eagles! Oh My! Claire rambled nervously. Claire hotfooted cautiously! All elk rushed close to Violet??? Diane hotfooted promptly. Bill crawled happily. A German crawled beneath one of the worms. His father and Henry slide thoughtfully close to the slide. ',
        1.5376140785171861E13, 1.921370831025835E12,     112, -1742719,              'CNKQKMFU',
        -0.4008206138606254, -5942741);"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 VALUES (       3,      68, 1.5376141514500479E13, 1770970,              '9NKQKMFU',
        null,
        0.4541633006839261, 'LD4U1', 1.921371445381568E12, -5942729,
        'M4D7K85L O4D7K85L H4D7K85L P4D7K85L J4D7K85L N4D7K85L RCD7K85L TCD7K85L 8CD7K85L 4CD7K85L KCD7K85L 0CD7K85L UCD7K85L 5CD7K85L QCD7K85L DCD7K85L ACD7K85L YCD7K85L ZCD7K85L GCD7K85L BCD7K85L 1CD7K85L WCD7K85L LCD7K85L FCD7K85L CCD7K85L 3CD7K85L XCD7K85L 7CD7K85L ECD7K85L VCD7K85L 9CD7K85L SCD7K85L ICD7K85L 2CD7K85L 6CD7K85L MCD7K85L OCD7K85L HCD7K85L PCD7K85L JCD7K85L NCD7K85L RAD7K85L TAD7K85L 8AD7K85L 4AD7K85L KAD7K85L 0AD7K85L UAD7K85L 5AD7K85L QAD7K85L DAD7K85L AAD7K85L YAD7K85L ZAD7K85L GAD7K85L BAD7K85L 1AD7K85L WAD7K85L LAD7K85L FAD7K85L CAD7K85L 3AD7K85L XAD7K85L 7AD7K85L EAD7K85L VAD7K85L 9AD7K85L SAD7K85L IAD7K85L 2AD7K85L 6AD7K85L MAD7K85L OAD7K85L HAD7K85L PAD7K85L JAD7K85L NAD7K85L R5D7K85L T5D7K85L 85D7K85L 45D7K85L  K5D7K85L 05D7K85L U5D7K85L 55D7K85L Q5D7K85L D5D7K85L A5D7K85L Y5D7K85L Z5D7K85L G5D7K85L B5D7K85L 15D7K85L  W5D7K85L L5D7K85L F5D7K85L C5D7K85L 35D7K85L ');"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( i1, i2, i3, G0, G1, G2, G3, G4, G5, G6, G7 )  VALUES (
        200,      67, 1.5376142243829098E13, -1774022,              'RNKQKMFU',
        '444444444444444444444444444444Birds and sharks and cows. Oh My! Michael ran around quite a few sheep. A sibling scampered rapidly. Joe sprinted kindly??? Whales and eagles and dolphins? Oh My! Many crows skedaddled over Diane! Lions and bears and dogs. Oh My! Madelyn slide through quite a few tigers? Lots of turtles hotfooted under Derek. The cows walked beside Iola! The fish sprinted beneath Madelyn! Mice and dogs and blue birds! Oh My! Some elk skipped towards Vince. Penguins and birds and crows! Oh My! Adam and Michelle hopped softly across one of the rug??? Several goats danced beside Edward. Mom danced slowly??? Emma scampered steadily. Birds and pigs and snails. Oh My! Dogs and fish and fish. Oh My! Genelle ran quickly! Bob hopped carelessly. Pigs and birds and sheep! Oh My! ',
        -1.5712848198077896, 'GD4U1',            null, -5942716,
        'S5D7K85L I5D7K85L 25D7K85L 65D7K85L M5D7K85L O5D7K85L H5D7K85L P5D7K85L J5D7K85L N5D7K85L R0D7K85L T0D7K85L 80D7K85L 40D7K85L K0D7K85L 00D7K85L U0D7K85L 50D7K85L Q0D7K85L D0D7K85L A0D7K85L Y0D7K85L Z0D7K85L G0D7K85L B0D7K85L 10D7K85L W0D7K85L L0D7K85L F0D7K85L C0D7K85L 30D7K85L X0D7K85L 70D7K85L E0D7K85L V0D7K85L 90D7K85L S0D7K85L I0D7K85L 20D7K85L 60D7K85L M0D7K85L O0D7K85L H0D7K85L P0D7K85L J0D7K85L N0D7K85L RXD7K85L TXD7K85L 8XD7K85L 4XD7K85L KXD7K85L 0XD7K85L UXD7K85L 5XD7K85L QXD7K85L DXD7K85L AXD7K85L YXD7K85L ZXD7K85L GXD7K85L BXD7K85L  1XD7K85L WXD7K85L LXD7K85L FXD7K85L CXD7K85L 3XD7K85L XXD7K85L 7XD7K85L EXD7K85L VXD7K85L 9XD7K85L SXD7K85L IXD7K85L 2XD7K85L 6XD7K85L  MXD7K85L OXD7K85L HXD7K85L PXD7K85L JXD7K85L NXD7K85L RED7K85L TED7K85L 8ED7K85L 4ED7K85L KED7K85L 0ED7K85L UED7K85L 5ED7K85L QED7K85L DED7K85L AED7K85L YED7K85L ZED7K85L ');"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 VALUES (    -107,      77, 1.5376142973157717E13, -1870320,              'LNKQKMFU',
        '::::::::::Blue birds and rats and chickens??? Oh My! Louise and Frank ran solemnly beside some string??? Some rats rolled through Michelle??? Alexandra skipped solemnly. Issac sprinted neatly! Mom hotfooted across those penguins. His father and Joe ran slowly beneath lots of hill. Dogs and eels and goats. Oh My! A sibling wormed around the lions. Claire flew kindly! Joseph ambled sloppily! Diane rushed under those whales. Henry wormed over many lions. His father and a guy from Silicon Valley strolled softly around a few roof. Bill dashed through many sheep. Lions and dogs and eagles? Oh My! His father and Joe wormed neatly close to quite a few plane. Susan and Chet hightailed rapidly through all slide. Dolphins and racoons and elk! Oh My! Dolphins and snails and blue birds. Oh My! ',
        -3.34334187995849, 'MD4U1', 1.9213720597373015E12, -5942702,
        'CED7K85L 3ED7K85L XED7K85L 7ED7K85L EED7K85L VED7K85L 9ED7K85L SED7K85L IED7K85L 2ED7K85L 6ED7K85L MED7K85L OED7K85L HED7K85L PED7K85L JED7K85L NED7K85L RYD7K85L TYD7K85L 8YD7K85L 4YD7K85L KYD7K85L 0YD7K85L UYD7K85L 5YD7K85L QYD7K85L DYD7K85L AYD7K85L YYD7K85L ZYD7K85L GYD7K85L BYD7K85L 1YD7K85L WYD7K85L LYD7K85L FYD7K85L CYD7K85L 3YD7K85L XYD7K85L 7YD7K85L EYD7K85L VYD7K85L 9YD7K85L SYD7K85L IYD7K85L 2YD7K85L 6YD7K85L MYD7K85L OYD7K85L HYD7K85L PYD7K85L JYD7K85L NYD7K85L RHD7K85L THD7K85L 8HD7K85L 4HD7K85L KHD7K85L 0HD7K85L UHD7K85L 5HD7K85L QHD7K85L  DHD7K85L AHD7K85L YHD7K85L ZHD7K85L GHD7K85L BHD7K85L 1HD7K85L WHD7K85L LHD7K85L FHD7K85L CHD7K85L 3HD7K85L XHD7K85L 7HD7K85L EHD7K85L VHD7K85L 9HD7K85L SHD7K85L IHD7K85L 2HD7K85L 6HD7K85L MHD7K85L OHD7K85L HHD7K85L PHD7K85L JHD7K85L NHD7K85L RMD7K85L TMD7K85L 8MD7K85L 4MD7K85L KMD7K85L 0MD7K85L UMD7K85L 5MD7K85L ');"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( G7, G5, G1, i1, G6, G0, G4, i3, i2, G2, G3 )  VALUES (
        'BMD7K85L 1MD7K85L  WMD7K85L LMD7K85L FMD7K85L CMD7K85L 3MD7K85L XMD7K85L 7MD7K85L EMD7K85L VMD7K85L 9MD7K85L SMD7K85L IMD7K85L 2MD7K85L 6MD7K85L MMD7K85L OMD7K85L HMD7K85L PMD7K85L JMD7K85L NMD7K85L RFD7K85L TFD7K85L 8FD7K85L 4FD7K85L KFD7K85L 0FD7K85L  UFD7K85L 5FD7K85L QFD7K85L DFD7K85L AFD7K85L YFD7K85L ZFD7K85L GFD7K85L BFD7K85L 1FD7K85L WFD7K85L LFD7K85L FFD7K85L CFD7K85L 3FD7K85L XFD7K85L 7FD7K85L EFD7K85L VFD7K85L 9FD7K85L SFD7K85L IFD7K85L 2FD7K85L 6FD7K85L MFD7K85L OFD7K85L HFD7K85L PFD7K85L JFD7K85L NFD7K85L RTD7K85L TTD7K85L 8TD7K85L 4TD7K85L KTD7K85L 0TD7K85L UTD7K85L 5TD7K85L QTD7K85L DTD7K85L ATD7K85L YTD7K85L ZTD7K85L  GTD7K85L BTD7K85L 1TD7K85L WTD7K85L LTD7K85L FTD7K85L CTD7K85L 3TD7K85L XTD7K85L 7TD7K85L ETD7K85L VTD7K85L 9TD7K85L STD7K85L ITD7K85L 2TD7K85L 6TD7K85L MTD7K85L OTD7K85L HTD7K85L PTD7K85L JTD7K85L NTD7K85L RLD7K85L TLD7K85L 8LD7K85L 4LD7K85L KLD7K85L ',
        1.921372674093035E12,              'WNKQKMFU',     -24, -5942687, -1284624, 'BD4U1',
        1.5376143702486332E13,      76,
        'Mike wormed neatly. Madelyn danced steadily. Callie and Genelle crawled sloppily over one of the train??? Lots of seals slide near an American. Fish and worms and mice. Oh My! Turtles and cows and dogs. Oh My! Joseph slide close to several elk. Bob jumped rarely. an Englishman split rarely! Diane walked thoughtfully. Genelle got out excitedly. Sharks and seals and cows! Oh My! A guy from Silicon Valley and Ben jumped nervously across one of the book. One of the horses flew near his father! Emma and mom crawled angrily beneath several table. A few eels danced over Fred? One of the turtles hotfooted over Issac! Mike ambled lovingly? my mother ran gracefully??? An American slide near one of the racoons. A German dashed close to a few bears??? llllllllllllllllllllllllllllllllllllllllll',
        4.860407377114671);"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO d4 ( G6, G5, G4, i3, i1, G3, G0, i2, G2, G7, G1 )  VALUES (
        -5942671, 1.9213732884487678E12, 'KD4U1', 1.537614443181495E13,    -156, 1.8677056376089114, -1164619,
        86,
        'A few penguins jumped beside Iola. Chet wormed luckily??? dad rambled rarely. Lots of sharks sprang across a guy from Silicon Valley. Vince and Ben skedaddled excitedly under the rug! Mike drove around several turtles. A German leaped beside those worms. A sibling rolled boldly. Tony danced luckily. Michelle and Chet ambled lovingly across several bike??? Michael and Genelle dashed sloppily around some rug. Dolphins and penguins and worms??? Oh My! Mike rolled thoughtfully. Alexandra skipped badly. My mother sprang across the whales! Issac hopped across some rats! Henry danced faithfully??? Genelle drove rarely. Several goats sprinted across Joe! Violet and Madelyn got out excitedly through quite a few car. Sue and Chet rolled leisurely near one of the truck???                     ',
        'ALD7K85L YLD7K85L ZLD7K85L GLD7K85L BLD7K85L 1LD7K85L WLD7K85L LLD7K85L FLD7K85L CLD7K85L 3LD7K85L XLD7K85L 7LD7K85L ELD7K85L VLD7K85L 9LD7K85L SLD7K85L ILD7K85L 2LD7K85L 6LD7K85L MLD7K85L OLD7K85L HLD7K85L PLD7K85L JLD7K85L NLD7K85L RPD7K85L TPD7K85L 8PD7K85L 4PD7K85L KPD7K85L 0PD7K85L UPD7K85L 5PD7K85L QPD7K85L DPD7K85L APD7K85L YPD7K85L ZPD7K85L GPD7K85L BPD7K85L 1PD7K85L WPD7K85L LPD7K85L FPD7K85L CPD7K85L 3PD7K85L XPD7K85L 7PD7K85L EPD7K85L VPD7K85L 9PD7K85L SPD7K85L IPD7K85L 2PD7K85L 6PD7K85L MPD7K85L OPD7K85L HPD7K85L PPD7K85L JPD7K85L NPD7K85L RUD7K85L TUD7K85L 8UD7K85L 4UD7K85L KUD7K85L 0UD7K85L UUD7K85L 5UD7K85L QUD7K85L DUD7K85L AUD7K85L YUD7K85L ZUD7K85L GUD7K85L BUD7K85L 1UD7K85L WUD7K85L LUD7K85L FUD7K85L CUD7K85L 3UD7K85L XUD7K85L 7UD7K85L EUD7K85L VUD7K85L 9UD7K85L SUD7K85L IUD7K85L 2UD7K85L 6UD7K85L MUD7K85L OUD7K85L HUD7K85L PUD7K85L JUD7K85L ',
        '5NKQKMFU');"""
    output = _dci.cmdexec(stmt)

    stmt = """Create table nsday (
        c1 char(27)no default not null,
        d1 interval day no default not null,
        l1 int no default not null,
        c2 char(27)no default not null,
        d2 interval day to hour no default not null,
        l2 int no default not null,
        c3 char(27)no default not null,
        d3 interval day to minute no default not null,
        l3 int no default not null,
        c4 char(27)no default not null,
        d4 interval day to second no default not null,
        l4 int no default not null,
        c5 char(27)no default not null,
        d5 interval day to second no default not null,
        l5 int no default not null,
        c6 char(27)no default not null,
        d6 interval day to second(6) no default not null,
        l6 int no default not null,
        c7 char(27)no default not null,
        d7 interval day to second(5) no default not null,
        l7 int no default not null,
        c8 char(27)no default not null,
        d8 interval day to second(4) no default not null,
        l8 int no default not null,
        c9 char(27)no default not null,
        d9 interval day to second(3) no default not null,
        l9 int no default not null,
        c10 char(27)no default not null,
        d10 interval day to second(2) no default not null,
        l10 int no default not null,
        c11 char(27)no default not null,
        d11 interval day to second(1) no default not null,
        l11 int no default not null
        )no partitions ;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nsday values
        ('13', interval '13' day, 2,
        '13:04', interval '13:04' day to hour, 5,
        '13:04:51', interval '13:04:51' day to minute, 8,
        '13:04:51:33', interval '13:04:51:33' day to second, 11,
        '13:04:51:33.123456', interval
        '13:04:51:33.123456' day to second, 18,
        '13:04:51:33.123456', interval
        '13:04:51:33.123456' day to second(6), 18,
        '13:04:51:33.12345', interval
        '13:04:51:33.12345' day to second(5), 17,
        '13:04:51:33.1234', interval
        '13:04:51:33.1234' day to second(4), 16,
        '13:04:51:33.123', interval
        '13:04:51:33.123' day to second(3), 15,
        '13:04:51:33.12', interval
        '13:04:51:33.12' day to second(2), 14,
        '13:04:51:33.1', interval
        '13:04:51:33.1' day to second(1), 13
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nsday values
        ('12', interval '12' day, 2,
        '12:10', interval '12:10' day to hour, 5,
        '12:10:44', interval '12:10:44' day to minute, 8,
        '12:10:44:33', interval '12:10:44:33' day to second, 11,
        '12:10:44:33.123456', interval
        '12:10:44:33.123456' day to second, 18,
        '12:10:44:33.123456', interval
        '12:10:44:33.123456' day to second(6), 18,
        '12:10:44:33.12345', interval
        '12:10:44:33.12345' day to second(5), 17,
        '12:10:44:33.1234', interval
        '12:10:44:33.1234' day to second(4), 16,
        '12:10:44:33.123', interval
        '12:10:44:33.123' day to second(3), 15,
        '12:10:44:33.12',interval
        '12:10:44:33.12' day to second(2), 14,
        '12:10:44:33.1', interval
        '12:10:44:33.1' day to second(1), 13
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nsday values
        ('31', interval '31' day, 2,
        '31:12', interval '31:12' day to hour, 5,
        '31:12:59', interval '31:12:59' day to minute,8,
        '31:12:59:46', interval '31:12:59:46' day to second, 11,
        '31:12:59:46.123456', interval
        '31:12:59:46.123456' day to second, 18,
        '31:12:59:46.123456', interval
        '31:12:59:46.123456' day to second(6), 18,
        '31:12:59:46.12345', interval
        '31:12:59:46.12345' day to second(5), 17,
        '31:12:59:46.1234', interval
        '31:12:59:46.1234' day to second(4), 16,
        '31:12:59:46.123', interval
        '31:12:59:46.123' day to second(3), 15,
        '31:12:59:46.12', interval
        '31:12:59:46.12' day to second(2), 14,
        '31:12:59:46.1', interval
        '31:12:59:46.1' day to second(1), 13
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nsday values
        ('01', interval '01' day , 2,
        '01:00', interval '01:00' day to hour, 5 ,
        '01:00:59', interval '01:00:59' day to minute, 8,
        '01:00:59:46', interval '01:00:59:46' day to second, 11,
        '01:00:59:46.003456', interval
        '01:00:59:46.003456' day to second, 18,
        '01:00:59:46.003456', interval
        '01:00:59:46.003456' day to second(6), 18,
        '01:00:59:46.00345', interval
        '01:00:59:46.00345' day to second(5), 17,
        '01:00:59:46.0034', interval
        '01:00:59:46.0034' day to second(4), 16,
        '01:00:59:46.003', interval
        '01:00:59:46.003' day to second(3), 15,
        '01:00:59:46.00', interval
        '01:00:59:46.00' day to second(2), 14,
        '01:00:59:46.0', interval
        '01:00:59:46.0' day to second(1), 13
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table nshour (
        c1 char(27)no default not null,
        d1 interval hour no default not null,
        l1 int no default not null,
        c2 char(27)no default not null,
        d2 interval hour to minute no default not null,
        l2 int no default not null,
        c3 char(27)no default not null,
        d3 interval hour to second no default not null,
        l3 int no default not null,
        c4 char(27)no default not null,
        d4 interval hour to second no default not null,
        l4 int no default not null,
        c5 char(27)no default not null,
        d5 interval hour to second(1) no default not null,
        l5 int no default not null,
        c6 char(27)no default not null,
        d6 interval hour to second(2) no default not null,
        l6 int no default not null,
        c7 char(27)no default not null,
        d7 interval hour to second(3) no default not null,
        l7 int no default not null,
        c8 char(27)no default not null,
        d8 interval hour to second(4) no default not null,
        l8 int no default not null,
        c9 char(27)no default not null,
        d9 interval hour to second(5) no default not null,
        l9 int no default not null,
        c10 char(27)no default not null,
        d10 interval hour to second(6) no default not null,
        l10 int no default not null,
        primary key (c9));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nshour values
        ('11', interval '11' hour, 2,
        '11:04', interval '11:04' hour to minute, 5,
        '11:04:22', interval '11:04:22' hour to second(0), 8,
        '11:04:22.122226',interval
        '11:04:22.122226' hour to second, 15,
        '11:04:22.122226', interval
        '11:04:22.1' hour to second(1), 10,
        '11:04:22.12', interval
        '11:04:22.12' hour to second(2), 11,
        '11:04:22.122', interval
        '11:04:22.122' hour to second(3), 12,
        '11:04:22.1222', interval
        '11:04:22.1222' hour to second(4), 13,
        '11:04:22.12222', interval
        '11:04:22.12222' hour to second(5), 14,
        '11:04:22.12222', interval
        '11:04:22.122222' hour to second(6), 15
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nshour values
        ('02', interval '02' hour, 2,
        '02:49', interval '02:49' hour to minute, 5,
        '02:49:22', interval '02:49:22' hour to second, 8,
        '02:49:22.333333', interval
        '02:49:22.333333' hour to second, 15,
        '02:49:22.333333', interval
        '02:49:22.3' hour to second(1), 10,
        '02:49:22.33', interval
        '02:49:22.33' hour to second(2), 11,
        '02:49:22.333', interval
        '02:49:22.333' hour to second(3), 12,
        '02:49:22.3333', interval
        '02:49:22.3333' hour to second(4), 13,
        '02:49:22.33333', interval
        '02:49:22.33333' hour to second(5), 14,
        '02:49:22.333333', interval
        '02:49:22.333333' hour to second(6), 15
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nshour values
        ('11', interval '11' hour, 2,
        '11:59', interval '11:59' hour to minute, 5,
        '11:59:59', interval '11:59:59' hour to second, 8,
        '11:59:59.555555', interval
        '11:59:59.555555' hour to second, 15,
        '11:59:59.5', interval
        '11:59:59.5' hour to second(1), 10,
        '11:59:59.55', interval
        '11:59:59.55' hour to second(2), 11,
        '11:59:59.555', interval
        '11:59:59.555' hour to second(3), 12,
        '11:59:59.5555', interval
        '11:59:59.5555' hour to second(4), 13,
        '11:59:59.55555', interval
        '11:59:59.55555' hour to second(5), 14,
        '11:59:59.555555', interval
        '11:59:59.555555' hour to second(6), 15
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nshour values
        ('20', interval '20' hour, 2,
        '20:49', interval '20:49' hour to minute, 5,
        '20:49:11', interval '20:49:11' hour to second, 8,
        '20:49:11.111111', interval
        '20:49:11.111111' hour to second, 15,
        '20:49:11.1', interval
        '20:49:11.1' hour to second(1), 10,
        '20:49:11.11', interval
        '20:49:11.11' hour to second(2), 11,
        '20:49:11.111', interval
        '20:49:11.111' hour to second(3), 12,
        '20:49:11.1111', interval
        '20:49:11.1111' hour to second(4), 13,
        '20:49:11.11111', interval
        '20:49:11.11111' hour to second(5), 14,
        '20:49:11.111111', interval
        '20:49:11.111111' hour to second(6), 15
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nshour values
        ('00', interval '00' hour, 2,
        '00:00', interval '00:00' hour to minute, 5,
        '00:00:01', interval '00:00:01' hour to second, 8,
        '00:00:01.000000', interval
        '00:00:01.000000' hour to second, 15,
        '00:00:01.0', interval
        '00:00:01.0' hour to second(1), 10,
        '00:00:01.00', interval
        '00:00:01.00' hour to second(2), 11,
        '00:00:01.000', interval
        '00:00:01.000' hour to second(3), 12,
        '00:00:01.0000', interval
        '00:00:01.0000' hour to second(4), 13,
        '00:00:01.00000', interval
        '00:00:01.00000' hour to second(5), 14,
        '00:00:01.000000', interval
        '00:00:01.000000' hour to second(6), 15
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table nsminute (
        c1 char(27)no default not null,
        d1 interval minute no default not null,
        l1 int no default not null,
        c2 char(27)no default not null,
        d2 interval minute to second no default not null,
        l2 int no default not null,
        c3 char(27)no default not null,
        d3 interval minute to second no default not null,
        l3 int no default not null,
        c4 char(27)no default not null,
        d4 interval minute to second(1) no default not null,
        l4 int no default not null,
        c5 char(27)no default not null,
        d5 interval minute to second(2) no default not null,
        l5 int no default not null,
        c6 char(27)no default not null,
        d6 interval minute to second(3) no default not null,
        l6 int no default not null,
        c7 char(27)no default not null,
        d7 interval minute to second(4) no default not null,
        l7 int no default not null,
        c8 char(27)no default not null,
        d8 interval minute to second(5) no default not null,
        l8 int no default not null,
        c9 char(27)no default not null,
        d9 interval minute to second(6) no default not null,
        l9 int no default not null,
        primary key (d3));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nsminute values
        ('13', interval '13' minute, 2,
        '13:04', interval '13:04' minute to second, 5,
        '13:04.123456', interval
        '13:04.123456' minute to second(6), 12,
        '13:04.1', interval
        '13:04.1' minute to second(1), 7,
        '13:04.12', interval
        '13:04.12' minute to second(2), 8,
        '13:04.123', interval
        '13:04.123' minute to second(3), 9,
        '13:04.1234', interval
        '13:04.1234' minute to second(4), 10,
        '13:04.12345', interval
        '13:04.12345' minute to second(5), 11,
        '13:04.123456', interval
        '13:04.123456' minute to second(6), 12
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nsminute values
        ('12', interval '12' minute, 2,
        '12:10', interval '12:10' minute to second, 5,
        '12:10', interval
        '12:10.123456' minute to second, 12,
        '12:10.1', interval
        '12:10.1' minute to second(1), 7,
        '12:10.12', interval
        '12:10.12' minute to second(2), 8,
        '12:10.123', interval
        '12:10.123' minute to second(3), 9,
        '12:10.1234', interval
        '12:10.1234' minute to second(4), 10,
        '12:10.12345', interval
        '12:10.12345' minute to second(5), 11,
        '12:10.123456', interval
        '12:10.123456' minute to second(6), 12
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nsminute values
        ('31', interval '31' minute, 2,
        '31:59', interval '31:59' minute to second, 5,
        '31:59.123456', interval
        '31:59.123456' minute to second, 12,
        '31:59.1', interval
        '31:59.1' minute to second(1), 7,
        '31:59.12', interval
        '31:59.12' minute to second(2), 8,
        '31:59.123', interval
        '31:59.123' minute to second(3), 9,
        '31:59.1234', interval
        '31:59.1234' minute to second(4), 10,
        '31:59.12345', interval
        '31:59.12345' minute to second(5), 11,
        '31:59.123456', interval
        '31:59.123456' minute to second(6), 12
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nsminute values
        ('01', interval '01' minute , 2,
        '01:59', interval '01:59' minute to second, 5,
        '01:59.999999', interval
        '01:59.999999' minute to second, 12,
        '01:59.9', interval
        '01:59.9' minute to second(1), 7,
        '01:59.99', interval
        '01:59.99' minute to second(2), 8,
        '01:59.999', interval
        '01:59.999' minute to second(3), 9,
        '01:59.9999', interval
        '01:59.9999' minute to second(4), 10,
        '01:59.99999', interval
        '01:59.99999' minute to second(5), 11,
        '01:59.999999', interval
        '01:59.999999' minute to second(6), 12
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table nssecond (
        c1 char(27)no default not null,
        d1 interval second no default not null,
        l1 int no default not null,
        c2 char(27)no default not null,
        d2 interval second no default not null,
        l2 int no default not null,
        c3 char(27)no default not null,
        d3 interval second(2,1) no default not null,
        l3 int no default not null,
        c4 char(27)no default not null,
        d4 interval second(2,2) no default not null,
        l4 int no default not null,
        c5 char(27)no default not null,
        d5 interval second(2,3) no default not null,
        l5 int no default not null,
        c6 char(27)no default not null,
        d6 interval second(2,4) no default not null,
        l6 int no default not null,
        c7 char(27)no default not null,
        d7 interval second(2,5) no default not null,
        l7 int no default not null,
        c8 char(27)no default not null,
        d8 interval second(2,6) no default not null,
        l8 int no default not null,
        primary key (d3));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nssecond values
        ('13',  interval '13' second, 2,
        '13.123455', interval
        '13.123455' second, 9,
        '13.1', interval
        '13.1' second(2,1), 4,
        '13.12', interval
        '13.12' second(2,2), 5,
        '13.123', interval
        '13.123' second(2,3), 6,
        '13.1234', interval
        '13.1234' second(2,4), 7,
        '13.12345', interval
        '13.12345' second(2,5) , 8,
        '13.123455', interval
        '13.123455' second(2,6) , 9
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nssecond values
        ('12', interval '12' second, 2,
        '12.123456', interval
        '12.123456' second, 9 ,
        '12:10.1', interval
        '12.1' second(2,1), 4,
        '12.12', interval
        '12.12' second(2,2), 5,
        '12.123', interval
        '12.123' second(2,3), 6,
        '12.1234', interval
        '12.1234' second(2,4), 7 ,
        '12.12345', interval
        '12.12345' second(2,5) , 8,
        '12.123456', interval
        '12.123456' second(2,6) , 9
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nssecond values
        ('59', interval '59' second, 2,
        '59.123456', interval
        '59.123456' second, 9,
        '59.1', interval
        '59.1' second(2,1), 4,
        '59.12', interval
        '59.12' second(2,2), 5,
        '59.123', interval
        '59.123' second(2,3), 6,
        '59.1234', interval
        '59.1234' second(2,4), 7,
        '59.12345', interval
        '59.12345' second(2,5) , 8,
        '59.123456', interval
        '59.123456' second(2,6), 9
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into nssecond values
        ('01', interval '01' second , 2,
        '01.999999',interval
        '01.999999' second, 9,
        '01.9', interval
        '01.9' second(2,1), 4,
        '01.99', interval
        '01.99' second(2,2), 5,
        '01.999', interval
        '01.999' second(2,3), 6,
        '01.9999', interval
        '01.9999' second(2,4), 7,
        '01.99999', interval
        '01.99999' second(2,5) , 8,
        '01.999999', interval
        '01.999999' second(2,6), 9
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table DAYTAB(
        d_t_m_e        TIMESTAMP       NO DEFAULT NOT NULL,
        d_n            CHAR(10)        NO DEFAULT NOT NULL,
        m_n            VARCHAR(10)     NO DEFAULT NOT NULL,
        d_of_y         INTEGER         NO DEFAULT NOT NULL,
        w_k            SMALLINT        NO DEFAULT NOT NULL,
        q_r            SMALLINT        NO DEFAULT NOT NULL,
        year_d         INT             NO DEFAULT NOT NULL,
        month_d        SMALLINT        NO DEFAULT NOT NULL,
        day_d          SMALLINT        NO DEFAULT NOT NULL,
        hour_d         SMALLINT        NO DEFAULT NOT NULL,
        minute_d       SMALLINT        NO DEFAULT NOT NULL,
        second_d       INT             NO DEFAULT NOT NULL
        ) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO DAYTAB VALUES(
        TIMESTAMP  '1901-10-10 23:15:00.300000',
        DAYNAME   (date '1989-01-11'),
        MONTHNAME (date '1976-10-31'),
        DAYOFYEAR (date '1920-01-01'),
        WEEK      (date '2040-12-31'),
        QUARTER   (date '2000-01-01'),
        YEAR      (date '1945-05-06'),
        MONTH     (date '1936-08-10'),
        DAY       (date '2000-12-31'),
        HOUR      (timestamp '1718-01-10 12:50:59.400000'),
        MINUTE    (timestamp '0001-01-01 01:59:50.400000'),
        SECOND    (timestamp '1210-11-11 11:01:00.999999')
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO DAYTAB VALUES(
        TIMESTAMP  '12/31/1999 23:59:59.999999',
        DAYNAME   (date '05/01/1989'),
        MONTHNAME (date '01/31/1956'),
        DAYOFYEAR (date '12/31/2001'),
        WEEK      (date '01/01/1998'),
        QUARTER   (date '06/30/1900'),
        YEAR      (date '05/06/0001'),
        MONTH     (date '07/10/1936'),
        DAY       (date '02/28/1951'),
        HOUR      (timestamp '01/10/0718 12:50:59.999 pm'),
        MINUTE    (timestamp '01/01/0001 01:59:50.000001 am'),
        SECOND    (timestamp '11/11/1210 11:01:59.999910')
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO DAYTAB VALUES(
        TIMESTAMP '13.12.0001 00.00.00.000000',
        DAYNAME   (date '11.01.1989'),
        MONTHNAME (date '31.10.1976'),
        DAYOFYEAR (date '01.01.1920'),
        WEEK      (date '21.09.2000'),
        QUARTER   (date '01.10.2000'),
        YEAR      (date '13.05.1945'),
        MONTH     (date '10.10.1946'),
        DAY       (date '29.02.1996'), -- leap year
        HOUR      (timestamp '10.01.1718 00.50.58.400000'),
        MINUTE    (timestamp '01.01.0001 01.00.50.400000'),
        SECOND    (timestamp '11.11.1210 11.01.40.590000')
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO DAYTAB VALUES(
        TIMESTAMP  '1901-05-10 15:19:59.300000',
        DAYNAME   (timestamp '1918-10-11 10:00:09.999930'),
        MONTHNAME (timestamp '1876-01-31 07:59:05.000000'),
        DAYOFYEAR (timestamp '0001-01-01 23:59:59.999999'),
        WEEK      (timestamp '1999-04-03 23:59:59.999999'),
        QUARTER   (timestamp '1191-09-30 23:59:59.999999'),
        YEAR      (timestamp '2106-01-01 00:00:00.000001'),
        MONTH     (timestamp '1433-04-10 22:22:22.222222'),
        DAY       (timestamp '1945-03-31 12:50:59.400000'),
        HOUR      (time '12:50:59.400000'),
        MINUTE    (time '23:59:59.999999'),
        SECOND    (time '00:00:01.000000')
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table stday (
        d         interval day                default interval '01' day,
        daytohr   interval day to hour        default interval '01:02' day to hour,
        daytomin  interval day to minute      default interval '01:02:03' day to minute,
        daytosec  interval day to second      no default not null,
        daytof    interval day to second    default interval '01:02:03:04.234234' day to second,
        daytof1   interval day to second(1) default interval '01:02:03:04.2' day to second(1),
        daytof2   interval day to second(2) default interval '01:02:03:04.23' day to second(2),
        daytof3   interval day to second(3) default interval '01:02:03:04.232' day to second(3),
        daytof4   interval day to second(4) default interval '01:02:03:04.2323' day to second(4),
        daytof5   interval day to second(5) default interval '01:02:03:04.23232' day to second(5),
        daytof6   interval day to second(6) default interval '01:02:03:04.232323' day to second(6),
        primary key (daytosec desc));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stday values (
        interval '05' day,
        interval '05:06' day to hour,
        interval '05:06:07' day to minute,
        interval '05:06:07:08' day to second,
        interval '05:06:07:08.901234' day to second,
        interval '05:06:07:08.9' day to second(1),
        interval '05:06:07:08.90' day to second(2),
        interval '05:06:07:08.901' day to second(3),
        interval '05:06:07:08.9012' day to second(4),
        interval '05:06:07:08.90123' day to second(5),
        interval '05:06:07:08.901234' day to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stday values (
        interval '10' day,
        interval '10:00' day to hour,
        interval '10:00:00' day to minute,
        interval '10:00:00:00' day to second,
        interval '10:00:00:00.000000' day to second,
        interval '10:00:00:00.0' day to second(1),
        interval '10:00:00:00.00' day to second(2),
        interval '10:00:00:00.000' day to second(3),
        interval '10:00:00:00.0000' day to second(4),
        interval '10:00:00:00.00000' day to second(5),
        interval '10:00:00:00.000000' day to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stday values (
        interval '20' day,
        interval '20:10' day to hour,
        interval '20:10:40' day to minute,
        interval '20:10:40:50' day to second,
        interval '20:10:40:50.666666' day to second,
        interval '20:10:40:50.6' day to second(1),
        interval '20:10:40:50.66' day to second(2),
        interval '20:10:40:50.666' day to second(3),
        interval '20:10:40:50.6666' day to second(4),
        interval '20:10:40:50.66666' day to second(5),
        interval '20:10:40:50.666666' day to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stday values (
        interval '30' day,
        interval '30:23' day to hour,
        interval '30:23:59' day to minute,
        interval '30:23:59:59' day to second,
        interval '30:23:59:59.999999' day to second,
        interval '30:23:59:59.9' day to second(1),
        interval '30:23:59:59.99' day to second(2),
        interval '30:23:59:59.999' day to second(3),
        interval '30:23:59:59.9999' day to second(4),
        interval '30:23:59:59.99999' day to second(5),
        interval '30:23:59:59.999999' day to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stday values (
        interval '31' day,
        interval '31:23' day to hour,
        interval '31:23:59' day to minute,
        interval '31:23:59:59' day to second,
        interval '31:23:59:59.999999' day to second,
        interval '31:23:59:59.9' day to second(1),
        interval '31:23:59:59.99' day to second(2),
        interval '31:23:59:59.999' day to second(3),
        interval '31:23:59:59.9999' day to second(4),
        interval '31:23:59:59.99999' day to second(5),
        interval '31:23:59:59.999999' day to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stday values (
        interval '19' day,
        interval '19:18' day to hour,
        interval '19:18:17' day to minute,
        interval '19:18:17:16' day to second,
        interval '19:18:17:16.151413' day to second,
        interval '19:18:17:16.1' day to second(1),
        interval '19:18:17:16.15' day to second(2),
        interval '19:18:17:16.151' day to second(3),
        interval '19:18:17:16.1514' day to second(4),
        interval '19:18:17:16.15141' day to second(5),
        interval '19:18:17:16.151413' day to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """create table sthour (
        h           interval hour                default interval '12' hour,
        htomin      interval hour to minute      default interval '12:01' hour to minute,
        htosec      interval hour to second      default interval '12:01:02' hour to second,
        htof        interval hour to second      default interval '12:01:02.345678' hour to second,
        htof1       interval hour to second(1) default interval '12:01:02.3' hour to second(1),
        htof2       interval hour to second(2) default interval '12:01:02.34' hour to second(2),
        htof3       interval hour to second(3) no default not null,
        htof4       interval hour to second(4) default interval '12:01:02.3456' hour to second(4),
        htof5       interval hour to second(5) default interval '12:01:02.34567' hour to second(5),
        htof6       interval hour to second(6) default interval '12:01:02.345678' hour to second(6),
        primary key (htof3));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into sthour values (
        interval '07' hour,
        interval '07:08' hour to minute,
        interval '07:08:09' hour to second,
        interval '07:08:09.012345' hour to second,
        interval '07:08:09.0' hour to second(1),
        interval '07:08:09.01' hour to second(2),
        interval '07:08:09.012' hour to second(3),
        interval '07:08:09.0123' hour to second(4),
        interval '07:08:09.01234' hour to second(5),
        interval '07:08:09.012345' hour to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into sthour values (
        interval '19' hour,
        interval '19:20' hour to minute,
        interval '19:20:21' hour to second,
        interval '19:20:21.232324' hour to second,
        interval '19:20:21.2' hour to second(1),
        interval '19:20:21.23' hour to second(2),
        interval '19:20:21.232' hour to second(3),
        interval '19:20:21.2323' hour to second(4),
        interval '19:20:21.23232' hour to second(5),
        interval '19:20:21.232324' hour to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into sthour values (
        interval '23' hour,
        interval '23:59' hour to minute,
        interval '23:59:59' hour to second,
        interval '23:59:59.999999' hour to second,
        interval '23:59:59.9' hour to second(1),
        interval '23:59:59.99' hour to second(2),
        interval '23:59:59.999' hour to second(3),
        interval '23:59:59.9999' hour to second(4),
        interval '23:59:59.99999' hour to second(5),
        interval '23:59:59.999999' hour to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into sthour values (
        interval '00' hour,
        interval '00:00' hour to minute,
        interval '00:00:00' hour to second,
        interval '00:00:00.000001' hour to second,
        interval '00:00:00.1' hour to second(1),
        interval '00:00:00.01' hour to second(2),
        interval '00:00:00.001' hour to second(3),
        interval '00:00:00.0001' hour to second(4),
        interval '00:00:00.00001' hour to second(5),
        interval '00:00:00.000001' hour to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into sthour values (
        interval '12' hour,
        interval '12:59' hour to minute,
        interval '12:59:59' hour to second,
        interval '12:59:59.000003' hour to second,
        interval '12:59:59.0' hour to second(1),
        interval '12:59:59.00' hour to second(2),
        interval '12:59:59.000' hour to second(3),
        interval '12:59:59.0000' hour to second(4),
        interval '12:59:59.00000' hour to second(5),
        interval '12:59:59.000003' hour to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into sthour values (
        interval '13' hour,
        interval '13:14' hour to minute,
        interval '13:14:15' hour to second,
        interval '13:14:15.161718' hour to second,
        interval '13:14:15.1' hour to second(1),
        interval '13:14:15.16' hour to second(2),
        interval '13:14:15.161' hour to second(3),
        interval '13:14:15.1617' hour to second(4),
        interval '13:14:15.16171' hour to second(5),
        interval '13:14:15.161718' hour to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """create table stmin (
        m            interval minute                default interval '17' minute,
        mtosec       interval minute to second      default interval '17:17' minute to second not null,
        mtof         interval minute to second    default interval '17:17.171717' minute to second,
        mtof1        interval minute to second    default interval '17:17.1' minute to second(1),
        mtof2        interval minute to second    default interval '17:17.17' minute to second(2),
        mtof3        interval minute to second    default interval '17:17.171' minute to second(3),
        mtof4        interval minute to second    default interval '17:17.1717' minute to second(4),
        mtof5        interval minute to second    default interval '17:17.17171' minute to second(5),
        mtof6        interval minute to second    default interval '17:17.171717' minute to second(6),
        primary key (mtosec desc));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into  stmin values (
        interval '23' minute,
        interval '23:24' minute to second,
        interval '23:24.252525' minute to second,
        interval '23:24.2' minute to second(1),
        interval '23:24.25' minute to second(2),
        interval '23:24.252' minute to second(3),
        interval '23:24.2525' minute to second(4),
        interval '23:24.25252' minute to second(5),
        interval '23:24.252525' minute to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into  stmin values (
        interval '59' minute,
        interval '59:59' minute to second,
        interval '59:59.999999' minute to second,
        interval '59:59.9' minute to second(1),
        interval '59:59.99' minute to second(2),
        interval '59:59.999' minute to second(3),
        interval '59:59.9999' minute to second(4),
        interval '59:59.99999' minute to second(5),
        interval '59:59.999999' minute to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into  stmin values (
        interval '01' minute,
        interval '01:00' minute to second,
        interval '01:00.000001' minute to second,
        interval '01:00.0' minute to second(1),
        interval '01:00.00' minute to second(2),
        interval '01:00.000' minute to second(3),
        interval '01:00.0000' minute to second(4),
        interval '01:00.00000' minute to second(5),
        interval '01:00.000001' minute to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into  stmin values (
        interval '30' minute,
        interval '30:31' minute to second,
        interval '30:31.323334' minute to second,
        interval '30:31.3' minute to second(1),
        interval '30:31.32' minute to second(2),
        interval '30:31.323' minute to second(3),
        interval '30:31.3233' minute to second(4),
        interval '30:31.32333' minute to second(5),
        interval '30:31.323334' minute to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into  stmin values (
        interval '12' minute,
        interval '12:59' minute to second,
        interval '12:59.111111' minute to second,
        interval '12:59.1' minute to second(1),
        interval '12:59.11' minute to second(2),
        interval '12:59.111' minute to second(3),
        interval '12:59.1111' minute to second(4),
        interval '12:59.11111' minute to second(5),
        interval '12:59.111111' minute to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into  stmin values (
        interval '08' minute,
        interval '08:01' minute to second,
        interval '08:01.999999' minute to second,
        interval '08:01.9' minute to second(1),
        interval '08:01.99' minute to second(2),
        interval '08:01.999' minute to second(3),
        interval '08:01.9999' minute to second(4),
        interval '08:01.99999' minute to second(5),
        interval '08:01.999999' minute to second(6));"""
    output = _dci.cmdexec(stmt)

    stmt = """create table stsec (
        s      interval second                default interval '59' second,
        stof1  interval second(2,1) default interval '59.9' second(2,1) not null,
        stof2  interval second(2,2) default interval '59.99' second(2,2),
        stof3  interval second(2,3) default interval '59.999' second(2,3),
        stof4  interval second(2,4) default interval '59.9999' second(2,4),
        stof5  interval second(2,5) default interval '59.99999' second(2,5),
        stof6  interval second(2,6) default interval '59.999999' second(2,6),
        stof   interval second    default interval '59.999999' second,
        primary key (stof1));"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stsec values (
        interval '20' second,
        interval '20.9' second(2,1),
        interval '20.99' second(2,2),
        interval '20.999' second(2,3),
        interval '20.9999' second(2,4),
        interval '20.99999' second(2,5),
        interval '20.999999' second(2,6),
        interval '20.999999' second);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stsec values (
        interval '40' second,
        interval '40.9' second(2,1),
        interval '40.99' second(2,2),
        interval '40.999' second(2,3),
        interval '40.9999' second(2,4),
        interval '40.99999' second(2,5),
        interval '40.999999' second(2,6),
        interval '40.999999' second);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stsec values (
        interval '59' second,
        interval '59.9' second(2,1),
        interval '59.99' second(2,2),
        interval '59.999' second(2,3),
        interval '59.9999' second(2,4),
        interval '59.99999' second(2,5),
        interval '59.999999' second(2,6),
        interval '59.999999' second);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stsec values (
        interval '20' second,
        interval '20.8' second(2,1),
        interval '20.88' second(2,2),
        interval '20.888' second(2,3),
        interval '20.8888' second(2,4),
        interval '20.88888' second(2,5),
        interval '20.888888' second(2,6),
        interval '20.888888' second);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stsec values (
        interval '01' second,
        interval '01.1' second(2,1),
        interval '01.19' second(2,2),
        interval '01.199' second(2,3),
        interval '01.1999' second(2,4),
        interval '01.19999' second(2,5),
        interval '01.199999' second(2,6),
        interval '01.199999' second);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into stsec values (
        interval '39' second,
        interval '39.5' second(2,1),
        interval '39.59' second(2,2),
        interval '39.599' second(2,3),
        interval '39.5999' second(2,4),
        interval '39.59999' second(2,5),
        interval '39.599999' second(2,6),
        interval '39.599999' second);"""
    output = _dci.cmdexec(stmt)

    stmt = """create table tbint (
        ivyr        interval year,
        ivmn        interval month,
        ivdy        interval day,
        ivhr        interval hour,
        ivmt        interval minute,
        ivsc        interval second,
        ivsc6       interval second(2,6)
        ) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tbint values (
        interval '97' year,
        interval '02' month,
        interval '11' day,
        interval '15' hour,
        interval '45' minute,
        interval '14' second,
        interval '23.123456' second(6)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tbint values (
        interval '00' year,
        interval '00' month,
        interval '00' day,
        interval '00' hour,
        interval '00' minute,
        interval '00' second,
        interval '00.000000' second(6)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tbint values (
        interval - '30' year,
        interval - '12' month,
        interval - '31' day,
        interval - '24' hour,
        interval - '60' minute,
        interval - '59' second,
        interval - '59.999999' second(6)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (11223, -12123434, 12123434, 1.9E19, 1.4E14,
        2.1E21, 2.2E22, 2.3E23, 5.2E52,
        5.3E53, 5.4E54, -1.17549436e-38, -2.2250738585072014e-308);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (22334, -22990, 2221122, 1.8E18, 2.4E14,
        2.4E21, 2.0E22, 2.2E23, 1.7272337110188889e-76,
        2.3E53, 2.4E54, 1.17549436e-38, 2.22E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (3338, -33112, 33327, 1.3E13, 3.4E14,
        3.1E21, 3.2E22, 3.3E23, 3.5E35,
        3.3E53, 3.4E54, -3.40282346e+38, 1.7976931348623157e+308);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (4445, -44112, 44, 1.4E14, 4.4E14,
        4.1E21, 4.2E22, -1.15792089237316192e77, 4.5E52,
        4.3E53, 4.4E54, 3.40282346e+38, 4.44E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (55, -501, 50023, 5.9E15, 5.4E14,
        5.1E21, 5.2E22, 5.3E23, 5.5E52,
        5.5E53, 5.5E54, 5.55E11, 5.55E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (68, 61290, 63301, 6.9E16, 6.4E14,
        6.1E21, 6.2E22, 6.3E23, 6.5E52,
        6.3E53, 6.4E54, 6.66E11, 6.66E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (770011, 74389, 7, 7.9E17, 7.4E14,
        7.1E21, 7.2E22, 7.3E23, 7.5E52,
        7.3E53, 7.4E54, 7.77E11, 7.77E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3   values (2147483647, 9.223E18, 0, 2.2250738585072014e-300,
        2.2250738585072014e-308, 2.2250738585072014e-307,
        1.7976931348623157e+308, 2.2250738585072014e-308,
        2.2250738585072014e-308, 1.7976931348623157e+308,
        1.7976931348623157e+308, 1.17549435e-38,
        1.7976931348623157e+308);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3  values (-2147483648, -9.223E18, 0, -2.2250738585072014e-308,
        -1.7976931348623157e+200, -2.2250738585072014e-300,
        -1.7976931348623157e+308, -2.2250738585072014e-308,
        -2.2250738585072014e-308, -1.7976931348623157e+308,
        -1.7976931348623157e+308, -1.17549435e-38,
        -1.7976931348623157e+308);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (11243, -13423434, 15623434, 1.7679E19, 1.4767E14,
        2.1E141, 2.12122E22, 2.3E33, 5.2E42,
        5.3E33, 5.4E53, -1.143434535e-37, -2.225475463633685072014e-37);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (242434, -32990, 26346476, 1.8E17, 2.32344E24,
        04.4E21, 2.0535E32, 2.5857352E23, 1.252356360188889e-74,
        2.3142643E52, 2.52337454E53, 1.178685736549436e-37, 2.22E51);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (-3338, -23112, 43327, 1.25363463E13, 3.758694E14,
        3.1253475861E21, 3.965735242E22, 3.26970073533E23, 3.14537475E35,
        3.5235637583E53, 3.42376474E54, -3.3414253640282346e+38, 1.7976931348623157e+35);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (4434345, -54112,64644, 0424241.4245245254E14, 9.1314252354E13,
        9.114253563E21, 6.24253563562E22, -1.16346465792776192e75, 4.31341424525E52,
        4.42536347643E53, 4.45256364E54, 3.4025235363682346e+38, 4.4142523563644E53);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (586765, -346361, 564623, 5.253636469E15, 5.6363463464E14,
        5.15235353E21, 5.25235335E22, 5.35235353E23, 5.5523535E52,
        5.5E53, 5.5E54, 5.555353535E11, 5.5424522535635E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (-6438, 664290, 633425, 6.35352359E36, 2.423535634E34,
        6.6346485661E41, -2.424242422E22, -6.142523633E23, -6.142424525E22,
        -6.352353647474E51, 6.363647474E54, 6.534647578524666E11, 4.1425635623566E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (77405311, 174389, 42452527, 3.42536369E47, 7.56346476464E44,
        7.42424221E21, 7.141242422E22, -7.2445243E33, 7.53131341341E54,
        7.424525252353E53, 7.5235252524E54, 7.5252525623577E11, 7.5252525577E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (1243423, -14232123434, 422123434, 1.943443E19, 1.2412424E14,
        2.1376457575E21, 2.3141242532E22, 2.535353763E23, 5.2313131425E52,
        5.364747E53, 5.53536764E54, 1.647785811E11, 1.256364764711E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (228786334, -22990, 2221122, 1.8E18, 2.4E14,
        2.4E21, 2.0E22, 2.2E23, 2.5E52,
        2.3E53, 2.4E54, 2.22E11, 2.22E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (5353338, -674733112, 37573327, 1.8683452353E13, 3.42424E14,
        3.141424E29, 3.23131E27, 3.5353E33, 3.5E33,
        3.3412424E52, 3.4563456346E54, 3.36346363E11, 3.3646346363E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (44349785, -644112, 944, 1.468E14, 4.9704E14,
        4.1412425E41, 4.275758E22, 4.64643E33, 4.5E51,
        4.6436473E54, 6.3463444E54, 4.63666444E11, 4.764755844E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (578735, -501, 50023, 5.9E15, 5.4E14,
        5.321E21, 5.244E22, 5.553E23, 5.665E52,
        5.555E53, 5.566E54, 5.5775E11, 5.8855E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (69898, 61290, 63301, 6.9E16, 6.4E14,
        6.134E21, 6.25456E22, 6.3656E23, 6.7675E52,
        6.4535433E53, 6.5454E54, 6.656666E11, 6.56467666E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (7870011, 2474389,457, 7.6469E17, 7.4E14,
        7.143E21, 7.34342E22, 7.33434E23, 7.5455E52,
        7.2423E53, 7.4344E54, 7.453477E11, 7.43477E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (11978263, -135363434, 7352534, 1.2458967639E19, 1.25363624144E14,
        2.14237474757E21, 2.64745785462E22, 2.525364783E23, 5.07098442E52,
        5.537675753E53, 5.647647854E54, 1.1452363461E11, 1.152337634761E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (22897734, -82990, 451122, 1.525356368E18, 2.75785352354E14,
        2.412312422535E21, 2.0563647457E42, 2.3125362412E43, 2.45235635635E32,
        2.353536346464E54, 2.5356346464E54, 2.26464764762E14, 2.23634646462E53);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (7345438, -43112, 3327, 1.34636463E13, 6.452452524E14,
        3.15353535E21, 3.2412424524E12, 3.5235235353E33, 3.5635355E45,
        6.335235353E53, 9.42424244E54, -3.4242452433E11, 3.352337854523E53);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (4445345, -56356344112, 5354, 1.535354E14, 4.535354E14,
        4.4444444441E21, 4.55555555552E22, 4.44444444444443E23, 4.63463464645E52,
        4.342424E53, 4.424244E54, 4.4242444E11, 4.424242444E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (508985, -501, 5064523, 5.5635359E15, 5.131315634E14,
        5.5353464641E21, 5.64646462E22, 5.6464646463E23, 5.42536585E52,
        5.12425365E53, 5.5578578565E54, 5.54124245255E11, 5.55314255363E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (6878663, 61290, 63301, 6.9E16, 6.4E14,
        6.424241E21, 6.535352E22, 6.6346363E23, 6.6636365E52,
        6.4525256363E53, 6.441245563E54, 6.17462266E11, 6.6636366E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (7730011, 74389, 53537, 7.533535359E17, 7.6464644E14,
        3.4253531E21, 7.331313412E22, 7.6432143E23, 7.5353535355E52,
        7.452353363E53, 7.535356354E54, 7.25364746577E11, 7.13412424524577E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (1187623, -1212434, 121434, 1.452352359E19, 1.535534E14,
        2.42342421E21, 2.424242422E22, 2.64646463E23, 5.6464646462E52,
        5.534657573E53, 5.53536475754E54, 1.13536474771E11, 1.16464647781E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (222340, -2990, 225464422, 1.53353538E18, 2.53535354E14,
        2.47575757E21, 2.980900E22, 2.6464642E23, 2.424245E52,
        2.35346475687E53, 2.4242444E54, 2.7674575722E11, 2.46464648682E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (3336568, -33112, 33327, 1.3E13, 3.4E14,
        3.1131313E21, 3.24242452E22, 3.42452532633E23, 3.5353563565E35,
        3.4242423E53, 3.452525254E54, 3.523523523533E11, 3.523523533E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (44445435, -44112, 44, 1.4E14, 4.4E14,
        4.1141241414E21, 4.4124442E22, 4.414143E23, 4.4141445E52,
        4.4144523E53, 4.42455234E54, 4.4141452444E11, 4.41414411444E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (5975235, -501, 50023, 5.9E15, 5.4E14,
        5.414124242421E21, 5.235364742E22, 5.4478586973E23, 5.97078-5E52,
        5.5707070E53, 5.56866979070E54, 5.708070796855E11, 5.07807880-55E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (1323268, 61290, 63301, 6.9E16, 6.4E14,
        6.1313E21, 6.253532E22, 6.5636463E23, 6.47578585E52,
        6.858893E53, 6.378584E54, 6.64578463566E11, 6.755866E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (7470011, 74389, 7, 7.9E17, 7.4E14,
        7.6346471E21, 7.7457572E22, 7.745757853E23, 7.996905E52,
        7.3476474748E53, 7.7856869694E54, 7.97979777E11, 7.976977E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (1125423, -12123434, 12123434, 1.9E19, 1.4E14,
        2.142452452E21, 2.52352532E22, 2.5633563E23, 5.525235352E52,
        5.52563783E53, 5.45235535E54, 1.1647781E11, 1.1523523521E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (22756764, -22990, 2221122, 1.8E18, 2.4E14,
        2.45635335E21, 2.6344897900E22, 2.075746572E23, 2.1443688585E52,
        2.35235235356E53, 2.24255634E54, 2.263662E11, 2.2533632E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (3309838, -33112, 33327, 1.3E13, 3.4E14,
        3.1423442345E21, 3.452342452E22, 3.535353E23, 3.5353535E35,
        3.34242424E53, 3.452353634476E54, 3.35367443E11, 3.646464633E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (444985, -44112, 44, 1.4E14, 4.4E14,
        4.535351E21, 4.53535352E22, 4.3535353E23, 4.535355E52,
        4.74575693E53, 4.45264E54, 4.46347478474E11, 4.21314244E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (5073225, -501, 50023, 5.9E15, 5.4E14,
        5.424241E21, 5.5353532E22, 5.5635363E23, 5.647689695E52,
        5.42678475E53, 5.53523657855E54, 5.5079857475E11, 5.59797-95E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (66565238, 61290, 63301, 6.9E16, 6.4E14,
        6.313151E21, 6.647242E22, 6.536742543E23, 6.4241342424245E52,
        6.53566263E53, 6.444784E54, 6.664772426E11, 6.654727271176E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (77220011, 74389, 7, 7.9E17, 7.4E14,
        7.424251E21, 7.53537578752E22, 7.525244233E23, 7.53564474745E52,
        7.34242634152E53, 7.452476545234E54, 7.745242427E11, 7.75646757324247E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (85424243, -12123434, 121243434, 1.42449E19, 1.42424244E14,
        2.14242424E21, 2.242424E22, 2.4242423E23, 5.4242422E52,
        5.34242424E53, 5.3142254E54, 1.13131311E11, 1.3145336647647611E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (98527462, -229490, 22421122, 1.424248E18, 2.42424E14,
        2.464646E21, 2.055356E22, 2.646462E23, 2.646645E52,
        2.345455E53, 2.464646E54, 2.64646422E11, 2.64646422E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_float, col_float52, col_float54, col_doublep)
        values (+2.2350738585072014e-309, 1.341E10, 1.45665, 6563.3);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (113223, -125123434, 121623434, 1.975786786E19, 1.8768794E14,
        2.979971E21, 2.24242E22, 2.397979E23, 5.297979E52,
        5.342146E53, 5.4647568E54, 1.11535647E11, 1.134657811E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3 (col_int, col_i64, col_u64, col_float, col_float4,
        col_float21, col_float22, col_float23, col_float52,
        col_float53, col_float54, col_real, col_doublep)
        values (2542334, -25452990, 22214242, 1.425356438E18, 2.4353644E14,
        2.443536E21, 2.03435E22, 2.341245362E23, 2.34253365E52,
        2.342546E53, 2.5634664E54, 2.646464622E11, 2.6464646622E54);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into i3
        (col_int, col_i64, col_u64, col_float,
        col_float4, col_float21,
        col_float22, col_float23,
        col_float52, col_float53,
        col_float54, col_real,
        col_doublep)
        values (497483647, 9.223E18, 0, 1.7272337e-76,
        1.1579208e76, -1.7272337e-76,
        -1.1579208e76, 1.15792089237316192e76,
        -1.1579208e76, 1.15792089237316192e76,
        1.15792089237316192e76, 1.7272337e-36,
        1.15792089237316192e76);"""
    output = _dci.cmdexec(stmt)

    stmt = """update i3 set col_float4  = -2.2250738585072014e-38,
        col_float21 = +1.7976931348623157e+38,
        col_float22 = -1.7976931348623157e+38,
        col_float23 = col_float23 + 2.225e-25,
        col_float53 = col_float53 + 2.225e-25
        where col_int < 5000;"""
    output = _dci.cmdexec(stmt)

    stmt = """update i3 set col_float23 = col_float23 * 1.0E+10,
        col_float53 = -1.7976931348623157e+38
        where col_int > 5000;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t5 values
        (1200289208, 1804250150, 3.577544e+012, '9qFmN'),
        (-1911855747, 939828307, 5.929045e+002, 'Z'),
        (361850430, 849361400, -8.209677e+019, 'u5ty4'),
        (622295003, 1809285824, 5.466672e+010, 'sw9Gg7'),
        (-1010337628, 1793029755, -9.981081e-023, 'n8qCj'),
        (241038239, -1897716755, 4.116314e+012, 'R'),
        (-1983773754, -950358290, 7.189010e-004, 'rvnYL'),
        (1726516212, -1122559750, 1.916176e-022, 'HIfj5ryIx'),
        (-745697006, 126711616, -8.819797e-020, 'PIlgna'),
        (2139835519, 1190125178, -1.507628e+013, 'AuVQL7x'),
        (291578890, -1954054944, 7.899256e-015, 'VavpP'),
        (1992656686, -495590500, 2.172544e-021, 'npZTe'),
        (1575271103, -397059813, 1.047654e-016, 'knFZKd'),
        (195124611, -501871502, 6.864592e+002, 'xoa'),
        (-1043895252, 1600974264, 8.462322e-018, 'ymJWeol'),
        (832709954, -816511212, 2.558570e+003, 'S1m8WhF9L'),
        (6993682, -842968251, 1.778113e-008, 'f8'),
        (-142040708, 1560314214, 2.807962e-020, 'D'),
        (-226326844, -805103577, 2.256136e+016, 'TJD10Kg'),
        (1807092559, 1373382000, -2.355337e+033, 's'),
        (-1571964760, 1740931602, -1.228042e+019, 'zwGjOl0'),
        (-2089855768, -221767552, -1.249224e+000, 'HfU23XU'),
        (1327776690, 1906626496, -1.504891e-004, '7CqhA'),
        (2029721678, -344996720, -1.229514e+033, 'bm9uop9s'),
        (708241173, -1662903369, -6.745526e-025, 'p6bgtop9'),
        (1853408622, 205018176, 4.848209e-017, '4s8Yoiu8R'),
        (1221529789, 351853084, -6.981630e-009, '5W3TCLpA'),
        (409083439, 243096214, -1.229993e+003, '3hE'),
        (958883394, -1780247728, 1.047528e-012, 'c6vjIq'),
        (667848502, -1485463700, 1.023636e-017, '2X3hzBczWz'),
        (-955199663, 206282436, -6.088428e+001, 'plqHITCjb'),
        (587219818, -1668413769, -2.125712e+000, '2h'),
        (-137768277, -1400545968, -4.998511e-009, '3bMa'),
        (501674582, -789448672, 3.243788e-013, 'Y'),
        (-2023810818, -431342789, 2.627385e+004, 'd'),
        (-1839560568, 1876169344, 5.157241e-031, '8zXoERoKZs'),
        (661775336, 1609811880, 2.149462e-001, 'RPdFFyK'),
        (701753639, 1467402658, 2.236046e+024, '1eiQ'),
        (-415165300, 634223298, -3.306182e+024, 'f8'),
        (-468089742, -2115140520, 3.100463e+004, 'Kpy'),
        (-1417565243, -1146722963, 3.353102e+011, '6OC'),
        (1268930815, -954873888, -2.309555e-015, '05WyLe'),
        (1410221262, -1873223192, 8.970686e-026, 'kBva'),
        (1031205383, 221636546, 3.841985e-004, 'iNT3oAxG'),
        (-35953274, 636905923, -9.721963e-023, 'p0'),
        (1645544448, 1025777625, 2.626179e-021, 'VkJE3WUZqg'),
        (-1898614319, -1023859529, -5.450540e+016, '2ax8X5'),
        (1928106228, 1898859449, -1.701739e+036, 'QXK'),
        (153066773, 1545085040, -4.653476e-026, 'g2Vp5PlJFL'),
        (-1036698765, 1388701250, -4.083894e-002, 'UIo090'),
        (-931773702, -23979552, 2.074003e-010, 'mE'),
        (-520845823, 475972278, -5.577474e+015, 'ZLHIe'),
        (-257478739, -405965242, 1.686734e-024, 'zW'),
        (-2104212424, -1761238280, -3.298090e+011, 'NF1li'),
        (-1056841069, 10127099, -4.529744e+008, 'Fllx'),
        (175973376, -285825316, 3.095372e+002, 'iAvmOumi'),
        (-1560706424, 1652550351, 7.434311e+003, 'O'),
        (2057764132, -23343277, 6.151614e-020, 'r'),
        (607916450, -1696021298, -3.707527e+004, 'ikySHE'),
        (204016776, 1991729212, 1.495400e+020, '44fgtOJ'),
        (1510350122, 1237533460, 1.000000e+000, 'LCSOnhiVDd'),
        (-38927809, 346814455, 1.888189e+025, 'jnle'),
        (1867583576, 1343822646, 1.922659e-014, 'E28LF'),
        (-1535605652, -1406353152, -5.828762e-034, 'N85P'),
        (-1210628959, 708490705, 2.337352e-009, 'naLXt'),
        (-1977701482, 2104744432, -1.495403e+021, 'TcUA8NMs'),
        (1391763040, 2093369539, -4.240750e+000, 'lnDNumwHW'),
        (-1234998817, -925550850, -1.272573e+017, '2'),
        (274436767, -887186414, -2.980383e-029, 'q8Pg'),
        (-2097027665, 1040058680, -2.757528e-016, 'TMwPcIxn'),
        (180568953, 1224462743, -3.597074e-005, 'ZcinJ'),
        (623419086, 245111833, 2.630397e+023, 'gdw'),
        (666717195, -397598270, 3.082784e-009, 'oQo'),
        (-1714699108, 1385174274, 6.597338e-006, 'QqS'),
        (1172846774, -1659655408, 5.402130e-022, 'rDz2NIIf'),
        (1333294662, -1621989292, -1.529935e+018, 'JdKD'),
        (-1018094204, 55137788, 8.440631e+025, 'uF'),
        (-1983432821, 1293594125, -4.433939e+011, '3jgHww'),
        (-1725014766, 720701160, 4.895897e-010, 'xrTSu2Y'),
        (-1853587649, -594035557, 1.076355e+017, 'X'),
        (968843295, 2095407134, -2.335086e-013, 'g1Wer'),
        (-1814119938, 377822296, -2.305646e-002, '1Po'),
        (-388231281, -1384768256, -6.852956e-009, 'slf'),
        (564951101, -1244758352, 8.224429e+015, 'qmO'),
        (143671331, -506148286, 3.791914e-013, 'DGo1wBME'),
        (1355256467, 1878677756, 8.722664e+003, 'cGOC'),
        (1798993136, -1832898030, 2.216786e-024, 'rkX'),
        (-1323493032, 730057007, 8.874381e-006, 'bGL3aoGj4g'),
        (1361685983, 632502080, -6.564823e+010, 'SCrttaz'),
        (588722667, -630442768, 1.345984e-007, 'xOx9rMnW4'),
        (2147222397, -1835179868, 1.337830e+007, 'eSvpfJ7Gg'),
        (921435927, 571747820, 1.666798e+012, 'G5qiDzao'),
        (-1397072436, -1693349964, 2.400936e+008, 'sya4RvEbmU'),
        (-1055701153, 1539275856, 3.405883e-011, 'Q'),
        (-719860005, 694508460, -4.351530e+016, 'Or'),
        (-1901171029, -541671824, -1.119526e+019, 't26n4p'),
        (1257126293, 89582435, -4.442185e+017, 'uif2'),
        (-1787188255, -1505084306, 5.552568e+022, 'oNB6e8m4'),
        (222444817, 1162620763, 1.005365e-012, 'v2'),
        (617094567, 1570143908, -4.346830e-018, 'gYFC0z')
        ;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('kUYm', 190641683, INTERVAL '4-7' YEAR(2) TO MONTH, INTERVAL '30:39' HOUR(2) TO MINUTE,
        1102836828, -1321787539);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('6ecDPehyZ', -400538679, INTERVAL '2-10' YEAR(2) TO MONTH, INTERVAL '1:53' HOUR(2) TO MINUTE,
        523007018, 1839056054);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('M', 517384848, INTERVAL '39-7' YEAR(2) TO MONTH, INTERVAL '8:16' HOUR(2) TO MINUTE,
        -880576225, -1067122833);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('L9jNuCbd', -763657792, INTERVAL '3-10' YEAR(2) TO MONTH, INTERVAL '6:55' HOUR(2) TO MINUTE,
        NULL, -1097124470);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('N', -423147649, INTERVAL '79-1' YEAR(2) TO MONTH, INTERVAL '28:37' HOUR(2) TO MINUTE,
        NULL, -2089622456);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('mdJRBg7oqH', 511432662, NULL, INTERVAL '8:17' HOUR(2) TO MINUTE, 1895714486, -1526181985
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('2nWNrIU', 059108505, INTERVAL '6-8' YEAR(2) TO MONTH, INTERVAL '8:05' HOUR(2) TO MINUTE,
        -234038213, 924008536);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('qRsuc', 659109838, INTERVAL '6-6' YEAR(2) TO MONTH, INTERVAL '16:28' HOUR(2) TO MINUTE,
        1616353683, 1814891532);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('ZKt6RWk6', 482020214, INTERVAL '51-6' YEAR(2) TO MONTH, INTERVAL '7:29' HOUR(2) TO MINUTE,
        28780996, -768068570);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('lX', NULL, INTERVAL '0-1' YEAR(2) TO MONTH, INTERVAL '2:33' HOUR(2) TO MINUTE,
        1519220102, -672654581);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('g', -514417202, NULL, INTERVAL '7:29' HOUR(2) TO MINUTE, 1669375894, 1977594200
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('I0CJ9Hh', 261685905, INTERVAL '7-0' YEAR(2) TO MONTH, INTERVAL '3:36' HOUR(2) TO MINUTE,
        -1656199612, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('DJ', 523712420, INTERVAL '23-7' YEAR(2) TO MONTH, INTERVAL '1:52' HOUR(2) TO MINUTE,
        1737977310, 1409999233);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('c5', -865749274, NULL, NULL, -1378078324, 759093722);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('Is', NULL, INTERVAL '11-5' YEAR(2) TO MONTH, INTERVAL '12:30' HOUR(2) TO MINUTE,
        NULL, -1688063259);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('d5Aq', -873368690, INTERVAL '00-5' YEAR(2) TO MONTH, INTERVAL '15:09' HOUR(2) TO MINUTE,
        -336463627, 594344536);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('aVI', -601358542, INTERVAL '8-5' YEAR(2) TO MONTH, INTERVAL '49:16' HOUR(2) TO MINUTE,
        -1040890366, 812541308);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('0ALiU', 674836291, INTERVAL '12-5' YEAR(2) TO MONTH, INTERVAL '3:03' HOUR(2) TO MINUTE,
        340405290, 1915984113);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('OymG', -397006801, INTERVAL '1-6' YEAR(2) TO MONTH, INTERVAL '32:58' HOUR(2) TO MINUTE,
        -1671177392, -2046946591);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('h4Q', -914168945, INTERVAL '3-6' YEAR(2) TO MONTH, INTERVAL '37:02' HOUR(2) TO MINUTE,
        775714580, 1826559375);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('sa4', -420100046, INTERVAL '9-2' YEAR(2) TO MONTH, INTERVAL '0:47' HOUR(2) TO MINUTE,
        -1626742353, 896651251);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('nsThilfh', -687293553, INTERVAL '7-0' YEAR(2) TO MONTH, INTERVAL '2:46' HOUR(2) TO MINUTE,
        1693692177, 433672345);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('Mw', 586486998, INTERVAL '40-8' YEAR(2) TO MONTH, INTERVAL '19:36' HOUR(2) TO MINUTE,
        155732715, -2018799930);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('LhY', 921538717, INTERVAL '22-11' YEAR(2) TO MONTH, NULL, NULL, -1332918087);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('RnAvp', -485881792, INTERVAL '8-5' YEAR(2) TO MONTH, INTERVAL '7:41' HOUR(2) TO MINUTE,
        -2065720469, -1337812683);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('X', -947110709, INTERVAL '77-2' YEAR(2) TO MONTH, INTERVAL '69:09' HOUR(2) TO MINUTE,
        -22369726, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('05kXmoq8DD', 185516326, INTERVAL '68-8' YEAR(2) TO MONTH, INTERVAL '33:49' HOUR(2) TO MINUTE,
        -913863534, 1167615774);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('tgv', -039480304, INTERVAL '3-8' YEAR(2) TO MONTH, INTERVAL '83:31' HOUR(2) TO MINUTE,
        356498597, -542893629);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('JH', 100423051, INTERVAL '30-5' YEAR(2) TO MONTH, INTERVAL '53:06' HOUR(2) TO MINUTE,
        NULL, 1402278323);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('Hxr8FwZW', -688882867, INTERVAL '42-7' YEAR(2) TO MONTH, INTERVAL '4:20' HOUR(2) TO MINUTE,
        560190040, 1278974370);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('a', 729915143, INTERVAL '5-8' YEAR(2) TO MONTH, INTERVAL '34:04' HOUR(2) TO MINUTE,
        421930502, 838328837);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('8GhGJ9TCv5', -678983277, INTERVAL '72-11' YEAR(2) TO MONTH, INTERVAL '4:38' HOUR(2) TO MINUTE,
        -883077926, -493846129);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('IaPUlH', 008077055, INTERVAL '72-10' YEAR(2) TO MONTH, INTERVAL '31:29' HOUR(2) TO MINUTE,
        1239127268, -1565381242);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('JRtZf', NULL, INTERVAL '9-11' YEAR(2) TO MONTH, INTERVAL '9:00' HOUR(2) TO MINUTE,
        -1557695961, 1576779957);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('K', 736935374, INTERVAL '63-11' YEAR(2) TO MONTH, INTERVAL '39:47' HOUR(2) TO MINUTE,
        728113442, -707193359);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('f2', 582401261, INTERVAL '53-9' YEAR(2) TO MONTH, NULL, 1751262538, 150240070);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('zwzHLQ', -895746679, INTERVAL '0-1' YEAR(2) TO MONTH, INTERVAL '29:37' HOUR(2) TO MINUTE,
        1192851505, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('MXQRX', 407091199, INTERVAL '5-0' YEAR(2) TO MONTH, NULL, -903153601, -2081311267
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('i', NULL, NULL, INTERVAL '92:10' HOUR(2) TO MINUTE, NULL, -86095575);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('qpBC6UF', 965330016, INTERVAL '1-0' YEAR(2) TO MONTH, INTERVAL '21:11' HOUR(2) TO MINUTE,
        538506558, 1065837614);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('VXfRPav', 010271282, INTERVAL '2-11' YEAR(2) TO MONTH, INTERVAL '03:39' HOUR(2) TO MINUTE,
        -1840336698, 1717062902);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('wktf7X', 961818966, INTERVAL '03-1' YEAR(2) TO MONTH, NULL, -1136596928, 195301141
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('kbAPNjW', -318042473, INTERVAL '2-2' YEAR(2) TO MONTH, INTERVAL '8:26' HOUR(2) TO MINUTE,
        385104124, 841150218);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('gXemak', -537153234, INTERVAL '4-0' YEAR(2) TO MONTH, INTERVAL '0:17' HOUR(2) TO MINUTE,
        NULL, 419267315);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('3Th1EHIohs', -681310354, INTERVAL '4-11' YEAR(2) TO MONTH, INTERVAL '4:23' HOUR(2) TO MINUTE,
        -609534270, -1782785802);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('sYM9', 877996832, INTERVAL '8-2' YEAR(2) TO MONTH, INTERVAL '93:07' HOUR(2) TO MINUTE,
        NULL, -622372758);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('fbQJkVnI', 909299882, INTERVAL '1-0' YEAR(2) TO MONTH, INTERVAL '75:20' HOUR(2) TO MINUTE,
        -104171422, -1589547632);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('mnmh', NULL, INTERVAL '7-5' YEAR(2) TO MONTH, NULL, NULL, -1298841906);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('tDSt8', 321316591, INTERVAL '26-6' YEAR(2) TO MONTH, INTERVAL '5:27' HOUR(2) TO MINUTE,
        1939455651, -1310890007);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('CPowoZmy', 764932122, INTERVAL '64-7' YEAR(2) TO MONTH, INTERVAL '3:46' HOUR(2) TO MINUTE,
        -1163952662, -1833943181);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('nTuCrBFqr', 267948753, INTERVAL '1-11' YEAR(2) TO MONTH, INTERVAL '7:09' HOUR(2) TO MINUTE,
        -382486062, -189750188);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('XMLlhCvOH', 141852530, INTERVAL '55-2' YEAR(2) TO MONTH, INTERVAL '2:05' HOUR(2) TO MINUTE,
        -1783313451, -1790685319);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('2hcjdx94KE', -118633235, NULL, INTERVAL '80:04' HOUR(2) TO MINUTE, NULL, 1466027262
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('tWXk', 486388637, INTERVAL '90-10' YEAR(2) TO MONTH, INTERVAL '6:49' HOUR(2) TO MINUTE,
        -231809823, 1217727421);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('91UUyBFJ60', NULL, INTERVAL '8-11' YEAR(2) TO MONTH, INTERVAL '00:08' HOUR(2) TO MINUTE,
        -905987092, -749828052);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('8MdUUik3', -474607918, NULL, NULL, 1580128705, 377303096);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('b7mB8SL3z', -904467129, INTERVAL '39-6' YEAR(2) TO MONTH, INTERVAL '4:33' HOUR(2) TO MINUTE,
        1068138640, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('7UJs3', -986023539, INTERVAL '7-2' YEAR(2) TO MONTH, INTERVAL '34:39' HOUR(2) TO MINUTE,
        -1417809823, 582210947);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('nv0Z', -023445040, INTERVAL '0-6' YEAR(2) TO MONTH, INTERVAL '0:14' HOUR(2) TO MINUTE,
        -1210852665, 1903417890);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('uwI', NULL, INTERVAL '1-11' YEAR(2) TO MONTH, INTERVAL '19:27' HOUR(2) TO MINUTE,
        -496304558, -1375495560);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('zRZqOxbpDI', -994957909, INTERVAL '1-4' YEAR(2) TO MONTH, NULL, 1993609602, -16347340
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('r', -515198180, INTERVAL '86-8' YEAR(2) TO MONTH, INTERVAL '6:59' HOUR(2) TO MINUTE,
        1906249784, 1370862714);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('OK4CS0', -746787627, INTERVAL '3-11' YEAR(2) TO MONTH, INTERVAL '87:07' HOUR(2) TO MINUTE,
        -908653605, -1788738440);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('9I', -170808286, INTERVAL '16-3' YEAR(2) TO MONTH, INTERVAL '93:34' HOUR(2) TO MINUTE,
        -146230965, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('TpXoZiY', -184527579, INTERVAL '68-0' YEAR(2) TO MONTH, NULL, 374389410, -210742281
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('A46mglyQil', 132062444, INTERVAL '5-11' YEAR(2) TO MONTH, INTERVAL '28:59' HOUR(2) TO MINUTE,
        -435235301, -1831036621);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('Rafx', -159211959, INTERVAL '16-4' YEAR(2) TO MONTH, INTERVAL '62:56' HOUR(2) TO MINUTE,
        19933837, 18415714);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('WH', 182998842, INTERVAL '80-4' YEAR(2) TO MONTH, INTERVAL '59:02' HOUR(2) TO MINUTE,
        -1819898745, -234287023);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('3', 152247628, INTERVAL '73-2' YEAR(2) TO MONTH, INTERVAL '77:18' HOUR(2) TO MINUTE,
        NULL, -572280271);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('NY', NULL, INTERVAL '7-0' YEAR(2) TO MONTH, INTERVAL '7:10' HOUR(2) TO MINUTE,
        NULL, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('ris', -882664033, INTERVAL '8-4' YEAR(2) TO MONTH, INTERVAL '09:08' HOUR(2) TO MINUTE,
        -144343981, -731679498);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('m1e', 103942166, INTERVAL '6-6' YEAR(2) TO MONTH, INTERVAL '4:25' HOUR(2) TO MINUTE,
        365159561, 986671880);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('L', 179227883, INTERVAL '02-9' YEAR(2) TO MONTH, INTERVAL '7:07' HOUR(2) TO MINUTE,
        1703787809, 195288234);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('ST3m', 470035440, INTERVAL '3-10' YEAR(2) TO MONTH, INTERVAL '9:50' HOUR(2) TO MINUTE,
        NULL, -2085010186);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('LBMNP0', 962225668, INTERVAL '93-7' YEAR(2) TO MONTH, INTERVAL '5:16' HOUR(2) TO MINUTE,
        35794862, -27937023);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('6mAwFUPwVy', 865414392, NULL, INTERVAL '06:53' HOUR(2) TO MINUTE, -1015125607,
        700324736);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('dJKl', NULL, INTERVAL '52-0' YEAR(2) TO MONTH, INTERVAL '18:54' HOUR(2) TO MINUTE,
        1617742622, -1748715929);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('i', 067351752, INTERVAL '5-0' YEAR(2) TO MONTH, INTERVAL '05:05' HOUR(2) TO MINUTE,
        -2137771885, -61936232);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('GUOghJ7', -457828745, INTERVAL '6-8' YEAR(2) TO MONTH, INTERVAL '77:23' HOUR(2) TO MINUTE,
        1828780676, 1671839194);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('xn', 973798789, INTERVAL '8-9' YEAR(2) TO MONTH, INTERVAL '6:51' HOUR(2) TO MINUTE,
        1831456315, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('8y2vp', 580890948, INTERVAL '70-2' YEAR(2) TO MONTH, INTERVAL '42:43' HOUR(2) TO MINUTE,
        117949372, -485438150);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('k62c3PzK', 262242555, INTERVAL '0-8' YEAR(2) TO MONTH, INTERVAL '79:58' HOUR(2) TO MINUTE,
        -356536617, -1997813929);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('o', NULL, INTERVAL '5-1' YEAR(2) TO MONTH, INTERVAL '40:55' HOUR(2) TO MINUTE,
        1419095396, 941462286);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('OSf', 906253576, INTERVAL '41-2' YEAR(2) TO MONTH, INTERVAL '23:25' HOUR(2) TO MINUTE,
        46588798, 837806688);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('Hd', 026572115, INTERVAL '0-10' YEAR(2) TO MONTH, INTERVAL '9:22' HOUR(2) TO MINUTE,
        1208708207, -1996947849);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('xYhg1W4GH', 620398029, INTERVAL '3-11' YEAR(2) TO MONTH, INTERVAL '29:39' HOUR(2) TO MINUTE,
        NULL, 2051423052);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('b13duY5B', -886422759, INTERVAL '2-10' YEAR(2) TO MONTH, INTERVAL '33:25' HOUR(2) TO MINUTE,
        928964245, 1699881177);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('O4CWr', 608573062, INTERVAL '76-4' YEAR(2) TO MONTH, INTERVAL '01:57' HOUR(2) TO MINUTE,
        -982559744, 391642015);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('eagn1', 113226870, INTERVAL '8-1' YEAR(2) TO MONTH, INTERVAL '53:29' HOUR(2) TO MINUTE,
        1452525, -597395713);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('EYEjq9', 328493934, INTERVAL '4-7' YEAR(2) TO MONTH, INTERVAL '69:54' HOUR(2) TO MINUTE,
        542045502, 1523823444);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('Vk3Q', -279571390, INTERVAL '76-5' YEAR(2) TO MONTH, INTERVAL '2:01' HOUR(2) TO MINUTE,
        NULL, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('iENyDO2967', 814085496, INTERVAL '3-1' YEAR(2) TO MONTH, INTERVAL '8:24' HOUR(2) TO MINUTE,
        -1007424115, 1802309145);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('pOOpALsLw5', NULL, INTERVAL '53-8' YEAR(2) TO MONTH, INTERVAL '6:46' HOUR(2) TO MINUTE,
        NULL, -909691150);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('5m8sx', 398902902, INTERVAL '16-3' YEAR(2) TO MONTH, INTERVAL '57:37' HOUR(2) TO MINUTE,
        NULL, -1312403887);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('tFv21OiwY', -940724783, INTERVAL '49-11' YEAR(2) TO MONTH, INTERVAL '05:02' HOUR(2) TO MINUTE,
        -129840282, -347526131);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('4DVSwXO', NULL, INTERVAL '11-1' YEAR(2) TO MONTH, INTERVAL '79:30' HOUR(2) TO MINUTE,
        1895539793, 513082050);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('X', -182410246, NULL, INTERVAL '12:58' HOUR(2) TO MINUTE, -192330393, -747614603
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('z5hAF6ftk', -592454430, INTERVAL '99-11' YEAR(2) TO MONTH, INTERVAL '28:01' HOUR(2) TO MINUTE,
        838326383, 954363767);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('UXhpE', 717832594, INTERVAL '3-1' YEAR(2) TO MONTH, INTERVAL '86:03' HOUR(2) TO MINUTE,
        -768869517, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t6
        values
        ('VUE', -277691255, NULL, INTERVAL '93:04' HOUR(2) TO MINUTE, 316146035, 1604030147
        )
        ;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t1 values(13232323,3434535),(41242424,25364675),(8684633,53536476),(3536372,523478),(89769463,647858);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t2 values('Radha','Rajani','Ramya'),('Sumathy','Sindhu','Sneha'),('Manasa','Manjula','Meghana');"""
    output = _dci.cmdexec(stmt)

    stmt = """create  table jdbctest (charcol char(10) default null, vcharcol varchar(10), decimalcol decimal(15,5),
        numericcol numeric(15,5), smallcol smallint, integercol int,realcol real,
        floatcol float, doublecol double precision, lvcol varchar(10), bitcol smallint not null,tinyintcol smallint,
        bigintcol largeint,bincol char(10),varbincol varchar(10),Lvarbincol varchar(10),
        datecol date,timecol time,tscol timestamp) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create  table jdbc_null_test (id char(30), charcol char(10) default null, vcharcol varchar(10), decimalcol decimal(15,5),
        numericcol numeric(15,5), smallcol char(10), integercol int,realcol real,
        floatcol float, doublecol double precision, bitcol char(10), tinyintcol char(10),
        bigintcol bigint,bincol char(10),varbincol varchar(10),
        datecol date,timecol time,tscol timestamp) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create  table gtest (charcol char(10) default null) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """create  table jdbcnull (id char(30), charcol char(10) default null, vcharcol varchar(10) default null, decimalcol decimal(15,5) default null,
        numericcol numeric(15,5) default null, smallcol smallint default null, integercol int default null, realcol real default null,
        floatcol float default null, doublecol double precision, bitcol smallint default null, tinyintcol smallint default null,
        bigintcol largeint default null, bincol char(10) default null, varbincol varchar(10) default null,
        datecol date default null, timecol time default null, tscol timestamp default null) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into jdbctest (charcol, vcharcol,decimalcol,numericcol,smallcol,integercol, realcol, floatcol,
        doublecol, lvcol, bitcol, tinyintcol,bigintcol, bincol, varbincol, Lvarbincol, datecol,timecol,tscol)
        values ('bc        ', 'bc', -2345.78900, -2345.78900, -2, 1, .34759, 3.14159, 3.14159,
        'bc', 1, 1, 1,  'bc', 'bc', 'bc', {d '1981-02-02'}, {t '01:01:01'}, {ts '1981-02-02 01:01:01'});"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into jdbctest (charcol, vcharcol,decimalcol,numericcol,smallcol,integercol, realcol, floatcol,
        doublecol, lvcol, bitcol, tinyintcol,bigintcol, bincol, varbincol, Lvarbincol, datecol,timecol,tscol)
        values ('cde       ', 'cde', 234567.90100, 234567.90100, 4, 2, 1.39036, 6.28318, 6.28318,
        'cde', 0, 2, 2,'cde', 'cde', 'cde', {d '1982-03-03'}, {t '02:02:02'},{ts '1982-03-03 02:02:02'});"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into jdbctest (charcol, vcharcol,decimalcol,numericcol,smallcol,integercol, realcol, floatcol,
        doublecol, lvcol, bitcol, tinyintcol,bigintcol, bincol, varbincol, Lvarbincol, datecol,timecol,tscol)
        values ('defg      ', 'defg', 3456789.12000, 3456789.12000, -6, 3, 3.12832, 9.42477, 9.42477,
        'defg', 0, 3, 3, 'defg', 'defg', 'defg', {d '1983-04-04'}, {t '03:03:03'}, {ts '1983-04-04 03:03:03'});"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into jdbctest (charcol, vcharcol,decimalcol,numericcol,smallcol,integercol, realcol, floatcol,
        doublecol, lvcol, bitcol, tinyintcol,bigintcol, bincol, varbincol, Lvarbincol, datecol,timecol,tscol)
        values ('efghi     ', 'efghi', -567.90123, -567.90123, 8, 4, 5.56146, 12.56636, 12.56636,
        'efghi', 0, 4, 4, 'efghi', 'efghi', 'efghi',{d '1984-05-05'}, {t '04:04:04'}, {ts '1984-05-05 04:04:04'});"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into jdbctest (charcol, vcharcol,decimalcol,numericcol,smallcol,integercol, realcol, floatcol,
        doublecol, lvcol, bitcol, tinyintcol,bigintcol, bincol, varbincol, Lvarbincol, datecol,timecol,tscol)
        values (null, 'fghijk', 56789.12340, 56789.12340, -10, 5, 8.68978, 15.70795, 15.70795,
        'fghijk', 0, 5, 5, 'fghijk', 'fghijk', 'fghijk',{d '1985-06-06'}, {t '05:05:05'}  ,{ts '1985-06-06 05:05:05'});"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into jdbctest (charcol, vcharcol,decimalcol,numericcol, smallcol,  integercol, realcol, floatcol,
        doublecol, lvcol, bitcol, tinyintcol,bigintcol, bincol, varbincol, Lvarbincol, datecol,timecol,tscol)
        values ('bc        ', 'bc', -2345.78900, -2345.78900, -20, 6, .34759, 3.14159, 3.14159,
        'bc', 0, 0, 1,  'bc', 'bc', 'bc', {d '1981-02-02'}, {t '01:01:01'},{ts '1981-02-02 01:01:01'});"""
    output = _dci.cmdexec(stmt)

    stmt = """create view trnv as select * from trn;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table b2pns03
        (
        sbin0_4             Integer             default 3 not null,
        time0_uniq          Time                          not null,
        varchar0_uniq       VarChar(8)         no default not null,
        sdec0_n1000         Decimal(9)                    no default,
        int0_dTOf6_4        Interval day to second(6)     not null,
        ts1_n100            Timestamp     heading 'ts1_n100 allowing nulls',
        ubin1_20            Numeric(9) unsigned  no default not null,
        int1_yTOm_n100      Interval year(1) to month     no default,
        double1_2           Double Precision              not null,
        udec1_nuniq         Decimal(4) unsigned           ,
        primary key ( time0_uniq  DESC)
        )
        store by primary key;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table btuns01
        (
        char0_20            Character(8)          not null,
        sbin0_2             Numeric(18) signed    not null,
        udec0_10            Decimal(9) unsigned   not null,
        varchar0_2          varchar(16)      not null,
        sdec0_1000          PIC S9(9)             not null,
        ubin0_20            PIC 9(7)V9(2) COMP    not null,
        char1_2             Character(16)         not null,
        sdec1_uniq          Decimal(18) signed    not null,
        sbin1_100           Numeric(4) signed     not null,
        varchar1_uniq       varchar(8)       not null
        ) no partitions;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table b2unl15
        (
        char0_100           Character(8)          not null,
        sbin0_uniq          Integer               not null,
        sdec0_n10           Decimal(4)           default 9,
        int0_yTOm_n1000     Interval year(2) to month    no default,
        date0_nuniq         Date                         no default,
        real1_uniq          Real                  not null,
        ts1_n100            Timestamp                     ,
        ubin1_500           Numeric(4) unsigned      no default not null,
        int1_dTOf6_nuniq    Interval day to second(6)       no default,
        udec1_50p           Decimal(9) unsigned   not null,
        primary key ( real1_uniq ) not droppable
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table b2uwl02
        (
        char0_n10           Character(2)
        default 'AD' heading 'char0_n10 with default AD',
        sbin0_uniq          Smallint                   not null,
        sdec0_n500          Decimal(18)                        ,
        date0_uniq          Date                 no default not null,
        int0_yTOm_nuniq     Interval year(5) to month    no default,
        int1_hTOs_1000      Interval hour(2) to second(0)   not null,
        date1_n4            Date                               ,
        real1_uniq          Real                    no default not null,
        ubin1_n2            Numeric(4) unsigned        no default,
        udec1_100           Decimal(2) unsigned        not null,
        char2_2             Character(2)               not null,
        sbin2_nuniq         Largeint                           ,
        sdec2_500           Decimal(9) signed       no default not null,
        date2_uniq          Date                       not null,
        int2_dTOf6_n2       Interval day to second(6)      no default,
        real2_500           Real                       not null,
        real3_n1000         Real                               ,
        int3_yTOm_4         Interval year(1) to month no default not null,
        date3_n2000         Date                            no default,
        udec3_n100          Decimal(9) unsigned                ,
        ubin3_n2000         Numeric(4) unsigned                ,
        char3_4             Character(8)             no default not null,
        sdec4_n20           Decimal(4)                  no default,
        int4_yTOm_uniq      Interval year(5) to month   not null,
        sbin4_n1000         Smallint                           ,
        time4_1000          Time                   no default not null,
        char4_n10           Character(8)               no default,
        real4_2000          Real                       not null,
        char5_n20           Character(8)                       ,
        sdec5_10            Decimal(9) signed       no default not null,
        ubin5_n500          Numeric(9) unsigned       no default,
        real5_uniq          Real                       not null,
        dt5_yTOmin_n500     Timestamp(0)            ,
        int5_hTOs_500       Interval hour to second(0) no default not null,
        int6_dTOf6_nuniq    Interval day to second(6)     no default,
        sbin6_nuniq         Largeint                      no default,
        double6_n2          Float(23)                          ,
        sdec6_4             Decimal(4) signed       no default not null,
        char6_n100          Character(8)               no default,
        date6_100           Date                       not null,
        time7_uniq          Time                       not null,
        sbin7_n20           Smallint                      no default,
        char7_500           Character(8)            no default not null,
        int7_hTOs_nuniq     Interval hour(2) to second(0)        ,
        udec7_n10           Decimal(4) unsigned                ,
        real7_n4            Real                               ,
        ubin8_10            Numeric(4) unsigned        not null,
        int8_y_n1000        Interval year(3)                   ,
        date8_10            Date                    no default not null,
        char8_n1000         Character(8)               no default,
        double8_n10         Double Precision           no default,
        sdec8_4             Decimal(9) unsigned        not null,
        sdec9_uniq          Decimal(18) signed       no default not null,
        real9_n20           Real                               ,
        time9_n4            Time                               ,
        char9_100           Character(2)             no default not null,
        int9_dTOf6_2000     Interval day to second(6)   no default not null,
        ubin9_n4            Numeric(9) unsigned         no default,
        ubin10_n2           Numeric(4) unsigned         no default,
        char10_nuniq        Character(8)                       ,
        int10_d_uniq        Interval day(6)            not null,
        ts10_n2             Timestamp                          ,
        real10_100          Real                       not null,
        udec10_uniq         Decimal(9) unsigned     no default not null,
        udec11_2000         Decimal(9) unsigned   no default not null,
        int11_h_n10         Interval hour(1)           no default,
        sbin11_100          Integer                    not null,
        time11_20           Time                       not null,
        char11_uniq         Character(8)               not null,
        double11_n100       Double Precision                   ,
        real12_n20          Real                               ,
        ubin12_2            Numeric(4) unsigned     no default not null,
        dt12_mTOh_1000      Timestamp(0)        no default not null,
        sdec12_n1000        Decimal(18) signed           no default,
        char12_n2000        Character(8)                no default,
        int12_yTOm_100      Interval year to month     not null,
        int13_yTOm_n1000    Interval year to month             ,
        udec13_500          Decimal(9) unsigned     no default not null,
        sbin13_n100         PIC S9(9)V9 COMP           no default,
        ts13_uniq           Timestamp                  not null,
        char13_1000         Character(8)               not null,
        real13_n1000        Real                               ,
        sbin14_1000         Integer                no default not null,
        double14_nuniq      Float(23)                 no default,
        udec14_100          Decimal(4) unsigned        not null,
        char14_n500         Character(8)                       ,
        int14_d_500         Interval day(3)         no default not null,
        ts14_n100           Timestamp               no default,
        dt15_mTOh_n100      Timestamp(0)                 no default,
        double15_uniq       Double Precision           not null,
        sbinneg15_nuniq     Largeint                           ,
        sdecneg15_100       Decimal(9) signed       no default not null,
        int15_dTOf6_n100    Interval day to second(6)     no default,
        char15_100          Character(8)               not null,
        dt16_m_n10          date                     ,
        int16_h_20          Interval hour           no default not null,
        ubin16_n10          Numeric(4) unsigned        no default,
        sdec16_uniq         Decimal(18) signed         not null,
        char16_n20          Character(5)        ,   -- len = 2,4
        real16_10           Real                  no default not null,
        int17_y_n10         Interval year(1)         no default,
        dt17_yTOmin_uniq    Timestamp(0)    not null,
        real17_n100         Real                               ,
        sbin17_uniq         Largeint  no default not null,  -- range: 0-149999
        sdec17_nuniq        Decimal(18)                no default,
        char17_2            Character(8)               not null
        )
        store by ( sbin0_uniq ) ;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table b2pwl06
        (
        date0_n10           Date
        default date '2100-01-09' heading 'date0_n10 with default 01/09/2100',
        int0_dTOf6_uniq     Interval day to second(6)    no default not null,
        char0_n2            Character(8)                           no default,
        sbin0_10            Largeint                   not null,
        sdec0_nuniq         Decimal(4)                         ,
        ubin1_10            Numeric(4) unsigned           no default not null,
        udec1_nuniq         Decimal(9) unsigned                    no default,
        int1_d_100          Interval day               not null,
        dt1_m_n10           Date                     ,
        real1_500           Real                          no default not null,
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
        int7_hTOs_nuniq     Interval hour(2) to second(0)         ,
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
        dt16_m_n10          Date                     ,
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
        char17_2            Character(8)               not null,
        primary key (sbin17_uniq)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table "b2pwl32"
        (
        "char0_100"           Character(8)               not null,
        "sbin0_uniq"          Integer                    not null,
        "sdec0_n10"           Decimal(4)                              default 9,
        "int0_yTOm_uniq"      Interval year(5) to month     no default not null,
        "date0_nuniq"         Date                                   no default,
        "double1_uniq"        Double Precision           not null,
        "ts1_n100"            Timestamp                          ,
        "ubin1_500"           Numeric(4) unsigned           no default not null,
        "int1_dTOf6_100"      Interval day to second(6)   no default not null,
        "udec1_n2000"         PIC 9(8)V9                         ,
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
        "dt16_m_n10"          Date                     ,
        "int16_h_20"          Interval hour                 no default not null,
        "ubin16_n10"          Numeric(4) unsigned                    no default,
        "sdec16_uniq"         Decimal(18) signed         not null,
        "char16_n20"          Character(5)        ,   -- len = 2,4
        "real16_10"           Real                          no default not null,
        "int17_y_n10"         Interval year(1)                       no default,
        "dt17_yTOmin_uniq"    Timestamp(0)    not null,
        "real17_n100"         Real                               ,
        "sbin17_uniq"         Largeint  no default not null,  -- range: 0-149999
        "sdec17_nuniq"        Decimal(18)                            no default,
        "char17_2"            Character(8)               not null,
        primary key  (  "int0_yTOm_uniq", "int1_dTOf6_100" DESC) not droppable
        )
        store by primary key;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table t4
        (
        Ch_1             CHAR(10) not null,
        Dec_1            DECIMAL(9, 0) SIGNED,
        IntvlYr_Mn_1     INTERVAL YEAR(2) TO MONTH,
        IntvlHr_Mi_2     INTERVAL HOUR(2) TO MINUTE,
        Int_1            INT ,
        Int_2            INT ,
        primary key( Ch_1)
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('kUYm', 190641683, INTERVAL '4-7' YEAR(2) TO MONTH, INTERVAL '30:39' HOUR(2) TO MINUTE,
        1102836828, -1321787539);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('6ecDPehyZ', -400538679, INTERVAL '2-10' YEAR(2) TO MONTH, INTERVAL '1:53' HOUR(2) TO MINUTE,
        523007018, 1839056054);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('M', 517384848, INTERVAL '39-7' YEAR(2) TO MONTH, INTERVAL '8:16' HOUR(2) TO MINUTE,
        -880576225, -1067122833);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('L9jNuCbd', -763657792, INTERVAL '3-10' YEAR(2) TO MONTH, INTERVAL '6:55' HOUR(2) TO MINUTE,
        NULL, -1097124470);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('N', -423147649, INTERVAL '79-1' YEAR(2) TO MONTH, INTERVAL '28:37' HOUR(2) TO MINUTE,
        NULL, -2089622456);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('mdJRBg7oqH', 511432662, NULL, INTERVAL '8:17' HOUR(2) TO MINUTE, 1895714486, -1526181985
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('2nWNrIU', 059108505, INTERVAL '6-8' YEAR(2) TO MONTH, INTERVAL '8:05' HOUR(2) TO MINUTE,
        -234038213, 924008536);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('qRsuc', 659109838, INTERVAL '6-6' YEAR(2) TO MONTH, INTERVAL '16:28' HOUR(2) TO MINUTE,
        1616353683, 1814891532);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('ZKt6RWk6', 482020214, INTERVAL '51-6' YEAR(2) TO MONTH, INTERVAL '7:29' HOUR(2) TO MINUTE,
        28780996, -768068570);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('lX', NULL, INTERVAL '0-1' YEAR(2) TO MONTH, INTERVAL '2:33' HOUR(2) TO MINUTE,
        1519220102, -672654581);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('g', -514417202, NULL, INTERVAL '7:29' HOUR(2) TO MINUTE, 1669375894, 1977594200
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('I0CJ9Hh', 261685905, INTERVAL '7-0' YEAR(2) TO MONTH, INTERVAL '3:36' HOUR(2) TO MINUTE,
        -1656199612, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('DJ', 523712420, INTERVAL '23-7' YEAR(2) TO MONTH, INTERVAL '1:52' HOUR(2) TO MINUTE,
        1737977310, 1409999233);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('c5', -865749274, NULL, NULL, -1378078324, 759093722);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('Is', NULL, INTERVAL '11-5' YEAR(2) TO MONTH, INTERVAL '12:30' HOUR(2) TO MINUTE,
        NULL, -1688063259);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('d5Aq', -873368690, INTERVAL '00-5' YEAR(2) TO MONTH, INTERVAL '15:09' HOUR(2) TO MINUTE,
        -336463627, 594344536);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('aVI', -601358542, INTERVAL '8-5' YEAR(2) TO MONTH, INTERVAL '49:16' HOUR(2) TO MINUTE,
        -1040890366, 812541308);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('0ALiU', 674836291, INTERVAL '12-5' YEAR(2) TO MONTH, INTERVAL '3:03' HOUR(2) TO MINUTE,
        340405290, 1915984113);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('OymG', -397006801, INTERVAL '1-6' YEAR(2) TO MONTH, INTERVAL '32:58' HOUR(2) TO MINUTE,
        -1671177392, -2046946591);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('h4Q', -914168945, INTERVAL '3-6' YEAR(2) TO MONTH, INTERVAL '37:02' HOUR(2) TO MINUTE,
        775714580, 1826559375);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('sa4', -420100046, INTERVAL '9-2' YEAR(2) TO MONTH, INTERVAL '0:47' HOUR(2) TO MINUTE,
        -1626742353, 896651251);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('nsThilfh', -687293553, INTERVAL '7-0' YEAR(2) TO MONTH, INTERVAL '2:46' HOUR(2) TO MINUTE,
        1693692177, 433672345);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('Mw', 586486998, INTERVAL '40-8' YEAR(2) TO MONTH, INTERVAL '19:36' HOUR(2) TO MINUTE,
        155732715, -2018799930);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('LhY', 921538717, INTERVAL '22-11' YEAR(2) TO MONTH, NULL, NULL, -1332918087);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('RnAvp', -485881792, INTERVAL '8-5' YEAR(2) TO MONTH, INTERVAL '7:41' HOUR(2) TO MINUTE,
        -2065720469, -1337812683);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('X', -947110709, INTERVAL '77-2' YEAR(2) TO MONTH, INTERVAL '69:09' HOUR(2) TO MINUTE,
        -22369726, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('05kXmoq8DD', 185516326, INTERVAL '68-8' YEAR(2) TO MONTH, INTERVAL '33:49' HOUR(2) TO MINUTE,
        -913863534, 1167615774);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('tgv', -039480304, INTERVAL '3-8' YEAR(2) TO MONTH, INTERVAL '83:31' HOUR(2) TO MINUTE,
        356498597, -542893629);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('JH', 100423051, INTERVAL '30-5' YEAR(2) TO MONTH, INTERVAL '53:06' HOUR(2) TO MINUTE,
        NULL, 1402278323);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('Hxr8FwZW', -688882867, INTERVAL '42-7' YEAR(2) TO MONTH, INTERVAL '4:20' HOUR(2) TO MINUTE,
        560190040, 1278974370);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('a', 729915143, INTERVAL '5-8' YEAR(2) TO MONTH, INTERVAL '34:04' HOUR(2) TO MINUTE,
        421930502, 838328837);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('8GhGJ9TCv5', -678983277, INTERVAL '72-11' YEAR(2) TO MONTH, INTERVAL '4:38' HOUR(2) TO MINUTE,
        -883077926, -493846129);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('IaPUlH', 008077055, INTERVAL '72-10' YEAR(2) TO MONTH, INTERVAL '31:29' HOUR(2) TO MINUTE,
        1239127268, -1565381242);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('JRtZf', NULL, INTERVAL '9-11' YEAR(2) TO MONTH, INTERVAL '9:00' HOUR(2) TO MINUTE,
        -1557695961, 1576779957);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('K', 736935374, INTERVAL '63-11' YEAR(2) TO MONTH, INTERVAL '39:47' HOUR(2) TO MINUTE,
        728113442, -707193359);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('f2', 582401261, INTERVAL '53-9' YEAR(2) TO MONTH, NULL, 1751262538, 150240070);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('zwzHLQ', -895746679, INTERVAL '0-1' YEAR(2) TO MONTH, INTERVAL '29:37' HOUR(2) TO MINUTE,
        1192851505, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('MXQRX', 407091199, INTERVAL '5-0' YEAR(2) TO MONTH, NULL, -903153601, -2081311267
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('i', NULL, NULL, INTERVAL '92:10' HOUR(2) TO MINUTE, NULL, -86095575);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('qpBC6UF', 965330016, INTERVAL '1-0' YEAR(2) TO MONTH, INTERVAL '21:11' HOUR(2) TO MINUTE,
        538506558, 1065837614);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('VXfRPav', 010271282, INTERVAL '2-11' YEAR(2) TO MONTH, INTERVAL '03:39' HOUR(2) TO MINUTE,
        -1840336698, 1717062902);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('wktf7X', 961818966, INTERVAL '03-1' YEAR(2) TO MONTH, NULL, -1136596928, 195301141
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('kbAPNjW', -318042473, INTERVAL '2-2' YEAR(2) TO MONTH, INTERVAL '8:26' HOUR(2) TO MINUTE,
        385104124, 841150218);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('gXemak', -537153234, INTERVAL '4-0' YEAR(2) TO MONTH, INTERVAL '0:17' HOUR(2) TO MINUTE,
        NULL, 419267315);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('3Th1EHIohs', -681310354, INTERVAL '4-11' YEAR(2) TO MONTH, INTERVAL '4:23' HOUR(2) TO MINUTE,
        -609534270, -1782785802);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('sYM9', 877996832, INTERVAL '8-2' YEAR(2) TO MONTH, INTERVAL '93:07' HOUR(2) TO MINUTE,
        NULL, -622372758);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('fbQJkVnI', 909299882, INTERVAL '1-0' YEAR(2) TO MONTH, INTERVAL '75:20' HOUR(2) TO MINUTE,
        -104171422, -1589547632);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('mnmh', NULL, INTERVAL '7-5' YEAR(2) TO MONTH, NULL, NULL, -1298841906);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('tDSt8', 321316591, INTERVAL '26-6' YEAR(2) TO MONTH, INTERVAL '5:27' HOUR(2) TO MINUTE,
        1939455651, -1310890007);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('CPowoZmy', 764932122, INTERVAL '64-7' YEAR(2) TO MONTH, INTERVAL '3:46' HOUR(2) TO MINUTE,
        -1163952662, -1833943181);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('nTuCrBFqr', 267948753, INTERVAL '1-11' YEAR(2) TO MONTH, INTERVAL '7:09' HOUR(2) TO MINUTE,
        -382486062, -189750188);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('XMLlhCvOH', 141852530, INTERVAL '55-2' YEAR(2) TO MONTH, INTERVAL '2:05' HOUR(2) TO MINUTE,
        -1783313451, -1790685319);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('2hcjdx94KE', -118633235, NULL, INTERVAL '80:04' HOUR(2) TO MINUTE, NULL, 1466027262
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('tWXk', 486388637, INTERVAL '90-10' YEAR(2) TO MONTH, INTERVAL '6:49' HOUR(2) TO MINUTE,
        -231809823, 1217727421);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('91UUyBFJ60', NULL, INTERVAL '8-11' YEAR(2) TO MONTH, INTERVAL '00:08' HOUR(2) TO MINUTE,
        -905987092, -749828052);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('8MdUUik3', -474607918, NULL, NULL, 1580128705, 377303096);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('b7mB8SL3z', -904467129, INTERVAL '39-6' YEAR(2) TO MONTH, INTERVAL '4:33' HOUR(2) TO MINUTE,
        1068138640, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('7UJs3', -986023539, INTERVAL '7-2' YEAR(2) TO MONTH, INTERVAL '34:39' HOUR(2) TO MINUTE,
        -1417809823, 582210947);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('nv0Z', -023445040, INTERVAL '0-6' YEAR(2) TO MONTH, INTERVAL '0:14' HOUR(2) TO MINUTE,
        -1210852665, 1903417890);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('uwI', NULL, INTERVAL '1-11' YEAR(2) TO MONTH, INTERVAL '19:27' HOUR(2) TO MINUTE,
        -496304558, -1375495560);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('zRZqOxbpDI', -994957909, INTERVAL '1-4' YEAR(2) TO MONTH, NULL, 1993609602, -16347340
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('r', -515198180, INTERVAL '86-8' YEAR(2) TO MONTH, INTERVAL '6:59' HOUR(2) TO MINUTE,
        1906249784, 1370862714);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('OK4CS0', -746787627, INTERVAL '3-11' YEAR(2) TO MONTH, INTERVAL '87:07' HOUR(2) TO MINUTE,
        -908653605, -1788738440);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('9I', -170808286, INTERVAL '16-3' YEAR(2) TO MONTH, INTERVAL '93:34' HOUR(2) TO MINUTE,
        -146230965, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('TpXoZiY', -184527579, INTERVAL '68-0' YEAR(2) TO MONTH, NULL, 374389410, -210742281
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('A46mglyQil', 132062444, INTERVAL '5-11' YEAR(2) TO MONTH, INTERVAL '28:59' HOUR(2) TO MINUTE,
        -435235301, -1831036621);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('Rafx', -159211959, INTERVAL '16-4' YEAR(2) TO MONTH, INTERVAL '62:56' HOUR(2) TO MINUTE,
        19933837, 18415714);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('WH', 182998842, INTERVAL '80-4' YEAR(2) TO MONTH, INTERVAL '59:02' HOUR(2) TO MINUTE,
        -1819898745, -234287023);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('3', 152247628, INTERVAL '73-2' YEAR(2) TO MONTH, INTERVAL '77:18' HOUR(2) TO MINUTE,
        NULL, -572280271);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('NY', NULL, INTERVAL '7-0' YEAR(2) TO MONTH, INTERVAL '7:10' HOUR(2) TO MINUTE,
        NULL, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('ris', -882664033, INTERVAL '8-4' YEAR(2) TO MONTH, INTERVAL '09:08' HOUR(2) TO MINUTE,
        -144343981, -731679498);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('m1e', 103942166, INTERVAL '6-6' YEAR(2) TO MONTH, INTERVAL '4:25' HOUR(2) TO MINUTE,
        365159561, 986671880);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('L', 179227883, INTERVAL '02-9' YEAR(2) TO MONTH, INTERVAL '7:07' HOUR(2) TO MINUTE,
        1703787809, 195288234);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('ST3m', 470035440, INTERVAL '3-10' YEAR(2) TO MONTH, INTERVAL '9:50' HOUR(2) TO MINUTE,
        NULL, -2085010186);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('LBMNP0', 962225668, INTERVAL '93-7' YEAR(2) TO MONTH, INTERVAL '5:16' HOUR(2) TO MINUTE,
        35794862, -27937023);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('6mAwFUPwVy', 865414392, NULL, INTERVAL '06:53' HOUR(2) TO MINUTE, -1015125607,
        700324736);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('dJKl', NULL, INTERVAL '52-0' YEAR(2) TO MONTH, INTERVAL '18:54' HOUR(2) TO MINUTE,
        1617742622, -1748715929);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('i', 067351752, INTERVAL '5-0' YEAR(2) TO MONTH, INTERVAL '05:05' HOUR(2) TO MINUTE,
        -2137771885, -61936232);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('GUOghJ7', -457828745, INTERVAL '6-8' YEAR(2) TO MONTH, INTERVAL '77:23' HOUR(2) TO MINUTE,
        1828780676, 1671839194);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('xn', 973798789, INTERVAL '8-9' YEAR(2) TO MONTH, INTERVAL '6:51' HOUR(2) TO MINUTE,
        1831456315, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('8y2vp', 580890948, INTERVAL '70-2' YEAR(2) TO MONTH, INTERVAL '42:43' HOUR(2) TO MINUTE,
        117949372, -485438150);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('k62c3PzK', 262242555, INTERVAL '0-8' YEAR(2) TO MONTH, INTERVAL '79:58' HOUR(2) TO MINUTE,
        -356536617, -1997813929);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('o', NULL, INTERVAL '5-1' YEAR(2) TO MONTH, INTERVAL '40:55' HOUR(2) TO MINUTE,
        1419095396, 941462286);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('OSf', 906253576, INTERVAL '41-2' YEAR(2) TO MONTH, INTERVAL '23:25' HOUR(2) TO MINUTE,
        46588798, 837806688);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('Hd', 026572115, INTERVAL '0-10' YEAR(2) TO MONTH, INTERVAL '9:22' HOUR(2) TO MINUTE,
        1208708207, -1996947849);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('xYhg1W4GH', 620398029, INTERVAL '3-11' YEAR(2) TO MONTH, INTERVAL '29:39' HOUR(2) TO MINUTE,
        NULL, 2051423052);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('b13duY5B', -886422759, INTERVAL '2-10' YEAR(2) TO MONTH, INTERVAL '33:25' HOUR(2) TO MINUTE,
        928964245, 1699881177);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('O4CWr', 608573062, INTERVAL '76-4' YEAR(2) TO MONTH, INTERVAL '01:57' HOUR(2) TO MINUTE,
        -982559744, 391642015);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('eagn1', 113226870, INTERVAL '8-1' YEAR(2) TO MONTH, INTERVAL '53:29' HOUR(2) TO MINUTE,
        1452525, -597395713);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('EYEjq9', 328493934, INTERVAL '4-7' YEAR(2) TO MONTH, INTERVAL '69:54' HOUR(2) TO MINUTE,
        542045502, 1523823444);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('Vk3Q', -279571390, INTERVAL '76-5' YEAR(2) TO MONTH, INTERVAL '2:01' HOUR(2) TO MINUTE,
        NULL, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('iENyDO2967', 814085496, INTERVAL '3-1' YEAR(2) TO MONTH, INTERVAL '8:24' HOUR(2) TO MINUTE,
        -1007424115, 1802309145);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('pOOpALsLw5', NULL, INTERVAL '53-8' YEAR(2) TO MONTH, INTERVAL '6:46' HOUR(2) TO MINUTE,
        NULL, -909691150);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('5m8sx', 398902902, INTERVAL '16-3' YEAR(2) TO MONTH, INTERVAL '57:37' HOUR(2) TO MINUTE,
        NULL, -1312403887);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('tFv21OiwY', -940724783, INTERVAL '49-11' YEAR(2) TO MONTH, INTERVAL '05:02' HOUR(2) TO MINUTE,
        -129840282, -347526131);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('4DVSwXO', NULL, INTERVAL '11-1' YEAR(2) TO MONTH, INTERVAL '79:30' HOUR(2) TO MINUTE,
        1895539793, 513082050);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('X', -182410246, NULL, INTERVAL '12:58' HOUR(2) TO MINUTE, -192330393, -747614603
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('z5hAF6ftk', -592454430, INTERVAL '99-11' YEAR(2) TO MONTH, INTERVAL '28:01' HOUR(2) TO MINUTE,
        838326383, 954363767);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('UXhpE', 717832594, INTERVAL '3-1' YEAR(2) TO MONTH, INTERVAL '86:03' HOUR(2) TO MINUTE,
        -768869517, NULL);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into t4
        values
        ('VUE', -277691255, NULL, INTERVAL '93:04' HOUR(2) TO MINUTE, 316146035, 1604030147
        )
        ;"""
    output = _dci.cmdexec(stmt)

    stmt = """CREATE TABLE employ (
        empnum         NUMERIC (5) UNSIGNED
        NO DEFAULT
        NOT NULL NOT DROPPABLE
        HEADING 'Employee/Number'
        ,first_name     CHARACTER (15)
        DEFAULT ' '
        NOT NULL NOT DROPPABLE
        HEADING 'First Name'
        ,last_name      CHARACTER (20)
        DEFAULT ' '
        NOT NULL NOT DROPPABLE
        HEADING 'Last Name'
        ,deptnum        NUMERIC (5)
        UNSIGNED
        NO DEFAULT
        NOT NULL NOT DROPPABLE
        HEADING 'Dept/Num'
        ,jobcode        NUMERIC (4) UNSIGNED
        NOT NULL NOT DROPPABLE
        HEADING 'Job/Code'
        ,salary         NUMERIC (8, 2) UNSIGNED
        DEFAULT NULL
        HEADING 'Salary'
        ,PRIMARY KEY    (empnum) NOT DROPPABLE
        );"""
    output = _dci.cmdexec(stmt)

    stmt = """INSERT INTO employ
        VALUES (   1,'ROGER'   ,'GREEN'     ,9000, 100,175500.00 ),
        (  23,'JERRY'   ,'HOWARD'    ,1000, 100,137000.10 ),
        (  29,'JANE'    ,'RAYMOND'   ,3000, 100,136000.00 ),
        (  32,'THOMAS'  ,'RUDLOFF'   ,2000, 100,138000.40 ),
        (  39,'KLAUS '  ,'SAFFERT'   ,3200, 100, 75000.00 ),
        (  43,'PAUL'    ,'WINTER'    ,3100, 100, 90000.00 ),
        (  65,'RACHEL'  ,'MCKAY'     ,4000, 100,118000.00 ),
        (  72,'GLENN'   ,'THOMAS'    ,3300, 100, 80000.00 ),
        (  75,'TIM'     ,'WALKER'    ,3000, 300, 32000.00 ),
        (  87,'ERIC'    ,'BROWN'     ,4000, 400, 89000.00 ),
        (  89,'PETER'   ,'SMITH'     ,3300, 300, 37000.40 ),
        (  93,'DONALD'  ,'TAYLOR'    ,3100, 300, 33000.00 ),
        ( 104,'DAVID'   ,'STRAND'    ,4000, 400, 69000.00 ),
        ( 109,'STEVE'   ,'COOK'      ,4000, 400, 68000.00 ),
        ( 111,'SHERRIE' ,'WONG'      ,3500, 100, 70000.00 ),
        ( 178,'JOHN'    ,'CHOU'      ,3500, 900, 28000.00 ),
        ( 180,'MANFRED' ,'CONRAD'    ,4000, 450, 32000.00 ),
        ( 201,'JIM'     ,'HERMAN'    ,3000, 300, 19000.00 ),
        ( 202,'LARRY'   ,'CLARK'     ,1000, 500, 25000.75 ),
        ( 203,'KATHRYN' ,'HALL'      ,4000, 400, 96000.00 ),
        ( 205,'GINNY'   ,'FOSTER'    ,3300, 900, 30000.00 ),
        ( 206,'DAVE'    ,'FISHER'    ,3200, 900, 25000.00 ),
        ( 207,'MARK'    ,'FOLEY'     ,4000, 420, 33000.00 ),
        ( 208,'SUE'     ,'CRAMER'    ,1000, 900, 19000.00 ),
        ( 209,'SUSAN'   ,'CHAPMAN'   ,1500, 900, 17000.00 ),
        ( 210,'RICHARD' ,'BARTON'    ,1000, 500, 29000.00 ),
        ( 211,'JIMMY'   ,'SCHNEIDER' ,1500, 600, 26000.00 ),
        ( 212,'JONATHAN','MITCHELL'  ,1500, 600, 32000.00 ),
        ( 213,'ROBERT'  ,'WHITE'     ,1500, 100, 90000.00 ),
        ( 214,'JULIA'   ,'KELLY'     ,1000, 500, 50000.00 ),
        ( 215,'WALTER'  ,'LANCASTER' ,4000, 450, 33000.50 ),
        ( 216,'JOHN'    ,'JONES'     ,4000, 450, 40000.00 ),
        ( 217,'MARLENE' ,'BONNY'     ,4000, 900, 24000.90 ),
        ( 218,'GEORGE'  ,'FRENCHMAN' ,4000, 420, 36000.00 ),
        ( 219,'DAVID'   ,'TERRY'     ,2000, 250, 27000.12 ),
        ( 220,'JOHN'    ,'HUGHES'    ,3200, 300, 33000.10 ),
        ( 221,'OTTO'    ,'SCHNABL'   ,3200, 300, 33000.00 ),
        ( 222,'MARTIN'  ,'SCHAEFFER' ,3200, 300, 31000.00 ),
        ( 223,'HERBERT' ,'KARAJAN'   ,3200, 300, 29000.00 ),
        ( 224,'MARIA'   ,'JOSEF'     ,4000, 420, 18000.10 ),
        ( 225,'KARL'    ,'HELMSTED'  ,4000, 450, 32000.00 ),
        ( 226,'HEIDI'   ,'WEIGL'     ,3200, 300, 22000.00 ),
        ( 227,'XAVIER'  ,'SEDLEMEYER',3300, 300, 30000.00 ),
        ( 228,'PETE'    ,'WELLINGTON',3100, 300, 32000.20 ),
        ( 229,'GEORGE'  ,'STRICKER'  ,3100, 300, 32222.00 ),
        ( 230,'ROCKY'   ,'LEWIS'     ,2000, 200, 24000.00 ),
        ( 231,'HERB'    ,'ALBERT'    ,3300, 300, 33000.00 ),
        ( 232,'THOMAS'  ,'SPINNER'   ,4000, 450, 45000.00 ),
        ( 233,'TED'     ,'MCDONALD'  ,2000, 250, 29000.00 ),
        ( 234,'MARY'    ,'MILLER'    ,2500, 100, 56000.00 ),
        ( 235,'MIRIAM'  ,'KING'      ,2500, 900, 18000.00 ),
        ( 321,'BILL'    ,'WINN'      ,2000, 900, 32000.00 ),
        ( 337,'DINAH'   ,'CLARK'     ,9000, 900, 37000.00 ),
        ( 343,'ALAN'    ,'TERRY'     ,3000, 900, 39500.00 ),
        ( 557,'BEN'     ,'HENDERSON' ,4000, 400, 65000.00 ),
        ( 568,'JESSICA' ,'CRINER'    ,3500, 300, 39500.00 ),
        ( 990,'thomas'  ,'stibbs'    ,3500, 100, 80000.00 ),
        ( 991,'Wayne'   ,'O''Neil'   ,3500, 200, 50000.00 ),
        ( 992,'Barry'   ,'Kinney'    ,3500, 250, 30000.00 ),
        ( 993,'Paul'    ,'Buskett'   ,3100, 450, 60000.00 ),
        ( 994,'Emmy'    ,'Buskett'   ,3100, 600, 90000.00 ),
        ( 995,'Walt'    ,'Farley'    ,3100, 800, 30000.00 ),
        ( 2000,'Nizan'  ,'Peleg'     ,9999, 700, 40234.00 ),
        ( 2001,'Rivka'  ,'Lad'       ,9999, 250, 40322.00 );"""
    output = _dci.cmdexec(stmt)

    stmt = """create table bd(a varchar(4018), b int not null primary key);"""
    output = _dci.cmdexec(stmt)

    stmt = """create table tp2(a time(6) not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tp2 values (time '14:58:03.330000');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tp2 values (time '12:45:45.12345');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tp2 values (time '12:45:45.1234');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tp2 values (time '12:45:45.123');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tp2 values (time '12:45:45.12');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tp2 values (time '12:45:45.1');"""
    output = _dci.cmdexec(stmt)

    stmt = """insert into tp2 values (time '12:45:45.0');"""
    output = _dci.cmdexec(stmt)

    stmt = """create table tp2(a time not null not droppable primary key);"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table b2uwl20
        (
        char0_100           Character(9)                  no default not null,
        sbin0_100           Integer                       no default not null,
        int0_dTOf6_n100     Interval day to second(6)            no default,
        sdec0_nuniq         Decimal(9)                             no default,
        date0_100           Date                       not null,
        time1_1000          Time                       not null,
        int1_yTOm_uniq      Interval year(5) to month  not null,
        udec1_2             Decimal(9) unsigned        not null,
        ubin1_uniq          Numeric(9) unsigned        not null,
        real1_uniq          Real                          no default not null,
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
        dt16_m_n10          Date                     ,
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
        char17_2            Character(8)               not null,
        primary key  (  date0_100,
        time1_1000 DESC,
        int1_yTOm_uniq) not droppable
        )
        store by primary key;"""
    output = _dci.cmdexec(stmt)

    stmt = """--  attributes audit;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table b2uwl22
        (
        date0_n10           Date
        default date '01/09/2100' heading 'date0_n10 with default 01/09/2100',
        int0_dTOf6_uniq     Interval day to second(6)    no default not null,
        char0_n2            Character(8)                           no default,
        sbin0_10            Largeint                   not null,
        sdec0_nuniq         Decimal(4)                         ,
        ubin1_10            Numeric(4) unsigned           no default not null,
        udec1_nuniq         Decimal(9) unsigned                    no default,
        int1_d_100          Interval day               not null,
        ts1_100             Timestamp                  not null,
        double1_uniq        Double Precision              no default not null,
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
        dt16_m_n10          Date                     ,
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
        char17_2            Character(8)               not null,
        primary key  (  ts1_100,
        double1_uniq,
        int1_d_100 DESC) not droppable
        )
        store by primary key;"""
    output = _dci.cmdexec(stmt)

    stmt = """--  attributes audit;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table b2pwl32
        (
        char0_100           Character(8)               not null,
        sbin0_uniq          Integer                    not null,
        sdec0_n10           Decimal(4)                              default 9,
        int0_yTOm_uniq      Interval year(5) to month     no default not null,
        date0_nuniq         Date                                   no default,
        double1_uniq        Double Precision           not null,
        ts1_n100            Timestamp                          ,
        ubin1_500           Numeric(4) unsigned           no default not null,
        int1_dTOf6_100      Interval day to second(6)   no default not null,
        udec1_n2000         PIC 9(8)V9                         ,
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
        dt16_m_n10          Date                     ,
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
        char17_2            Character(8)               not null,
        primary key  (  int0_yTOm_uniq, int1_dTOf6_100 DESC) not droppable
        )
        store by primary key
        attributes extent(1024,1024), maxextents 512;"""
    output = _dci.cmdexec(stmt)

    stmt = """Create Table b2pwl16
        (
        char0_100           Character(8)               not null,
        sbin0_uniq          Integer                    not null,
        sdec0_n10           Decimal(4)                              default 9,
        int0_yTOm_n1000     Interval year(2) to month              no default,
        date0_nuniq         Date                                   no default,
        real1_uniq          Real                       not null,
        ts1_n100            Timestamp                          ,
        ubin1_500           Numeric(4) unsigned           no default not null,
        int1_dTOf6_nuniq    Interval day to second(6)            no default,
        udec1_2000          Decimal(9) unsigned        not null,
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
        dt16_m_n10          Date                     ,
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
        char17_2            Character(8)               not null,
        primary key  (  real1_uniq ) not droppable
        )
        store by primary key
        attributes extent(1024,1024), maxextents 512;"""
    output = _dci.cmdexec(stmt)

    stmt = """create table txn1 (c1 int not null primary key, c2 varchar(20) not null, c3 int);"""
    output = _dci.cmdexec(stmt)
    _dci.expect_complete_msg(output)

    _testmgr.testcase_end(desc)
