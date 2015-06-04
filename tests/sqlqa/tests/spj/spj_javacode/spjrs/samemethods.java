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
import java.sql.ResultSet;
import java.sql.Time;
import java.sql.Timestamp;

public class samemethods
{
  public static void main(String[] paramArrayOfString)
  {
  }

  public static void sop(String paramString)
  {
    System.out.println(paramString);
  }

  public static void N0210(Byte paramByte, Byte[] paramArrayOfByte)
  {
    paramArrayOfByte[0] = paramByte;
  }

  protected static void N0200(String paramString, String[] paramArrayOfString)
  {
    paramArrayOfString[0] = paramString;
  }

  public static void N0215(java.sql.Date[] paramArrayOfDate1, java.sql.Date[] paramArrayOfDate2)
  {
    paramArrayOfDate2[0] = paramArrayOfDate1[0];
  }

  public static void N0215(java.sql.Date[] paramArrayOfDate1, java.sql.Date[] paramArrayOfDate2, java.sql.Date paramDate1, java.sql.Date paramDate2)
  {
    paramArrayOfDate2[0] = paramArrayOfDate1[0];
  }

  public static void N0215(java.sql.Date paramDate, java.sql.Date[] paramArrayOfDate)
  {
    paramArrayOfDate[0] = paramDate;
  }

  public static void N0215(java.sql.Date paramDate1, java.sql.Date paramDate2)
  {
    paramDate2 = paramDate1;
  }

  public static void N0215(java.sql.Date paramDate)
  {
  }

  public static void N0215(java.sql.Date paramDate, java.sql.Date[] paramArrayOfDate1, java.sql.Date[] paramArrayOfDate2)
  {
    paramArrayOfDate1[0] = paramDate;
  }

  public static void N0215(java.sql.Date paramDate1, java.sql.Date[] paramArrayOfDate, java.sql.Date paramDate2)
  {
    paramArrayOfDate[0] = paramDate1;
  }

  public static void N0215(java.sql.Date paramDate, java.util.Date[] paramArrayOfDate)
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

  public static void N0215(Timestamp paramTimestamp, Timestamp[] paramArrayOfTimestamp)
  {
    if (paramTimestamp == null)
      paramArrayOfTimestamp[0] = null;
    else
      paramArrayOfTimestamp[0] = paramTimestamp;
  }

  public static void sales_proc(String paramString, int[] paramArrayOfInt, ResultSet[] paramArrayOfResultSet)
  {
  }

  public static void proc(String paramString, int[] paramArrayOfInt)
  {
    paramArrayOfInt[0] = Integer.valueOf(paramString).intValue();
  }

  public static void N0200RS(String paramString, ResultSet[] paramArrayOfResultSet)
  {
  }
}
