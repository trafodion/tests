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

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.LineNumberReader;
import java.io.PrintStream;
import java.math.BigDecimal;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Time;
import java.sql.Timestamp;

public class Spjqa
{
  public static void sop(String paramString)
  {
    System.out.println(paramString);
  }

  public static void N1320(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localConnection.setAutoCommit(false);
      localStatement.executeUpdate("create table qatab( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into qatab values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      Thread.sleep(30000L);
      localStatement.executeUpdate("update qatab set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',    e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0 ");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from qatab");
      System.err.println("Row deleted successfully");
      localConnection.commit();
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1321(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("drop table qatab");
      System.err.println("Table dropped successfully");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1322(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("create table sptab0( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab0");
      System.err.println("Table1 dropped successfully");
      localStatement.executeUpdate("create table sptab1( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab1");
      System.err.println("Table2 dropped successfully");
      localStatement.executeUpdate("create table sptab2( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab2");
      System.err.println("Table3 dropped successfully");
      localStatement.executeUpdate("create table sptab3( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab3");
      System.err.println("Table4 dropped successfully");
      localStatement.executeUpdate("create table sptab4( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab4");
      System.err.println("Table5 dropped successfully");
      localStatement.executeUpdate("create table sptab5( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab5");
      System.err.println("Table6 dropped successfully");
      localStatement.executeUpdate("create table sptab6( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab6");
      System.err.println("Table7 dropped successfully");
      localStatement.executeUpdate("create table sptab7( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab7");
      System.err.println("Table8 dropped successfully");
      localStatement.executeUpdate("create table sptab8( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab8");
      System.err.println("Table9 dropped successfully");
      localStatement.executeUpdate("create table sptab9( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab9");
      System.err.println("Table10 dropped successfully");
      localStatement.executeUpdate("create table sptab10( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab10");
      System.err.println("Table11 dropped successfully");
      localStatement.executeUpdate("create table sptab11( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab11");
      System.err.println("Table11 dropped successfully");
      localStatement.executeUpdate("create table sptab12( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab12");
      System.err.println("Table12 dropped successfully");
      localStatement.executeUpdate("create table sptab13( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab13");
      System.err.println("Table13 dropped successfully");
      localStatement.executeUpdate("create table sptab14( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab14");
      System.err.println("Table14 dropped successfully");
      localStatement.executeUpdate("create table sptab15( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab15");
      System.err.println("Table15 dropped successfully");
      localStatement.executeUpdate("create table sptab16( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab16");
      System.err.println("Table16 dropped successfully");
      localStatement.executeUpdate("create table sptab17( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab17");
      System.err.println("Table17 dropped successfully");
      localStatement.executeUpdate("create table sptab18( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab18");
      System.err.println("Table18 dropped successfully");
      localStatement.executeUpdate("create table sptab19( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab19");
      System.err.println("Table19 dropped successfully");
      localStatement.executeUpdate("create table sptab20( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table sptab20");
      System.err.println("Table20 dropped successfully");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1323(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("create table nstab( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',    e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab");
      System.err.println("Table1 dropped successfully");
      localStatement.executeUpdate("create table nstab1( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab1 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab1 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab1 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',   e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab1");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab1");
      System.err.println("Table2 dropped successfully");
      localStatement.executeUpdate("create table nstab2( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab2 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab2 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab2 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',   e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab2");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab2");
      System.err.println("Table3 dropped successfully");
      localStatement.executeUpdate("create table nstab3( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab3 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab3 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab3 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',   e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab3");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab3");
      System.err.println("Table4 dropped successfully");
      localStatement.executeUpdate("create table nstab4( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab4 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab4 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab4 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',   e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab4");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab4");
      System.err.println("Table5 dropped successfully");
      localStatement.executeUpdate("create table nstab5( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab5 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab5 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab5 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',   e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab5");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab5");
      System.err.println("Table6 dropped successfully");
      localStatement.executeUpdate("create table nstab6( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab6 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab6 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab6 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',   e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab6");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab6");
      System.err.println("Table7 dropped successfully");
      localStatement.executeUpdate("create table nstab7( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab7 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab7 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab7 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',   e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab7");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab7");
      System.err.println("Table8 dropped successfully");
      localStatement.executeUpdate("create table nstab8( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab8 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab8 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab8 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',   e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab8");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab8");
      System.err.println("Table9 dropped successfully");
      localStatement.executeUpdate("create table nstab9( e_name varchar(20) not null, e_num int not null, e_city char(15),   e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab9 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab9 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab9 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',   e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab9");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab9");
      System.err.println("Table10 dropped successfully");
      localStatement.executeUpdate("create table nstab10( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab10 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab10 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab10 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab10");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab10");
      System.err.println("Table11 dropped successfully");
      localStatement.executeUpdate("create table nstab11( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab11 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab11 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab11 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab11");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab11");
      System.err.println("Table11 dropped successfully");
      localStatement.executeUpdate("create table nstab12( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab12 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab12 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab12 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab12");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab12");
      System.err.println("Table12 dropped successfully");
      localStatement.executeUpdate("create table nstab13( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab13 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab13 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab13 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab13");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab13");
      System.err.println("Table13 dropped successfully");
      localStatement.executeUpdate("create table nstab14( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab14 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab14 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab14 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab14");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab14");
      System.err.println("Table14 dropped successfully");
      localStatement.executeUpdate("create table nstab15( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab15 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab15 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab15 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab15");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab15");
      System.err.println("Table15 dropped successfully");
      localStatement.executeUpdate("create table nstab16( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab16 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab16 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab16 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab16");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab16");
      System.err.println("Table16 dropped successfully");
      localStatement.executeUpdate("create table nstab17( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab17 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab17 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab17 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab17");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab17");
      System.err.println("Table17 dropped successfully");
      localStatement.executeUpdate("create table nstab18( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab18 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab18 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab18 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab18");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab18");
      System.err.println("Table18 dropped successfully");
      localStatement.executeUpdate("create table nstab19( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab19 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab19 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab19 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab19");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab19");
      System.err.println("Table19 dropped successfully");
      localStatement.executeUpdate("create table nstab20( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into nstab20 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update nstab20 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nstab20 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("delete from nstab20");
      System.err.println("Row deleted successfully");
      localStatement.executeUpdate("drop table nstab20");
      System.err.println("Table20 dropped successfully");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1532(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("insert into testtab values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("Rows are inserting successfully");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1327(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("CREATE TABLE spjaddr (id NUMBER CONSTRAINT addresses_pk PRIMARY KEY, customer_id  NUMBER CONSTRAINT addresses_fk_customers REFERENCES customers(id), street       VARCHAR2(255) NOT NULL, city VARCHAR2(255) NOT NULL, state CHAR(2) NOT NULL, country VARCHAR2(255) NOT NULL)");
      System.err.println("spj_add1 Table Created successfully");
      localStatement.executeUpdate("drop table spjaddr");
      System.err.println("Table dropped successfully");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1326()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("create table  tantab( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("insert into tantab values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      System.err.println("First row inserted successfully");
      localStatement.executeUpdate("update  tantab set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0 ");
      System.err.println("Table Updated successfully");
      localStatement.executeUpdate("drop table tantab");
      System.err.println("Table Dropped successfully");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1329(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("create table javatab0( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab0");
      System.err.println("Table1 dropped successfully");
      localStatement.executeUpdate("create table javatab1( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab1");
      System.err.println("Table2 dropped successfully");
      localStatement.executeUpdate("create table javatab2( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab2");
      System.err.println("Table3 dropped successfully");
      localStatement.executeUpdate("create table javatab3( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab3");
      System.err.println("Table4 dropped successfully");
      localStatement.executeUpdate("create table javatab4( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab4");
      System.err.println("Table5 dropped successfully");
      localStatement.executeUpdate("create table javatab5( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab5");
      System.err.println("Table6 dropped successfully");
      localStatement.executeUpdate("create table javatab6( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab6");
      System.err.println("Table7 dropped successfully");
      localStatement.executeUpdate("create table javatab7( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab7");
      System.err.println("Table8 dropped successfully");
      localStatement.executeUpdate("create table javatab8( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab8");
      System.err.println("Table9 dropped successfully");
      localStatement.executeUpdate("create table javatab9( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab9");
      System.err.println("Table10 dropped successfully");
      localStatement.executeUpdate("create table javatab10( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab10");
      System.err.println("Table11 dropped successfully");
      localStatement.executeUpdate("create table javatab11( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab11");
      System.err.println("Table11 dropped successfully");
      localStatement.executeUpdate("create table javatab12( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab12");
      System.err.println("Table12 dropped successfully");
      localStatement.executeUpdate("create table javatab13( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab13");
      System.err.println("Table13 dropped successfully");
      localStatement.executeUpdate("create table javatab14( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab14");
      System.err.println("Table14 dropped successfully");
      localStatement.executeUpdate("create table javatab15( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab15");
      System.err.println("Table15 dropped successfully");
      localStatement.executeUpdate("create table javatab16( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab16");
      System.err.println("Table16 dropped successfully");
      localStatement.executeUpdate("create table javatab17( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab17");
      System.err.println("Table17 dropped successfully");
      localStatement.executeUpdate("create table javatab18( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab18");
      System.err.println("Table18 dropped successfully");
      localStatement.executeUpdate("create table javatab19( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab19");
      System.err.println("Table19 dropped successfully");
      localStatement.executeUpdate("create table javatab22( e_name varchar(20) not null, e_num int not null, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Table created successfully");
      localStatement.executeUpdate("drop table javatab22");
      System.err.println("Table20 dropped successfully");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1331(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("create table nsdtab0( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab1( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab2( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab3( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab4( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab5( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab6( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab7( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab8( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab9( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab10( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab11( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab12( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab13( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab14( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab15( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab16( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab17( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab18( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab19( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab20( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab21( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab22( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab23( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab24( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab25( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab26( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab27( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab28( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab29( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab30( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab31( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab32( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab33( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab34( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab35( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab36( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab37( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab38( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab39( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab40( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab41( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab42( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab43( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab44( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab45( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab46( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab47( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab48( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab49( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab50( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab51( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab52( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab53( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab54( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab55( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab56( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab57( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab58( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab59( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab60( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab61( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab62( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.close();
      localConnection.close();
      System.err.println("All the tables are  created successfully");
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1332(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("drop table nsdtab0");
      localStatement.executeUpdate("drop table nsdtab1");
      localStatement.executeUpdate("drop table nsdtab2");
      localStatement.executeUpdate("drop table nsdtab3");
      localStatement.executeUpdate("drop table nsdtab4");
      localStatement.executeUpdate("drop table nsdtab5");
      localStatement.executeUpdate("drop table nsdtab6");
      localStatement.executeUpdate("drop table nsdtab7");
      localStatement.executeUpdate("drop table nsdtab8");
      localStatement.executeUpdate("drop table nsdtab9");
      localStatement.executeUpdate("drop table nsdtab10");
      localStatement.executeUpdate("drop table nsdtab11");
      localStatement.executeUpdate("drop table nsdtab12");
      localStatement.executeUpdate("drop table nsdtab13");
      localStatement.executeUpdate("drop table nsdtab14");
      localStatement.executeUpdate("drop table nsdtab15");
      localStatement.executeUpdate("drop table nsdtab16");
      localStatement.executeUpdate("drop table nsdtab17");
      localStatement.executeUpdate("drop table nsdtab18");
      localStatement.executeUpdate("drop table nsdtab19");
      localStatement.executeUpdate("drop table nsdtab20");
      localStatement.executeUpdate("drop table nsdtab21");
      localStatement.executeUpdate("drop table nsdtab22");
      localStatement.executeUpdate("drop table nsdtab23");
      localStatement.executeUpdate("drop table nsdtab24");
      localStatement.executeUpdate("drop table nsdtab25");
      localStatement.executeUpdate("drop table nsdtab26");
      localStatement.executeUpdate("drop table nsdtab27");
      localStatement.executeUpdate("drop table nsdtab28");
      localStatement.executeUpdate("drop table nsdtab29");
      localStatement.executeUpdate("drop table nsdtab30");
      localStatement.executeUpdate("drop table nsdtab31");
      localStatement.executeUpdate("drop table nsdtab32");
      localStatement.executeUpdate("drop table nsdtab33");
      localStatement.executeUpdate("drop table nsdtab34");
      localStatement.executeUpdate("drop table nsdtab35");
      localStatement.executeUpdate("drop table nsdtab36");
      localStatement.executeUpdate("drop table nsdtab37");
      localStatement.executeUpdate("drop table nsdtab38");
      localStatement.executeUpdate("drop table nsdtab39");
      localStatement.executeUpdate("drop table nsdtab40");
      localStatement.executeUpdate("drop table nsdtab41");
      localStatement.executeUpdate("drop table nsdtab42");
      localStatement.executeUpdate("drop table nsdtab43");
      localStatement.executeUpdate("drop table nsdtab44");
      localStatement.executeUpdate("drop table nsdtab45");
      localStatement.executeUpdate("drop table nsdtab46");
      localStatement.executeUpdate("drop table nsdtab47");
      localStatement.executeUpdate("drop table nsdtab48");
      localStatement.executeUpdate("drop table nsdtab49");
      localStatement.executeUpdate("drop table nsdtab50");
      localStatement.executeUpdate("drop table nsdtab51");
      localStatement.executeUpdate("drop table nsdtab52");
      localStatement.executeUpdate("drop table nsdtab53");
      localStatement.executeUpdate("drop table nsdtab54");
      localStatement.executeUpdate("drop table nsdtab55");
      localStatement.executeUpdate("drop table nsdtab56");
      localStatement.executeUpdate("drop table nsdtab57");
      localStatement.executeUpdate("drop table nsdtab58");
      localStatement.executeUpdate("drop table nsdtab59");
      localStatement.executeUpdate("drop table nsdtab60");
      localStatement.executeUpdate("drop table nsdtab61");
      localStatement.executeUpdate("drop table nsdtab62");
      localStatement.close();
      localConnection.close();
      System.err.println("All the tables are dropped successfully");
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1333(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("insert into nsdtab0 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab0 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab0 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab1 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab1 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab1 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab2 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab2 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab2 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab3 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab3 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab3 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab4 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab4 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab4 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab5 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab5 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab5 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab6 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab6 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab6 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab7 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab7 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab7 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab8 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab8 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab8 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab9 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab9 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab9 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab10 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab10 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab10 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab11 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab11 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab11 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab12 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab12 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab12 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab13 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab13 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab13 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab14 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab14 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab14 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab15 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab15 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab15 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab16 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab16 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab16 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab17 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab17 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab17 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab18 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab18 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab18 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab19 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab19 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab19 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("insert into nsdtab20 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("update nsdtab20 set e_name = 'BBB Computers' where (e_name = 'AAA Computers')");
      localStatement.executeUpdate("update nsdtab20 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      System.err.println("Rows are inserted and updated successfully");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1334(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("create table nsdtab0( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab1( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab2( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab3( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab4( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab5( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab6( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab7( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab8( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab9( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.executeUpdate("create table nsdtab10( e_name varchar(20) not null, e_num int not null, e_city char(15), e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      System.err.println("Executing procedure N1335");
      CallableStatement localCallableStatement = localConnection.prepareCall("{call N1335(?,?)}");
      localCallableStatement.setString(1, "Smith");
      localCallableStatement.registerOutParameter(2, 12);
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1335(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("drop table nsdtab0");
      localStatement.executeUpdate("drop table nsdtab1");
      localStatement.executeUpdate("drop table nsdtab2");
      localStatement.executeUpdate("drop table nsdtab3");
      localStatement.executeUpdate("drop table nsdtab4");
      localStatement.executeUpdate("drop table nsdtab5");
      localStatement.executeUpdate("drop table nsdtab6");
      localStatement.executeUpdate("drop table nsdtab7");
      localStatement.executeUpdate("drop table nsdtab8");
      localStatement.executeUpdate("drop table nsdtab9");
      localStatement.executeUpdate("drop table nsdtab10");
      System.err.println("Executing procedure N1334");
      CallableStatement localCallableStatement = localConnection.prepareCall("{call N1334(?,?)}");
      localCallableStatement.setString(1, "Smith");
      localCallableStatement.registerOutParameter(2, 12);
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1336(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement();
    sop("Inserting sql(hello)");
    localStatement.executeUpdate("insert into testtab values('AAA Computers', 1234567890, 'San Francisco', 'programmer', 123456789, 32766, date '2001-10-31',  time '10:10:10',  timestamp '2001-10-10 10:10:10.00', 123456789987654321, 3.40E+37, 3.0125E+18, 1.78145E+75, 8765432.45678,  8765478.56895,  987654321.0,  123456789.0)");
    ResultSet localResultSet = localStatement.executeQuery("select e_title from testtab");
    localResultSet.next();
    paramString = localResultSet.getString(1);
    paramArrayOfString[0] = paramString;
    localStatement.close();
    localConnection.close();
  }

  public static void N1337(String paramString, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
  }

  public static void N1338(String paramString, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
  }

  public static void N1339(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("insert into nsdtab0 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab1 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab2 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab3 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab4 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab5 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab6 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab7 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab8 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab9 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab10 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab11 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab12 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab13 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab14 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab15 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab16 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab17 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab18 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab19 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab20 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab21 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab22 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab23 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab24 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab25 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab26 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab27 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab28 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab29 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab30 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab31 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab32 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab33 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab34 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab35 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab36 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab37 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab38 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab39 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab40 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab41 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab42 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab43 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab44 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab45 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab46 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab47 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab48 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab49 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab50 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab51 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab52 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab53 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab54 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab55 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab56 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab57 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab58 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab59 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab60 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab61 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.executeUpdate("insert into nsdtab62 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
      localStatement.close();
      localConnection.close();
      System.err.println("All the rows are  inserted successfully");
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1340(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("update nsdtab0 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',    e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab1 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab2 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab3 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab4 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab5 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab6 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab7 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab8 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab9 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab10 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab11 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab12 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab13 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab14 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab15 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab16 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab17 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab18 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab19 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab20 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab21 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab22 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab23 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab24 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab25 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab26 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab27 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab28 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab29 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab30 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab31 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab32 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab33 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab34 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab35 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab36 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab37 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab38 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab39 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab40 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab41 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab42 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab43 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab44 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab45 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab46 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab47 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab48 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab49 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab50 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab51 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab52 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab53 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab54 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab55 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab56 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab57 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab58 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab59 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab60 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab61 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("update nsdtab62 set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31', e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.close();
      localConnection.close();
      System.err.println("All the rows are updated successfully");
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1341(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    try
    {
      localStatement.executeUpdate("delete from nsdtab0");
      localStatement.executeUpdate("delete from nsdtab1");
      localStatement.executeUpdate("delete from nsdtab2");
      localStatement.executeUpdate("delete from nsdtab3");
      localStatement.executeUpdate("delete from nsdtab4");
      localStatement.executeUpdate("delete from nsdtab5");
      localStatement.executeUpdate("delete from nsdtab6");
      localStatement.executeUpdate("delete from nsdtab7");
      localStatement.executeUpdate("delete from nsdtab8");
      localStatement.executeUpdate("delete from nsdtab9");
      localStatement.executeUpdate("delete from nsdtab10");
      localStatement.executeUpdate("delete from nsdtab11");
      localStatement.executeUpdate("delete from nsdtab12");
      localStatement.executeUpdate("delete from nsdtab13");
      localStatement.executeUpdate("delete from nsdtab14");
      localStatement.executeUpdate("delete from nsdtab15");
      localStatement.executeUpdate("delete from nsdtab16");
      localStatement.executeUpdate("delete from nsdtab17");
      localStatement.executeUpdate("delete from nsdtab18");
      localStatement.executeUpdate("delete from nsdtab19");
      localStatement.executeUpdate("delete from nsdtab20");
      localStatement.executeUpdate("delete from nsdtab21");
      localStatement.executeUpdate("delete from nsdtab22");
      localStatement.executeUpdate("delete from nsdtab23");
      localStatement.executeUpdate("delete from nsdtab24");
      localStatement.executeUpdate("delete from nsdtab25");
      localStatement.executeUpdate("delete from nsdtab26");
      localStatement.executeUpdate("delete from nsdtab27");
      localStatement.executeUpdate("delete from nsdtab28");
      localStatement.executeUpdate("delete from nsdtab29");
      localStatement.executeUpdate("delete from nsdtab30");
      localStatement.executeUpdate("delete from nsdtab31");
      localStatement.executeUpdate("delete from nsdtab32");
      localStatement.executeUpdate("delete from nsdtab33");
      localStatement.executeUpdate("delete from nsdtab34");
      localStatement.executeUpdate("delete from nsdtab35");
      localStatement.executeUpdate("delete from nsdtab36");
      localStatement.executeUpdate("delete from nsdtab37");
      localStatement.executeUpdate("delete from nsdtab38");
      localStatement.executeUpdate("delete from nsdtab39");
      localStatement.executeUpdate("delete from nsdtab40");
      localStatement.executeUpdate("delete from nsdtab41");
      localStatement.executeUpdate("delete from nsdtab42");
      localStatement.executeUpdate("delete from nsdtab43");
      localStatement.executeUpdate("delete from nsdtab44");
      localStatement.executeUpdate("delete from nsdtab45");
      localStatement.executeUpdate("delete from nsdtab46");
      localStatement.executeUpdate("delete from nsdtab47");
      localStatement.executeUpdate("delete from nsdtab48");
      localStatement.executeUpdate("delete from nsdtab49");
      localStatement.executeUpdate("delete from nsdtab50");
      localStatement.executeUpdate("delete from nsdtab51");
      localStatement.executeUpdate("delete from nsdtab52");
      localStatement.executeUpdate("delete from nsdtab53");
      localStatement.executeUpdate("delete from nsdtab54");
      localStatement.executeUpdate("delete from nsdtab55");
      localStatement.executeUpdate("delete from nsdtab56");
      localStatement.executeUpdate("delete from nsdtab57");
      localStatement.executeUpdate("delete from nsdtab58");
      localStatement.executeUpdate("delete from nsdtab59");
      localStatement.executeUpdate("delete from nsdtab60");
      localStatement.executeUpdate("delete from nsdtab61");
      localStatement.executeUpdate("delete from nsdtab62");
      localStatement.close();
      localConnection.close();
      System.err.println("All the rows are deleted successfully");
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N9876(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("drop table sptab0");
    localStatement.executeUpdate("drop table sptab1");
    localStatement.executeUpdate("drop table sptab2");
    localStatement.executeUpdate("drop table sptab3");
    localStatement.executeUpdate("drop table sptab4");
    localStatement.executeUpdate("drop table sptab5");
    localStatement.executeUpdate("drop table sptab6");
    localStatement.executeUpdate("drop table sptab7");
    localStatement.executeUpdate("drop table sptab8");
    localStatement.executeUpdate("drop table sptab9");
    localStatement.executeUpdate("drop table sptab10");
    localStatement.executeUpdate("drop table sptab11");
    localStatement.executeUpdate("drop table sptab12");
    localStatement.executeUpdate("drop table sptab13");
    localStatement.executeUpdate("drop table sptab14");
    localStatement.executeUpdate("drop table sptab15");
    localStatement.executeUpdate("drop table sptab16");
    localStatement.executeUpdate("drop table sptab17");
    localStatement.executeUpdate("drop table sptab18");
    localStatement.executeUpdate("drop table sptab19");
    localStatement.executeUpdate("drop table sptab20");
    localStatement.close();
    localConnection.close();
    System.err.println("All the tables are dropped successfully");
  }

  public static void N1336A(int paramInt, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    try
    {
      PreparedStatement localPreparedStatement = localConnection.prepareStatement("insert into testtab values('AAA Computers', 1234567890, 'San Francisco', 'programmer', 123456789, 32766, date '2001-10-31',  time '10:10:10',  timestamp '2001-10-10 10:10:10.00', 123456789987654321, 3.40E+37, 3.0125E+18, 1.78145E+75, 8765432.45678,  8765478.56895,  987654321.0,  123456789.0)");
      localPreparedStatement.execute();
      localPreparedStatement.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Error: can not execute stored procedure");
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1336B(int paramInt, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    ResultSet localResultSet;
    try
    {
      Statement localStatement = localConnection.createStatement();
      localResultSet = localStatement.executeQuery("Select count(*) from testtab");
    }
    catch (SQLException localSQLException1)
    {
      System.out.println("Problem reading scale");
      SQLException localSQLException2 = localSQLException1.getNextException();
      for (; localSQLException2 != null; localSQLException2 = localSQLException1.getNextException()) {
        System.out.println("Message:" + localSQLException1.getMessage());
      }
      return;
    }
    try
    {
      localResultSet.next();
      paramInt = localResultSet.getInt(1);
      paramArrayOfInt[0] = paramInt;
    }
    catch (SQLException localSQLException3)
    {
      System.err.println("Sqlcode = " + localSQLException3.getErrorCode());
      System.err.println("Message = " + localSQLException3.getMessage());
      System.err.println("Sqlstate = " + localSQLException3.getSQLState());
      localSQLException3.printStackTrace();
    }
  }

  public static void N1336C(int paramInt, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    try
    {
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("delete from testtab");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1336D(int paramInt, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    try
    {
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("update testtab set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1336E(int paramInt, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    try
    {
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("insert into testtab values('AAA Computers', 1234567890, 'San Francisco', 'programmer', 123456789, 32766, date '2001-10-31',  time '10:10:10',  timestamp '2001-10-10 10:10:10.00', 123456789987654321, 3.40E+37, 3.0125E+18, 1.78145E+75, 8765432.45678,  8765478.56895,  987654321.0,  123456789.0)");
      localStatement.executeUpdate("update testtab set e_name = 'Hewlett Packard', e_num = 122121212, e_city = 'Los Angels', e_title = 'Business Analyst', e_salary = 13213235, e_code = 32321, e_date = date '2002-05-31',  e_time = time '12:45:45', e_tstamp =  timestamp '2002-08-15 12:15:15.00', e_long =   123456789987654321, e_float =  3.40E+35, e_real =  2.0125E+15, e_double =  1.78145E+69, e_numeric =    8765432.54321, e_decimal =  8765478.98765, e_numeric1 =  987654321.0, e_decimal1 =  123456789.0");
      localStatement.executeUpdate("delete from testtab");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1336F(int paramInt, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    try
    {
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("drop table testtab");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1336G(int paramInt, int[] paramArrayOfInt)
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    try
    {
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("create table testtab( e_name varchar(20) not null, e_num int not null, e_city char(15),  e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0))");
      localStatement.close();
      localConnection.close();
    }
    catch (SQLException localSQLException)
    {
      System.err.println("Sqlcode = " + localSQLException.getErrorCode());
      System.err.println("Message = " + localSQLException.getMessage());
      System.err.println("Sqlstate = " + localSQLException.getSQLState());
      localSQLException.printStackTrace();
    }
  }

  public static void N1505(Double paramDouble, Double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N1201(Float paramFloat, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramFloat.toString();
  }

  public static void N1166(long paramLong, BigDecimal[] paramArrayOfBigDecimal1, BigDecimal[] paramArrayOfBigDecimal2)
  {
    paramArrayOfBigDecimal2[0] = paramArrayOfBigDecimal1[0];
    paramArrayOfBigDecimal1[0] = new BigDecimal(paramLong);
  }

  public static void N0226A(String paramString1, int paramInt, String paramString2, String paramString3, BigDecimal paramBigDecimal1, short paramShort, Date paramDate, Time paramTime, Timestamp paramTimestamp, long paramLong, double paramDouble1, float paramFloat, double paramDouble2, BigDecimal paramBigDecimal2, BigDecimal paramBigDecimal3, BigDecimal paramBigDecimal4, BigDecimal paramBigDecimal5, String[] paramArrayOfString1, int[] paramArrayOfInt, String[] paramArrayOfString2, String[] paramArrayOfString3, BigDecimal[] paramArrayOfBigDecimal1, short[] paramArrayOfShort, Date[] paramArrayOfDate, Time[] paramArrayOfTime, Timestamp[] paramArrayOfTimestamp, long[] paramArrayOfLong, double[] paramArrayOfDouble1, float[] paramArrayOfFloat, double[] paramArrayOfDouble2, BigDecimal[] paramArrayOfBigDecimal2, BigDecimal[] paramArrayOfBigDecimal3, BigDecimal[] paramArrayOfBigDecimal4, BigDecimal[] paramArrayOfBigDecimal5)
  {
    paramArrayOfString1[0] = paramString1;
    paramArrayOfInt[0] = paramInt;
    paramArrayOfString2[0] = paramString2;
    paramArrayOfString3[0] = paramString3;
    paramArrayOfBigDecimal1[0] = paramBigDecimal1;
    paramArrayOfShort[0] = paramShort;
    paramArrayOfDate[0] = paramDate;
    paramArrayOfTime[0] = paramTime;
    paramArrayOfTimestamp[0] = paramTimestamp;
    paramArrayOfLong[0] = paramLong;
    paramArrayOfDouble1[0] = paramDouble1;
    paramArrayOfFloat[0] = paramFloat;
    paramArrayOfDouble2[0] = paramDouble2;
    paramArrayOfBigDecimal2[0] = paramBigDecimal2;
    paramArrayOfBigDecimal3[0] = paramBigDecimal3;
    paramArrayOfBigDecimal4[0] = paramBigDecimal4;
    paramArrayOfBigDecimal5[0] = paramBigDecimal5;
  }

  public static void NA014(short paramShort, Integer[] paramArrayOfInteger)
  {
    paramArrayOfInteger[0] = new Integer(paramShort);
  }

  public static void NA015(Date paramDate, Time paramTime, Timestamp paramTimestamp, Date[] paramArrayOfDate, Time[] paramArrayOfTime, Timestamp[] paramArrayOfTimestamp)
  {
    paramArrayOfDate[0] = paramDate;
    paramArrayOfTime[0] = paramTime;
    paramArrayOfTimestamp[0] = paramTimestamp;
  }

  public static void NA016(int paramInt, Integer[] paramArrayOfInteger)
  {
    paramArrayOfInteger[0] = new Integer(paramInt);
  }

  public static void NA17()
  {
    System.exit(1);
  }

  public static void NA18(long paramLong)
  {
    System.out.println("INOUT1 Value    :" + paramLong);
  }

  public static void NA19(long[] paramArrayOfLong)
  {
    System.out.println("INOUT1 Value    :" + paramArrayOfLong[0]);
  }

  public static void S0749(String paramString)
  {
    System.out.println("IN Value    :" + paramString);
  }

  public static void S0750(long[] paramArrayOfLong)
  {
    System.out.println("OUT1 Value    :" + paramArrayOfLong[0]);
  }

  public static void NA20(long[] paramArrayOfLong)
  {
    System.out.println("OUT1 Value    :" + paramArrayOfLong[0]);
  }

  public static void S0751(String paramString, String[] paramArrayOfString1, String[] paramArrayOfString2)
  {
    paramArrayOfString2[0] = paramArrayOfString1[0];
    paramArrayOfString1[0] = paramString;
  }

  public static void S0851(String paramString, String[] paramArrayOfString1, String[] paramArrayOfString2)
  {
    paramArrayOfString2[0] = paramArrayOfString1[0];
    paramArrayOfString1[0] = paramString;
  }

  public static void N1500(String paramString, String[] paramArrayOfString)
  {
    try
    {
      DataInputStream localDataInputStream = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString)));
      double d1 = localDataInputStream.readDouble();
      String str1 = localDataInputStream.readUTF();
      double d2 = localDataInputStream.readDouble();
      String str2 = localDataInputStream.readUTF();
      DataOutputStream localDataOutputStream = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(paramArrayOfString[0])));
      localDataOutputStream.writeDouble(d1);
      localDataOutputStream.writeUTF(str1);
      localDataOutputStream.writeDouble(d2);
      localDataOutputStream.writeUTF(str2);
      localDataOutputStream.close();
      paramArrayOfString[0] = paramString;
    }
    catch (FileNotFoundException localFileNotFoundException)
    {
      System.err.println("File Not Found: " + paramString);
    }
    catch (IOException localIOException)
    {
      localIOException.printStackTrace();
    }
  }

  public static void N1525()
  {
    try
    {
      FileInputStream localFileInputStream = new FileInputStream("Encode.in.txt");
      InputStreamReader localInputStreamReader = new InputStreamReader(localFileInputStream);
      LineNumberReader localLineNumberReader = new LineNumberReader(localInputStreamReader);
      FileOutputStream localFileOutputStream = new FileOutputStream("Encode.out.txt");
      PrintStream localPrintStream = new PrintStream(localFileOutputStream);
      Connection localConnection = DriverManager.getConnection("jdbc:default:connection");
      for (String str1 = localLineNumberReader.readLine(); str1 != null; str1 = localLineNumberReader.readLine())
      {
        Statement localStatement = localConnection.createStatement();
        localStatement.executeUpdate("DELETE FROM ACCOUNT");
        localStatement.close();
        CallableStatement localCallableStatement = localConnection.prepareCall("CALL N0500(?, ?)");
        localCallableStatement.setString(1, str1);
        localCallableStatement.setInt(2, 1);
        localCallableStatement.execute();
        localCallableStatement.close();
        localCallableStatement = localConnection.prepareCall("CALL N0501(?, ?)");
        localCallableStatement.registerOutParameter(1, 1);
        localCallableStatement.registerOutParameter(2, 4);
        localCallableStatement.execute();
        String str2 = localCallableStatement.getString(1);
        localCallableStatement.close();
        localPrintStream.println(str2);
      }

      localConnection.close();
      localFileInputStream.close();
      localFileOutputStream.close();
    }
    catch (Exception localException)
    {
      System.err.println(localException);
      localException.printStackTrace();
    }
  }

  public static void S0505(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("create table newtab(e_date date) no partition");
    localStatement.executeUpdate("create table mytab like newtab");
    localStatement.executeUpdate("insert into mytab(select * from newtab)");
    localStatement.executeUpdate("alter table mytab add e_time time");
    localStatement.executeUpdate("insert into mytab(e_date,e_time) values(current_date,current_time)");
    ResultSet localResultSet = localStatement.executeQuery("select e_date from mytab");
    localResultSet.next();
    paramString = localResultSet.getString(1);
    paramArrayOfString[0] = paramString;
    localStatement.executeUpdate("drop table mytab");
    localStatement.executeUpdate("drop table newtab");
    localStatement.close();
    localConnection.close();
  }

  public static void N4321()
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
    }
    catch (Exception localException)
    {
      localException.printStackTrace();
    }
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("create table w2( e_name varchar(20) not null, e_num int not null not droppable, e_city char(15),    e_title varchar(20), e_salary numeric(11,2), e_code SMALLINT, e_date date, e_time time,  e_tstamp timestamp, e_long largeint, e_float float,  e_real real, e_double double precision,  e_numeric numeric(12,5), e_decimal decimal(12,5),e_numeric1 numeric(9,0), e_decimal1 decimal(9,0), primary key(e_num))");
    localStatement.executeUpdate("insert into w2 values('AAA Computers',1234567890,'San Francisco','programmer',123456789,32766,date '2001-10-31',time '10:10:10',timestamp '2001-10-10 10:10:10.00',123456789987654321,3.40E+37,3.0125E+18,1.78145E+75,8765432.45678,8765478.56895,987654321.0,123456789.0)");
  }
}
