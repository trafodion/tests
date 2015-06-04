// @@@ START COPYRIGHT @@@
//
// (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
//
// @@@ END COPYRIGHT @@@

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class hp2004
{
  public static void N0165()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("CREATE PROCEDURE SPJTEST(VARCHAR(50), OUT VARCHAR(50)) EXTERNAL NAME 'Procs.N0200(java.lang.String,java.lang.String[])' EXTERNAL PATH 'spjcall' LANGUAGE JAVA PARAMETER STYLE JAVA CONTAINS SQL NO ISOLATE");
  }

  public static void N0166()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("CREATE PROCEDURE SPJTEST(VARCHAR(50), OUT VARCHAR(50)) EXTERNAL NAME 'Procs.N0200(java.lang.String,java.lang.String)' EXTERNAL PATH 'spjcall' LANGUAGE JAVA PARAMETER STYLE JAVA CONTAINS SQL NO ISOLATE");
  }

  public static void N0167()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("CREATE PROCEDURE SPJTEST(CHAR(50), INTEGER, NUMERIC,REAL, DATE,OUT VARCHAR(150) ) EXTERNAL NAME 'Procs.N0602' EXTERNAL PATH 'spjcall' LANGUAGE JAVA PARAMETER STYLE JAVA CONTAINS SQL NO ISOLATE");
  }

  public static void N0168()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("CREATE PROCEDURE SPJTEST(OUT VARCHAR(50),IN CHAR(20)) EXTERNAL NAME 'Procs.N0200' EXTERNAL PATH 'spjcall' LANGUAGE JAVA PARAMETER STYLE JAVA CONTAINS SQL NO ISOLATE");
  }

  public static void N0169()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("CREATE PROCEDURE SPJTEST(IN CHAR VARYING(10), OUT VARCHAR(10) UPSHIFT) EXTERNAL NAME 'Procs.N0200' EXTERNAL PATH 'spjcall' LANGUAGE JAVA PARAMETER STYLE JAVA");
  }

  public static void N0170()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("CREATE PROCEDURE SPJTEST(IN IN1 INT, OUT OUT1 REAL)  EXTERNAL NAME 'Pack.PackProcs.N1200 (java.lang.Integer,float[])' EXTERNAL PATH 'spjcall' LANGUAGE JAVA PARAMETER STYLE JAVA CONTAINS SQL NO ISOLATE");
  }

  public static void N0171()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("CREATE PROCEDURE SPJTEST(IN IN1 INT, OUT OUT1 int)                EXTERNAL NAME 'Procs.N0210' EXTERNAL PATH 'spjcall' LANGUAGE JAVA PARAMETER STYLE JAVA LOCATION $FC0300 CONTAINS SQL NO ISOLATE");
  }

  public static void N0172()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("CREATE PROCEDURE SPJTEST(IN IN1 INT, OUT OUT1 REAL)  EXTERNAL NAME 'Pack.PackProcs.N1200 (java.lang.Integer,float[])' EXTERNAL PATH 'spjcall' LANGUAGE JAVA PARAMETER STYLE JAVA LOCATION $CX0132.ZSDSJAVA.JAVAQA00 CONTAINS SQL NO ISOLATE");
  }

  public static void N0173()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("create procedure spjtest(int , int) external name 'Procs.N0210(int,int)' external path 'spjcall' language java parameter style java contains sql no isolate");
  }

  public static void N0174(String paramString1, String paramString2, String paramString3, String paramString4, String paramString5, String paramString6, String paramString7, String paramString8, String paramString9, String paramString10, String paramString11, String paramString12, String paramString13, String paramString14, String paramString15, String paramString16, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    ResultSet localResultSet = localStatement.executeQuery("SELECT  spj1.e_name, spj2.e_long, spj3.e_float, spj4.e_real, spj5.e_double, spj6.e_short, spj7.e_nume, spj8.e_deci, spj9.e_nume, spj10.e_deci, spj11.e_nume, spj12.e_deci, spj13.e_time, spj14.e_tstamp, spj15.e_char, spj16.e_date1 FROM spj1, spj2, spj3, spj4, spj5, spj6, spj7, spj8, spj9, spj10, spj11, spj12, spj13, spj14, spj15, spj16 WHERE spj1.e_date=spj2.e_date and spj3.e_date=spj4.e_date and spj5.e_date=spj6.e_date and spj7.e_date=spj8.e_date and spj9.e_date=spj10.e_date and spj11.e_date=spj12.e_date and spj13.e_date=spj14.e_date and spj15.e_date=spj16.e_date;");

    localResultSet.next();
    paramString1 = localResultSet.getString(1);
    paramString2 = localResultSet.getString(2);
    paramString3 = localResultSet.getString(3);
    paramString4 = localResultSet.getString(4);
    paramString5 = localResultSet.getString(5);
    paramString6 = localResultSet.getString(6);
    paramString7 = localResultSet.getString(7);
    paramString8 = localResultSet.getString(8);
    paramString9 = localResultSet.getString(9);
    paramString10 = localResultSet.getString(10);
    paramString11 = localResultSet.getString(11);
    paramString12 = localResultSet.getString(12);
    paramString13 = localResultSet.getString(13);
    paramString14 = localResultSet.getString(14);
    paramString15 = localResultSet.getString(15);
    paramString16 = localResultSet.getString(16);

    paramArrayOfString[0] = paramString1;
    paramArrayOfString[0] = paramString2;
    paramArrayOfString[0] = paramString3;
    paramArrayOfString[0] = paramString4;
    paramArrayOfString[0] = paramString5;
    paramArrayOfString[0] = paramString6;
    paramArrayOfString[0] = paramString7;
    paramArrayOfString[0] = paramString8;
    paramArrayOfString[0] = paramString9;
    paramArrayOfString[0] = paramString10;
    paramArrayOfString[0] = paramString11;
    paramArrayOfString[0] = paramString12;
    paramArrayOfString[0] = paramString13;
    paramArrayOfString[0] = paramString14;
    paramArrayOfString[0] = paramString15;
    paramArrayOfString[0] = paramString16;
  }

  public static void N0175(String paramString1, String paramString2, String paramString3, String paramString4, String paramString5, String paramString6, String paramString7, String paramString8, String paramString9, String paramString10, String paramString11, String paramString12, String paramString13, String paramString14, String paramString15, String paramString16, String paramString17, String paramString18, String paramString19, String paramString20, String[] paramArrayOfString1, String[] paramArrayOfString2, String[] paramArrayOfString3, String[] paramArrayOfString4, String[] paramArrayOfString5, String[] paramArrayOfString6, String[] paramArrayOfString7, String[] paramArrayOfString8, String[] paramArrayOfString9, String[] paramArrayOfString10, String[] paramArrayOfString11, String[] paramArrayOfString12, String[] paramArrayOfString13, String[] paramArrayOfString14, String[] paramArrayOfString15, String[] paramArrayOfString16, String[] paramArrayOfString17, String[] paramArrayOfString18, String[] paramArrayOfString19, String[] paramArrayOfString20)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    ResultSet localResultSet = localStatement.executeQuery("SELECT  spj1.e_name, spj2.e_long, spj3.e_float, spj4.e_real, spj5.e_double, spj6.e_short, spj7.e_nume, spj8.e_deci, spj9.e_nume, spj10.e_deci, spj11.e_nume, spj12.e_deci, spj13.e_time, spj14.e_tstamp, spj15.e_char, spj16.e_date1, spj17.e_time1, spj18.e_tstamp1, spj19.e_vchar, spj20.e_char1 FROM spj1, spj2, spj3, spj4, spj5, spj6, spj7, spj8, spj9, spj10, spj11, spj12, spj13, spj14, spj15, spj16, spj17, spj18, spj19, spj20 WHERE spj1.e_date=spj2.e_date and spj3.e_date=spj4.e_date and spj5.e_date=spj6.e_date and spj7.e_date=spj8.e_date and spj9.e_date=spj10.e_date and spj11.e_date=spj12.e_date and spj13.e_date=spj14.e_date and spj15.e_date=spj16.e_date and spj17.e_date=spj18.e_date and spj19.e_date=spj20.e_date;");

    localResultSet.next();
    paramString1 = localResultSet.getString(1);
    paramString2 = localResultSet.getString(2);
    paramString3 = localResultSet.getString(3);
    paramString4 = localResultSet.getString(4);
    paramString5 = localResultSet.getString(5);
    paramString6 = localResultSet.getString(6);
    paramString7 = localResultSet.getString(7);
    paramString8 = localResultSet.getString(8);
    paramString9 = localResultSet.getString(9);
    paramString10 = localResultSet.getString(10);
    paramString11 = localResultSet.getString(11);
    paramString12 = localResultSet.getString(12);
    paramString13 = localResultSet.getString(13);
    paramString14 = localResultSet.getString(14);
    paramString15 = localResultSet.getString(15);
    paramString16 = localResultSet.getString(16);
    paramString17 = localResultSet.getString(17);
    paramString18 = localResultSet.getString(18);
    paramString19 = localResultSet.getString(19);
    paramString20 = localResultSet.getString(20);

    paramArrayOfString1[0] = paramString1;
    paramArrayOfString2[0] = paramString2;
    paramArrayOfString3[0] = paramString3;
    paramArrayOfString4[0] = paramString4;
    paramArrayOfString5[0] = paramString5;
    paramArrayOfString6[0] = paramString6;
    paramArrayOfString7[0] = paramString7;
    paramArrayOfString8[0] = paramString8;
    paramArrayOfString9[0] = paramString9;
    paramArrayOfString10[0] = paramString10;
    paramArrayOfString11[0] = paramString11;
    paramArrayOfString12[0] = paramString12;
    paramArrayOfString13[0] = paramString13;
    paramArrayOfString14[0] = paramString14;
    paramArrayOfString15[0] = paramString15;
    paramArrayOfString16[0] = paramString16;
    paramArrayOfString17[0] = paramString17;
    paramArrayOfString18[0] = paramString18;
    paramArrayOfString19[0] = paramString19;
    paramArrayOfString20[0] = paramString20;
  }

  public static void N0259()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("control query default POS 'OFF'");
    localStatement.executeUpdate("control query default DDL_DEFAULT_LOCATIONS ''");
    localStatement.executeUpdate("create table spj1(e_id smallint not null not droppable, e_name varchar(50),e_date date,     primary key (e_id))");
    localStatement.executeUpdate("create table spj2(e_id smallint not null not droppable, e_long largeint , e_date date ,     primary key (e_id))");
    localStatement.executeUpdate("create table spj3(e_id smallint not null not droppable, e_float float(54)   ,e_date date,   primary key (e_id))");
    localStatement.executeUpdate("create table spj4(e_id smallint not null not droppable, e_real real, e_date date,           primary key (e_id))");
    localStatement.executeUpdate("create table spj5(e_id smallint not null not droppable, e_double double precision ,e_date date, primary key (e_id))");
    localStatement.executeUpdate("create table spj6(e_id smallint not null not droppable, e_short smallint    ,e_date date,   primary key (e_id))");
    localStatement.executeUpdate("create table spj7(e_id smallint not null not droppable, e_nume numeric(15,6),e_date date,   primary key (e_id))");
    localStatement.executeUpdate("create table spj8(e_id smallint not null not droppable, e_deci decimal(15,6) ,e_date date,  primary key (e_id))");
    localStatement.executeUpdate("create table spj9(e_id smallint not null not droppable, e_nume numeric(9,0)  ,e_date date,  primary key (e_id))");
    localStatement.executeUpdate("create table spj10(e_id smallint not null not droppable, e_deci decimal(9,0) , e_date date, primary key (e_id))");
  }

  public static void N0260()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("insert into spj1 values(1,'Hewlett Packard', current_date)");
    localStatement.executeUpdate("insert into spj2 values(2,9875412358965874, current_date)");
    localStatement.executeUpdate("insert into spj3 values(3,1.2145E37, current_date)");
    localStatement.executeUpdate("insert into spj4 values(4,1.5412E18, current_date)");
    localStatement.executeUpdate("insert into spj5 values(5,1.124E75, current_date)");
    localStatement.executeUpdate("insert into spj6 values(6,32225, current_date)");
    localStatement.executeUpdate("insert into spj7 values(7,852963741.654321, current_date)");
    localStatement.executeUpdate("insert into spj8 values(8,123456789.32154, current_date)");
    localStatement.executeUpdate("insert into spj9 values(9,985674123.0, current_date)");
    localStatement.executeUpdate("insert into spj10 values(10,987523641.0, current_date)");
  }

  public static void N0261()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("update spj1 set e_name='No down time at all'");
    localStatement.executeUpdate("update spj2 set e_long= 5357979535935935797");
    localStatement.executeUpdate("update spj3 set e_float=1.001245E36");
    localStatement.executeUpdate("update spj4 set e_real=2.0124E12");
    localStatement.executeUpdate("update spj5 set e_double=3.2145E35");
    localStatement.executeUpdate("update spj6 set e_short=25625");
    localStatement.executeUpdate("update spj7 set e_nume=963852741.654321");
    localStatement.executeUpdate("update spj8 set e_deci=321654987.852741");
    localStatement.executeUpdate("update spj9 set e_nume=999999999");
    localStatement.executeUpdate("update spj10 set e_deci=666666666");
  }

  public static void N0262()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("delete from spj1");
    localStatement.executeUpdate("delete from spj2");
    localStatement.executeUpdate("delete from spj3");
    localStatement.executeUpdate("delete from spj4");
    localStatement.executeUpdate("delete from spj5");
    localStatement.executeUpdate("delete from spj6");
    localStatement.executeUpdate("delete from spj7");
    localStatement.executeUpdate("delete from spj8");
    localStatement.executeUpdate("delete from spj9");
    localStatement.executeUpdate("delete from spj10");
  }

  public static void N0263()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("drop table spj1");
    localStatement.executeUpdate("drop table spj2");
    localStatement.executeUpdate("drop table spj3");
    localStatement.executeUpdate("drop table spj4");
    localStatement.executeUpdate("drop table spj5");
    localStatement.executeUpdate("drop table spj6");
    localStatement.executeUpdate("drop table spj7");
    localStatement.executeUpdate("drop table spj8");
    localStatement.executeUpdate("drop table spj9");
    localStatement.executeUpdate("drop table spj10");
  }

  public static void N0264()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("control query default DDL_DEFAULT_LOCATIONS ''");
    localStatement.executeUpdate("create unique index empind on emp(ename) populate");
  }

  public static void N0265()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("control query default DDL_DEFAULT_LOCATIONS ''");
    localStatement.executeUpdate("Create table newtab(e_name varchar(100)not null primary key )");
    localStatement.executeUpdate("alter table newtab add e_date date");
    localStatement.executeUpdate("create unique index newind on newtab(e_date) populate");
  }

  public static void N0266()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("control query default DDL_DEFAULT_LOCATIONS ''");
    localStatement.executeUpdate("create view newview as select e_name,e_date from testtab");
  }

  public static void N0267()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("control query default DDL_DEFAULT_LOCATIONS ''");
    localStatement.executeUpdate("Create table newtab(e_name varchar(100) not null primary key)");
    localStatement.executeUpdate("alter table newtab add e_date date");
    localStatement.executeUpdate("create view newview as select e_date from newtab");
  }

  public static void N0268()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    for (int i = 1234567000; i <= 1234568000; i++) {
      localStatement.executeUpdate("insert into mxtab values(:i)");
      localStatement.executeUpdate("insert into mptab (select * from mxtab)");
    }
  }

  public static void N0269()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    for (int i = 1234567000; i <= 1234568000; i++) {
      localStatement.executeUpdate("insert into mxtab values(:i)");
      localStatement.executeUpdate("update mxtab set e_num=987654321");
    }

    for (int i = 1234567000; i <= 1234568000; i++) {
      localStatement.executeUpdate("insert into mptab values(:i)");
      localStatement.executeUpdate("update mptab set e_num=123654789");
    }
  }

  public static void N0274()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("CREATE PROCEDURE SPJTEST(VARCHAR(50), OUT VARCHAR(50)) EXTERNAL NAME 'Procs.N0200(java.lang.String,java.lang.String[])' EXTERNAL PATH 'spjcall' LANGUAGE JAVA PARAMETER STYLE JAVA CONTAINS SQL NO ISOLATE");
  }

  public static void N0278()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("drop procedure N0278");
    localStatement.executeUpdate("CREATE PROCEDURE N0278() EXTERNAL NAME 'hp2004.N0278' EXTERNAL PATH 'spjcall' LANGUAGE JAVA PARAMETER STYLE JAVA CONTAINS SQL NO ISOLATE");
  }

  public static void N0279()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("drop procedure N0001");
    localStatement.executeUpdate("call N0001()");
  }

  public static void N0280()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    for (int i = 1234560000; i <= 1234562000; i++) {
      localStatement.executeUpdate("delete from testtab");
      localStatement.executeUpdate("insert into testtab values('AAA Computers', 1234567890, 'San Francisco', 'programmer',  123456789,  32766, date '2001-10-31',  time '10:10:10', timestamp '2001-10-10 10:10:10.00', 123456789987654321, 3.40E+37, 3.0125E+18, 1.78145E+75, 8765432.45678,  8765478.56895,  987654321.0,  123456789.0 )");
    }

    localStatement.executeUpdate("control query default POS 'OFF'");
    localStatement.executeUpdate("control query default DDL_DEFAULT_LOCATIONS ''");
    localStatement.executeUpdate("create table spj  like testtab");
    localStatement.executeUpdate("create table spj1 like spj");
    localStatement.executeUpdate("create table spj2 like spj1");
    localStatement.executeUpdate("create table spj3 like spj2");
    localStatement.executeUpdate("create table spj4 like spj3");
    localStatement.executeUpdate("create table spj5 like spj4");
    localStatement.executeUpdate("create table spj6 like spj5");
    localStatement.executeUpdate("create table spj7 like spj6");
    localStatement.executeUpdate("create table spj8 like spj7");
    localStatement.executeUpdate("create table spj9 like spj8");
    localStatement.executeUpdate("create table spj10 like spj9");

    localStatement.executeUpdate("drop table spj");
    localStatement.executeUpdate("drop table spj1");
    localStatement.executeUpdate("drop table spj2");
    localStatement.executeUpdate("drop table spj3");
    localStatement.executeUpdate("drop table spj4");
    localStatement.executeUpdate("drop table spj5");
    localStatement.executeUpdate("drop table spj6");
    localStatement.executeUpdate("drop table spj7");
    localStatement.executeUpdate("drop table spj8");
    localStatement.executeUpdate("drop table spj9");
    localStatement.executeUpdate("drop table spj10");
  }

  public static void N0281()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("control query default DDL_DEFAULT_LOCATIONS ''");
    localStatement.executeUpdate("create table ttab(ename varchar(50) not null primary key)");
    localStatement.executeUpdate("create trigger spjtrig BEFORE INSERT ON ttab signal sqlstate 's9999' ('Can not insert')");
  }

  public static void N0282()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("control query default DDL_DEFAULT_LOCATIONS ''");
    localStatement.executeUpdate("create table ttab(ename varchar(50) not null primary key)");
    localStatement.executeUpdate("create trigger spjtrig BEFORE INSERT ON ttab signal sqlstate 's9999' ('Can not insert')");

    localStatement.executeUpdate("drop trigger spjtrig");
    localStatement.executeUpdate("drop table ttab");
  }

  public static void N0283()
    throws Exception
  {
    Connection localConnection = null;

    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    localStatement.executeUpdate("control query default DDL_DEFAULT_LOCATIONS ''");

    localStatement.executeUpdate("create table T002A (col1 char(5)   UPSHIFT    no default not null, col2 numeric (6) unsigned no default not null, PRIMARY KEY (col1) NOT DROPPABLE) STORE BY PRIMARY KEY");

    localStatement.executeUpdate("create table T002B (col3 char(5)   UPSHIFT    no default not null primary key, col4 varchar(2)   no default not null, FOREIGN KEY (col3) REFERENCES T002A(col1))");

    localStatement.executeUpdate("create table T002C (col3 char(5)   UPSHIFT    no default not null, col4 varchar(2)   no default not null, PRIMARY KEY (col3) NOT DROPPABLE, CONSTRAINT C2 FOREIGN KEY (col3) REFERENCES T002A(col1))");
  }

  public static void N0284(String paramString1, String paramString2, String paramString3, String paramString4, String paramString5, String paramString6, String paramString7, String paramString8, String paramString9, String paramString10, String paramString11, String paramString12, String paramString13, String paramString14, String paramString15, String paramString16, String paramString17, String paramString18, String paramString19, String paramString20, String[] paramArrayOfString1, String[] paramArrayOfString2, String[] paramArrayOfString3, String[] paramArrayOfString4, String[] paramArrayOfString5, String[] paramArrayOfString6, String[] paramArrayOfString7, String[] paramArrayOfString8, String[] paramArrayOfString9, String[] paramArrayOfString10, String[] paramArrayOfString11, String[] paramArrayOfString12, String[] paramArrayOfString13, String[] paramArrayOfString14, String[] paramArrayOfString15, String[] paramArrayOfString16, String[] paramArrayOfString17, String[] paramArrayOfString18, String[] paramArrayOfString19, String[] paramArrayOfString20)
    throws Exception
  {
    Connection localConnection = null;

    String str = "jdbc:default:connection";

    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();

    ResultSet localResultSet = localStatement.executeQuery("select spj1.e_name, spj2.e_long, spj3.e_float, spj4.e_real, spj5.e_double, spj6.e_short, spj7.e_nume, spj8.e_deci, spj9.e_nume, spj10.e_deci, spj11.e_nume, spj12.e_deci, spj13.e_time, spj14.e_tstamp, spj15.e_char, spj16.e_date1, spj17.e_time1, spj18.e_tstamp1, spj19.e_vchar, spj20.e_char1 from spj1, spj2,spj3, spj4,spj5, spj6,spj7, spj8,spj9, spj10,spj11,spj12, spj13, spj14,spj15, spj16,spj17, spj18, spj19, spj20");

    localResultSet.next();
    paramString1 = localResultSet.getString(1);
    paramString2 = localResultSet.getString(2);
    paramString3 = localResultSet.getString(3);
    paramString4 = localResultSet.getString(4);
    paramString5 = localResultSet.getString(5);
    paramString6 = localResultSet.getString(6);
    paramString7 = localResultSet.getString(7);
    paramString8 = localResultSet.getString(8);
    paramString9 = localResultSet.getString(9);
    paramString10 = localResultSet.getString(10);
    paramString11 = localResultSet.getString(11);
    paramString12 = localResultSet.getString(12);
    paramString13 = localResultSet.getString(13);
    paramString14 = localResultSet.getString(14);
    paramString15 = localResultSet.getString(15);
    paramString16 = localResultSet.getString(16);
    paramString17 = localResultSet.getString(17);
    paramString18 = localResultSet.getString(18);
    paramString19 = localResultSet.getString(19);
    paramString20 = localResultSet.getString(20);

    paramArrayOfString1[0] = paramString1;
    paramArrayOfString2[0] = paramString2;
    paramArrayOfString3[0] = paramString3;
    paramArrayOfString4[0] = paramString4;
    paramArrayOfString5[0] = paramString5;
    paramArrayOfString6[0] = paramString6;
    paramArrayOfString7[0] = paramString7;
    paramArrayOfString8[0] = paramString8;
    paramArrayOfString9[0] = paramString9;
    paramArrayOfString10[0] = paramString10;
    paramArrayOfString11[0] = paramString11;
    paramArrayOfString12[0] = paramString12;
    paramArrayOfString13[0] = paramString13;
    paramArrayOfString14[0] = paramString14;
    paramArrayOfString15[0] = paramString15;
    paramArrayOfString16[0] = paramString16;
    paramArrayOfString17[0] = paramString17;
    paramArrayOfString18[0] = paramString18;
    paramArrayOfString19[0] = paramString19;
    paramArrayOfString20[0] = paramString20;
  }
}
