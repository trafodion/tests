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

import java.math.BigDecimal;
import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class Sales
{
  public static void lowerPrice()
    throws SQLException
  {
    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    PreparedStatement localPreparedStatement1 = localConnection.prepareStatement("SELECT p.partnum,   SUM(qty_ordered) AS qtyOrdered FROM parts p LEFT JOIN      odetail o   ON p.partnum = o.partnum GROUP BY p.partnum");

    PreparedStatement localPreparedStatement2 = localConnection.prepareStatement("UPDATE parts SET price = price * 0.9 WHERE partnum = ?");

    ResultSet localResultSet = localPreparedStatement1.executeQuery();
    while (localResultSet.next())
    {
      BigDecimal localBigDecimal1 = localResultSet.getBigDecimal(2);
      if ((localBigDecimal1 == null) || (localBigDecimal1.intValue() < 50))
      {
        BigDecimal localBigDecimal2 = localResultSet.getBigDecimal(1);
        localPreparedStatement2.setBigDecimal(1, localBigDecimal2);
        localPreparedStatement2.executeUpdate();
      }
    }
  }

  public static void numDailyOrders(Date paramDate, int[] paramArrayOfInt)
    throws SQLException
  {
    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    PreparedStatement localPreparedStatement = localConnection.prepareStatement("SELECT COUNT(order_date) FROM orders WHERE order_date = ?");

    localPreparedStatement.setDate(1, paramDate);
    ResultSet localResultSet = localPreparedStatement.executeQuery();
    localResultSet.next();
    paramArrayOfInt[0] = localResultSet.getInt(1);
  }

  public static void numMonthlyOrders(int paramInt, int[] paramArrayOfInt)
    throws SQLException
  {
    if ((paramInt < 1) || (paramInt > 12))
    {
      throw new SQLException("Invalid value for month. Retry the CALL statement using a number from 1 to 12 to represent the month.", "38001");
    }

    Connection localConnection = DriverManager.getConnection("jdbc:default:connection");

    PreparedStatement localPreparedStatement = localConnection.prepareStatement("SELECT COUNT(month(order_date)) FROM orders WHERE month(order_date) = ?");

    localPreparedStatement.setInt(1, paramInt);
    ResultSet localResultSet = localPreparedStatement.executeQuery();
    localResultSet.next();
    paramArrayOfInt[0] = localResultSet.getInt(1);
  }

  public static void totalPrice(BigDecimal paramBigDecimal, String paramString, BigDecimal[] paramArrayOfBigDecimal)
    throws SQLException
  {
    BigDecimal localBigDecimal1 = new BigDecimal(0);

    if (paramString.equals("economy"))
    {
      localBigDecimal1 = new BigDecimal(1.95D);
    }
    else if (paramString.equals("standard"))
    {
      localBigDecimal1 = new BigDecimal(4.99D);
    }
    else if (paramString.equals("nextday"))
    {
      localBigDecimal1 = new BigDecimal(14.99D);
    }
    else
    {
      throw new SQLException("Invalid value for shipping speed. Retry the CALL statement using 'economy' for 7 to 9 days, 'standard' for 3 to 5 days, or 'nextday' for one day.", "38002");
    }

    BigDecimal localBigDecimal2 = paramArrayOfBigDecimal[0].multiply(paramBigDecimal);

    BigDecimal localBigDecimal3 = new BigDecimal(0.0825D);
    BigDecimal localBigDecimal4 = localBigDecimal2.multiply(localBigDecimal3);
    BigDecimal localBigDecimal5 = localBigDecimal4.add(localBigDecimal1);

    paramArrayOfBigDecimal[0] = localBigDecimal2.add(localBigDecimal5);
    paramArrayOfBigDecimal[0] = paramArrayOfBigDecimal[0].setScale(2, 4);
  }
}
