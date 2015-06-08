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

#ifdef UNICODE
#define	MAX_INTERVAL_SINGLE_FIELD	15
#define	MAX_INTERVAL_MULTIPLE_FIELD	10
#else
#define	MAX_INTERVAL_SINGLE_FIELD	9
#define	MAX_INTERVAL_MULTIPLE_FIELD	4
#endif

#define	MAX_INTERVAL_DEFAULT		13

PassFail TestMXSQLGetDataInterval(TestInfo *pTestInfo)
{   
	TEST_DECLARE;
 	TCHAR			Heading[MAX_STRING_SIZE];
 	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;

	int		i,k;
	TCHAR	*InsStr;
	TCHAR	TempCType[50];

	SQL_INTERVAL_STRUCT	CIntSingleFieldOutput[MAX_INTERVAL_SINGLE_FIELD];
	SQLLEN	CIntSingleFieldOutputLen[MAX_INTERVAL_SINGLE_FIELD];

	SQL_INTERVAL_STRUCT	CIntMultipleFieldOutput[MAX_INTERVAL_MULTIPLE_FIELD];
	SQLLEN	CIntMultipleFieldOutputLen[MAX_INTERVAL_MULTIPLE_FIELD];

	SQL_INTERVAL_STRUCT	CIntDefaultOutput[MAX_INTERVAL_DEFAULT];
	SQLLEN	CIntDefaultOutputLen[MAX_INTERVAL_DEFAULT];

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_YEAR.
 
	TCHAR	*TestCTypeIntYear[] = {	_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_YEAR"),_T("SQL_LONGVARCHAR")
#ifdef UNICODE
									,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),
									_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
#endif
								  };
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	yr[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTYEAR[] = 
						{
#ifdef UNICODE
							{
								SQL_C_INTERVAL_YEAR,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' year,'01','01','01','01','01','01','01')"),
								1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_YEAR,SQL_SUCCESS_WITH_INFO,
								_T("('99','23',12.1,15.3,65,44,53,interval '86' year,'72','99','23','72','99','23','72')"),
								99,23,12,15,65,44,53,86,72,99,23,72,99,23,72
							},
							{
 								SQL_C_INTERVAL_YEAR,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_YEAR,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' year,'01')"),
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_YEAR,SQL_SUCCESS_WITH_INFO,
								_T("('99','23',12.1,15.3,65,44,53,interval '86' year,'72')"),
								99,23,12,15,65,44,53,86,72
							},
							{
 								SQL_C_INTERVAL_YEAR,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabYr,*CrtTabYr,*InsTabYr,*SelTabYr;

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_MONTH.
  
	TCHAR	*TestCTypeIntMonth[] = { _T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_MONTH"),_T("SQL_LONGVARCHAR")
									#ifdef UNICODE							
									,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
									,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
									#endif	
									};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	mo[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTMONTH[] = {
#ifdef UNICODE
							{
								SQL_C_INTERVAL_MONTH,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' month,'01','01','01','01','01','01','01')"),
								1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_MONTH,SQL_SUCCESS_WITH_INFO,
								_T("('99','23',12.1,15.3,65,44,53,interval '86' month,'72','99','23','72','99','23','72')"),
								99,23,12,15,65,44,53,86,72,99,23,72,99,23,72
							},
							{
 								SQL_C_INTERVAL_MONTH,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_MONTH,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' month,'01')"),
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_MONTH,SQL_SUCCESS_WITH_INFO,
								_T("('99','23',12.1,15.3,65,44,53,interval '86' month,'72')"),
								99,23,12,15,65,44,53,86,72
							},
							{
 								SQL_C_INTERVAL_MONTH,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabMo,*CrtTabMo,*InsTabMo,*SelTabMo;

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_YEAR_TO_MONTH.
 
	TCHAR	*TestCTypeIntYearMonth[] = { _T("SQL_CHAR"),_T("SQL_VARCHAR"),
										 _T("SQL_LONGVARCHAR"),_T("SQL_INTERVAL_YEAR_TO_MONTH")
										 #ifdef UNICODE
										 ,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
										 #endif
										};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	yr[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	mo[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTYEARMONTH[] = 
						{
#ifdef UNICODE
							{
								SQL_C_INTERVAL_YEAR_TO_MONTH,SQL_SUCCESS,
								_T("('01-01','01-01','01-01',interval '01-01' year to month,'01-01','01-01','01-01','01-01','01-01','01-01')"),
								1,1,1,1,1,1,1,1,1,1,
								1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_YEAR_TO_MONTH,SQL_SUCCESS,
								_T("('2002-12','2000-23','99-72',interval '1923-11' year(4) to month,'2002-12','2000-23','99-72','2002-12','2000-23','99-72')"),
								2002,2000,99,1923,2002,2000,99,2002,2000,99,
								12,23,72,11,12,23,72,12,23,72
							},
							{
 								SQL_C_INTERVAL_YEAR_TO_MONTH,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_YEAR_TO_MONTH,SQL_SUCCESS,
								_T("('01-01','01-01','01-01',interval '01-01' year to month)"),
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_YEAR_TO_MONTH,SQL_SUCCESS,
								_T("('2002-12','2000-23','99-72',interval '1923-11' year(4) to month)"),
								2002,2000,99,1923,
								12,  23,  72,11
							},
							{
 								SQL_C_INTERVAL_YEAR_TO_MONTH,SQL_SUCCESS,
 								_T("(null,null,null,null)"),
 								0,0,0,0,
								0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabYrMo,*CrtTabYrMo,*InsTabYrMo,*SelTabYrMo;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_DAY.
 
	TCHAR	*TestCTypeIntDay[] = {_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_DAY"),_T("SQL_LONGVARCHAR")
								 #ifdef UNICODE									 
								 ,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
						      	 ,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
								#endif
								 };
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	day[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTDAY[] = {
#ifdef UNICODE
							{
								SQL_C_INTERVAL_DAY,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' day,'01','01','01','01','01','01','01')"),
								1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY,SQL_SUCCESS_WITH_INFO,
								_T("('100','0',12.0,15.3,65,44,53,interval '99' day,'72','100','0','72','100','0','72')"),
								100,0,12,15,65,44,53,99,72,100,0,72,100,0,72
							},
							{
 								SQL_C_INTERVAL_DAY,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_DAY,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' day,'01')"),
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY,SQL_SUCCESS_WITH_INFO,
								_T("('100','0',12.0,15.3,65,44,53,interval '99' day,'72')"),
								100,0,12,15,65,44,53,99,72
							},
							{
 								SQL_C_INTERVAL_DAY,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabDay,*CrtTabDay,*InsTabDay,*SelTabDay;

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_HOUR.
 
	TCHAR	*TestCTypeIntHr[] = {_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_HOUR"),_T("SQL_LONGVARCHAR")
							    #ifdef UNICODE
								,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
								,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
								#endif
								};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	hr[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTHOUR[] = {
#ifdef UNICODE
							{
								SQL_C_INTERVAL_HOUR,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' hour,'01','01','01','01','01','01','01')"),
								1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_HOUR,SQL_SUCCESS_WITH_INFO,
								_T("('100','0',12.0,15.3,65,44,53,interval '99' hour,'72','100','0','72','100','0','72')"),
								100,0,12,15,65,44,53,99,72,100,0,72,100,0,72
							},
							{
 								SQL_C_INTERVAL_HOUR,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_HOUR,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' hour,'01')"),
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_HOUR,SQL_SUCCESS_WITH_INFO,
								_T("('100','0',12.0,15.3,65,44,53,interval '99' hour,'72')"),
								100,0,12,15,65,44,53,99,72
							},
							{
 								SQL_C_INTERVAL_HOUR,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabHr,*CrtTabHr,*InsTabHr,*SelTabHr;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_MINUTE.
 
	TCHAR	*TestCTypeIntMin[] = {_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_MINUTE"),_T("SQL_LONGVARCHAR")
								 #ifdef UNICODE
								 ,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
								 ,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
								 #endif
								 };
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	min[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTMINUTE[] = {
#ifdef UNICODE
							{
								SQL_C_INTERVAL_MINUTE,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' minute,'01','01','01','01','01','01','01')"),
								1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_MINUTE,SQL_SUCCESS_WITH_INFO,
								_T("('100','0',12.273,15.3,65,44,59,interval '0' minute,'72','100','0','72','100','0','72')"),
								100,0,12,15,65,44,59,0,72,100,0,72,100,0,72
							},
							{
 								SQL_C_INTERVAL_MINUTE,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_MINUTE,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' minute,'01')"),
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_MINUTE,SQL_SUCCESS_WITH_INFO,
								_T("('100','0',12.273,15.3,65,44,59,interval '0' minute,'72')"),
								100,0,12,15,65,44,59,0,72
							},
							{
 								SQL_C_INTERVAL_MINUTE,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabMin,*CrtTabMin,*InsTabMin,*SelTabMin;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_SECOND.

	TCHAR	*TestCTypeIntSec[] = {
									_T("SQL_CHAR"),_T("SQL_VARCHAR"),_T("SQL_DECIMAL"),_T("SQL_NUMERIC"),_T("SQL_SMALLINT"),_T("SQL_INTEGER"),_T("SQL_BIGINT"),_T("SQL_INTERVAL_SECOND"),_T("SQL_LONGVARCHAR")
									#ifdef UNICODE
									,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
									,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
									#endif
								};
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	sec[MAX_INTERVAL_SINGLE_FIELD];
	} SQLTOCINTSECOND[] = {
#ifdef UNICODE
							{
								SQL_C_INTERVAL_SECOND,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' second,'01','01','01','01','01','01','01')"),
								1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_SECOND,SQL_SUCCESS_WITH_INFO,
								_T("('100','0',12.59,15.0,60,44,53,interval '99' second,'59','100','0','59','100','0','59')"),
								100,0,12,15,60,44,53,99,59,100,0,59,100,0,59
							},
							{
 								SQL_C_INTERVAL_SECOND,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_SECOND,SQL_SUCCESS,
								_T("('01','01',1,1,1,1,1,interval '01' second,'01')"),
								1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_SECOND,SQL_SUCCESS_WITH_INFO,
								_T("('100','0',12.59,15.0,60,44,53,interval '99' second,'59')"),
								100,0,12,15,60,44,53,99,59
							},
							{
 								SQL_C_INTERVAL_SECOND,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabSec,*CrtTabSec,*InsTabSec,*SelTabSec;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_DAY_TO_HOUR.
 
	TCHAR	*TestCTypeIntDayHour[] = {	_T("SQL_CHAR"),_T("SQL_VARCHAR"),
										_T("SQL_LONGVARCHAR"),_T("SQL_INTERVAL_DAY_TO_HOUR")
										#ifdef UNICODE
										,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
										#endif
									 };
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	day[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	hr[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTDAYHOUR[] = {
#ifdef UNICODE
							{
								SQL_C_INTERVAL_DAY_TO_HOUR,SQL_SUCCESS,
								_T("('01 01','01 01','01 01',interval '01 01' day to hour,'01 01','01 01','01 01','01 01','01 01','01 01')"),
								1,1,1,1,1,1,1,1,1,1,
								1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY_TO_HOUR,SQL_SUCCESS,
								_T("('99 23','999 12','365 0',interval '0 23' day(3) to hour,'99 23','999 12','365 0','99 23','999 12','365 0')"),
								99,999,365,0,99,999,365,99,999,365,
								23,12,0,23,23,12,0,23,12,0
							},
							{
 								SQL_C_INTERVAL_DAY_TO_HOUR,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_DAY_TO_HOUR,SQL_SUCCESS,
								_T("('01 01','01 01','01 01',interval '01 01' day to hour)"),
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY_TO_HOUR,SQL_SUCCESS,
								_T("('99 23','999 12','365 0',interval '0 23' day(3) to hour)"),
								99,999,365,0 ,
								23,12, 0,  23
							},
							{
 								SQL_C_INTERVAL_DAY_TO_HOUR,SQL_SUCCESS,
 								_T("(null,null,null,null)"),
 								0,0,0,0,
								0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabDayHr,*CrtTabDayHr,*InsTabDayHr,*SelTabDayHr;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_DAY_TO_MINUTE.
 
	TCHAR	*TestCTypeIntDayMin[] = {	_T("SQL_CHAR"),_T("SQL_VARCHAR"),
										_T("SQL_LONGVARCHAR"),_T("SQL_INTERVAL_DAY_TO_MINUTE")
										#ifdef UNICODE
										,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
										#endif
									};

	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	day[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	hr[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	min[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTDAYMINUTE[] = 
						{
#ifdef UNICODE
							{
								SQL_C_INTERVAL_DAY_TO_MINUTE,SQL_SUCCESS,
								_T("('01 01:01','01 01:01','01 01:01',interval '01 01:01' day to minute,'01 01:01','01 01:01','01 01:01','01 01:01','01 01:01','01 01:01')"),
								1,1,1,1,1,1,1,1,1,1,
								1,1,1,1,1,1,1,1,1,1,
								1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY_TO_MINUTE,SQL_SUCCESS,
								_T("('99 23:59','999 12:30','365 0:0',interval '0 23:54' day(3) to minute,'99 23:59','999 12:30','365 0:0','99 23:59','999 12:30','365 0:0')"),
								99,999,365,0,99,999,365,99,999,365,
								23,12,0,23,23,12,0,23,12,0,
								59,30,0,54,59,30,0,59,30,0
							},
							{
 								SQL_C_INTERVAL_DAY_TO_MINUTE,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_DAY_TO_MINUTE,SQL_SUCCESS,
								_T("('01 01:01','01 01:01','01 01:01',interval '01 01:01' day to minute)"),
								1,1,1,1,
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY_TO_MINUTE,SQL_SUCCESS,
								_T("('99 23:59','999 12:30','365 0:0',interval '0 23:54' day(3) to minute)"),
								99,999,365,0,
								23,12, 0,  23,
								59,30, 0,  54
							},
							{
 								SQL_C_INTERVAL_DAY_TO_MINUTE,SQL_SUCCESS,
 								_T("(null,null,null,null)"),
 								0,0,0,0,
								0,0,0,0,
								0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabDayMin,*CrtTabDayMin,*InsTabDayMin,*SelTabDayMin;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_DAY_TO_SECOND.
 
	TCHAR	*TestCTypeIntDaySec[] = {
										_T("SQL_CHAR"),_T("SQL_VARCHAR"),
										_T("SQL_LONGVARCHAR"),_T("SQL_INTERVAL_DAY_TO_SECOND")
										#ifdef UNICODE
										,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
										#endif
									};

	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	day[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	hr[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	min[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	sec[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTDAYSECOND[] = 
						{
#ifdef UNICODE
							{
								SQL_C_INTERVAL_DAY_TO_SECOND,SQL_SUCCESS,
								_T("('01 01:01:01','01 01:01:01','01 01:01:01',interval '01 01:01:01' day to second,'01 01:01:01','01 01:01:01','01 01:01:01','01 01:01:01','01 01:01:01','01 01:01:01')"),
								1,1,1,1,1,1,1,1,1,1,
								1,1,1,1,1,1,1,1,1,1,
								1,1,1,1,1,1,1,1,1,1,
								1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY_TO_SECOND,SQL_SUCCESS,
								_T("('99 23:59:59','999 12:30:30','365 0:0:0',interval '0 23:54:28' day(3) to second,'99 23:59:59','999 12:30:30','365 0:0:0','99 23:59:59','999 12:30:30','365 0:0:0')"),
								99,999,365,0,99,999,365,99,999,365,
								23,12,0,23,23,12,0,23,12,0,
								59,30,0,54,59,30,0,59,30,0,
								59,30,0,28,59,30,0,59,30,0
							},
							{
 								SQL_C_INTERVAL_DAY_TO_SECOND,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_DAY_TO_SECOND,SQL_SUCCESS,
								_T("('01 01:01:01','01 01:01:01','01 01:01:01',interval '01 01:01:01' day to second)"),
								1,1,1,1,
								1,1,1,1,
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_DAY_TO_SECOND,SQL_SUCCESS,
								_T("('99 23:59:59','999 12:30:30','365 0:0:0',interval '0 23:54:28' day(3) to second)"),
								99,999,365,0,
								23,12, 0,  23,
								59,30, 0,  54,
								59,30, 0,  28
							},
							{
 								SQL_C_INTERVAL_DAY_TO_SECOND,SQL_SUCCESS,
 								_T("(null,null,null,null)"),
 								0,0,0,0,
								0,0,0,0,
								0,0,0,0,
								0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabDaySec,*CrtTabDaySec,*InsTabDaySec,*SelTabDaySec;

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_HOUR_TO_MINUTE.
 
	TCHAR	*TestCTypeIntHrMin[] = {
									_T("SQL_CHAR"),_T("SQL_VARCHAR"),
									_T("SQL_LONGVARCHAR"),_T("SQL_INTERVAL_HOUR_TO_MINUTE")
									#ifdef UNICODE
									,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
									#endif
							   	   };
	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	hr[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	min[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTHOURMINUTE[] = 
						{
#ifdef UNICODE
							{
								SQL_C_INTERVAL_HOUR_TO_MINUTE,SQL_SUCCESS,
								_T("('01:01','01:01','01:01',interval '01:01' hour to minute,'01:01','01:01','01:01','01:01','01:01','01:01')"),
								1,1,1,1,1,1,1,1,1,1,
								1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_HOUR_TO_MINUTE,SQL_SUCCESS,
								_T("('23:59','999:30','0:0',interval '23:54' hour(3) to minute,'23:59','999:30','0:0','23:59','999:30','0:0')"),
								23,999,0,23,23,999,0,23,999,0,
								59,30,0,54,59,30,0,59,30,0
							},
							{
 								SQL_C_INTERVAL_HOUR_TO_MINUTE,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_HOUR_TO_MINUTE,SQL_SUCCESS,
								_T("('01:01','01:01','01:01',interval '01:01' hour to minute)"),
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_HOUR_TO_MINUTE,SQL_SUCCESS,
								_T("('23:59','999:30','0:0',interval '23:54' hour(3) to minute)"),
								23,999,0,23,
								59,30, 0,54
							},
							{
 								SQL_C_INTERVAL_HOUR_TO_MINUTE,SQL_SUCCESS,
 								_T("(null,null,null,null)"),
 								0,0,0,0,
								0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabHrMin,*CrtTabHrMin,*InsTabHrMin,*SelTabHrMin;
 
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_HOUR_TO_SECOND.
 
	TCHAR	*TestCTypeIntHrSec[] = {
									_T("SQL_CHAR"),_T("SQL_VARCHAR"),
									_T("SQL_LONGVARCHAR"),_T("SQL_INTERVAL_HOUR_TO_SECOND")
									#ifdef UNICODE
									,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
									#endif
									};

	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	hr[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	min[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	sec[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTHOURSECOND[] = 
						{
#ifdef UNICODE
							{
								SQL_C_INTERVAL_HOUR_TO_SECOND,SQL_SUCCESS,
								_T("('01:01:01','01:01:01','01:01:01',interval '01:01:01' hour to second,'01:01:01','01:01:01','01:01:01','01:01:01','01:01:01','01:01:01')"),
								1,1,1,1,1,1,1,1,1,1,
								1,1,1,1,1,1,1,1,1,1,
								1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_HOUR_TO_SECOND,SQL_SUCCESS,
								_T("('23:59:59','999:30:30','0:0:0',interval '23:54:28' hour(3) to second,'23:59:59','999:30:30','0:0:0','23:59:59','999:30:30','0:0:0')"),
								23,999,0,23,23,999,0,23,999,0,
								59,30,0,54,59,30,0,59,30,0,
								59,30,0,28,59,30,0,59,30,0
							},
							{
 								SQL_C_INTERVAL_HOUR_TO_SECOND,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_HOUR_TO_SECOND,SQL_SUCCESS,
								_T("('01:01:01','01:01:01','01:01:01',interval '01:01:01' hour to second)"),
								1,1,1,1,
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_HOUR_TO_SECOND,SQL_SUCCESS,
								_T("('23:59:59','999:30:30','0:0:0',interval '23:54:28' hour(3) to second)"),
								23,999,0,23,
								59,30, 0,54,
								59,30, 0,28
							},
							{
 								SQL_C_INTERVAL_HOUR_TO_SECOND,SQL_SUCCESS,
 								_T("(null,null,null,null)"),
 								0,0,0,0,
								0,0,0,0,
								0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabHrSec,*CrtTabHrSec,*InsTabHrSec,*SelTabHrSec;

//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_MINUTE_TO_SECOND.
 
	TCHAR	*TestCTypeIntMinSec[] = {
										_T("SQL_CHAR"),_T("SQL_VARCHAR"),
										_T("SQL_LONGVARCHAR"),_T("SQL_INTERVAL_MINUTE_TO_SECOND")
										#ifdef UNICODE
										,_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR"),_T("SQL_WCHAR"),_T("SQL_WVARCHAR"),_T("SQL_WLONGVARCHAR")
										#endif
										};

	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
		SQLUINTEGER	min[MAX_INTERVAL_MULTIPLE_FIELD];
		SQLUINTEGER	sec[MAX_INTERVAL_MULTIPLE_FIELD];
	} SQLTOCINTMINUTESECOND[] = 
						{
#ifdef UNICODE
							{
								SQL_C_INTERVAL_MINUTE_TO_SECOND,SQL_SUCCESS,
								_T("('01:01','01:01','01:01',interval '01:01' minute to second,'01:01','01:01','01:01','01:01','01:01','01:01')"),
								1,1,1,1,1,1,1,1,1,1,
								1,1,1,1,1,1,1,1,1,1
							},
							{
								SQL_C_INTERVAL_MINUTE_TO_SECOND,SQL_SUCCESS,
								_T("('59:59','999:99','0:0',interval '54:28' minute(3) to second,'59:59','999:99','0:0','59:59','999:99','0:0')"),
								59,999,0,54,59,999,0,59,999,0,
								59,99,0,28,59,99,0,59,99,0
							},
							{
 								SQL_C_INTERVAL_MINUTE_TO_SECOND,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null)"),
 								0,0,0,0,0,0,0,0,0,0,
								0,0,0,0,0,0,0,0,0,0
							},
#else
							{
								SQL_C_INTERVAL_MINUTE_TO_SECOND,SQL_SUCCESS,
								_T("('01:01','01:01','01:01',interval '01:01' minute to second)"),
								1,1,1,1,
								1,1,1,1
							},
							{
								SQL_C_INTERVAL_MINUTE_TO_SECOND,SQL_SUCCESS,
								_T("('59:59','999:99','0:0',interval '54:28' minute(3) to second)"),
								59,999,0,54,
								59,99, 0,28
							},
							{
 								SQL_C_INTERVAL_MINUTE_TO_SECOND,SQL_SUCCESS,
 								_T("(null,null,null,null)"),
 								0,0,0,0,
								0,0,0,0
							},
#endif
							{
								999,
							}
						};

	TCHAR	*DrpTabMinSec,*CrtTabMinSec,*InsTabMinSec,*SelTabMinSec;
  
//===========================================================================================================
//====== Data Structures for conversion to SQL_C_INTERVAL_DEFAULT.
 
	TCHAR	*TestCTypeIntDef[] = {_T("SQL_INTERVAL_YEAR"),_T("SQL_INTERVAL_MONTH"),_T("SQL_INTERVAL_YEAR_TO_MONTH"),_T("SQL_INTERVAL_DAY"),_T("SQL_INTERVAL_HOUR"),_T("SQL_INTERVAL_MINUTE"),_T("SQL_INTERVAL_SECOND"),_T("SQL_INTERVAL_DAY_TO_HOUR"),_T("SQL_INTERVAL_DAY_TO_MINUTE"),_T("SQL_INTERVAL_DAY_TO_SECOND"),_T("SQL_INTERVAL_HOUR_TO_MINUTE"),_T("SQL_INTERVAL_HOUR_TO_SECOND"),_T("SQL_INTERVAL_MINUTE_TO_SECOND")};
	SQLSMALLINT	TestSQLType[] = {SQL_INTERVAL_YEAR,SQL_INTERVAL_MONTH,SQL_INTERVAL_YEAR_TO_MONTH,SQL_INTERVAL_DAY,SQL_INTERVAL_HOUR,SQL_INTERVAL_MINUTE,SQL_INTERVAL_SECOND,SQL_INTERVAL_DAY_TO_HOUR,SQL_INTERVAL_DAY_TO_MINUTE,SQL_INTERVAL_DAY_TO_SECOND,SQL_INTERVAL_HOUR_TO_MINUTE,SQL_INTERVAL_HOUR_TO_SECOND,SQL_INTERVAL_MINUTE_TO_SECOND};

	struct
	{
		SQLSMALLINT CType;
		RETCODE		rcode;
		TCHAR		*InsCol;
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
								_T("(interval '01' year,interval '01' month,interval '01-01' year to month,interval '01' day,interval '01' hour,interval '01' minute,interval '01' second,interval '01 01' day to hour,interval '01 01:01' day to minute,interval '01 01:01:01' day to second,interval '01:01' hour to minute,interval '01:01:01' hour to second,interval '01:01' minute to second)"),
								1,0,1,0,0,0,0,0,0,0,0,0,0,
								0,1,1,0,0,0,0,0,0,0,0,0,0,
								0,0,0,1,0,0,0,1,1,1,0,0,0,
								0,0,0,0,1,0,0,1,1,1,1,1,0,
								0,0,0,0,0,1,0,0,1,1,1,1,1,
								0,0,0,0,0,0,1,0,0,1,0,1,1,
							},
							{
 								SQL_C_DEFAULT,SQL_SUCCESS,
 								_T("(interval '99' year,interval '99' month,interval '99-11' year to month,interval '99' day,interval '99' hour,interval '99' minute,interval '99' second,interval '99 23' day to hour,interval '99 23:59' day to minute,interval '99 23:59:59' day to second,interval '99:59' hour to minute,interval '99:59:59' hour to second,interval '99:59' minute to second)"),
 								99,0,99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
								0,99,11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
								0, 0, 0,99, 0, 0, 0,99,99,99, 0, 0, 0,
								0, 0, 0, 0,99, 0, 0,23,23,23,99,99, 0,
								0, 0, 0, 0, 0,99, 0, 0,59,59,59,59,99,
								0, 0, 0, 0, 0, 0,99, 0, 0,59, 0,59,59,
							},
							{
 								SQL_C_DEFAULT,SQL_SUCCESS,
 								_T("(null,null,null,null,null,null,null,null,null,null,null,null,null)"),
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

	TCHAR	*DrpTabDef,*CrtTabDef,*InsTabDef,*SelTabDef;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLGetDataInterval"), charset_file);
	if (var_list == NULL) return FAILED;

	DrpTabYr = var_mapping(_T("SQLGetDataInterval_DrpTabYr"), var_list);
	CrtTabYr = var_mapping(_T("SQLGetDataInterval_CrtTabYr"), var_list);
	InsTabYr = var_mapping(_T("SQLGetDataInterval_InsTabYr"), var_list);
	SelTabYr = var_mapping(_T("SQLGetDataInterval_SelTabYr"), var_list);

	DrpTabMo = var_mapping(_T("SQLGetDataInterval_DrpTabMo"), var_list);
	CrtTabMo = var_mapping(_T("SQLGetDataInterval_CrtTabMo"), var_list);
	InsTabMo = var_mapping(_T("SQLGetDataInterval_InsTabMo"), var_list);
	SelTabMo = var_mapping(_T("SQLGetDataInterval_SelTabMo"), var_list);

	DrpTabYrMo = var_mapping(_T("SQLGetDataInterval_DrpTabYrMo"), var_list);
	CrtTabYrMo = var_mapping(_T("SQLGetDataInterval_CrtTabYrMo"), var_list);
	InsTabYrMo = var_mapping(_T("SQLGetDataInterval_InsTabYrMo"), var_list);
	SelTabYrMo = var_mapping(_T("SQLGetDataInterval_SelTabYrMo"), var_list);

	DrpTabDay = var_mapping(_T("SQLGetDataInterval_DrpTabDay"), var_list);
	CrtTabDay = var_mapping(_T("SQLGetDataInterval_CrtTabDay"), var_list);
	InsTabDay = var_mapping(_T("SQLGetDataInterval_InsTabDay"), var_list);
	SelTabDay = var_mapping(_T("SQLGetDataInterval_SelTabDay"), var_list);

	DrpTabHr = var_mapping(_T("SQLGetDataInterval_DrpTabHr"), var_list);
	CrtTabHr = var_mapping(_T("SQLGetDataInterval_CrtTabHr"), var_list);
	InsTabHr = var_mapping(_T("SQLGetDataInterval_InsTabHr"), var_list);
	SelTabHr = var_mapping(_T("SQLGetDataInterval_SelTabHr"), var_list);

	DrpTabMin = var_mapping(_T("SQLGetDataInterval_DrpTabMin"), var_list);
	CrtTabMin = var_mapping(_T("SQLGetDataInterval_CrtTabMin"), var_list);
	InsTabMin = var_mapping(_T("SQLGetDataInterval_InsTabMin"), var_list);
	SelTabMin = var_mapping(_T("SQLGetDataInterval_SelTabMin"), var_list);

	DrpTabSec = var_mapping(_T("SQLGetDataInterval_DrpTabSec"), var_list);
	CrtTabSec = var_mapping(_T("SQLGetDataInterval_CrtTabSec"), var_list);
	InsTabSec = var_mapping(_T("SQLGetDataInterval_InsTabSec"), var_list);
	SelTabSec = var_mapping(_T("SQLGetDataInterval_SelTabSec"), var_list);

	DrpTabDayHr = var_mapping(_T("SQLGetDataInterval_DrpTabDayHr"), var_list);
	CrtTabDayHr = var_mapping(_T("SQLGetDataInterval_CrtTabDayHr"), var_list);
	InsTabDayHr = var_mapping(_T("SQLGetDataInterval_InsTabDayHr"), var_list);
	SelTabDayHr = var_mapping(_T("SQLGetDataInterval_SelTabDayHr"), var_list);

	DrpTabDaySec = var_mapping(_T("SQLGetDataInterval_DrpTabDaySec"), var_list);
	CrtTabDaySec = var_mapping(_T("SQLGetDataInterval_CrtTabDaySec"), var_list);
	InsTabDaySec = var_mapping(_T("SQLGetDataInterval_InsTabDaySec"), var_list);
	SelTabDaySec = var_mapping(_T("SQLGetDataInterval_SelTabDaySec"), var_list);

	DrpTabDayMin = var_mapping(_T("SQLGetDataInterval_DrpTabDayMin"), var_list);
	CrtTabDayMin = var_mapping(_T("SQLGetDataInterval_CrtTabDayMin"), var_list);
	InsTabDayMin = var_mapping(_T("SQLGetDataInterval_InsTabDayMin"), var_list);
	SelTabDayMin = var_mapping(_T("SQLGetDataInterval_SelTabDayMin"), var_list);

	DrpTabHrMin = var_mapping(_T("SQLGetDataInterval_DrpTabHrMin"), var_list);
	CrtTabHrMin = var_mapping(_T("SQLGetDataInterval_CrtTabHrMin"), var_list);
	InsTabHrMin = var_mapping(_T("SQLGetDataInterval_InsTabHrMin"), var_list);
	SelTabHrMin = var_mapping(_T("SQLGetDataInterval_SelTabHrMin"), var_list);

	DrpTabHrSec = var_mapping(_T("SQLGetDataInterval_DrpTabHrSec"), var_list);
	CrtTabHrSec = var_mapping(_T("SQLGetDataInterval_CrtTabHrSec"), var_list);
	InsTabHrSec = var_mapping(_T("SQLGetDataInterval_InsTabHrSec"), var_list);
	SelTabHrSec = var_mapping(_T("SQLGetDataInterval_SelTabHrSec"), var_list);

	DrpTabMinSec = var_mapping(_T("SQLGetDataInterval_DrpTabMinSec"), var_list);
	CrtTabMinSec = var_mapping(_T("SQLGetDataInterval_CrtTabMinSec"), var_list);
	InsTabMinSec = var_mapping(_T("SQLGetDataInterval_InsTabMinSec"), var_list);
	SelTabMinSec = var_mapping(_T("SQLGetDataInterval_SelTabMinSec"), var_list);

	DrpTabDef = var_mapping(_T("SQLGetDataInterval_DrpTabDef"), var_list);
	CrtTabDef = var_mapping(_T("SQLGetDataInterval_CrtTabDef"), var_list);
	InsTabDef = var_mapping(_T("SQLGetDataInterval_InsTabDef"), var_list);
	SelTabDef = var_mapping(_T("SQLGetDataInterval_SelTabDef"), var_list);
 
//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLGetData.\n"));

	TEST_INIT;

	TESTCASE_BEGIN("Setup for SQLGetData Interval tests\n");
	if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
	{
		LogMsg(NONE,_T("Unable to connect\n"));
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
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabYr,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabYr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabYr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabYr);
		_tcscat(InsStr,SQLTOCINTYEAR[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabYr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  
			
		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTYEAR[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntYear[i],SQLCTypeToChar(SQLTOCINTYEAR[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntYear[i],SQLCTypeToChar(SQLTOCINTYEAR[k].CType,TempCType),ReturnColumnDefinition(CrtTabYr,i));
			TESTCASE_BEGINW(Heading);
			if (CIntSingleFieldOutput[i].intval.year_month.year == SQLTOCINTYEAR[k].yr[i])
			{
				LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTYEAR[k].yr[i],CIntSingleFieldOutput[i].intval.year_month.year);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTYEAR[k].yr[i],CIntSingleFieldOutput[i].intval.year_month.year);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabYr,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_MONTH
 	k = 0;
	while (SQLTOCINTMONTH[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMo,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabMo);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabMo,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabMo);
		_tcscat(InsStr,SQLTOCINTMONTH[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabMo,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTMONTH[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  


		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntMonth[i],SQLCTypeToChar(SQLTOCINTMONTH[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntMonth[i],SQLCTypeToChar(SQLTOCINTMONTH[k].CType,TempCType),ReturnColumnDefinition(CrtTabMo,i));
			TESTCASE_BEGINW(Heading);
			if (CIntSingleFieldOutput[i].intval.year_month.month == SQLTOCINTMONTH[k].mo[i])
			{
				LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTMONTH[k].mo[i],CIntSingleFieldOutput[i].intval.year_month.month);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTMONTH[k].mo[i],CIntSingleFieldOutput[i].intval.year_month.month);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMo,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_YEAR_TO_MONTH
	k = 0;
	while (SQLTOCINTYEARMONTH[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabYrMo,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabYrMo);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabYrMo,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabYrMo);
		_tcscat(InsStr,SQLTOCINTYEARMONTH[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabYrMo,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTYEARMONTH[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntYearMonth[i],SQLCTypeToChar(SQLTOCINTYEARMONTH[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntYearMonth[i],SQLCTypeToChar(SQLTOCINTYEARMONTH[k].CType,TempCType),ReturnColumnDefinition(CrtTabYrMo,i));
			TESTCASE_BEGINW(Heading);
			if ((CIntMultipleFieldOutput[i].intval.year_month.year == SQLTOCINTYEARMONTH[k].yr[i]) &&
				(CIntMultipleFieldOutput[i].intval.year_month.month == SQLTOCINTYEARMONTH[k].mo[i]))
			{
				LogMsg(NONE,_T("expect: %d-%d and actual: %d-%d are matched\n"),SQLTOCINTYEARMONTH[k].yr[i],SQLTOCINTYEARMONTH[k].mo[i],CIntMultipleFieldOutput[i].intval.year_month.year,CIntMultipleFieldOutput[i].intval.year_month.month);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d-%d and actual: %d-%d are not matched\n"),SQLTOCINTYEARMONTH[k].yr[i],SQLTOCINTYEARMONTH[k].mo[i],CIntMultipleFieldOutput[i].intval.year_month.year,CIntMultipleFieldOutput[i].intval.year_month.month);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabYrMo,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_DAY
	k = 0;
	while (SQLTOCINTDAY[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDay,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabDay);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabDay,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabDay);
		_tcscat(InsStr,SQLTOCINTDAY[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabDay,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTDAY[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END; 

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntDay[i],SQLCTypeToChar(SQLTOCINTDAY[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntDay[i],SQLCTypeToChar(SQLTOCINTDAY[k].CType,TempCType),ReturnColumnDefinition(CrtTabDay,i));
			TESTCASE_BEGINW(Heading);
			if (CIntSingleFieldOutput[i].intval.day_second.day == SQLTOCINTDAY[k].day[i])
			{
				LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTDAY[k].day[i],CIntSingleFieldOutput[i].intval.day_second.day);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTDAY[k].day[i],CIntSingleFieldOutput[i].intval.day_second.day);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDay,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_HOUR
	k = 0;
	while (SQLTOCINTHOUR[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabHr,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabHr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabHr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabHr);
		_tcscat(InsStr,SQLTOCINTHOUR[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabHr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTHOUR[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntHr[i],SQLCTypeToChar(SQLTOCINTHOUR[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntHr[i],SQLCTypeToChar(SQLTOCINTHOUR[k].CType,TempCType),ReturnColumnDefinition(CrtTabHr,i));
			TESTCASE_BEGINW(Heading);
			if (CIntSingleFieldOutput[i].intval.day_second.hour == SQLTOCINTHOUR[k].hr[i])
			{
				LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTHOUR[k].hr[i],CIntSingleFieldOutput[i].intval.day_second.hour);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTHOUR[k].hr[i],CIntSingleFieldOutput[i].intval.day_second.hour);
			}
			TESTCASE_END;
		}

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabHr,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_MINUTE
	k = 0;
	while (SQLTOCINTMINUTE[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMin,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabMin);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabMin);
		_tcscat(InsStr,SQLTOCINTMINUTE[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END; 
		
		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTMINUTE[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntMin[i],SQLCTypeToChar(SQLTOCINTMINUTE[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntMin[i],SQLCTypeToChar(SQLTOCINTMINUTE[k].CType,TempCType),ReturnColumnDefinition(CrtTabMin,i));
			TESTCASE_BEGINW(Heading);
			if (CIntSingleFieldOutput[i].intval.day_second.minute == SQLTOCINTMINUTE[k].min[i])
			{
				LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTMINUTE[k].min[i],CIntSingleFieldOutput[i].intval.day_second.minute);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTMINUTE[k].min[i],CIntSingleFieldOutput[i].intval.day_second.minute);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMin,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_SECOND
	k = 0;
	while (SQLTOCINTSECOND[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabSec,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabSec);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabSec);
		_tcscat(InsStr,SQLTOCINTSECOND[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTSECOND[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_SINGLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntSec[i],SQLCTypeToChar(SQLTOCINTSECOND[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntSec[i],SQLCTypeToChar(SQLTOCINTSECOND[k].CType,TempCType),ReturnColumnDefinition(CrtTabSec,i));
			TESTCASE_BEGINW(Heading);
			if (CIntSingleFieldOutput[i].intval.day_second.second == SQLTOCINTSECOND[k].sec[i])
			{
				LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTSECOND[k].sec[i],CIntSingleFieldOutput[i].intval.day_second.second);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTSECOND[k].sec[i],CIntSingleFieldOutput[i].intval.day_second.second);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabSec,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_DAY_TO_HOUR
	k = 0;
	while (SQLTOCINTDAYHOUR[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDayHr,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabDayHr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabDayHr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabDayHr);
		_tcscat(InsStr,SQLTOCINTDAYHOUR[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabDayHr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTDAYHOUR[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END; 

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntDayHour[i],SQLCTypeToChar(SQLTOCINTDAYHOUR[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntDayHour[i],SQLCTypeToChar(SQLTOCINTDAYHOUR[k].CType,TempCType),ReturnColumnDefinition(CrtTabDayHr,i));
			TESTCASE_BEGINW(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.day  == SQLTOCINTDAYHOUR[k].day[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.hour == SQLTOCINTDAYHOUR[k].hr[i]))
			{
				LogMsg(NONE,_T("expect: %d %d and actual: %d %d are matched\n"),SQLTOCINTDAYHOUR[k].day[i],SQLTOCINTDAYHOUR[k].hr[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d %d and actual: %d %d are not matched\n"),SQLTOCINTDAYHOUR[k].day[i],SQLTOCINTDAYHOUR[k].hr[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDayHr,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_DAY_TO_MINUTE
	k = 0;
	while (SQLTOCINTDAYMINUTE[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDayMin,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabDayMin);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabDayMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabDayMin);
		_tcscat(InsStr,SQLTOCINTDAYMINUTE[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabDayMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTDAYMINUTE[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntDayMin[i],SQLCTypeToChar(SQLTOCINTDAYMINUTE[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntDayMin[i],SQLCTypeToChar(SQLTOCINTDAYMINUTE[k].CType,TempCType),ReturnColumnDefinition(CrtTabDayMin,i));
			TESTCASE_BEGINW(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.day  == SQLTOCINTDAYMINUTE[k].day[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.hour == SQLTOCINTDAYMINUTE[k].hr[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.minute == SQLTOCINTDAYMINUTE[k].min[i]))
			{
				LogMsg(NONE,_T("expect: %d %d:%d and actual: %d %d:%d are matched\n"),SQLTOCINTDAYMINUTE[k].day[i],SQLTOCINTDAYMINUTE[k].hr[i],SQLTOCINTDAYMINUTE[k].min[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d %d:%d and actual: %d %d:%d are not matched\n"),SQLTOCINTDAYMINUTE[k].day[i],SQLTOCINTDAYMINUTE[k].hr[i],SQLTOCINTDAYMINUTE[k].min[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDayMin,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_DAY_TO_SECOND
	k = 0;
	while (SQLTOCINTDAYSECOND[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDaySec,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabDaySec);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabDaySec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabDaySec);
		_tcscat(InsStr,SQLTOCINTDAYSECOND[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabDaySec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTDAYSECOND[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntDaySec[i],SQLCTypeToChar(SQLTOCINTDAYSECOND[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntDaySec[i],SQLCTypeToChar(SQLTOCINTDAYSECOND[k].CType,TempCType),ReturnColumnDefinition(CrtTabDaySec,i));
			TESTCASE_BEGINW(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.day  == SQLTOCINTDAYSECOND[k].day[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.hour == SQLTOCINTDAYSECOND[k].hr[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.minute == SQLTOCINTDAYSECOND[k].min[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.second == SQLTOCINTDAYSECOND[k].sec[i]))
			{
				LogMsg(NONE,_T("expect: %d %d:%d:%d and actual: %d %d:%d:%d are matched\n"),SQLTOCINTDAYSECOND[k].day[i],SQLTOCINTDAYSECOND[k].hr[i],SQLTOCINTDAYSECOND[k].min[i],SQLTOCINTDAYSECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d %d:%d:%d and actual: %d %d:%d:%d are not matched\n"),SQLTOCINTDAYSECOND[k].day[i],SQLTOCINTDAYSECOND[k].hr[i],SQLTOCINTDAYSECOND[k].min[i],SQLTOCINTDAYSECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.day ,CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDaySec,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_HOUR_TO_MINUTE
	k = 0;
	while (SQLTOCINTHOURMINUTE[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabHrMin,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabHrMin);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabHrMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabHrMin);
		_tcscat(InsStr,SQLTOCINTHOURMINUTE[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabHrMin,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTHOURMINUTE[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntHrMin[i],SQLCTypeToChar(SQLTOCINTHOURMINUTE[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntHrMin[i],SQLCTypeToChar(SQLTOCINTHOURMINUTE[k].CType,TempCType),ReturnColumnDefinition(CrtTabHrMin,i));
			TESTCASE_BEGINW(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.hour == SQLTOCINTHOURMINUTE[k].hr[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.minute == SQLTOCINTHOURMINUTE[k].min[i]))
			{
				LogMsg(NONE,_T("expect: %d:%d and actual: %d:%d are matched\n"),SQLTOCINTHOURMINUTE[k].hr[i],SQLTOCINTHOURMINUTE[k].min[i],CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d:%d and actual: %d:%d are not matched\n"),SQLTOCINTHOURMINUTE[k].hr[i],SQLTOCINTHOURMINUTE[k].min[i],CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabHrMin,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_HOUR_TO_SECOND
	k = 0;
	while (SQLTOCINTHOURSECOND[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabHrSec,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabHrSec);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabHrSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabHrSec);
		_tcscat(InsStr,SQLTOCINTHOURSECOND[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabHrSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTHOURSECOND[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END; 

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntHrSec[i],SQLCTypeToChar(SQLTOCINTHOURSECOND[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntHrSec[i],SQLCTypeToChar(SQLTOCINTHOURSECOND[k].CType,TempCType),ReturnColumnDefinition(CrtTabHrSec,i));
			TESTCASE_BEGINW(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.hour == SQLTOCINTHOURSECOND[k].hr[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.minute == SQLTOCINTHOURSECOND[k].min[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.second == SQLTOCINTHOURSECOND[k].sec[i]))
			{
				LogMsg(NONE,_T("expect: %d:%d:%d and actual: %d:%d:%d are matched\n"),SQLTOCINTHOURSECOND[k].hr[i],SQLTOCINTHOURSECOND[k].min[i],SQLTOCINTHOURSECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d:%d:%d and actual: %d:%d:%d are not matched\n"),SQLTOCINTHOURSECOND[k].hr[i],SQLTOCINTHOURSECOND[k].min[i],SQLTOCINTHOURSECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.hour,CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabHrSec,SQL_NTS);
		free(InsStr);
		k++;
	}

//=============================================================================================================
// Testing conversion from SQL to SQL_C_INTERVAL_MINUTE_TO_SECOND
	k = 0;
	while (SQLTOCINTMINUTESECOND[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMinSec,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabMinSec);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabMinSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabMinSec);
		_tcscat(InsStr,SQLTOCINTMINUTESECOND[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabMinSec,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTMINUTESECOND[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_MULTIPLE_FIELD; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntMinSec[i],SQLCTypeToChar(SQLTOCINTMINUTESECOND[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntMinSec[i],SQLCTypeToChar(SQLTOCINTMINUTESECOND[k].CType,TempCType),ReturnColumnDefinition(CrtTabMinSec,i));
			TESTCASE_BEGINW(Heading);
			if ((CIntMultipleFieldOutput[i].intval.day_second.minute == SQLTOCINTMINUTESECOND[k].min[i]) &&
				(CIntMultipleFieldOutput[i].intval.day_second.second == SQLTOCINTMINUTESECOND[k].sec[i]))
			{
				LogMsg(NONE,_T("expect: %d:%d and actual: %d:%d are matched\n"),SQLTOCINTMINUTESECOND[k].min[i],SQLTOCINTMINUTESECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}	
			else
			{
				TEST_FAILED;	
				LogMsg(ERRMSG,_T("expect: %d:%d and actual: %d:%d are not matched\n"),SQLTOCINTMINUTESECOND[k].min[i],SQLTOCINTMINUTESECOND[k].sec[i],CIntMultipleFieldOutput[i].intval.day_second.minute,CIntMultipleFieldOutput[i].intval.day_second.second);
			}
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabMinSec,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================
// Testing conversion from SQL(interval datatypes to SQL_C_DEFAULT
	k = 0;
	while (SQLTOCINTDEFAULT[k].CType != 999)
	{
		_stprintf(Heading,_T("SQLGetData: create insert and select from table \n"));
		TESTCASE_BEGINW(Heading);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDef,SQL_NTS);
		LogMsg(NONE,_T("%s\n"),CrtTabDef);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)CrtTabDef,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		InsStr = (TCHAR *)malloc(MAX_NOS_SIZE);
		_tcscpy(InsStr,_T(""));
		_tcscat(InsStr,InsTabDef);
		_tcscat(InsStr,SQLTOCINTDEFAULT[k].InsCol);
		LogMsg(NONE,_T("%s\n"),InsStr);
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)InsStr,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		returncode = SQLExecDirect(hstmt,(SQLTCHAR*)SelTabDef,SQL_NTS);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
		}
		TESTCASE_END;  

		_stprintf(Heading,_T("SQLGetData: Positive test fetch from sql to %s.\n"),SQLCTypeToChar(SQLTOCINTDEFAULT[k].CType,TempCType));
		TESTCASE_BEGINW(Heading);
		returncode = SQLFetch(hstmt);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFetch"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		TESTCASE_END;  

		for (i = 0; i < MAX_INTERVAL_DEFAULT; i++)
		{  
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for converting %s to %s after fetch.\n"),i+1,TestCTypeIntDef[i],SQLCTypeToChar(SQLTOCINTDEFAULT[k].CType,TempCType));
			TESTCASE_BEGINW(Heading);
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
			_stprintf(Heading,_T("SQLGetData: Positive test #%d for comparing values %s to %s after fetched for column %s.\n"),i+1,TestCTypeIntDef[i],SQLCTypeToChar(SQLTOCINTDEFAULT[k].CType,TempCType),ReturnColumnDefinition(CrtTabDef,i));
			TESTCASE_BEGINW(Heading);
		
			switch (TestSQLType[i])
			{
			case SQL_INTERVAL_YEAR:
				if (CIntDefaultOutput[i].intval.year_month.year == SQLTOCINTDEFAULT[k].yr[i])
				{
					LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTDEFAULT[k].yr[i],CIntDefaultOutput[i].intval.year_month.year);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTDEFAULT[k].yr[i],CIntDefaultOutput[i].intval.year_month.year);
				}
				break;
			case SQL_INTERVAL_MONTH:
				if (CIntDefaultOutput[i].intval.year_month.month == SQLTOCINTDEFAULT[k].mo[i])
				{
					LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTDEFAULT[k].mo[i],CIntDefaultOutput[i].intval.year_month.month);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTDEFAULT[k].mo[i],CIntDefaultOutput[i].intval.year_month.month);
				}
				break;
			case SQL_INTERVAL_YEAR_TO_MONTH:
				if ((CIntDefaultOutput[i].intval.year_month.year == SQLTOCINTDEFAULT[k].yr[i]) &&
					(CIntDefaultOutput[i].intval.year_month.month == SQLTOCINTDEFAULT[k].mo[i]))
				{
					LogMsg(NONE,_T("expect: %d-%d and actual: %d-%d are matched\n"),SQLTOCINTDEFAULT[k].yr[i],SQLTOCINTDEFAULT[k].mo[i],CIntDefaultOutput[i].intval.year_month.year,CIntDefaultOutput[i].intval.year_month.month);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d-%d and actual: %d-%d are not matched\n"),SQLTOCINTDEFAULT[k].yr[i],SQLTOCINTDEFAULT[k].mo[i],CIntDefaultOutput[i].intval.year_month.year,CIntDefaultOutput[i].intval.year_month.month);
				}
				break;
			case SQL_INTERVAL_DAY:
				if (CIntDefaultOutput[i].intval.day_second.day == SQLTOCINTDEFAULT[k].day[i])
				{
					LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTDEFAULT[k].day[i],CIntDefaultOutput[i].intval.day_second.day);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTDEFAULT[k].day[i],CIntDefaultOutput[i].intval.day_second.day);
				}
				break;
			case SQL_INTERVAL_HOUR:
				if (CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i])
				{
					LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTDEFAULT[k].hr[i],CIntDefaultOutput[i].intval.day_second.hour);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTDEFAULT[k].hr[i],CIntDefaultOutput[i].intval.day_second.hour);
				}
				break;
			case SQL_INTERVAL_MINUTE:
				if (CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i])
				{
					LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.minute);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.minute);
				}
				break;
			case SQL_INTERVAL_SECOND:
				if (CIntDefaultOutput[i].intval.day_second.second == SQLTOCINTDEFAULT[k].sec[i])
				{
					LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.second);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d and actual: %d are not matched\n"),SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.second);
				}
				break;
			case SQL_INTERVAL_DAY_TO_HOUR:
				if ((CIntDefaultOutput[i].intval.day_second.day  == SQLTOCINTDEFAULT[k].day[i]) &&
					(CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i]))
				{
					LogMsg(NONE,_T("expect: %d %d and actual: %d %d are matched\n"),SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d %d and actual: %d %d are not matched\n"),SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour);
				}
				break;
			case SQL_INTERVAL_DAY_TO_MINUTE:
				if ((CIntDefaultOutput[i].intval.day_second.day  == SQLTOCINTDEFAULT[k].day[i]) &&
					(CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i]) &&
					(CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i]))
				{
					LogMsg(NONE,_T("expect: %d %d:%d and actual: %d %d:%d are matched\n"),SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d %d:%d and actual: %d %d:%d are not matched\n"),SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute);
				}
				break;
			case SQL_INTERVAL_DAY_TO_SECOND:
				if ((CIntDefaultOutput[i].intval.day_second.day  == SQLTOCINTDEFAULT[k].day[i]) &&
					(CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i]) &&
					(CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i]) &&
					(CIntDefaultOutput[i].intval.day_second.second == SQLTOCINTDEFAULT[k].sec[i]))
				{
					LogMsg(NONE,_T("expect: %d %d:%d:%d and actual: %d %d:%d:%d are matched\n"),SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d %d:%d:%d and actual: %d %d:%d:%d are not matched\n"),SQLTOCINTDEFAULT[k].day[i],SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.day ,CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}
				break;
			case SQL_INTERVAL_HOUR_TO_MINUTE:
				if ((CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i]) &&
					(CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i]))
				{
					LogMsg(NONE,_T("expect: %d:%d and actual: %d:%d are matched\n"),SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d:%d and actual: %d:%d are not matched\n"),SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute);
				}
				break;
			case SQL_INTERVAL_HOUR_TO_SECOND:
				if ((CIntDefaultOutput[i].intval.day_second.hour == SQLTOCINTDEFAULT[k].hr[i]) &&
					(CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i]) &&
					(CIntDefaultOutput[i].intval.day_second.second == SQLTOCINTDEFAULT[k].sec[i]))
				{
					LogMsg(NONE,_T("expect: %d:%d:%d and actual: %d:%d:%d are matched\n"),SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d:%d:%d and actual: %d:%d:%d are not matched\n"),SQLTOCINTDEFAULT[k].hr[i],SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.hour,CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}
				break;
			case SQL_INTERVAL_MINUTE_TO_SECOND:
				if ((CIntDefaultOutput[i].intval.day_second.minute == SQLTOCINTDEFAULT[k].min[i]) &&
					(CIntDefaultOutput[i].intval.day_second.second == SQLTOCINTDEFAULT[k].sec[i]))
				{
					LogMsg(NONE,_T("expect: %d:%d and actual: %d:%d are matched\n"),SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}	
				else
				{
					TEST_FAILED;	
					LogMsg(ERRMSG,_T("expect: %d:%d and actual: %d:%d are not matched\n"),SQLTOCINTDEFAULT[k].min[i],SQLTOCINTDEFAULT[k].sec[i],CIntDefaultOutput[i].intval.day_second.minute,CIntDefaultOutput[i].intval.day_second.second);
				}
				break;
			default: break;

			} // end switch
			TESTCASE_END;
		}  

		SQLFreeStmt(hstmt,SQL_CLOSE);
		SQLFreeStmt(hstmt,SQL_UNBIND);
		SQLExecDirect(hstmt,(SQLTCHAR*) DrpTabDef,SQL_NTS);
		free(InsStr);
		k++;
	}
 
//=============================================================================================================

	FullDisconnect3(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLGetData.\n"));
	free_list(var_list);
	TEST_RETURN;
}
