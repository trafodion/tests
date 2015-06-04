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
import java.io.PrintStream;
import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Time;
import java.sql.Timestamp;

public class nProcs
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void sop(String paramString)
  {
    System.err.println(paramString);
  }

  public String order(double[] paramArrayOfDouble) throws Exception {
    int i = paramArrayOfDouble.length;
    while (true) { i--; if (i < 0) break;
      int j = 0;
      for (int k = 0; k < i; k++) {
        if (paramArrayOfDouble[k] > paramArrayOfDouble[(k + 1)]) {
          double d = paramArrayOfDouble[k];
          paramArrayOfDouble[k] = paramArrayOfDouble[(k + 1)];
          paramArrayOfDouble[(k + 1)] = d;
          j = 1;
        }
      }
    }

    String str = "";
    for (int j = 0; j < paramArrayOfDouble.length; j++)
      str = str + paramArrayOfDouble[j] + " ";
    return str;
  }

  public static void N1320(String paramString, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
  }

  public static void N1321(long paramLong, long[] paramArrayOfLong)
  {
    paramArrayOfLong[0] = paramLong;
  }

  public static void N1323(short paramShort, short[] paramArrayOfShort)
  {
    paramArrayOfShort[0] = paramShort;
  }

  public static void N1325(double paramDouble, double[] paramArrayOfDouble)
  {
    paramArrayOfDouble[0] = paramDouble;
  }

  public static void N1329(int paramInt, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = paramInt;
  }

  public static void N1331(BigDecimal paramBigDecimal, BigDecimal[] paramArrayOfBigDecimal)
  {
    paramArrayOfBigDecimal[0] = paramBigDecimal;
  }

  public static void N1332(float paramFloat, float[] paramArrayOfFloat)
  {
    paramArrayOfFloat[0] = paramFloat;
  }

  public static void N1339(String paramString1, String paramString2, String[] paramArrayOfString)
  {
    try
    {
      DataInputStream localDataInputStream = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString1)));

      double d1 = localDataInputStream.readDouble();
      String str1 = localDataInputStream.readUTF();
      double d2 = localDataInputStream.readDouble();
      String str2 = localDataInputStream.readUTF();

      DataOutputStream localDataOutputStream = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(paramString2)));

      localDataOutputStream.writeDouble(d1);
      localDataOutputStream.writeUTF(str1);
      localDataOutputStream.writeDouble(d2);
      localDataOutputStream.writeUTF(str2);
      localDataOutputStream.close();

      paramArrayOfString[0] = paramString2;
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString1);
    }
    catch (IOException localIOException)
    {
      localIOException.printStackTrace();
    }
  }

  public static void N1340(String paramString, String[] paramArrayOfString)
  {
    try
    {
      DataInputStream localDataInputStream = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString)));

      double d1 = localDataInputStream.readDouble();
      String str1 = localDataInputStream.readUTF();
      double d2 = localDataInputStream.readDouble();
      String str2 = localDataInputStream.readUTF();

      DataOutputStream localDataOutputStream = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(paramString)));

      double d3 = 0.1232141D;
      localDataOutputStream.writeDouble(d1);
      localDataOutputStream.writeUTF(str1);

      if (d2 != d3) {
        localDataOutputStream.writeDouble(d3);
      }

      localDataOutputStream.writeUTF(str2);
      localDataOutputStream.close();

      paramArrayOfString[0] = paramString;
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString);
    }
    catch (IOException localIOException)
    {
      localIOException.printStackTrace();
    }
  }

  public static void N1341(String paramString, String[] paramArrayOfString)
  {
    try
    {
      DataInputStream localDataInputStream = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString)));

      double d1 = localDataInputStream.readDouble();
      String str1 = localDataInputStream.readUTF();
      double d2 = localDataInputStream.readDouble();
      String str2 = localDataInputStream.readUTF();

      DataOutputStream localDataOutputStream = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(paramString)));

      localDataOutputStream.writeDouble(d1);
      localDataOutputStream.writeUTF(str1);
      localDataOutputStream.close();
      paramArrayOfString[0] = paramString;
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString);
    }
    catch (IOException localIOException)
    {
      localIOException.printStackTrace();
    }
  }

  public static void N1342(String paramString, double[] paramArrayOfDouble)
    throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    try
    {
      DataInputStream localDataInputStream = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString)));

      double d1 = localDataInputStream.readDouble();
      String str2 = localDataInputStream.readUTF();
      double d2 = localDataInputStream.readDouble();
      String str3 = localDataInputStream.readUTF();

      localConnection = DriverManager.getConnection(str1);

      PreparedStatement localPreparedStatement = localConnection.prepareStatement("insert into dtime(number,salary,monthname) values(5,?,'August')");
      localPreparedStatement.setDouble(1, d1);
      localPreparedStatement.execute();
      System.err.println("SQL insert completed");

      Statement localStatement = localConnection.createStatement();
      ResultSet localResultSet = localStatement.executeQuery("select salary from dtime where number = 5");
      localResultSet.next();
      paramArrayOfDouble[0] = localResultSet.getDouble(1);
      localStatement.close();
    }
    catch (SQLException localSQLException1) {
      localSQLException1.printStackTrace();
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString);
    }
    catch (IOException localIOException)
    {
      localIOException.printStackTrace();
    }
  }

  public static void N1343(String paramString, double[] paramArrayOfDouble1, double[] paramArrayOfDouble2)
    throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    try
    {
      DataInputStream localDataInputStream = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString)));

      double d1 = localDataInputStream.readDouble();
      String str2 = localDataInputStream.readUTF();
      double d2 = localDataInputStream.readDouble();
      String str3 = localDataInputStream.readUTF();
      localConnection = DriverManager.getConnection(str1);

      PreparedStatement localPreparedStatement1 = localConnection.prepareStatement("insert into dtime(number,salary,monthname) values(3,?,'May')");
      localPreparedStatement1.setDouble(1, d1);
      localPreparedStatement1.execute();
      System.err.println("SQL insert completed");

      PreparedStatement localPreparedStatement2 = localConnection.prepareStatement("insert into atable(index,salary,hiredate) values(20,?,date '1999-12-10') ");
      localPreparedStatement2.setDouble(1, d2);
      localPreparedStatement2.execute();
      System.err.println("SQL insert completed");

      Statement localStatement = localConnection.createStatement();
      ResultSet localResultSet1 = localStatement.executeQuery("select salary from dtime where number = 3");
      localResultSet1.next();
      paramArrayOfDouble1[0] = localResultSet1.getDouble(1);

      ResultSet localResultSet2 = localStatement.executeQuery("select salary from atable where index = 20");
      localResultSet2.next();
      paramArrayOfDouble2[0] = localResultSet2.getDouble(1);
      localStatement.close();
    }
    catch (SQLException localSQLException1) {
      localSQLException1.printStackTrace();
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString);
    }
    catch (IOException localIOException) {
      localIOException.printStackTrace();
    }
  }

  public static void N1344(String paramString1, String paramString2, String[] paramArrayOfString, double[] paramArrayOfDouble)
    throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    try
    {
      DataInputStream localDataInputStream1 = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString1)));

      double d1 = localDataInputStream1.readDouble();
      String str2 = localDataInputStream1.readUTF();

      DataInputStream localDataInputStream2 = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString2)));

      double d2 = localDataInputStream2.readDouble();
      String str3 = localDataInputStream2.readUTF();

      localConnection = DriverManager.getConnection(str1);
      PreparedStatement localPreparedStatement = localConnection.prepareStatement("insert into dtime(number,salary,monthname) values(10,?,?)");
      localPreparedStatement.setDouble(1, d1);
      localPreparedStatement.setString(2, str3);
      localPreparedStatement.execute();
      System.err.println("SQL insert completed");

      Statement localStatement1 = localConnection.createStatement();
      ResultSet localResultSet1 = localStatement1.executeQuery("select salary from dtime where number = 10");
      Statement localStatement2 = localConnection.createStatement();
      ResultSet localResultSet2 = localStatement2.executeQuery("select monthname from dtime where number = 10");

      localResultSet1.next();
      paramArrayOfDouble[0] = localResultSet1.getDouble(1);
      localResultSet2.next();
      paramArrayOfString[0] = localResultSet2.getString(1);

      localStatement1.close();
      localStatement2.close();
    }
    catch (SQLException localSQLException1) {
      localSQLException1.printStackTrace();
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString1);
    }
    catch (IOException localIOException) {
      localIOException.printStackTrace();
    }
  }

  public static void N1345(String paramString1, String paramString2, String[] paramArrayOfString, double[] paramArrayOfDouble)
    throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    try
    {
      DataInputStream localDataInputStream1 = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString1)));

      double d1 = localDataInputStream1.readDouble();
      String str2 = localDataInputStream1.readUTF();

      DataInputStream localDataInputStream2 = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString2)));

      double d2 = localDataInputStream2.readDouble();
      String str3 = localDataInputStream2.readUTF();

      localConnection = DriverManager.getConnection(str1);
      PreparedStatement localPreparedStatement1 = localConnection.prepareStatement("insert into dtime(number,salary,monthname) values(17,?,'June')");
      localPreparedStatement1.setDouble(1, d1);
      localPreparedStatement1.execute();
      System.err.println("SQL insert completed");

      PreparedStatement localPreparedStatement2 = localConnection.prepareStatement("insert into atable(index,name,hiredate) values(21,?,date '1998-11-04') ");
      localPreparedStatement2.setString(1, str3);
      localPreparedStatement2.execute();
      System.err.println("SQL insert completed");

      Statement localStatement1 = localConnection.createStatement();
      ResultSet localResultSet1 = localStatement1.executeQuery("select salary from dtime where number =17");
      localResultSet1.next();
      paramArrayOfDouble[0] = localResultSet1.getDouble(1);
      localStatement1.close();

      Statement localStatement2 = localConnection.createStatement();
      ResultSet localResultSet2 = localStatement2.executeQuery("select name from atable where index = 21");
      localResultSet2.next();
      paramArrayOfString[0] = localResultSet2.getString(1);
      localStatement2.close();
    }
    catch (SQLException localSQLException1) {
      localSQLException1.printStackTrace();
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString1);
    }
    catch (IOException localIOException) {
      localIOException.printStackTrace();
    }
  }

  public static void N1346(String paramString, double[] paramArrayOfDouble, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);

      Statement localStatement1 = localConnection.createStatement();
      ResultSet localResultSet1 = localStatement1.executeQuery("select salary from dtime where number =1");
      localResultSet1.next();
      paramArrayOfDouble[0] = localResultSet1.getDouble(1);
      localStatement1.close();

      Statement localStatement2 = localConnection.createStatement();
      ResultSet localResultSet2 = localStatement2.executeQuery("select monthname from dtime where number = 1");
      localResultSet2.next();
      paramArrayOfString[0] = localResultSet2.getString(1);
      localStatement2.close();

      DataOutputStream localDataOutputStream = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(paramString)));

      localDataOutputStream.writeDouble(paramArrayOfDouble[0]);
      localDataOutputStream.writeUTF(paramArrayOfString[0]);
      localDataOutputStream.close();
    }
    catch (SQLException localSQLException1) {
      localSQLException1.printStackTrace();
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString);
    }
    catch (IOException localIOException) {
      localIOException.printStackTrace();
    }
  }

  public static void N1347(String paramString1, String paramString2, double[] paramArrayOfDouble, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);

      Statement localStatement1 = localConnection.createStatement();
      ResultSet localResultSet1 = localStatement1.executeQuery("select salary from dtime where number =1");
      localResultSet1.next();
      paramArrayOfDouble[0] = localResultSet1.getDouble(1);
      localStatement1.close();

      Statement localStatement2 = localConnection.createStatement();
      ResultSet localResultSet2 = localStatement2.executeQuery("select monthname from dtime where number = 1");
      localResultSet2.next();
      paramArrayOfString[0] = localResultSet2.getString(1);
      localStatement2.close();

      DataOutputStream localDataOutputStream1 = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(paramString1)));

      localDataOutputStream1.writeDouble(paramArrayOfDouble[0]);
      localDataOutputStream1.writeUTF(paramArrayOfString[0]);
      localDataOutputStream1.close();

      DataOutputStream localDataOutputStream2 = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(paramString2)));

      localDataOutputStream2.writeDouble(paramArrayOfDouble[0]);
      localDataOutputStream2.writeUTF(paramArrayOfString[0]);
      localDataOutputStream2.close();
    }
    catch (SQLException localSQLException1) {
      localSQLException1.printStackTrace();
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString1);
    }
    catch (IOException localIOException) {
      localIOException.printStackTrace();
    }
  }

  public static void N1348(String paramString, double[] paramArrayOfDouble1, double[] paramArrayOfDouble2, double[] paramArrayOfDouble3)
    throws Exception
  {
    Connection localConnection = null;
    String str1 = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str1);

      Statement localStatement1 = localConnection.createStatement();
      ResultSet localResultSet1 = localStatement1.executeQuery("select salary from dtime where number = 1");
      localResultSet1.next();
      paramArrayOfDouble1[0] = localResultSet1.getDouble(1);
      localStatement1.close();

      Statement localStatement2 = localConnection.createStatement();
      ResultSet localResultSet2 = localStatement2.executeQuery("select salary from atable where index = 5");
      localResultSet2.next();
      paramArrayOfDouble2[0] = localResultSet2.getDouble(1);
      localStatement2.close();

      Statement localStatement3 = localConnection.createStatement();
      ResultSet localResultSet3 = localStatement3.executeQuery("select salary from atable where index = 2");
      localResultSet3.next();
      paramArrayOfDouble3[0] = localResultSet3.getDouble(1);
      localStatement3.close();

      double[] arrayOfDouble = new double[3];
      arrayOfDouble[0] = paramArrayOfDouble1[0];
      arrayOfDouble[1] = paramArrayOfDouble2[0];
      arrayOfDouble[2] = paramArrayOfDouble3[0];
      nProcs localnProcs = new nProcs();
      String str2 = localnProcs.order(arrayOfDouble);

      DataOutputStream localDataOutputStream = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(paramString)));

      localDataOutputStream.writeUTF(str2);
      localDataOutputStream.close();
    }
    catch (SQLException localSQLException1) {
      localSQLException1.printStackTrace();
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString);
    }
    catch (IOException localIOException) {
      localIOException.printStackTrace();
    }
  }

  public static void N1349(String paramString1, String paramString2, String paramString3, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";

    double[] arrayOfDouble = new double[3];
    String[] arrayOfString = new String[3];
    try
    {
      DataInputStream localDataInputStream1 = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString1)));

      arrayOfDouble[0] = localDataInputStream1.readDouble();
      arrayOfString[0] = localDataInputStream1.readUTF();

      DataInputStream localDataInputStream2 = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString2)));

      arrayOfDouble[1] = localDataInputStream2.readDouble();
      arrayOfString[1] = localDataInputStream2.readUTF();

      DataInputStream localDataInputStream3 = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString3)));

      arrayOfDouble[2] = localDataInputStream3.readDouble();
      arrayOfString[2] = localDataInputStream3.readUTF();

      localConnection = DriverManager.getConnection(str);
      PreparedStatement localPreparedStatement1 = localConnection.prepareStatement("insert into dtime(number,salary,monthname) values(11,?,?)");
      localPreparedStatement1.setDouble(1, arrayOfDouble[0]);
      localPreparedStatement1.setString(2, arrayOfString[0]);
      localPreparedStatement1.execute();
      System.err.println("SQL insert completed");

      PreparedStatement localPreparedStatement2 = localConnection.prepareStatement("insert into dtime(number,salary,monthname) values(12,?,?)");
      localPreparedStatement2.setDouble(1, arrayOfDouble[1]);
      localPreparedStatement2.setString(2, arrayOfString[1]);
      localPreparedStatement2.execute();
      System.err.println("SQL insert completed");

      PreparedStatement localPreparedStatement3 = localConnection.prepareStatement("insert into dtime(number,salary,monthname) values(13,?,?)");
      localPreparedStatement3.setDouble(1, arrayOfDouble[2]);
      localPreparedStatement3.setString(2, arrayOfString[2]);
      localPreparedStatement3.execute();
      System.err.println("SQL insert completed");

      Statement localStatement = localConnection.createStatement();
      ResultSet localResultSet = localStatement.executeQuery("select monthname from dtime order by salary");
      localResultSet.next();
      paramArrayOfString[0] = localResultSet.getString(1);
      localStatement.close();
    }
    catch (SQLException localSQLException1) {
      localSQLException1.printStackTrace();
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString1);
    }
    catch (IOException localIOException) {
      localIOException.printStackTrace();
    }
  }

  public static void N1350(String paramString, double[] paramArrayOfDouble)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);

      Statement localStatement = localConnection.createStatement();
      ResultSet localResultSet = localStatement.executeQuery("select salary from dtime union (select salary from atable union (select salary from testtime where  number > 23)) order by salary asc");
      localResultSet.next();
      paramArrayOfDouble[0] = localResultSet.getDouble(1);
      localStatement.close();

      DataOutputStream localDataOutputStream = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(paramString)));

      localDataOutputStream.writeDouble(paramArrayOfDouble[0]);
      localDataOutputStream.close();
    }
    catch (SQLException localSQLException1) {
      localSQLException1.printStackTrace();
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    }
    catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString);
    }
    catch (IOException localIOException) {
      localIOException.printStackTrace();
    }
  }

  public static void N1351(String paramString, String[] paramArrayOfString, double[] paramArrayOfDouble)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);

      DataInputStream localDataInputStream = new DataInputStream(new BufferedInputStream(new FileInputStream(paramString)));

      paramArrayOfString[0] = localDataInputStream.readUTF();

      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate(paramArrayOfString[0]);
      ResultSet localResultSet = localStatement.executeQuery("SELECT salary from testtime where number = 11");
      localResultSet.next();
      paramArrayOfDouble[0] = localResultSet.getDouble(1);
      localStatement.close();
    }
    catch (SQLException localSQLException1) {
      localSQLException1.printStackTrace();
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    } catch (FileNotFoundException localFileNotFoundException) {
      System.err.println("File Not Found: " + paramString);
    } catch (IOException localIOException) {
      localIOException.printStackTrace();
    }
  }

  public static void N1353(Timestamp paramTimestamp, Timestamp[] paramArrayOfTimestamp)
  {
    paramArrayOfTimestamp[0] = paramTimestamp;
  }

  public static void N1392(int paramInt, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = String.valueOf(paramInt);
  }

  public static void N1358(Date paramDate, Date[] paramArrayOfDate)
  {
    paramArrayOfDate[0] = paramDate;
  }

  public static void N1362(Time paramTime, Time[] paramArrayOfTime)
  {
    paramArrayOfTime[0] = paramTime;
  }

  public static void N1374(Date paramDate, Date[] paramArrayOfDate1, Date[] paramArrayOfDate2)
  {
    paramArrayOfDate2[0] = paramArrayOfDate1[0];
    paramArrayOfDate1[0] = paramDate;
  }

  public static void N1376(Timestamp paramTimestamp, Timestamp[] paramArrayOfTimestamp1, Timestamp[] paramArrayOfTimestamp2)
  {
    paramArrayOfTimestamp2[0] = paramArrayOfTimestamp1[0];
    paramArrayOfTimestamp1[0] = paramTimestamp;
  }

  public static void N1384(long paramLong, Timestamp[] paramArrayOfTimestamp)
  {
    paramArrayOfTimestamp[0] = new Timestamp(paramLong);
  }

  public static void N1426(String paramString, String[] paramArrayOfString)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
      paramArrayOfString[0] = paramString;
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }
  }

  public static void N1427(int paramInt, int[] paramArrayOfInt)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
      paramArrayOfInt[0] = paramInt;
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      localException.printStackTrace();
    }
  }

  public static void N1433(String paramString)
    throws Exception
  {
    try
    {
      FileOutputStream localFileOutputStream = new FileOutputStream(paramString);
      BufferedOutputStream localBufferedOutputStream = new BufferedOutputStream(localFileOutputStream);
      DataOutputStream localDataOutputStream = new DataOutputStream(localBufferedOutputStream);

      localDataOutputStream.writeUTF("Hello, Streams");
      localDataOutputStream.writeInt(2000);
      localDataOutputStream.writeChar(74);
      localDataOutputStream.close();
      localBufferedOutputStream.close();
      localFileOutputStream.close();
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

  public static void N1434(String paramString)
    throws Exception
  {
    try
    {
      FileInputStream localFileInputStream = new FileInputStream(paramString);
      BufferedInputStream localBufferedInputStream = new BufferedInputStream(localFileInputStream);
      DataInputStream localDataInputStream = new DataInputStream(localBufferedInputStream);

      System.out.println(localDataInputStream.readUTF());
      System.out.println(localDataInputStream.readInt());
      System.out.println(localDataInputStream.readChar());
      localDataInputStream.close();
      localBufferedInputStream.close();
      localFileInputStream.close();
    }
    catch (FileNotFoundException localFileNotFoundException)
    {
      System.err.println("File Not Found: " + paramString);
    }
    catch (IOException localIOException) {
      localIOException.printStackTrace();
    }
  }

  public static void N1492(int paramInt, int[] paramArrayOfInt)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("insert into dtime values(11,63829.11,'June',date '1986-12-03',time '09:34:59',timestamp '2011-01-12 07:53:32')");
      ResultSet localResultSet = localStatement.executeQuery("ROLL BACK");
      localResultSet.next();
      paramInt = localResultSet.getInt(1);
      paramArrayOfInt[0] = paramInt;
    }
    catch (SQLException localSQLException1) {
      System.err.println("Problem reading scale");
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }
  }

  public static void N1484(int paramInt, int[] paramArrayOfInt)
    throws Exception
  {
    Connection localConnection = null;
    String str = "jdbc:default:connection";
    try
    {
      localConnection = DriverManager.getConnection(str);
      Statement localStatement = localConnection.createStatement();
      localStatement.executeUpdate("DELETE from dtime where number = 1");
      localStatement.executeUpdate("DELETE from dtime where number = 2");
      ResultSet localResultSet = localStatement.executeQuery("ROLL BACK");
      localResultSet.next();
      paramInt = localResultSet.getInt(1);
      paramArrayOfInt[0] = paramInt;
    }
    catch (SQLException localSQLException1) {
      System.err.println("Problem reading scale");
      while (localSQLException1 != null) {
        System.err.println("Message:" + localSQLException1.getMessage());
        SQLException localSQLException2 = localSQLException1.getNextException();
      }
    } catch (Exception localException) {
      sop("ex.toString is: " + localException.toString());
      sop("ex.printStackTrace is: ");
      localException.printStackTrace();
    }
  }
}
