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

import java.io.PrintStream;
import java.math.BigDecimal;
import java.sql.BatchUpdateException;
import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Savepoint;
import java.sql.Statement;
import java.sql.Time;
import java.sql.Timestamp;
import java.util.StringTokenizer;

public class spjrs
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void sop(String paramString)
  {
    System.out.println(paramString);
  }

  public static void N2503(String paramString, int[] paramArrayOfInt, ResultSet[] paramArrayOfResultSet)
  {
  }

  public static void N0999(int paramInt1, double paramDouble1, int[] paramArrayOfInt1, double[] paramArrayOfDouble1, int[] paramArrayOfInt2, double[] paramArrayOfDouble2, Timestamp paramTimestamp1, Date paramDate1, Timestamp[] paramArrayOfTimestamp1, Date[] paramArrayOfDate1, Timestamp[] paramArrayOfTimestamp2, Date[] paramArrayOfDate2, String paramString1, String paramString2, String[] paramArrayOfString1, String[] paramArrayOfString2, String[] paramArrayOfString3, String[] paramArrayOfString4, BigDecimal paramBigDecimal1, long paramLong1, BigDecimal[] paramArrayOfBigDecimal1, long[] paramArrayOfLong1, BigDecimal[] paramArrayOfBigDecimal2, long[] paramArrayOfLong2, float paramFloat1, short paramShort1, float[] paramArrayOfFloat1, short[] paramArrayOfShort1, float[] paramArrayOfFloat2, short[] paramArrayOfShort2, int paramInt2, double paramDouble2, int[] paramArrayOfInt3, double[] paramArrayOfDouble3, int[] paramArrayOfInt4, double[] paramArrayOfDouble4, Timestamp paramTimestamp2, Date paramDate2, Timestamp[] paramArrayOfTimestamp3, Date[] paramArrayOfDate3, Timestamp[] paramArrayOfTimestamp4, Date[] paramArrayOfDate4, String paramString3, String paramString4, String[] paramArrayOfString5, String[] paramArrayOfString6, String[] paramArrayOfString7, String[] paramArrayOfString8, BigDecimal paramBigDecimal2, long paramLong2, BigDecimal[] paramArrayOfBigDecimal3, long[] paramArrayOfLong3, BigDecimal[] paramArrayOfBigDecimal4, long[] paramArrayOfLong4, float paramFloat2, short paramShort2, float[] paramArrayOfFloat3, short[] paramArrayOfShort3, float[] paramArrayOfFloat4, short[] paramArrayOfShort4, int paramInt3, double paramDouble3, int[] paramArrayOfInt5, double[] paramArrayOfDouble5, int[] paramArrayOfInt6, double[] paramArrayOfDouble6, Timestamp paramTimestamp3, Date paramDate3, Timestamp[] paramArrayOfTimestamp5, Date[] paramArrayOfDate5, Timestamp[] paramArrayOfTimestamp6, Date[] paramArrayOfDate6, String paramString5, String paramString6, String[] paramArrayOfString9, String[] paramArrayOfString10, String[] paramArrayOfString11, String[] paramArrayOfString12, BigDecimal paramBigDecimal3, long paramLong3, BigDecimal[] paramArrayOfBigDecimal5, long[] paramArrayOfLong5, BigDecimal[] paramArrayOfBigDecimal6, long[] paramArrayOfLong6, float paramFloat3, short paramShort3, float[] paramArrayOfFloat5, short[] paramArrayOfShort5, float[] paramArrayOfFloat6, short[] paramArrayOfShort6, int paramInt4, double paramDouble4, int[] paramArrayOfInt7, double[] paramArrayOfDouble7, int[] paramArrayOfInt8, double[] paramArrayOfDouble8, Timestamp paramTimestamp4, Date paramDate4, Timestamp[] paramArrayOfTimestamp7, Date[] paramArrayOfDate7, Timestamp[] paramArrayOfTimestamp8, Date[] paramArrayOfDate8, String paramString7, String paramString8, String[] paramArrayOfString13, String[] paramArrayOfString14, String[] paramArrayOfString15, String[] paramArrayOfString16, BigDecimal paramBigDecimal4, long paramLong4, BigDecimal[] paramArrayOfBigDecimal7, long[] paramArrayOfLong7, BigDecimal[] paramArrayOfBigDecimal8, long[] paramArrayOfLong8, float paramFloat4, short paramShort4, float[] paramArrayOfFloat7, short[] paramArrayOfShort7, float[] paramArrayOfFloat8, short[] paramArrayOfShort8)
  {
    paramArrayOfInt1[0] = paramArrayOfInt2[0];
    paramArrayOfInt2[0] = paramInt1;

    paramArrayOfDouble1[0] = paramArrayOfDouble2[0];
    paramArrayOfDouble2[0] = paramDouble1;

    paramArrayOfTimestamp1[0] = paramArrayOfTimestamp2[0];
    paramArrayOfTimestamp2[0] = paramTimestamp1;

    paramArrayOfDate1[0] = paramArrayOfDate2[0];
    paramArrayOfDate2[0] = paramDate1;

    paramArrayOfString1[0] = paramArrayOfString3[0];
    paramArrayOfString3[0] = paramString1;

    paramArrayOfString2[0] = paramArrayOfString4[0];
    paramArrayOfString4[0] = paramString2;

    paramArrayOfBigDecimal1[0] = paramArrayOfBigDecimal2[0];
    paramArrayOfBigDecimal2[0] = paramBigDecimal1;

    paramArrayOfLong1[0] = paramArrayOfLong2[0];
    paramArrayOfLong2[0] = paramLong1;

    paramArrayOfFloat1[0] = paramArrayOfFloat2[0];
    paramArrayOfFloat2[0] = paramFloat1;

    paramArrayOfShort1[0] = paramArrayOfShort2[0];
    paramArrayOfShort2[0] = paramShort1;

    paramArrayOfInt3[0] = paramArrayOfInt4[0];
    paramArrayOfInt4[0] = paramInt2;

    paramArrayOfDouble3[0] = paramArrayOfDouble4[0];
    paramArrayOfDouble4[0] = paramDouble2;

    paramArrayOfTimestamp3[0] = paramArrayOfTimestamp4[0];
    paramArrayOfTimestamp4[0] = paramTimestamp2;

    paramArrayOfDate3[0] = paramArrayOfDate4[0];
    paramArrayOfDate4[0] = paramDate2;

    paramArrayOfString5[0] = paramArrayOfString7[0];
    paramArrayOfString7[0] = paramString3;

    paramArrayOfString6[0] = paramArrayOfString8[0];
    paramArrayOfString8[0] = paramString4;

    paramArrayOfBigDecimal3[0] = paramArrayOfBigDecimal4[0];
    paramArrayOfBigDecimal4[0] = paramBigDecimal2;

    paramArrayOfLong3[0] = paramArrayOfLong4[0];
    paramArrayOfLong4[0] = paramLong2;

    paramArrayOfFloat3[0] = paramArrayOfFloat4[0];
    paramArrayOfFloat4[0] = paramFloat2;

    paramArrayOfShort3[0] = paramArrayOfShort4[0];
    paramArrayOfShort4[0] = paramShort2;

    paramArrayOfInt5[0] = paramArrayOfInt6[0];
    paramArrayOfInt6[0] = paramInt3;

    paramArrayOfDouble5[0] = paramArrayOfDouble6[0];
    paramArrayOfDouble6[0] = paramDouble3;

    paramArrayOfTimestamp5[0] = paramArrayOfTimestamp6[0];
    paramArrayOfTimestamp6[0] = paramTimestamp3;

    paramArrayOfDate5[0] = paramArrayOfDate6[0];
    paramArrayOfDate6[0] = paramDate3;

    paramArrayOfString9[0] = paramArrayOfString11[0];
    paramArrayOfString11[0] = paramString5;

    paramArrayOfString10[0] = paramArrayOfString12[0];
    paramArrayOfString12[0] = paramString6;

    paramArrayOfBigDecimal5[0] = paramArrayOfBigDecimal6[0];
    paramArrayOfBigDecimal6[0] = paramBigDecimal3;

    paramArrayOfLong5[0] = paramArrayOfLong6[0];
    paramArrayOfLong6[0] = paramLong3;

    paramArrayOfFloat5[0] = paramArrayOfFloat6[0];
    paramArrayOfFloat6[0] = paramFloat3;

    paramArrayOfShort5[0] = paramArrayOfShort6[0];
    paramArrayOfShort6[0] = paramShort3;

    paramArrayOfInt7[0] = paramArrayOfInt8[0];
    paramArrayOfInt8[0] = paramInt4;

    paramArrayOfDouble7[0] = paramArrayOfDouble8[0];
    paramArrayOfDouble8[0] = paramDouble4;

    paramArrayOfTimestamp7[0] = paramArrayOfTimestamp8[0];
    paramArrayOfTimestamp8[0] = paramTimestamp4;

    paramArrayOfDate7[0] = paramArrayOfDate8[0];
    paramArrayOfDate8[0] = paramDate4;

    paramArrayOfString13[0] = paramArrayOfString15[0];
    paramArrayOfString15[0] = paramString7;

    paramArrayOfString14[0] = paramArrayOfString16[0];
    paramArrayOfString16[0] = paramString8;

    paramArrayOfBigDecimal7[0] = paramArrayOfBigDecimal8[0];
    paramArrayOfBigDecimal8[0] = paramBigDecimal4;

    paramArrayOfLong7[0] = paramArrayOfLong8[0];
    paramArrayOfLong8[0] = paramLong4;

    paramArrayOfFloat7[0] = paramArrayOfFloat8[0];
    paramArrayOfFloat8[0] = paramFloat4;

    paramArrayOfShort7[0] = paramArrayOfShort8[0];
    paramArrayOfShort8[0] = paramShort4;
  }

  public static void N2503(String paramString, int[] paramArrayOfInt, ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
  {
  }

  public static void N0215(String paramString, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
  }

  public static void N0215(Date paramDate, Date[] paramArrayOfDate)
  {
    paramArrayOfDate[0] = paramDate;
  }

  public static void N0215(Time paramTime, Time[] paramArrayOfTime)
  {
    if (paramTime == null)
      paramArrayOfTime[0] = null;
    else
      paramArrayOfTime[0] = paramTime;
  }

  public static void N0217(Timestamp paramTimestamp, Timestamp[] paramArrayOfTimestamp, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    if (paramTimestamp == null)
      paramArrayOfTimestamp[0] = null;
    else {
      paramArrayOfTimestamp[0] = paramTimestamp;
    }
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select * from t1";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void getobject(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    String str2 = "select * from t1,t2";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS200A(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS200B(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from t1";
    String str3 = "select * from t2";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();
    paramArrayOfResultSet1[0] = localStatement1.executeQuery(str2);
    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery(str3);
  }

  public static void RS200c(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from s2";
    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS200d(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);

      Statement localStatement = localConnection.createStatement();
      String str2 = "select * from t1";
      paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
    }
    catch (SQLException localSQLException)
    {
      System.err.print("SQLException: ");
      System.err.println(localSQLException.getMessage());
      localSQLException.getNextException();
    }
  }

  public static void RS200e(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement1 = localConnection.createStatement();
    String str2 = "select * from t1";
    paramArrayOfResultSet[0] = localStatement1.executeQuery(str2);
    Statement localStatement2 = localConnection.createStatement();
    String str3 = "select * from t2";
    paramArrayOfResultSet[0] = localStatement2.executeQuery(str3);
  }

  public static void RS200(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select e_name,e_title,e_city,e_salary,e_code,e_long,e_float,e_real,e_double,e_numeric,e_numeric1,e_decimal,e_decimal1,e_date,e_time,e_tstamp from testtab";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS201(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    ResultSet tmp29_24 = localStatement.executeQuery("select * from coffees"); paramArrayOfResultSet1[0] = tmp29_24; paramArrayOfResultSet2[0] = tmp29_24;
  }

  public static void RS201b(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();
    localStatement.setFetchSize(1000);
    paramArrayOfResultSet[0] = localStatement.executeQuery("select * from i3");
  }

  public static void RS202(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2, ResultSet[] paramArrayOfResultSet3)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    Statement localStatement1 = localConnection.createStatement(1005, 1007);

    paramArrayOfResultSet1[0] = localStatement1.executeQuery("select e_city from testtab");
    Statement localStatement2 = localConnection.createStatement();
    paramArrayOfResultSet2[0] = localStatement2.executeQuery("select e_date from testtab");
    Statement localStatement3 = localConnection.createStatement();
    paramArrayOfResultSet3[0] = localStatement3.executeQuery("select e_long from testtab");
  }

  public static void RS205(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement(1004, 1007);

    paramArrayOfResultSet[0] = localStatement.executeQuery("select e_city from testtab");
    paramArrayOfResultSet[0].afterLast();
  }

  public static void RS266(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement();

    paramArrayOfResultSet[0] = localStatement.executeQuery("select e_city from testtab");
    paramArrayOfResultSet[0].afterLast();
  }

  public static void RS206(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1004, 1008);

    ResultSet localResultSet = localStatement.executeQuery("select e_name from testtab");
    localResultSet.afterLast();

    while (localResultSet.previous())
    {
      String str2 = localResultSet.getString("e_name");
      System.out.print("e_name: " + str2);
    }
  }

  public static void RS207(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    Statement localStatement = localConnection.createStatement(1005, 1007);

    paramArrayOfResultSet1[0] = localStatement.executeQuery("select a from bd");

    paramArrayOfResultSet2[0] = localStatement.executeQuery("select a from bd");
  }

  public static void RS208(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);

    Statement localStatement = localConnection.createStatement(1005, 1007);

    paramArrayOfResultSet[0] = localStatement.executeQuery("select e_long from testtab");
    paramArrayOfResultSet[0].next();
  }

  public static void RS209(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1005, 1007);

    ResultSet localResultSet = localStatement.executeQuery("select e_name from testtab");
    localResultSet.relative(2);
    while (localResultSet.next())
    {
      String str2 = localResultSet.getString("e_name");
      System.out.print("e_name: " + str2);
    }
  }

  public static void RS204(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select *  from testtab";
    ResultSet localResultSet = localStatement.executeQuery(str2);

    while (localResultSet.next());
  }

  public static void RS205b(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    String str2 = "select *  from testtab";
    ResultSet localResultSet = localStatement.executeQuery(str2);

    while (localResultSet.next());
  }

  public static void RS211(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1005, 1007);

    localStatement.executeUpdate("delete from coffees");
    localStatement.executeUpdate("insert into coffees values ('Colombian', 101, 7.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('French_Roast', 49, 8.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('Espresso', 150, 9.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('Colombian_Decaf', 101, 8.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('French_Roast_Decaf', 49, 9.99, 0, 0)");

    String str2 = "select *  from coffees";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS212(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    localConnection.setAutoCommit(false);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("Delete from coffees ");
    localStatement.executeUpdate("insert into coffees values ('Colombian', 101, 7.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('French_Roast', 49, 8.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('Espresso', 150, 9.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('Colombian_Decaf', 101, 8.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('French_Roast_Decaf', 49, 9.99, 0, 0)");

    localConnection.rollback();
    String str2 = "select *  from coffees";
    paramArrayOfResultSet[0] = localStatement.executeQuery(str2);
  }

  public static void RS213(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1005, 1007);

    String str2 = "select e_name from testtab";

    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
    paramArrayOfResultSet1[0].moveToCurrentRow();
    paramArrayOfResultSet2[0] = localStatement.executeQuery(str2);
  }

  public static void RS214(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";
    try
    {
      Connection localConnection = DriverManager.getConnection(str1);

      Statement localStatement = localConnection.createStatement(1005, 1007);

      ResultSet localResultSet = localStatement.executeQuery("select cof_name, price from coffees");

      localResultSet.absolute(4);
      int i = localResultSet.getRow();
      System.out.println("rowNum should be 4 " + i);
      localResultSet.relative(-3);
      i = localResultSet.getRow();
      System.out.println("rowNum should be 1 " + i);
      localResultSet.relative(2);
      i = localResultSet.getRow();
      System.out.println("rowNum should be 3 " + i);

      localResultSet.absolute(1);
      System.out.println("after last? " + localResultSet.isAfterLast());
      String str2;
      float f;
      if (!localResultSet.isAfterLast()) {
        str2 = localResultSet.getString("cof_name");
        f = localResultSet.getFloat("price");
        System.out.println(str2 + "     " + f);
      }

      localResultSet.afterLast();
      while (localResultSet.previous()) {
        str2 = localResultSet.getString("cof_name");
        f = localResultSet.getFloat("price");
        System.out.println(str2 + "     " + f);
      }

      if (localResultSet != null) localResultSet.close();
      if (localStatement != null) localStatement.close();
      if (localConnection != null) localConnection.close(); 
    }
    catch (BatchUpdateException localBatchUpdateException)
    {
      System.err.println("-----BatchUpdateException-----");
      System.err.println("SQLState:  " + localBatchUpdateException.getSQLState());
      System.err.println("Message:  " + localBatchUpdateException.getMessage());
      System.err.println("Vendor:  " + localBatchUpdateException.getErrorCode());
      System.err.print("Update counts:  ");
      int[] arrayOfInt = localBatchUpdateException.getUpdateCounts();
      for (int j = 0; j < arrayOfInt.length; ++j) {
        System.err.print(arrayOfInt[j] + "   ");
      }
      System.out.println("");
    }
    catch (SQLException localSQLException) {
      System.err.println("-----SQLException-----");
      System.err.println("SQLState:  " + localSQLException.getSQLState());
      System.err.println("Message:  " + localSQLException.getMessage());
      System.err.println("Vendor:  " + localSQLException.getErrorCode());
    }
  }

  public static void RS215(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    paramArrayOfResultSet[0] = localStatement.executeQuery("select e_salary,e_name,e_float,e_num from testtab");
    paramArrayOfResultSet[0].next();
    String str2 = "";

    str2 = str2 + paramArrayOfResultSet[0].getInt(1) + " " + paramArrayOfResultSet[0].getString(2) + " " + paramArrayOfResultSet[0].getFloat(3) + " " + paramArrayOfResultSet[0].getInt(4) + "\n";
  }

  public static void RS216(ResultSet[] paramArrayOfResultSet1, ResultSet[] paramArrayOfResultSet2)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select e_date,e_time,e_tstamp from testtab";
    paramArrayOfResultSet1[0] = localStatement.executeQuery(str2);
    localStatement.close();
    paramArrayOfResultSet2[0] = localStatement.executeQuery(str2);
  }

  public static void RS217(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1005, 1007);

    ResultSet localResultSet = localStatement.executeQuery("select e_name from testtab");

    DatabaseMetaData localDatabaseMetaData = localConnection.getMetaData();

    localResultSet = localDatabaseMetaData.getTableTypes();
    System.out.println(localResultSet);

    while (localResultSet.next()) {
      String str2 = localResultSet.getString("e_name");
      System.out.print(str2);
    }
  }

  public static void RS218(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select * from bigb";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();

    ResultSet localResultSet = localStatement.executeQuery(str2);
    ResultSetMetaData localResultSetMetaData = localResultSet.getMetaData();

    int i = localResultSetMetaData.getColumnCount();
    String str3;
    for (int j = 1; j <= i; ++j)
    {
      if (j > 1) System.out.print(",  ");
      str3 = localResultSetMetaData.getColumnName(j);
    }

    System.out.println("");

    while (localResultSet.next())
    {
      for (int j = 1; j <= i; ++j)
      {
        if (j > 1) System.out.print(",  ");
        str3 = localResultSet.getString(j);
      }
    }
  }

  public static void RS220(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    localConnection.setAutoCommit(false);
    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate("control query default udr_java_options '-Dcatalog=cat -Dschema=javaqa'");
    localStatement.executeUpdate("Delete from coffees ");
    localStatement.executeUpdate("insert into coffees values ('Colombian', 101, 7.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('French_Roast', 49, 8.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('Espresso', 150, 9.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('Colombian_Decaf', 101, 8.99, 0, 0)");

    localStatement.executeUpdate("insert into coffees values ('French_Roast_Decaf', 49, 9.99, 0, 0)");

    localConnection.commit();
    String str2 = "select *  from coffees";
    ResultSet localResultSet = localStatement.executeQuery(str2);
  }

  public static void RS221(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    Statement localStatement = localConnection.createStatement();
    String str2 = "select *  from coffees";
    ResultSet localResultSet1 = localStatement.executeQuery(str2);
    System.out.println("Getting the first result set");
    localResultSet1 = localStatement.getResultSet();
    while (localResultSet1.next())
    {
      System.out.println("cof_name    : " + localResultSet1.getString("cof_name"));
      System.out.println("sup_id      : " + localResultSet1.getInt("sup_id"));
      System.out.println("price       : " + localResultSet1.getFloat("price"));
    }

    String str3 = "select *  from testtab";
    ResultSet localResultSet2 = localStatement.executeQuery(str3);
    System.out.println("Getting the second result set :");
    localResultSet2 = localStatement.getResultSet();
  }

  public static void RS222(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    Object localObject1 = null;
    Object localObject2 = null;

    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);
    localConnection.setAutoCommit(false);

    Statement localStatement = localConnection.createStatement();

    localStatement.addBatch("insert into coffees values('Amaretto', 49, 9.99, 0, 0)");

    localStatement.addBatch("insert into coffees values('Hazelnut', 49, 9.99, 0, 0)");

    localStatement.addBatch("insert into coffees values('Amaretto_decaf', 49, 10.99, 0, 0)");

    localStatement.addBatch("insert into coffees values('Hazelnut_decaf', 49, 10.99, 0, 0)");

    int[] arrayOfInt = localStatement.executeBatch();
    localConnection.commit();
    localConnection.setAutoCommit(true);

    ResultSet localResultSet = localStatement.executeQuery("select * from coffees");

    System.out.println("Table coffees after insertion:");
    while (localResultSet.next()) {
      String str2 = localResultSet.getString("cof_name");
      int i = localResultSet.getInt("sup_id");
      float f = localResultSet.getFloat("price");
      int j = localResultSet.getInt("sales");
      int k = localResultSet.getInt("total");
    }
  }

  public static void RS223(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement(1005, 1007);

    ResultSet localResultSet = localStatement.executeQuery("select e_name,e_city,e_salary,e_code,e_title from testtab");

    DatabaseMetaData localDatabaseMetaData = localConnection.getMetaData();

    System.out.println("\nConnected to " + localDatabaseMetaData.getURL() + " using driver = " + localDatabaseMetaData.getDriverName() + ", version = " + localDatabaseMetaData.getDriverVersion());

    System.out.println("\nVendor product name is " + localDatabaseMetaData.getDatabaseProductName() + ".\n\tDatabase software version is " + localDatabaseMetaData.getDatabaseProductVersion() + ".\n\tUser name is " + localDatabaseMetaData.getUserName() + ".\n\tCatalog is called " + localDatabaseMetaData.getCatalogTerm() + ".\n\tSchema is called " + localDatabaseMetaData.getSchemaTerm() + ".\n\tProcedure is called " + localDatabaseMetaData.getProcedureTerm() + ".");

    System.out.println("\nNumeric functions are:\n" + localDatabaseMetaData.getNumericFunctions() + "\nString functions are:\n" + localDatabaseMetaData.getStringFunctions() + "\nDate and Time functions are:\n" + localDatabaseMetaData.getTimeDateFunctions() + "\nSystem functions are:\n" + localDatabaseMetaData.getSystemFunctions() + "\n");

    System.out.println("Use the escape string \"" + localDatabaseMetaData.getSearchStringEscape() + "\" to escape wildcard characters.");

    System.out.println("Is the database in read only mode? Answer: " + localDatabaseMetaData.isReadOnly() + "");

    int i = localResultSet.getType();
    System.out.println("srs is type :" + i);

    int j = localResultSet.getConcurrency();
    System.out.println("srs has concurrency: " + j);

    String str2 = localResultSet.getCursorName();
    System.out.println("String Cursor Name :" + str2);

    int k = localResultSet.getFetchDirection();
    System.out.println("get fetch direction :" + k);

    int l = localResultSet.getFetchSize();
    System.out.println("get fetch Size :" + l);
    int i1 = localResultSet.getType();
    System.out.println("get Type of RS :" + i1);
    int i2 = localResultSet.getRow();
    System.out.println("get cursor position:" + i2);

    while (localResultSet.next())
    {
      String str3 = localResultSet.getString("e_name");
      String str4 = localResultSet.getString("e_city");
      String str5 = localResultSet.getString("e_title");
      int i3 = localResultSet.getInt("e_salary");
      int i4 = localResultSet.getShort("e_code");
    }
  }

  public static void RS224(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "create table suppliersPK (sup_id INTEGER NOT NULL, sup_name VARCHAR(40), STREET VARCHAR(40), CITY VARCHAR(20), STATE CHAR(2), ZIP CHAR(5), primary key(sup_id))";

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement();
    localStatement.executeUpdate(str2);

    DatabaseMetaData localDatabaseMetaData = localConnection.getMetaData();

    ResultSet localResultSet = localDatabaseMetaData.getPrimaryKeys("spjrs", "type4", "suppliersPK");
    while (localResultSet.next()) {
      String str3 = localResultSet.getString("TABLE_NAME");
      String str4 = localResultSet.getString("COLUMN_NAME");
      String str5 = localResultSet.getString("KEY_SEQ");
      String str6 = localResultSet.getString("PK_NAME");
      System.out.println("table name :  " + str3);
      System.out.println("column name:  " + str4);
      System.out.println("sequence in key:  " + str5);
      System.out.println("primary key name:  " + str6);
      System.out.println("");
    }
  }

  public static void RS225(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select e_name,e_title,e_city from testtab";
    String str3 = null;

    Connection localConnection = DriverManager.getConnection(str1);

    Statement localStatement = localConnection.createStatement();

    ResultSet localResultSet = localStatement.executeQuery(str2);

    if (localResultSet.next()) {
      return;
    }
    str3 = "100 : NO DATA FOUND";
    throw new SQLException(str3);
  }

  public static void RS226(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    String str2 = "select suppliers.sup_name, coffees.cof_name from coffees, suppliers where suppliers.sup_name like 'Acme, Inc.' and suppliers.sup_id = coffees.sup_id";

    Connection localConnection = DriverManager.getConnection(str1, "myLogin", "myPassword");

    Statement localStatement = localConnection.createStatement();

    ResultSet localResultSet = localStatement.executeQuery(str2);
    System.out.println("Supplier, Coffee:");
    while (localResultSet.next()) {
      String str3 = localResultSet.getString(1);
      String str4 = localResultSet.getString(2);
      System.out.println("    " + str3 + ", " + str4);
    }
  }

  public static void RS227(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    DatabaseMetaData localDatabaseMetaData = localConnection.getMetaData();

    System.out.println("SQL Keywords supported: ");
    StringTokenizer localStringTokenizer = new StringTokenizer(localDatabaseMetaData.getSQLKeywords(), ",");

    while (localStringTokenizer.hasMoreTokens()) {
      System.out.println(" " + localStringTokenizer.nextToken());
    }
    localConnection.close();
  }

  public static void RS228(ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str);
    DatabaseMetaData localDatabaseMetaData = localConnection.getMetaData();

    String[] arrayOfString = { "TABLE" };
    paramArrayOfResultSet[0] = localDatabaseMetaData.getTables("cat", "javaqa", null, arrayOfString);
  }

  public static void RS229(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    String str1 = "jdbc:default:connection";

    Connection localConnection = DriverManager.getConnection(str1, "myLogin", "myPassword");

    localConnection.setAutoCommit(false);

    String str2 = "SELECT cof_name, PRICE FROM coffees WHERE TOTAL > ?";

    String str3 = "UPDATE coffees SET PRICE = ? WHERE cof_name = ?";

    PreparedStatement localPreparedStatement1 = localConnection.prepareStatement(str2);
    PreparedStatement localPreparedStatement2 = localConnection.prepareStatement(str3);

    localPreparedStatement1.setInt(1, 7000);
    ResultSet localResultSet = localPreparedStatement1.executeQuery();

    Savepoint localSavepoint = localConnection.setSavepoint();
    float f2;
    while (localResultSet.next()) {
      String localObject1 = localResultSet.getString("cof_name");
      float f1 = localResultSet.getFloat("PRICE");
      f2 = f1 + f1 * 0.05F;
      localPreparedStatement2.setFloat(1, f2);
      localPreparedStatement2.setString(2, (String)localObject1);
      localPreparedStatement2.executeUpdate();
      System.out.println("New price of " + (String)localObject1 + " is " + f2);

      if (f2 > 11.99D) {
        localConnection.rollback(localSavepoint);
      }

    }

    localPreparedStatement1 = localConnection.prepareStatement(str2);
    localPreparedStatement2 = localConnection.prepareStatement(str3);

    localPreparedStatement1.setInt(1, 8000);

    localResultSet = localPreparedStatement1.executeQuery();
    System.out.println();

    Object localObject1 = localConnection.setSavepoint();
    float f3;
    while (localResultSet.next()) {
      String localObject2 = localResultSet.getString("cof_name");
      f2 = localResultSet.getFloat("PRICE");
      f3 = f2 + f2 * 0.05F;
      localPreparedStatement2.setFloat(1, f3);
      localPreparedStatement2.setString(2, (String)localObject2);
      localPreparedStatement2.executeUpdate();
      System.out.println("New price of " + (String)localObject2 + " is " + f3);

      if (f3 > 11.99D) {
        localConnection.rollback((Savepoint)localObject1);
      }
    }

    localConnection.commit();

    Object localObject2 = localConnection.createStatement();
    localResultSet = ((Statement)localObject2).executeQuery("SELECT cof_name, PRICE FROM coffees");

    System.out.println();
    while (localResultSet.next()) {
      String str4 = localResultSet.getString("cof_name");
      f3 = localResultSet.getFloat("PRICE");
      System.out.println("Current price of " + str4 + " is " + f3);
    }

    if (localResultSet != null) localResultSet.close();
    if (localObject2 != null) ((Statement)localObject2).close();
    if (localConnection == null) return; localConnection.close();
  }

  public static void RS230(String paramString, ResultSet[] paramArrayOfResultSet)
    throws Exception
  {
    int i = 5;

    for (int j = 1; j <= i; ++j)
    {
      jdbcThread localjdbcThread = new jdbcThread("Thread " + j);
      localjdbcThread.start();
    }
  }
}
