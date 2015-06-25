/**
  @@@ START COPYRIGHT @@@

  (C) Copyright 2015 Hewlett-Packard Development Company, L.P.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  @@@ END COPYRIGHT @@@
*/

#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sql.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"


#define NAME_LEN			300
#define	MAX_INTERVAL_SINGLE_FIELD	9
#define	MAX_INTERVAL_MULTIPLE_FIELD	4
#define	MAX_INTERVAL_DEFAULT		13

PassFail TestMXSQLGetDataInterval(TestInfo *pTestInfo)
{   
	TEST_DECLARE;
 	char			Heading[MAX_STRING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;

	int		i,k;
	char	*InsStr;
	char	TempCType[50];

	SQL_INTERVAL_STRUCT	CIntSingleFieldOutput[MAX_INTERVAL_SINGLE_FIELD];
	SQLLEN	CIntSingleFieldOutputLen[MAX_INTERVAL_SINGLE_FIELD];

	SQL_INTERVAL_STRUCT	CIntMultipleFieldOutput[MAX_INTERVAL_MULTIPLE_FIELD];
	SQLLEN	CIntMultipleFieldOutputLen[MAX_INTERVAL_MULTIPLE_FIELD];

	SQL_INTERVAL_STRUCT	CIntDefaultOutput[MAX_INTERVAL_DEFAULT];
	SQLLEN	CIntDefaultOutputLen[MAX_INTERVAL_DEFAULT];

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_YEAR.
 
	char	*TestCTypeIntYear[] = {"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_BIGINT","SQL_INTERVAL_YEAR","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	yr[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTYEAR[] = 
						{
							{
								SQL_C_INTERVAL_YEAR,SQL_SUCCESS,
								"('01','01',1,1,1,1,1,interval '01' year,'01')",
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_YEAR,SQL_SUCCESS_WITH_INFO,
								"('99','23',12.1,15.3,65,44,53,interval '86' year,'72')",
								99,23,12,15,65,44,53,86,72
							},
							{
 								SQL_C_INTERVAL_YEAR,SQL_SUCCESS,
 								"(null,null,null,null,null,null,null,null,null)",
 								0,0,0,0,0,0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabYr,*CrtTabYr,*InsTabYr,*SelTabYr;

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_MONTH.
  
	char	*TestCTypeIntMonth[] = {"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_BIGINT","SQL_INTERVAL_MONTH","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	mo[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTMONTH[] = 
						{
							{
								SQL_C_INTERVAL_MONTH,SQL_SUCCESS,
								"('01','01',1,1,1,1,1,interval '01' month,'01')",
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_MONTH,SQL_SUCCESS_WITH_INFO,
								"('99','23',12.1,15.3,65,44,53,interval '86' month,'72')",
								99,23,12,15,65,44,53,86,72
							},
							{
 								SQL_C_INTERVAL_MONTH,SQL_SUCCESS,
 								"(null,null,null,null,null,null,null,null,null)",
 								0,0,0,0,0,0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabMo,*CrtTabMo,*InsTabMo,*SelTabMo;

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_YEAR_TO_MONTH.
 
	char	*TestCTypeIntYearMonth[] = {"SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR","SQL_INTERVAL_YEAR_TO_MONTH"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	yr[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	mo[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTYEARMONTH[] = 
						{
							{
								SQL_C_INTERVAL_YEAR_TO_MONTH,SQL_SUCCESS,
								"('01-01','01-01','01-01',interval '01-01' year to month)",
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_YEAR_TO_MONTH,SQL_SUCCESS,
								"('2002-12','2000-23','99-72',interval '1923-11' year(4) to month)",
								2002,2000,99,1923,
								12,23,72,11
							},
							{
 								SQL_C_INTERVAL_YEAR_TO_MONTH,SQL_SUCCESS,
 								"(null,null,null,null)",
 								0,0,0,0,
								0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabYrMo,*CrtTabYrMo,*InsTabYrMo,*SelTabYrMo;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_DAY.
 
	char	*TestCTypeIntDay[] = {"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_BIGINT","SQL_INTERVAL_DAY","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	day[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTDAY[] = 
						{
							{
								SQL_C_INTERVAL_DAY,SQL_SUCCESS,
								"('01','01',1,1,1,1,1,interval '01' day,'01')",
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY,SQL_SUCCESS_WITH_INFO,
								"('100','0',12.0,15.3,65,44,53,interval '99' day,'72')",
								100,0,12,15,65,44,53,99,72
							},
							{
 								SQL_C_INTERVAL_DAY,SQL_SUCCESS,
 								"(null,null,null,null,null,null,null,null,null)",
 								0,0,0,0,0,0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabDay,*CrtTabDay,*InsTabDay,*SelTabDay;

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_HOUR.
 
	char	*TestCTypeIntHr[] = {"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_BIGINT","SQL_INTERVAL_HOUR","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	hr[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTHOUR[] = 
						{
							{
								SQL_C_INTERVAL_HOUR,SQL_SUCCESS,
								"('01','01',1,1,1,1,1,interval '01' hour,'01')",
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_HOUR,SQL_SUCCESS_WITH_INFO,
								"('100','0',12.0,15.3,65,44,53,interval '99' hour,'72')",
								100,0,12,15,65,44,53,99,72
							},
							{
 								SQL_C_INTERVAL_HOUR,SQL_SUCCESS,
 								"(null,null,null,null,null,null,null,null,null)",
 								0,0,0,0,0,0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabHr,*CrtTabHr,*InsTabHr,*SelTabHr;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_MINUTE.
 
	char	*TestCTypeIntMin[] = {"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_BIGINT","SQL_INTERVAL_MINUTE","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	min[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTMINUTE[] = 
						{
							{
								SQL_C_INTERVAL_MINUTE,SQL_SUCCESS,
								"('01','01',1,1,1,1,1,interval '01' minute,'01')",
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_MINUTE,SQL_SUCCESS_WITH_INFO,
								"('100','0',12.273,15.3,65,44,59,interval '0' minute,'72')",
								100,0,12,15,65,44,59,0,72
							},
							{
 								SQL_C_INTERVAL_MINUTE,SQL_SUCCESS,
 								"(null,null,null,null,null,null,null,null,null)",
 								0,0,0,0,0,0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabMin,*CrtTabMin,*InsTabMin,*SelTabMin;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_SECOND.

	char	*TestCTypeIntSec[] = {"SQL_CHAR","SQL_VARCHAR","SQL_DECIMAL","SQL_NUMERIC","SQL_SMALLINT","SQL_INTEGER","SQL_BIGINT","SQL_INTERVAL_SECOND","SQL_LONGVARCHAR"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	sec[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTSECOND[] = 
						{
							{
								SQL_C_INTERVAL_SECOND,SQL_SUCCESS,
								"('01','01',1,1,1,1,1,interval '01' second,'01')",
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_SECOND,SQL_SUCCESS_WITH_INFO,
								"('100','0',12.59,15.0,60,44,53,interval '99' second,'59')",
								100,0,12,15,60,44,53,99,59
							},
							{
 								SQL_C_INTERVAL_SECOND,SQL_SUCCESS,
 								"(null,null,null,null,null,null,null,null,null)",
 								0,0,0,0,0,0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabSec,*CrtTabSec,*InsTabSec,*SelTabSec;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_DAY_TO_HOUR.
 
	char	*TestCTypeIntDayHour[] = {"SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR","SQL_INTERVAL_DAY_TO_HOUR"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	day[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	hr[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTDAYHOUR[] = 
						{
							{
								SQL_C_INTERVAL_DAY_TO_HOUR,SQL_SUCCESS,
								"('01 01','01 01','01 01',interval '01 01' day to hour)",
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY_TO_HOUR,SQL_SUCCESS,
								"('99 23','999 12','365 0',interval '0 23' day(3) to hour)",
								99,999,365,0,
								23,12,0,23
							},
							{
 								SQL_C_INTERVAL_DAY_TO_HOUR,SQL_SUCCESS,
 								"(null,null,null,null)",
 								0,0,0,0,
								0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabDayHr,*CrtTabDayHr,*InsTabDayHr,*SelTabDayHr;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_DAY_TO_MINUTE.
 
	char	*TestCTypeIntDayMin[] = {"SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR","SQL_INTERVAL_DAY_TO_MINUTE"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	day[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	hr[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	min[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTDAYMINUTE[] = 
						{
							{
								SQL_C_INTERVAL_DAY_TO_MINUTE,SQL_SUCCESS,
								"('01 01:01','01 01:01','01 01:01',interval '01 01:01' day to minute)",
								1,1,1,1,
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY_TO_MINUTE,SQL_SUCCESS,
								"('99 23:59','999 12:30','365 0:0',interval '0 23:54' day(3) to minute)",
								99,999,365,0,
								23,12,0,23,
								59,30,0,54
							},
							{
 								SQL_C_INTERVAL_DAY_TO_MINUTE,SQL_SUCCESS,
 								"(null,null,null,null)",
 								0,0,0,0,
								0,0,0,0,
								0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabDayMin,*CrtTabDayMin,*InsTabDayMin,*SelTabDayMin;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_DAY_TO_SECOND.
 
	char	*TestCTypeIntDaySec[] = {"SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR","SQL_INTERVAL_DAY_TO_SECOND"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	day[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	hr[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	min[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	sec[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTDAYSECOND[] = 
						{
							{
								SQL_C_INTERVAL_DAY_TO_SECOND,SQL_SUCCESS,
								"('01 01:01:01','01 01:01:01','01 01:01:01',interval '01 01:01:01' day to second)",
								1,1,1,1,
								1,1,1,1,
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY_TO_SECOND,SQL_SUCCESS,
								"('99 23:59:59','999 12:30:30','365 0:0:0',interval '0 23:54:28' day(3) to second)",
								99,999,365,0,
								23,12,0,23,
								59,30,0,54,
								59,30,0,28
							},
							{
 								SQL_C_INTERVAL_DAY_TO_SECOND,SQL_SUCCESS,
 								"(null,null,null,null)",
 								0,0,0,0,
								0,0,0,0,
								0,0,0,0,
								0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabDaySec,*CrtTabDaySec,*InsTabDaySec,*SelTabDaySec;

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_HOUR_TO_MINUTE.
 
	char	*TestCTypeIntHrMin[] = {"SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR","SQL_INTERVAL_HOUR_TO_MINUTE"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	hr[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	min[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTHOURMINUTE[] = 
						{
							{
								SQL_C_INTERVAL_HOUR_TO_MINUTE,SQL_SUCCESS,
								"('01:01','01:01','01:01',interval '01:01' hour to minute)",
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_HOUR_TO_MINUTE,SQL_SUCCESS,
								"('23:59','999:30','0:0',interval '23:54' hour(3) to minute)",
								23,999,0,23,
								59,30,0,54
							},
							{
 								SQL_C_INTERVAL_HOUR_TO_MINUTE,SQL_SUCCESS,
 								"(null,null,null,null)",
 								0,0,0,0,
								0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabHrMin,*CrtTabHrMin,*InsTabHrMin,*SelTabHrMin;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_HOUR_TO_SECOND.
 
	char	*TestCTypeIntHrSec[] = {"SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR","SQL_INTERVAL_HOUR_TO_SECOND"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	hr[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	min[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	sec[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTHOURSECOND[] = 
						{
							{
								SQL_C_INTERVAL_HOUR_TO_SECOND,SQL_SUCCESS,
								"('01:01:01','01:01:01','01:01:01',interval '01:01:01' hour to second)",
								1,1,1,1,
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_HOUR_TO_SECOND,SQL_SUCCESS,
								"('23:59:59','999:30:30','0:0:0',interval '23:54:28' hour(3) to second)",
								23,999,0,23,
								59,30,0,54,
								59,30,0,28
							},
							{
 								SQL_C_INTERVAL_HOUR_TO_SECOND,SQL_SUCCESS,
 								"(null,null,null,null)",
 								0,0,0,0,
								0,0,0,0,
								0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabHrSec,*CrtTabHrSec,*InsTabHrSec,*SelTabHrSec;

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_MINUTE_TO_SECOND.
 
	char	*TestCTypeIntMinSec[] = {"SQL_CHAR","SQL_VARCHAR","SQL_LONGVARCHAR","SQL_INTERVAL_MINUTE_TO_SECOND"};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	min[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	sec[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTMINUTESECOND[] = 
						{
							{
								SQL_C_INTERVAL_MINUTE_TO_SECOND,SQL_SUCCESS,
								"('01:01','01:01','01:01',interval '01:01' minute to second)",
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_MINUTE_TO_SECOND,SQL_SUCCESS,
								"('59:59','999:99','0:0',interval '54:28' minute(3) to second)",
								59,999,0,54,
								59,99,0,28
							},
							{
 								SQL_C_INTERVAL_MINUTE_TO_SECOND,SQL_SUCCESS,
 								"(null,null,null,null)",
 								0,0,0,0,
								0,0,0,0
							},
							{
								999,
							}
						};

	char	*DrpTabMinSec,*CrtTabMinSec,*InsTabMinSec,*SelTabMinSec;
  
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_DEFAULT.
 
	char	*TestCTypeIntDef[] = {"SQL_INTERVAL_YEAR","SQL_INTERVAL_MONTH","SQL_INTERVAL_YEAR_TO_MONTH","SQL_INTERVAL_DAY","SQL_INTERVAL_HOUR","SQL_INTERVAL_MINUTE","SQL_INTERVAL_SECOND","SQL_INTERVAL_DAY_TO_HOUR","SQL_INTERVAL_DAY_TO_MINUTE","SQL_INTERVAL_DAY_TO_SECOND","SQL_INTERVAL_HOUR_TO_MINUTE","SQL_INTERVAL_HOUR_TO_SECOND","SQL_INTERVAL_MINUTE_TO_SECOND"};
	SQLSMALLINT	TestSQLType[] = {SQL_INTERVAL_YEAR,SQL_INTERVAL_MONTH,SQL_INTERVAL_YEAR_TO_MONTH,SQL_INTERVAL_DAY,SQL_INTERVAL_HOUR,SQL_INTERVAL_MINUTE,SQL_INTERVAL_SECOND,SQL_INTERVAL_DAY_TO_HOUR,SQL_INTERVAL_DAY_TO_MINUTE,SQL_INTERVAL_DAY_TO_SECOND,SQL_INTERVAL_HOUR_TO_MINUTE,SQL_INTERVAL_HOUR_TO_SECOND,SQL_INTERVAL_MINUTE_TO_SECOND};

	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		char		*InsCol;
		SQLUINTEGER	yr[MAX_INTERVAL_DEFAULT];
		SQLUINTEGER	mo[MAX_INTERVAL_DEFAULT];
		SQLUINTEGER	day[MAX_INTERVAL_DEFAULT];
		SQLUINTEGER	hr[MAX_INTERVAL_DEFAULT];
		SQLUINTEGER	min[MAX_INTERVAL_DEFAULT];
		SQLUINTEGER	sec[MAX_INTERVAL_DEFAULT];
	} SQLTOCINTDEFAULT[] = 
						{
							{
								SQL_C_DEFAULT,SQL_SUCCESS,
								"(interval '01' year,interval '01' month,interval '01-01' year to month,interval '01' day,interval '01' hour,interval '01' minute,interval '01' second,interval '01 01' day to hour,interval '01 01:01' day to minute,interval '01 01:01:01' day to second,interval '01:01' hour to minute,interval '01:01:01' hour to second,interval '01:01' minute to second)",
								1,0,1,0,0,0,0,0,0,0,0,0,0,
								0,1,1,0,0,0,0,0,0,0,0,0,0,
								0,0,0,1,0,0,0,1,1,1,0,0,0,
								0,0,0,0,1,0,0,1,1,1,1,1,0,
								0,0,0,0,0,1,0,0,1,1,1,1,1,
								0,0,0,0,0,0,1,0,0,1,0,1,1,
							},
							{
 								SQL_C_DEFAULT,SQL_SUCCESS,
 								"(interval '99' year,interval '99' month,interval '99-11' year to month,interval '99' day,interval '99' hour,interval '99' minute,interval '99' second,interval '99 23' day to hour,interval '99 23:59' day to minute,interval '99 23:59:59' day to second,interval '99:59' hour to minute,interval '99:59:59' hour to second,interval '99:59' minute to second)",
 								99,0,99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
								0,99,11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
								0, 0, 0,99, 0, 0, 0,99,99,99, 0, 0, 0,
								0, 0, 0, 0,99, 0, 0,23,23,23,99,99, 0,
								0, 0, 0, 0, 0,99, 0, 0,59,59,59,59,99,
								0, 0, 0, 0, 0, 0,99, 0, 0,59, 0,59,59,
							},
							{
 								SQL_C_DEFAULT,SQL_SUCCESS,
 								"(null,null,null,null,null,null,null,null,null,null,null,null,null)",
								0,0,0,0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0,0,0,0,
							},
							{
								999,
							}
						};

	char	*DrpTabDef,*CrtTabDef,*InsTabDef,*SelTabDef;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars("SQLGetDataInterval", charset_file);
	if (var_list == NULL) return FAILED;

	DrpTabYr = var_mapping("SQLGetDataInterval_DrpTabYr", var_list);
	CrtTabYr = var_mapping("SQLGetDataInterval_CrtTabYr", var_list);
	InsTabYr = var_mapping("SQLGetDataInterval_InsTabYr", var_list);
	SelTabYr = var_mapping("SQLGetDataInterval_SelTabYr", var_list);

	DrpTabMo = var_mapping("SQLGetDataInterval_DrpTabMo", var_list);
	CrtTabMo = var_mapping("SQLGetDataInterval_CrtTabMo", var_list);
	InsTabMo = var_mapping("SQLGetDataInterval_InsTabMo", var_list);
	SelTabMo = var_mapping("SQLGetDataInterval_SelTabMo", var_list);

	DrpTabYrMo = var_mapping("SQLGetDataInterval_DrpTabYrMo", var_list);
	CrtTabYrMo = var_mapping("SQLGetDataInterval_CrtTabYrMo", var_list);
	InsTabYrMo = var_mapping("SQLGetDataInterval_InsTabYrMo", var_list);
	SelTabYrMo = var_mapping("SQLGetDataInterval_SelTabYrMo", var_list);

	DrpTabDay = var_mapping("SQLGetDataInterval_DrpTabDay", var_list);
	CrtTabDay = var_mapping("SQLGetDataInterval_CrtTabDay", var_list);
	InsTabDay = var_mapping("SQLGetDataInterval_InsTabDay", var_list);
	SelTabDay = var_mapping("SQLGetDataInterval_SelTabDay", var_list);

	DrpTabHr = var_mapping("SQLGetDataInterval_DrpTabHr", var_list);
	CrtTabHr = var_mapping("SQLGetDataInterval_CrtTabHr", var_list);
	InsTabHr = var_mapping("SQLGetDataInterval_InsTabHr", var_list);
	SelTabHr = var_mapping("SQLGetDataInterval_SelTabHr", var_list);

	DrpTabMin = var_mapping("SQLGetDataInterval_DrpTabMin", var_list);
	CrtTabMin = var_mapping("SQLGetDataInterval_CrtTabMin", var_list);
	InsTabMin = var_mapping("SQLGetDataInterval_InsTabMin", var_list);
	SelTabMin = var_mapping("SQLGetDataInterval_SelTabMin", var_list);

	DrpTabSec = var_mapping("SQLGetDataInterval_DrpTabSec", var_list);
	CrtTabSec = var_mapping("SQLGetDataInterval_CrtTabSec", var_list);
	InsTabSec = var_mapping("SQLGetDataInterval_InsTabSec", var_list);
	SelTabSec = var_mapping("SQLGetDataInterval_SelTabSec", var_list);

	DrpTabDayHr = var_mapping("SQLGetDataInterval_DrpTabDayHr", var_list);
	CrtTabDayHr = var_mapping("SQLGetDataInterval_CrtTabDayHr", var_list);
	InsTabDayHr = var_mapping("SQLGetDataInterval_InsTabDayHr", var_list);
	SelTabDayHr = var_mapping("SQLGetDataInterval_SelTabDayHr", var_list);

	DrpTabDaySec = var_mapping("SQLGetDataInterval_DrpTabDaySec", var_list);
	CrtTabDaySec = var_mapping("SQLGetDataInterval_CrtTabDaySec", var_list);
	InsTabDaySec = var_mapping("SQLGetDataInterval_InsTabDaySec", var_list);
	SelTabDaySec = var_mapping("SQLGetDataInterval_SelTabDaySec", var_list);

	DrpTabDayMin = var_mapping("SQLGetDataInterval_DrpTabDayMin", var_list);
	CrtTabDayMin = var_mapping("SQLGetDataInterval_CrtTabDayMin", var_list);
	InsTabDayMin = var_mapping("SQLGetDataInterval_InsTabDayMin", var_list);
	SelTabDayMin = var_mapping("SQLGetDataInterval_SelTabDayMin", var_list);

	DrpTabHrMin = var_mapping("SQLGetDataInterval_DrpTabHrMin", var_list);
	CrtTabHrMin = var_mapping("SQLGetDataInterval_CrtTabHrMin", var_list);
	InsTabHrMin = var_mapping("SQLGetDataInterval_InsTabHrMin", var_list);
	SelTabHrMin = var_mapping("SQLGetDataInterval_SelTabHrMin", var_list);

	DrpTabHrSec = var_mapping("SQLGetDataInterval_DrpTabHrSec", var_list);
	CrtTabHrSec = var_mapping("SQLGetDataInterval_CrtTabHrSec", var_list);
	InsTabHrSec = var_mapping("SQLGetDataInterval_InsTabHrSec", var_list);
	SelTabHrSec = var_mapping("SQLGetDataInterval_SelTabHrSec", var_list);

	DrpTabMinSec = var_mapping("SQLGetDataInterval_DrpTabMinSec", var_list);
	CrtTabMinSec = var_mapping("SQLGetDataInterval_CrtTabMinSec", var_list);
	InsTabMinSec = var_mapping("SQLGetDataInterval_InsTabMinSec", var_list);
	SelTabMinSec = var_mapping("SQLGetDataInterval_SelTabMinSec", var_list);

	DrpTabDef = var_mapping("SQLGetDataInterval_DrpTabDef", var_list);
	CrtTabDef = var_mapping("SQLGetDataInterval_CrtTabDef", var_list);
	InsTabDef = var_mapping("SQLGetDataInterval_InsTabDef", var_list);
	SelTabDef = var_mapping("SQLGetDataInterval_SelTabDef", var_list);
 
//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,"Begin testing API =>SQLGetData | SQLGetDataInterval | sqlgetdatainterval.c\n");

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLGetData Interval tests\n");
	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,"Unable to connect\n");
		TEST_FAILED;
		TEST_RETURN;
	}
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocStmt"))
	{
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
	}
	TESTCASE_END;  // end of setup

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_YEAR
 
	k = 0;
	while (SQLTOCINTYEAR[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabYr,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabYr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabYr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabYr);
		strcat(InsStr,SQLTOCINTYEAR[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabYr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  
			
		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTYEAR[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntYear[i],SQLCTypeToChar(SQLTOCINTYEAR[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntSingleFieldOutput[i], 0, sizeof(CIntSingleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTYEAR[k].CType,&CIntSingleFieldOutput[i],0,&CIntSingleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}  

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntYear[i],SQLCTypeToChar(SQLTOCINTYEAR[k].CType,TempCType),ReturnColumnDefinition(CrtTabYr,i));
			TESTCASE_BEGIN(Heading);
			if (CIntSingleFieldOutput[i].intval.year_month.year == SQLTOCINTYEAR[k].yr[i])
			{
				//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTYEAR[k].yr[i],CIntSingleFieldOutput[i].intval.year_month.year);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTYEAR[k].yr[i],CIntSingleFieldOutput[i].intval.year_month.year);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabYr,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_MONTH
 	k = 0;
	while (SQLTOCINTMONTH[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMo,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabMo);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabMo,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabMo);
		strcat(InsStr,SQLTOCINTMONTH[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabMo,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTMONTH[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  


		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntMonth[i],SQLCTypeToChar(SQLTOCINTMONTH[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntSingleFieldOutput[i], 0, sizeof(CIntSingleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTMONTH[k].CType,&CIntSingleFieldOutput[i],0,&CIntSingleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}  

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntMonth[i],SQLCTypeToChar(SQLTOCINTMONTH[k].CType,TempCType),ReturnColumnDefinition(CrtTabMo,i));
			TESTCASE_BEGIN(Heading);
			if (CIntSingleFieldOutput[i].intval.year_month.month == SQLTOCINTMONTH[k].mo[i])
			{
				//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTMONTH[k].mo[i],CIntSingleFieldOutput[i].intval.year_month.month);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTMONTH[k].mo[i],CIntSingleFieldOutput[i].intval.year_month.month);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMo,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_YEAR_TO_MONTH
	k = 0;
	while (SQLTOCINTYEARMONTH[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabYrMo,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabYrMo);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabYrMo,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabYrMo);
		strcat(InsStr,SQLTOCINTYEARMONTH[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabYrMo,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTYEARMONTH[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntYearMonth[i],SQLCTypeToChar(SQLTOCINTYEARMONTH[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntMultipleFieldOutput[i], 0, sizeof(CIntMultipleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTYEARMONTH[k].CType,&CIntMultipleFieldOutput[i],0,&CIntMultipleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntYearMonth[i],SQLCTypeToChar(SQLTOCINTYEARMONTH[k].CType,TempCType),ReturnColumnDefinition(CrtTabYrMo,i));
			TESTCASE_BEGIN(Heading);
			if ((CIntMultipleFieldOutput[i].intval.year_month.year == SQLTOCINTYEARMONTH[k].yr[i]) &&
				(CIntMultipleFieldOutput[i].intval.year_month.month == SQLTOCINTYEARMONTH[k].mo[i]))
			{
				//LogMsg(NONE,"expect: %d-%d and actual: %d-%d are matched\n",SQLTOCINTYEARMONTH[k].yr[i],SQLTOCINTYEARMONTH[k].mo[i],CIntMultipleFieldOutput[i].intval.year_month.year,CIntMultipleFieldOutput[i].intval.year_month.month);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d-%d and actual: %d-%d are not matched\n",SQLTOCINTYEARMONTH[k].yr[i],SQLTOCINTYEARMONTH[k].mo[i],CIntMultipleFieldOutput[i].intval.year_month.year,CIntMultipleFieldOutput[i].intval.year_month.month);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabYrMo,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_DAY
	k = 0;
	while (SQLTOCINTDAY[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDay,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabDay);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabDay,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabDay);
		strcat(InsStr,SQLTOCINTDAY[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabDay,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTDAY[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END; 

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntDay[i],SQLCTypeToChar(SQLTOCINTDAY[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntSingleFieldOutput[i], 0, sizeof(CIntSingleFieldOutput[i]));  
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTDAY[k].CType,&CIntSingleFieldOutput[i],0,&CIntSingleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
			TESTCASE_END;  
		}   

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntDay[i],SQLCTypeToChar(SQLTOCINTDAY[k].CType,TempCType),ReturnColumnDefinition(CrtTabDay,i));
			TESTCASE_BEGIN(Heading);
			if (CIntSingleFieldOutput[i].intval.day_second.day == SQLTOCINTDAY[k].day[i])
			{
				//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTDAY[k].day[i],CIntSingleFieldOutput[i].intval.day_second.day);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTDAY[k].day[i],CIntSingleFieldOutput[i].intval.day_second.day);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDay,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_HOUR
	k = 0;
	while (SQLTOCINTHOUR[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabHr,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabHr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabHr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabHr);
		strcat(InsStr,SQLTOCINTHOUR[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabHr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTHOUR[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntHr[i],SQLCTypeToChar(SQLTOCINTHOUR[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntSingleFieldOutput[i], 0, sizeof(CIntSingleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTHOUR[k].CType,&CIntSingleFieldOutput[i],0,&CIntSingleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}  

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntHr[i],SQLCTypeToChar(SQLTOCINTHOUR[k].CType,TempCType),ReturnColumnDefinition(CrtTabHr,i));
			TESTCASE_BEGIN(Heading);
			if (CIntSingleFieldOutput[i].intval.day_second.hour == SQLTOCINTHOUR[k].hr[i])
			{
				//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTHOUR[k].hr[i],CIntSingleFieldOutput[i].intval.day_second.hour);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTHOUR[k].hr[i],CIntSingleFieldOutput[i].intval.day_second.hour);
			}
			TESTCASE_END;
		}

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabHr,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_MINUTE
	k = 0;
	while (SQLTOCINTMINUTE[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMin,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabMin);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabMin);
		strcat(InsStr,SQLTOCINTMINUTE[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END; 
		
		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTMINUTE[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntMin[i],SQLCTypeToChar(SQLTOCINTMINUTE[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntSingleFieldOutput[i], 0, sizeof(CIntSingleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTMINUTE[k].CType,&CIntSingleFieldOutput[i],0,&CIntSingleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}    

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntMin[i],SQLCTypeToChar(SQLTOCINTMINUTE[k].CType,TempCType),ReturnColumnDefinition(CrtTabMin,i));
			TESTCASE_BEGIN(Heading);
			if (CIntSingleFieldOutput[i].intval.day_second.minute == SQLTOCINTMINUTE[k].min[i])
			{
				//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTMINUTE[k].min[i],CIntSingleFieldOutput[i].intval.day_second.minute);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTMINUTE[k].min[i],CIntSingleFieldOutput[i].intval.day_second.minute);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMin,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_SECOND
	k = 0;
	while (SQLTOCINTSECOND[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabSec,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabSec);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabSec);
		strcat(InsStr,SQLTOCINTSECOND[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTSECOND[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntSec[i],SQLCTypeToChar(SQLTOCINTSECOND[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntSingleFieldOutput[i], 0, sizeof(CIntSingleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTSECOND[k].CType,&CIntSingleFieldOutput[i],0,&CIntSingleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}  

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntSec[i],SQLCTypeToChar(SQLTOCINTSECOND[k].CType,TempCType),ReturnColumnDefinition(CrtTabSec,i));
			TESTCASE_BEGIN(Heading);
			if (CIntSingleFieldOutput[i].intval.day_second.second == SQLTOCINTSECOND[k].sec[i])
			{
				//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTSECOND[k].sec[i],CIntSingleFieldOutput[i].intval.day_second.second);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTSECOND[k].sec[i],CIntSingleFieldOutput[i].intval.day_second.second);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabSec,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_DAY_TO_HOUR
	k = 0;
	while (SQLTOCINTDAYHOUR[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDayHr,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabDayHr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabDayHr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabDayHr);
		strcat(InsStr,SQLTOCINTDAYHOUR[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabDayHr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTDAYHOUR[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END; 

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntDayHour[i],SQLCTypeToChar(SQLTOCINTDAYHOUR[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntMultipleFieldOutput[i], 0, sizeof(CIntMultipleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTDAYHOUR[k].CType,&CIntMultipleFieldOutput[i],0,&CIntMultipleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}   

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntDayHour[i],SQLCTypeToChar(SQLTOCINTDAYHOUR[k].CType,TempCType),ReturnColumnDefinition(CrtTabDayHr,i));
			TESTCASE_BEGIN(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.day  == SQLTOCINTDAYHOUR[k].day[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.hour == SQLTOCINTDAYHOUR[k].hr[i]))
			{
				//LogMsg(NONE,"expect: %d %d and actual: %d %d are matched\n",SQLTOCINTDAYHOUR[k].day[i],SQLTOCINTDAYHOUR[k].hr[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d %d and actual: %d %d are not matched\n",SQLTOCINTDAYHOUR[k].day[i],SQLTOCINTDAYHOUR[k].hr[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDayHr,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_DAY_TO_MINUTE
	k = 0;
	while (SQLTOCINTDAYMINUTE[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDayMin,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabDayMin);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabDayMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabDayMin);
		strcat(InsStr,SQLTOCINTDAYMINUTE[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabDayMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTDAYMINUTE[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntDayMin[i],SQLCTypeToChar(SQLTOCINTDAYMINUTE[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntMultipleFieldOutput[i], 0, sizeof(CIntMultipleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTDAYMINUTE[k].CType,&CIntMultipleFieldOutput[i],0,&CIntMultipleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntDayMin[i],SQLCTypeToChar(SQLTOCINTDAYMINUTE[k].CType,TempCType),ReturnColumnDefinition(CrtTabDayMin,i));
			TESTCASE_BEGIN(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.day  == SQLTOCINTDAYMINUTE[k].day[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.hour == SQLTOCINTDAYMINUTE[k].hr[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.minute == SQLTOCINTDAYMINUTE[k].min[i]))
			{
				//LogMsg(NONE,"expect: %d %d:%d and actual: %d %d:%d are matched\n",SQLTOCINTDAYMINUTE[k].day[i],SQLTOCINTDAYMINUTE[k].hr[i],SQLTOCINTDAYMINUTE[k].min[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d %d:%d and actual: %d %d:%d are not matched\n",SQLTOCINTDAYMINUTE[k].day[i],SQLTOCINTDAYMINUTE[k].hr[i],SQLTOCINTDAYMINUTE[k].min[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDayMin,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_DAY_TO_SECOND
	k = 0;
	while (SQLTOCINTDAYSECOND[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDaySec,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabDaySec);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabDaySec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabDaySec);
		strcat(InsStr,SQLTOCINTDAYSECOND[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabDaySec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTDAYSECOND[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntDaySec[i],SQLCTypeToChar(SQLTOCINTDAYSECOND[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntMultipleFieldOutput[i], 0, sizeof(CIntMultipleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTDAYSECOND[k].CType,&CIntMultipleFieldOutput[i],0,&CIntMultipleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntDaySec[i],SQLCTypeToChar(SQLTOCINTDAYSECOND[k].CType,TempCType),ReturnColumnDefinition(CrtTabDaySec,i));
			TESTCASE_BEGIN(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.day  == SQLTOCINTDAYSECOND[k].day[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.hour == SQLTOCINTDAYSECOND[k].hr[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.minute == SQLTOCINTDAYSECOND[k].min[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.second == SQLTOCINTDAYSECOND[k].sec[i]))
			{
				//LogMsg(NONE,"expect: %d %d:%d:%d and actual: %d %d:%d:%d are matched\n",SQLTOCINTDAYSECOND[k].day[i],SQLTOCINTDAYSECOND[k].hr[i],SQLTOCINTDAYSECOND[k].min[i],SQLTOCINTDAYSECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d %d:%d:%d and actual: %d %d:%d:%d are not matched\n",SQLTOCINTDAYSECOND[k].day[i],SQLTOCINTDAYSECOND[k].hr[i],SQLTOCINTDAYSECOND[k].min[i],SQLTOCINTDAYSECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDaySec,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_HOUR_TO_MINUTE
	k = 0;
	while (SQLTOCINTHOURMINUTE[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabHrMin,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabHrMin);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabHrMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabHrMin);
		strcat(InsStr,SQLTOCINTHOURMINUTE[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabHrMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTHOURMINUTE[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntHrMin[i],SQLCTypeToChar(SQLTOCINTHOURMINUTE[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntMultipleFieldOutput[i], 0, sizeof(CIntMultipleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTHOURMINUTE[k].CType,&CIntMultipleFieldOutput[i],0,&CIntMultipleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntHrMin[i],SQLCTypeToChar(SQLTOCINTHOURMINUTE[k].CType,TempCType),ReturnColumnDefinition(CrtTabHrMin,i));
			TESTCASE_BEGIN(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.hour == SQLTOCINTHOURMINUTE[k].hr[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.minute == SQLTOCINTHOURMINUTE[k].min[i]))
			{
				//LogMsg(NONE,"expect: %d:%d and actual: %d:%d are matched\n",SQLTOCINTHOURMINUTE[k].hr[i],SQLTOCINTHOURMINUTE[k].min[i],CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d:%d and actual: %d:%d are not matched\n",SQLTOCINTHOURMINUTE[k].hr[i],SQLTOCINTHOURMINUTE[k].min[i],CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabHrMin,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_HOUR_TO_SECOND
	k = 0;
	while (SQLTOCINTHOURSECOND[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabHrSec,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabHrSec);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabHrSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabHrSec);
		strcat(InsStr,SQLTOCINTHOURSECOND[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabHrSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTHOURSECOND[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END; 

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntHrSec[i],SQLCTypeToChar(SQLTOCINTHOURSECOND[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntMultipleFieldOutput[i], 0, sizeof(CIntMultipleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTHOURSECOND[k].CType,&CIntMultipleFieldOutput[i],0,&CIntMultipleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}   

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntHrSec[i],SQLCTypeToChar(SQLTOCINTHOURSECOND[k].CType,TempCType),ReturnColumnDefinition(CrtTabHrSec,i));
			TESTCASE_BEGIN(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.hour == SQLTOCINTHOURSECOND[k].hr[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.minute == SQLTOCINTHOURSECOND[k].min[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.second == SQLTOCINTHOURSECOND[k].sec[i]))
			{
				//LogMsg(NONE,"expect: %d:%d:%d and actual: %d:%d:%d are matched\n",SQLTOCINTHOURSECOND[k].hr[i],SQLTOCINTHOURSECOND[k].min[i],SQLTOCINTHOURSECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d:%d:%d and actual: %d:%d:%d are not matched\n",SQLTOCINTHOURSECOND[k].hr[i],SQLTOCINTHOURSECOND[k].min[i],SQLTOCINTHOURSECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabHrSec,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_MINUTE_TO_SECOND
	k = 0;
	while (SQLTOCINTMINUTESECOND[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMinSec,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabMinSec);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabMinSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabMinSec);
		strcat(InsStr,SQLTOCINTMINUTESECOND[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabMinSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTMINUTESECOND[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntMinSec[i],SQLCTypeToChar(SQLTOCINTMINUTESECOND[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntMultipleFieldOutput[i], 0, sizeof(CIntMultipleFieldOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTMINUTESECOND[k].CType,&CIntMultipleFieldOutput[i],0,&CIntMultipleFieldOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		}  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntMinSec[i],SQLCTypeToChar(SQLTOCINTMINUTESECOND[k].CType,TempCType),ReturnColumnDefinition(CrtTabMinSec,i));
			TESTCASE_BEGIN(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.minute == SQLTOCINTMINUTESECOND[k].min[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.second == SQLTOCINTMINUTESECOND[k].sec[i]))
			{
				//LogMsg(NONE,"expect: %d:%d and actual: %d:%d are matched\n",SQLTOCINTMINUTESECOND[k].min[i],SQLTOCINTMINUTESECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,"expect: %d:%d and actual: %d:%d are not matched\n",SQLTOCINTMINUTESECOND[k].min[i],SQLTOCINTMINUTESECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabMinSec,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL(interval datatypes to SQL_C_DEFAULT
	k = 0;
	while (SQLTOCINTDEFAULT[k].CType != 999)
	{
		sprintf(Heading,"SQLGetData: create insert and select from table \n");
		TESTCASE_BEGIN(Heading);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDef,SQL_NTS);
		//LogMsg(NONE,"%s\n",CrtTabDef);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)CrtTabDef,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (char *)malloc(MAX_NOS_SIZE);
		strcpy(InsStr,"");
		strcat(InsStr,InsTabDef);
		strcat(InsStr,SQLTOCINTDEFAULT[k].InsCol);
		//LogMsg(NONE,"%s\n",InsStr);
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLCHAR*)SelTabDef,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		sprintf(Heading,"SQLGetData: Positive test fetch from sql to %s.\n",SQLCTypeToChar(SQLTOCINTDEFAULT[k].CType,TempCType));
		TESTCASE_BEGIN(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_DEFAULT; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for converting %s to %s after fetch.\n",i+1,TestCTypeIntDef[i],SQLCTypeToChar(SQLTOCINTDEFAULT[k].CType,TempCType));
			TESTCASE_BEGIN(Heading);
			memset (&CIntDefaultOutput[i], 0, sizeof(CIntDefaultOutput[i]));
			returncode = SQLGetData(hstmt,(SWORD)(i+1),SQLTOCINTDEFAULT[k].CType,&CIntDefaultOutput[i],sizeof(CIntDefaultOutput[i]),&CIntDefaultOutputLen[i]);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLGetData"))
			{
				TEST_FAILED;
				LogAllErrors(henv,hdbc,hstmt);
			}
			TESTCASE_END;  
		} 

		for (i = 0; i < MAX_INTERVAL_DEFAULT; i++)
		{  
			sprintf(Heading,"SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n",i+1,TestCTypeIntDef[i],SQLCTypeToChar(SQLTOCINTDEFAULT[k].CType,TempCType),ReturnColumnDefinition(CrtTabDef,i));
			TESTCASE_BEGIN(Heading);
		
			switch (TestSQLType[i])
			{
			case SQL_INTERVAL_YEAR:
				if (CIntDefaultOutput[i].intval.year_month.year == SQLTOCINTDEFAULT[k].yr[i])
				{
					//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTDEFAULT[k].yr[i],CIntDefaultOutput[i].intval.year_month.year);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTDEFAULT[k].yr[i],CIntDefaultOutput[i].intval.year_month.year);
				}
				break;
			case SQL_INTERVAL_MONTH:
				if (CIntDefaultOutput[i].intval.year_month.month == SQLTOCINTDEFAULT[k].mo[i])
				{
					//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTDEFAULT[k].mo[i],CIntDefaultOutput[i].intval.year_month.month);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTDEFAULT[k].mo[i],CIntDefaultOutput[i].intval.year_month.month);
				}
				break;
			case SQL_INTERVAL_YEAR_TO_MONTH:
				if ((CIntDefaultOutput[i].intval.year_month.year == SQLTOCINTDEFAULT[k].yr[i]) &&
					(CIntDefaultOutput[i].intval.year_month.month == SQLTOCINTDEFAULT[k].mo[i]))
				{
					//LogMsg(NONE,"expect: %d-%d and actual: %d-%d are matched\n",SQLTOCINTDEFAULT[k].yr[i],SQLTOCINTDEFAULT[k].mo[i],CIntDefaultOutput[i].intval.year_month.year,CIntDefaultOutput[i].intval.year_month.month);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d-%d and actual: %d-%d are not matched\n",SQLTOCINTDEFAULT[k].yr[i],SQLTOCINTDEFAULT[k].mo[i],CIntDefaultOutput[i].intval.year_month.year,CIntDefaultOutput[i].intval.year_month.month);
				}
				break;
			case SQL_INTERVAL_DAY:
				if (CIntDefaultOutput[i].intval.day_second.day == SQLTOCINTDEFAULT[k].day[i])
				{
					//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTDEFAULT[k].day[i],CIntDefaultOutput[i].intval.day_second.day);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTDEFAULT[k].day[i],CIntDefaultOutput[i].intval.day_second.day);
				}
				break;
			case SQL_INTERVAL_HOUR:
				if (CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i])
				{
					//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTDEFAULT[k].hr[i],CIntDefaultOutput[i].intval.day_second.hour);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTDEFAULT[k].hr[i],CIntDefaultOutput[i].intval.day_second.hour);
				}
				break;
			case SQL_INTERVAL_MINUTE:
				if (CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i])
				{
					//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.minute);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.minute);
				}
				break;
			case SQL_INTERVAL_SECOND:
				if (CIntDefaultOutput[i].intval.day_second.second == SQLTOCINTDEFAULT[k].sec[i])
				{
					//LogMsg(NONE,"expect: %d and actual: %d are matched\n",SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.second);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d and actual: %d are not matched\n",SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.second);
				}
				break;
			case SQL_INTERVAL_DAY_TO_HOUR:
				if ((CIntDefaultOutput[i].intval.day_second.day  == SQLTOCINTDEFAULT[k].day[i]) &&
					(CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i]))
				{
					//LogMsg(NONE,"expect: %d %d and actual: %d %d are matched\n",SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d %d and actual: %d %d are not matched\n",SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour);
				}
				break;
			case SQL_INTERVAL_DAY_TO_MINUTE:
				if ((CIntDefaultOutput[i].intval.day_second.day  == SQLTOCINTDEFAULT[k].day[i]) &&
					(CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i]) &&
					(CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i]))
				{
					//LogMsg(NONE,"expect: %d %d:%d and actual: %d %d:%d are matched\n",SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d %d:%d and actual: %d %d:%d are not matched\n",SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute);
				}
				break;
			case SQL_INTERVAL_DAY_TO_SECOND:
				if ((CIntDefaultOutput[i].intval.day_second.day  == SQLTOCINTDEFAULT[k].day[i]) &&
					(CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i]) &&
					(CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i]) &&
					(CIntDefaultOutput[i].intval.day_second.second == SQLTOCINTDEFAULT[k].sec[i]))
				{
					//LogMsg(NONE,"expect: %d %d:%d:%d and actual: %d %d:%d:%d are matched\n",SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d %d:%d:%d and actual: %d %d:%d:%d are not matched\n",SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}
				break;
			case SQL_INTERVAL_HOUR_TO_MINUTE:
				if ((CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i]) &&
					(CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i]))
				{
					//LogMsg(NONE,"expect: %d:%d and actual: %d:%d are matched\n",SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d:%d and actual: %d:%d are not matched\n",SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute);
				}
				break;
			case SQL_INTERVAL_HOUR_TO_SECOND:
				if ((CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i]) &&
					(CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i]) &&
					(CIntDefaultOutput[i].intval.day_second.second == SQLTOCINTDEFAULT[k].sec[i]))
				{
					//LogMsg(NONE,"expect: %d:%d:%d and actual: %d:%d:%d are matched\n",SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d:%d:%d and actual: %d:%d:%d are not matched\n",SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}
				break;
			case SQL_INTERVAL_MINUTE_TO_SECOND:
				if ((CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i]) &&
					(CIntDefaultOutput[i].intval.day_second.second == SQLTOCINTDEFAULT[k].sec[i]))
				{
					//LogMsg(NONE,"expect: %d:%d and actual: %d:%d are matched\n",SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,"expect: %d:%d and actual: %d:%d are not matched\n",SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}
				break;
			default: break;

			} // end switch
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLCHAR*) DrpTabDef,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================

	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,"End testing API => SQLGetData.\n");
	free_list(var_list);
	TEST_RETURN;
}
