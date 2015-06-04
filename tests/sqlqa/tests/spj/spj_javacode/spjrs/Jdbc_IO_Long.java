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

public class Jdbc_IO_Long
{
  public static void ioLong(long[] paramArrayOfLong)
    throws Exception
  {
    System.err.println("In the Java Stored Procedure !");

    if (paramArrayOfLong[0] == 10000000000L)
      paramArrayOfLong[0] = 20000000000L;
    else
      paramArrayOfLong[0] = 10000000000L;
  }
}
