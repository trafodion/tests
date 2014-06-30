/**************************************************************
** common.c
**
** This file contains all the common functions used by the 
** functions which do ODBC 2.0 testing.
**************************************************************/
#include <stdlib.h>    
#include <stdio.h> 
#include <string.h>
#include <windows.h>
#include <sqlext.h>
#include <assert.h>
#include <time.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#ifdef unixcli
#define NSK_PLATFORM
#define far
#endif

/****************************************************************
** Global data
****************************************************************/
BOOL g_Trace=FALSE;
TEST_GLOBALS;
/* new stuff */
CRITICAL_SECTION error_process_mutex;
int critical_count;
BOOL g_MPSyntax = FALSE;
/* end new stuff */

TCHAR	column_string[1000];
TCHAR	ColumnDefinition[100];

TCHAR charset_file[256];
int		myLogID;

BOOL    isCharSet = FALSE;
BOOL    isUCS2 = FALSE;

char	*inputLocale = NULL;

/****************************************************************
** blank_pad()
** pads a string with blanks
****************************************************************/
void blank_pad( TCHAR *s, int len )
{
	int i;
	for ( i=_tcslen(s); i<(len-1); i++)
		s[i] = ' ';
	s[len-1] = '\0';
}


//************************************************************
// BufferToHex()
// This function will format a buffer to be displayed as a hex
// string.
//************************************************************
VOID BufferToHex( TCHAR *In
                , TCHAR *Out
                , int Length )
{
	int i;
	//static TCHAR  *HexChars=_T("0123456789ABCDEF");
	static TCHAR *HexChars = _T("0123456789ABCDEF");
	
	if(Length <= 0 ){
		*Out='\0';
		return;
		}
	
	// convert the input bytes to hex
	for( i = 0; i < Length; i++ ){
		*Out++ = HexChars[(*In) >> 4];
		*Out++ = HexChars[(*In++) & 0X0F];
		}
	
	*Out = '\0';
	return;
	}  // end of BufferToHex


//************************************************************
// FormatHexOutput()
// This function will format a buffer to be displayed as a hex
// string followed by its ascii representation, if possible.
//************************************************************
VOID FormatHexOutput( TCHAR *In
                    , TCHAR *Out
                    , int Length )
{
	int i;
	TCHAR far *InBase = In;
	//static TCHAR  *HexChars=_T("0123456789ABCDEF");
	static TCHAR *HexChars = {_T("0123456789ABCDEF")};
	
	if(Length <= 0 ){
		*Out='\0';
		return;
		}
	
	// format offset to 4 hex digits
	//*Out++ = HexChars[Offset >> 12];
	//*Out++ = HexChars[(Offset & 0X0FFF) >>  8];
	//*Out++ = HexChars[(Offset & 0X00FF) >>  4];
	//*Out++ = HexChars[ Offset & 0X000F];
	//*Out++ = ' ';
	//*Out++ = ' ';
	
	// convert the input bytes to hex
	for( i = 0; i < Length; i++ ){
		*Out++ = HexChars[(*In) >> 4];
		*Out++ = HexChars[(*In++) & 0X0F];
		*Out++ = ' ';
		}
	
	*Out++ = ' ';
	
	// Align the ascii to 16 data bytes
	//for( i = 0; i < (16-Length); i++ ){
		//*Out++ = ' ';
		//*Out++ = ' ';
		//*Out++ = ' ';
		//}
	
	// output the original data
	In = InBase;
	for( i = 0; i < Length; i++ ){
		if( isprint( *In ) )
			*Out++ = *In++;
		else{
			*Out++ = '.';
			++In;
			}
		}
	//*Out++ = '\n';
	*Out = '\0';
	
	return;
	
	}  // end of FormatHexOutput


/****************************************************************
** ReturncodeToChar()
**
** This function will attempt to convert a returncode from an
** ODBC function call into a more user friendly character string.
** If the returncode isn't one of the standard errors then this
** function converts the returncode into a numeric string.
****************************************************************/
TCHAR *ReturncodeToChar(RETCODE retcode, TCHAR *buf)
{
   switch (retcode) {
      case SQL_SUCCESS:
         _tcscpy (buf, _T("SQL_SUCCESS"));
         break;
      case SQL_ERROR:
         _tcscpy (buf, _T("SQL_ERROR"));
         break;
      case SQL_SUCCESS_WITH_INFO:
         _tcscpy (buf, _T("SQL_SUCCESS_WITH_INFO"));
         break;
      case SQL_NO_DATA_FOUND:
         _tcscpy (buf, _T("SQL_NO_DATA_FOUND"));
         break;
      case SQL_NEED_DATA:
         _tcscpy (buf, _T("SQL_NEED_DATA"));
         break;
      case SQL_INVALID_HANDLE:
         _tcscpy (buf, _T("SQL_INVALID_HANDLE"));
         break;
      case SQL_STILL_EXECUTING:
         _tcscpy (buf, _T("SQL_STILL_EXECUTING"));
         break;
      default:
         _itot(retcode,buf,10);
	}
	return buf;
}

/****************************************************************
** SQLTypeToChar()
**
** This function will attempt to convert a SQLType value from an
** ODBC function call into a more user friendly character string.
** If the SQLType isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *SQLTypeToChar(SWORD SQLType, TCHAR *buf)
{
   switch (SQLType) {
		case SQL_CHAR:		_tcscpy (buf,_T("SQL_CHAR"));break;
		case SQL_WCHAR:		_tcscpy (buf,_T("SQL_WCHAR"));break;
		case SQL_NUMERIC:	_tcscpy (buf,_T("SQL_NUMERIC"));break;
		case SQL_DECIMAL:	_tcscpy (buf,_T("SQL_DECIMAL"));break;
		case SQL_INTEGER:	_tcscpy (buf,_T("SQL_INTEGER"));break;
		case SQL_SMALLINT:	_tcscpy (buf,_T("SQL_SMALLINT"));break;
		case SQL_FLOAT:		_tcscpy (buf,_T("SQL_FLOAT"));break;
		case SQL_REAL:		_tcscpy (buf,_T("SQL_REAL"));break;
		case SQL_DOUBLE:	_tcscpy (buf,_T("SQL_DOUBLE"));break;
		case SQL_VARCHAR:	_tcscpy (buf,_T("SQL_VARCHAR"));break;
		case SQL_WVARCHAR:	_tcscpy (buf,_T("SQL_WVARCHAR"));break;
		case SQL_DATE:		_tcscpy (buf,_T("SQL_DATE"));break;
		case SQL_TYPE_DATE:	_tcscpy (buf,_T("SQL_DATE"));break;
		case SQL_TIME:		_tcscpy (buf,_T("SQL_TIME"));break;
		case SQL_TYPE_TIME:	_tcscpy (buf,_T("SQL_TIME"));break;
		case SQL_BINARY:	_tcscpy (buf,_T("SQL_BINARY"));break;
		case SQL_BIGINT:	_tcscpy (buf,_T("SQL_BIGINT"));break;
		case SQL_TINYINT:	_tcscpy (buf,_T("SQL_TINYINT"));break;
		case SQL_BIT:		_tcscpy (buf,_T("SQL_BIT"));break;
		case SQL_TIMESTAMP:		_tcscpy (buf,_T("SQL_TIMESTAMP"));break;
		case SQL_TYPE_TIMESTAMP: _tcscpy (buf,_T("SQL_TIMESTAMP"));break;
		case SQL_LONGVARCHAR:	_tcscpy (buf,_T("SQL_LONGVARCHAR"));break;
		case SQL_WLONGVARCHAR:	_tcscpy (buf,_T("SQL_WLONGVARCHAR"));break;
		case SQL_VARBINARY:		_tcscpy (buf,_T("SQL_VARBINARY"));break;
		case SQL_LONGVARBINARY:	_tcscpy (buf,_T("SQL_LONGVARBINARY"));break;
		case SQL_INTERVAL_YEAR:	_tcscpy (buf,_T("SQL_INTERVAL_YEAR"));break;
		case SQL_INTERVAL_MONTH:	_tcscpy (buf,_T("SQL_INTERVAL_MONTH"));break;
		case SQL_INTERVAL_YEAR_TO_MONTH:	_tcscpy (buf,_T("SQL_INTERVAL_YEAR_TO_MONTH"));break;
		case SQL_INTERVAL_DAY:		_tcscpy (buf,_T("SQL_INTERVAL_DAY"));break;
		case SQL_INTERVAL_HOUR:		_tcscpy (buf,_T("SQL_INTERVAL_HOUR"));break;
		case SQL_INTERVAL_MINUTE:	_tcscpy (buf,_T("SQL_INTERVAL_MINUTE"));break;
		case SQL_INTERVAL_SECOND:	_tcscpy (buf,_T("SQL_INTERVAL_SECOND"));break;
		case SQL_INTERVAL_DAY_TO_HOUR:	_tcscpy (buf,_T("SQL_INTERVAL_DAY_TO_HOUR"));break;
		case SQL_INTERVAL_DAY_TO_MINUTE:	_tcscpy (buf,_T("SQL_INTERVAL_DAY_TO_MINUTE"));break;
		case SQL_INTERVAL_DAY_TO_SECOND:	_tcscpy (buf,_T("SQL_INTERVAL_DAY_TO_SECOND"));break;
		case SQL_INTERVAL_HOUR_TO_MINUTE:	_tcscpy (buf,_T("SQL_INTERVAL_HOUR_TO_MINUTE"));break;
		case SQL_INTERVAL_HOUR_TO_SECOND:	_tcscpy (buf,_T("SQL_INTERVAL_HOUR_TO_SECOND"));break;
		case SQL_INTERVAL_MINUTE_TO_SECOND:	_tcscpy (buf,_T("SQL_INTERVAL_MINUTE_TO_SECOND"));break;
      default:
         _itot(SQLType,buf,10);
	}
	return buf;
}

/****************************************************************
** SQLTypeToChar()
**
** This function will attempt to convert a character string SQLType
** value from an ODBC function call into SQLType.
** If the SQLType isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
SWORD	CharToSQLType(TCHAR *buffer)
{
	SWORD	SQLType = 999;
	
	if (_tcsicmp(buffer,_T("SQL_WCHAR")) == 0)
	{
		SQLType = SQL_WCHAR;
	}
	else if (_tcsicmp(buffer,_T("SQL_NUMERIC")) == 0)
	{
		SQLType = SQL_NUMERIC;
	}
	else if (_tcsicmp(buffer,_T("SQL_DECIMAL")) == 0)
	{
		SQLType = SQL_DECIMAL;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTEGER")) == 0)
	{
		SQLType = SQL_INTEGER;
	}
	else if (_tcsicmp(buffer,_T("SQL_SMALLINT")) == 0)
	{
		SQLType = SQL_SMALLINT;
	}
	else if (_tcsicmp(buffer,_T("SQL_FLOAT")) == 0)
	{
		SQLType = SQL_FLOAT;
	}
	else if (_tcsicmp(buffer,_T("SQL_REAL")) == 0)
	{
		SQLType = SQL_REAL;
	}
	else if (_tcsicmp(buffer,_T("SQL_DOUBLE")) == 0)
	{
		SQLType = SQL_DOUBLE;
	}
	else if (_tcsicmp(buffer,_T("SQL_WVARCHAR")) == 0)
	{
		SQLType = SQL_WVARCHAR;
	}
	else if (_tcsicmp(buffer,_T("SQL_DATE")) == 0)
	{
		SQLType = SQL_DATE;
	}
	else if (_tcsicmp(buffer,_T("SQL_TIME")) == 0)
	{
		SQLType = SQL_TIME;
	}
	else if (_tcsicmp(buffer,_T("SQL_BINARY")) == 0)
	{
		SQLType = SQL_BINARY;
	}
	else if (_tcsicmp(buffer,_T("SQL_BIGINT")) == 0)
	{
		SQLType = SQL_BIGINT;
	}
	else if (_tcsicmp(buffer,_T("SQL_TINYINT")) == 0)
	{
		SQLType = SQL_TINYINT;
	}
	else if (_tcsicmp(buffer,_T("SQL_BIT")) == 0)
	{
		SQLType = SQL_BIT;
	}
	else if (_tcsicmp(buffer,_T("SQL_TIMESTAMP")) == 0)
	{
		SQLType = SQL_TIMESTAMP;
	}
	else if (_tcsicmp(buffer,_T("SQL_WLONGVARCHAR")) == 0)
	{
		SQLType = SQL_WLONGVARCHAR;
	}
	else if (_tcsicmp(buffer,_T("SQL_VARBINARY")) == 0)
	{
		SQLType = SQL_VARBINARY;
	}
	else if (_tcsicmp(buffer,_T("SQL_LONGVARBINARY")) == 0)
	{
		SQLType = SQL_LONGVARBINARY;
	}
		else if (_tcsicmp(buffer,_T("SQL_INTERVAL_YEAR")) == 0)
	{
		SQLType = SQL_INTERVAL_YEAR;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_MONTH")) == 0)
	{
		SQLType = SQL_INTERVAL_MONTH;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_DAY")) == 0)
	{
		SQLType = SQL_INTERVAL_DAY;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_HOUR")) == 0)
	{
		SQLType = SQL_INTERVAL_HOUR;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_MINUTE")) == 0)
	{
		SQLType = SQL_INTERVAL_MINUTE;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_SECOND")) == 0)
	{
		SQLType = SQL_INTERVAL_SECOND;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_YEAR_TO_MONTH")) == 0)
	{
		SQLType = SQL_INTERVAL_YEAR_TO_MONTH;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_DAY_TO_HOUR")) == 0)
	{
		SQLType = SQL_INTERVAL_DAY_TO_HOUR;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_DAY_TO_MINUTE")) == 0)
	{
		SQLType = SQL_INTERVAL_DAY_TO_MINUTE;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_DAY_TO_SECOND")) == 0)
	{
		SQLType = SQL_INTERVAL_DAY_TO_SECOND;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_HOUR_TO_MINUTE")) == 0)
	{
		SQLType = SQL_INTERVAL_HOUR_TO_MINUTE;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_HOUR_TO_SECOND")) == 0)
	{
		SQLType = SQL_INTERVAL_HOUR_TO_SECOND;
	}
	else if (_tcsicmp(buffer,_T("SQL_INTERVAL_MINUTE_TO_SECOND")) == 0)
	{
		SQLType = SQL_INTERVAL_MINUTE_TO_SECOND;
	}
	
	return SQLType;
}

/****************************************************************
** SQLNullToChar()
**
** This function will attempt to convert a null state value from an
** ODBC function call into a more user friendly character string.
** If the null state isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *SQLNullToChar(SWORD NullState, TCHAR *buf)
{
   switch (NullState) {
		case SQL_NO_NULLS:			_tcscpy (buf,_T("SQL_NO_NULLS"));break;
		case SQL_NULLABLE:			_tcscpy (buf,_T("SQL_NULLABLE"));break;
		case SQL_NULLABLE_UNKNOWN:	_tcscpy (buf,_T("SQL_NULLABLE_UNKNOWN"));break;
      default:
         _itot(NullState,buf,10);
	}
	return buf;
}

/****************************************************************
** CatalogLocationToString()
**
** This function will attempt to convert a catalog location value
** into a more user friendly character string.
** If the catalog location value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *CatalogLocationToString(SWORD CatLoc, TCHAR *buf)
{
   switch (CatLoc) {
		case SQL_CL_START:			_tcscpy (buf,_T("SQL_CL_START"));break;
		case SQL_CL_END:				_tcscpy (buf,_T("SQL_CL_END"));break;
      default:
         _itot(CatLoc,buf,10);
	}
	return buf;
}

/****************************************************************
** SQLDescToChar()
**
** This function will attempt to convert a column description value from an
** ODBC function call into a more user friendly character string.
** If the column description isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *SQLDescToChar(SWORD Desc, TCHAR *buf)
{
   switch (Desc) {
		case SQL_COLUMN_COUNT:_tcscpy (buf,_T("SQL_COLUMN_COUNT"));break;
		case SQL_COLUMN_NAME:_tcscpy (buf,_T("SQL_COLUMN_NAME"));break;
		case SQL_COLUMN_TYPE:_tcscpy (buf,_T("SQL_COLUMN_TYPE"));break;
		case SQL_COLUMN_LENGTH:_tcscpy (buf,_T("SQL_COLUMN_LENGTH"));break;
		case SQL_COLUMN_PRECISION:_tcscpy (buf,_T("SQL_COLUMN_PRECISION"));break;
		case SQL_COLUMN_SCALE:_tcscpy (buf,_T("SQL_COLUMN_SCALE"));break;
		case SQL_COLUMN_DISPLAY_SIZE:_tcscpy (buf,_T("SQL_COLUMN_DISPLAY_SIZE"));break;
		case SQL_COLUMN_NULLABLE:_tcscpy (buf,_T("SQL_COLUMN_NULLABLE"));break;
		case SQL_COLUMN_UNSIGNED:_tcscpy (buf,_T("SQL_COLUMN_UNSIGNED"));break;
		case SQL_COLUMN_MONEY:_tcscpy (buf,_T("SQL_COLUMN_MONEY"));break;
		case SQL_COLUMN_UPDATABLE:_tcscpy (buf,_T("SQL_COLUMN_UPDATABLE"));break;
		case SQL_COLUMN_AUTO_INCREMENT:_tcscpy (buf,_T("SQL_COLUMN_AUTO_INCREMENT"));break;
		case SQL_COLUMN_CASE_SENSITIVE:_tcscpy (buf,_T("SQL_COLUMN_CASE_SENSITIVE"));break;
		case SQL_COLUMN_SEARCHABLE:_tcscpy (buf,_T("SQL_COLUMN_SEARCHABLE"));break;
		case SQL_COLUMN_TYPE_NAME:_tcscpy (buf,_T("SQL_COLUMN_TYPE_NAME"));break;
		case SQL_COLUMN_TABLE_NAME:_tcscpy (buf,_T("SQL_COLUMN_TABLE_NAME"));break;
		case SQL_COLUMN_OWNER_NAME:_tcscpy (buf,_T("SQL_COLUMN_OWNER_NAME"));break;
		case SQL_COLUMN_QUALIFIER_NAME:_tcscpy (buf,_T("SQL_COLUMN_QUALIFIER_NAME"));break;
		case SQL_COLUMN_LABEL:_tcscpy (buf,_T("SQL_COLUMN_LABEL"));break;
      default:
         _itot(Desc,buf,10);
	}
	return buf;
}

//----------------------------------------------------------------------------
/****************************************************************
** SQLDescAttrToChar()
**
** This function will attempt to convert a column description value from an
** ODBC function call into a more user friendly character string.
** If the column description isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *SQLDescAttrToChar(SWORD Desc, TCHAR *buf)
{
   switch (Desc) {
		case SQL_DESC_AUTO_UNIQUE_VALUE:_tcscpy (buf,_T("SQL_DESC_AUTO_UNIQUE_VALUE"));break;
		case SQL_DESC_CASE_SENSITIVE:_tcscpy (buf,_T("SQL_DESC_CASE_SENSITIVE"));break;
		case SQL_DESC_COUNT:_tcscpy (buf,_T("SQL_DESC_COUNT"));break;
		case SQL_DESC_DISPLAY_SIZE:_tcscpy (buf,_T("SQL_DESC_DISPLAY_SIZE"));break;
		case SQL_DESC_LENGTH:_tcscpy (buf,_T("SQL_DESC_LENGTH"));break;
		case SQL_DESC_FIXED_PREC_SCALE:_tcscpy (buf,_T("SQL_DESC_FIXED_PREC_SCALE"));break;
		case SQL_DESC_NULLABLE:_tcscpy (buf,_T("SQL_DESC_NULLABLE"));break;
		case SQL_DESC_PRECISION:_tcscpy (buf,_T("SQL_DESC_PRECISION"));break;
		case SQL_DESC_SCALE:_tcscpy (buf,_T("SQL_DESC_SCALE"));break;
		case SQL_DESC_SEARCHABLE:_tcscpy (buf,_T("SQL_DESC_SEARCHABLE"));break;
		case SQL_DESC_TYPE:_tcscpy (buf,_T("SQL_DESC_TYPE"));break;
		case SQL_DESC_CONCISE_TYPE:_tcscpy (buf,_T("SQL_DESC_CONCISE_TYPE"));break;
		case SQL_DESC_UNSIGNED:_tcscpy (buf,_T("SQL_DESC_UNSIGNED"));break;
		case SQL_DESC_UPDATABLE:_tcscpy (buf,_T("SQL_DESC_UPDATABLE"));break;
		case SQL_DESC_NAME:_tcscpy (buf,_T("SQL_DESC_NAME"));break;
		case SQL_DESC_TYPE_NAME:_tcscpy (buf,_T("SQL_DESC_TYPE_NAME"));break;
		case SQL_DESC_SCHEMA_NAME:_tcscpy (buf,_T("SQL_DESC_SCHEMA_NAME"));break;
		case SQL_DESC_CATALOG_NAME:_tcscpy (buf,_T("SQL_DESC_CATALOG_NAME"));break;
		case SQL_DESC_TABLE_NAME:_tcscpy (buf,_T("SQL_DESC_TABLE_NAME"));break;
		case SQL_DESC_LABEL:_tcscpy (buf,_T("SQL_DESC_LABEL"));break;
      default:
         _itot(Desc,buf,10);
	}
	return buf;
}

//----------------------------------------------------------------------------
TCHAR * StatementOptionToChar( long Option, TCHAR *buf )
{
	switch (Option) 
	{
		case SQL_QUERY_TIMEOUT:		_stprintf(buf,_T("SQL_QUERY_TIMEOUT(%ld)"),Option);break;
		case SQL_MAX_ROWS:			_stprintf(buf,_T("SQL_MAX_ROWS(%ld)"),Option);break;
		case SQL_NOSCAN:			_stprintf(buf,_T("SQL_NOSCAN(%ld)"),Option);break;
		case SQL_MAX_LENGTH:		_stprintf(buf,_T("SQL_MAX_LENGTH(%ld)"),Option);break;
		case SQL_ASYNC_ENABLE:		_stprintf(buf,_T("SQL_ASYNC_ENABLE(%ld)"),Option);break;
		case SQL_BIND_TYPE:			_stprintf(buf,_T("SQL_BIND_TYPE(%ld)"),Option);break;
		case SQL_CURSOR_TYPE:		_stprintf(buf,_T("SQL_CURSOR_TYPE(%ld)"),Option);break;
		case SQL_CONCURRENCY:		_stprintf(buf,_T("SQL_CONCURRENCY(%ld)"),Option);break;
		case SQL_KEYSET_SIZE:		_stprintf(buf,_T("SQL_KEYSET_SIZE(%ld)"),Option);break;
		case SQL_ROWSET_SIZE:		_stprintf(buf,_T("SQL_ROWSET_SIZE(%ld)"),Option);break;
		case SQL_SIMULATE_CURSOR:	_stprintf(buf,_T("SQL_SIMULATE_CURSOR(%ld)"),Option);break;
		case SQL_RETRIEVE_DATA:		_stprintf(buf,_T("SQL_RETRIEVE_DATA(%ld)"),Option);break;
		case SQL_USE_BOOKMARKS:		_stprintf(buf,_T("SQL_USE_BOOKMARKS(%ld)"),Option);break;
		case SQL_GET_BOOKMARK:		_stprintf(buf,_T("SQL_GET_BOOKMARK(%ld)"),Option);break;
		case SQL_ROW_NUMBER:		_stprintf(buf,_T("SQL_ROW_NUMBER(%ld)"),Option);break;
		case SQL_ATTR_CURSOR_SCROLLABLE:	_stprintf(buf,_T("SQL_CURSOR_SCROLLABLE(%ld)"),Option);break;
		case SQL_ATTR_CURSOR_SENSITIVITY:	_stprintf(buf,_T("SQL_CURSOR_SENSITIVITY(%ld)"),Option);break;
		case SQL_ATTR_ENABLE_AUTO_IPD:	_stprintf(buf,_T("SQL_ROW_ARRAY_SIZE(%ld)"),Option);break;
		case SQL_ATTR_ROW_ARRAY_SIZE:	_stprintf(buf,_T("SQL_ENABLE_AUTO_IPD(%ld)"),Option);break;
		case SQL_ATTR_METADATA_ID:		_stprintf(buf,_T("SQL_METADATA_ID(%ld)"),Option);break;
		default:
            _stprintf(buf,_T("%ld"),Option);
			break;
	}
	return buf;
}

//****************************************************************************
TCHAR *StatementParamToChar( long Option, long Param, TCHAR *buf )
{
	switch (Option) 
	{
		case SQL_QUERY_TIMEOUT:		
			_stprintf(buf,_T("%ld seconds"),Param);
			break;

		case SQL_NOSCAN:
			switch (Param)
			{
			case SQL_NOSCAN_OFF:		_stprintf(buf,_T("SQL_NOSCAN_OFF(%ld)"),Param);break;
			case SQL_NOSCAN_ON:			_stprintf(buf,_T("SQL_NOSCAN_ON(%ld)"),Param);break;
			}
			break;

		case SQL_ASYNC_ENABLE:
			switch (Param)
			{
			case SQL_ASYNC_ENABLE_OFF:		_stprintf(buf,_T("SQL_ASYNC_ENABLE_OFF(%ld)"),Param);break;
			case SQL_ASYNC_ENABLE_ON:		_stprintf(buf,_T("SQL_ASYNC_ENABLE_ON(%ld)"),Param);break;
			}
			break;

		case SQL_BIND_TYPE:
			if( Param == SQL_BIND_BY_COLUMN) _stprintf(buf,_T("SQL_BIND_BY_COLUMN(%ld)"),Param);
			break;

		case SQL_CURSOR_TYPE:
			switch (Param)
			{
			case SQL_CURSOR_FORWARD_ONLY:	_stprintf(buf,_T("SQL_CURSOR_FORWARD_ONLY(%ld)"),Param);break;
			case SQL_CURSOR_KEYSET_DRIVEN:	_stprintf(buf,_T("SQL_CURSOR_KEYSET_DRIVEN(%ld)"),Param);break;
			case SQL_CURSOR_DYNAMIC:		_stprintf(buf,_T("SQL_CURSOR_DYNAMIC(%ld)"),Param);break;
			case SQL_CURSOR_STATIC:			_stprintf(buf,_T("SQL_CURSOR_STATIC(%ld)"),Param);break;
			}
			break;

		case SQL_CONCURRENCY:
			switch (Param)
			{
			case SQL_CONCUR_READ_ONLY:		_stprintf(buf,_T("SQL_CONCUR_READ_ONLY(%ld)"),Param);break;
			case SQL_CONCUR_LOCK:			_stprintf(buf,_T("SQL_CONCUR_LOCK(%ld)"),Param);break;
			case SQL_CONCUR_ROWVER:			_stprintf(buf,_T("SQL_CONCUR_ROWVER(%ld)"),Param);break;
			case SQL_CONCUR_VALUES:			_stprintf(buf,_T("SQL_CONCUR_VALUES(%ld)"),Param);break;
			}
			break;

		case SQL_SIMULATE_CURSOR:
			switch (Param)
			{
			case SQL_SC_NON_UNIQUE:			_stprintf(buf,_T("SQL_SC_NON_UNIQUE(%ld)"),Param);break;
			case SQL_SC_TRY_UNIQUE:			_stprintf(buf,_T("SQL_SC_TRY_UNIQUE(%ld)"),Param);break;
			case SQL_SC_UNIQUE:				_stprintf(buf,_T("SQL_SC_UNIQUE(%ld)"),Param);break;
			}
			break;

		case SQL_RETRIEVE_DATA:
			switch (Param)
			{
			case SQL_RD_OFF:				_stprintf(buf,_T("SQL_RD_OFF(%ld)"),Param);break;
			case SQL_RD_ON:					_stprintf(buf,_T("SQL_RD_ON(%ld)"),Param);break;
			}
			break;

		case SQL_USE_BOOKMARKS:
			switch (Param)
			{
			case SQL_UB_OFF:				_stprintf(buf,_T("SQL_UB_OFF(%ld)"),Param);break;
			case SQL_UB_ON:					_stprintf(buf,_T("SQL_UB_ON(%ld)"),Param);break;
			}
			break;

		case SQL_ATTR_CURSOR_SENSITIVITY:
			switch (Param)
			{
			case SQL_INSENSITIVE:			_stprintf(buf,_T("SQL_INSENSITIVE(%ld)"),Param);break;
			case SQL_SENSITIVE:				_stprintf(buf,_T("SQL_SENSITIVE(%ld)"),Param);break;
			case SQL_UNSPECIFIED:			_stprintf(buf,_T("SQL_UNSPECIFIED(%ld)"),Param);break;
			}
			break;

		case SQL_ATTR_ENABLE_AUTO_IPD:
		case SQL_ATTR_METADATA_ID:
			switch (Param)
			{
			case SQL_FALSE:					_stprintf(buf,_T("SQL_FALSE(%ld)"),Param);break;
			case SQL_TRUE:					_stprintf(buf,_T("SQL_TRUE(%ld)"),Param);break;
			}
			break;

		case SQL_GET_BOOKMARK:
		case SQL_ROW_NUMBER:
		case SQL_MAX_ROWS:
		case SQL_MAX_LENGTH:
		case SQL_KEYSET_SIZE:
		case SQL_ROWSET_SIZE:
			_stprintf(buf,_T("%ld"),Param);
			break;

		default:
			_stprintf(buf,_T("%ld"),Param);
            break;
	}
	return buf;
}

//----------------------------------------------------------------------------
TCHAR * ConnectionOptionToChar( long Option, TCHAR *buf )
{
	switch (Option) 
	{
		case SQL_ACCESS_MODE:				_stprintf(buf,_T("SQL_ACCESS_MODE(%ld)"),Option);break;
		case SQL_AUTOCOMMIT:				_stprintf(buf,_T("SQL_AUTOCOMMIT(%ld)"),Option);break;
		case SQL_LOGIN_TIMEOUT:				_stprintf(buf,_T("SQL_LOGIN_TIMEOUT(%ld)"),Option);break;
		case SQL_OPT_TRACE:					_stprintf(buf,_T("SQL_OPT_TRACE(%ld)"),Option);break;
		case SQL_TRANSLATE_OPTION:			_stprintf(buf,_T("SQL_TRANSLATE_OPTION(%ld)"),Option);break;
		case SQL_TXN_ISOLATION:				_stprintf(buf,_T("SQL_TXN_ISOLATION(%ld)"),Option);break;
		case SQL_ODBC_CURSORS:				_stprintf(buf,_T("SQL_ODBC_CURSORS(%ld)"),Option);break;
		case SQL_PACKET_SIZE:				_stprintf(buf,_T("SQL_PACKET_SIZE(%ld)"),Option);break;

		case SQL_ATTR_ODBC_VERSION:			_stprintf(buf,_T("SQL_ATTR_ODBC_VERSION(%ld)"),Option);break;
		case SQL_ATTR_CONNECTION_POOLING:	_stprintf(buf,_T("SQL_ATTR_CONNECTION_POOLING(%ld)"),Option);break;
		case SQL_ATTR_CP_MATCH:				_stprintf(buf,_T("SQL_ATTR_CP_MATCH(%ld)"),Option);break;
		case SQL_ATTR_OUTPUT_NTS:			_stprintf(buf,_T("SQL_ATTR_OUTPUT_NTS(%ld)"),Option);break;
		default:
            _stprintf(buf,_T("Unknown SQL option: %ld"), Option);
			//_ltot(Option,buf,10);
	}
	return buf;
}

//****************************************************************************
TCHAR *ConnectionParamToChar( long Option, long Param, TCHAR *buf )
{
	switch (Option) 
	{
		case SQL_ACCESS_MODE:			
			switch (Param)
			{
				case SQL_MODE_READ_WRITE:	_stprintf(buf,_T("SQL_MODE_READ_WRITE%ld seconds"),Param);break;
				case SQL_MODE_READ_ONLY:	_stprintf(buf,_T("SQL_MODE_READ_ONLY%ld seconds"),Param);break;
			}
			break;

		case SQL_AUTOCOMMIT:
			switch (Param)
			{
				case SQL_AUTOCOMMIT_OFF:			_stprintf(buf,_T("SQL_AUTOCOMMIT_OFF(%ld)"),Param);break;
				case SQL_AUTOCOMMIT_ON:				_stprintf(buf,_T("SQL_AUTOCOMMIT_ON(%ld)"),Param);break;
			}
			break;

		case SQL_LOGIN_TIMEOUT:
			_stprintf(buf,_T("%ld seconds"),Param);
			break;

		case SQL_OPT_TRACE:
			switch (Param)
			{
				case SQL_OPT_TRACE_OFF:				_stprintf(buf,_T("SQL_OPT_TRACE_OFF(%ld)"),Param);break;
				case SQL_OPT_TRACE_ON:				_stprintf(buf,_T("SQL_OPT_TRACE_ON(%ld)"),Param);break;
			}
			break;

		case SQL_TRANSLATE_OPTION:
			_stprintf(buf,_T("%ld seconds"),Param);
			break;

		case SQL_TXN_ISOLATION:
			switch (Param)
			{
				case SQL_TXN_READ_UNCOMMITTED:	_stprintf(buf,_T("SQL_TXN_READ_UNCOMMITTED(%ld)"),Param);break;
				case SQL_TXN_READ_COMMITTED:		_stprintf(buf,_T("SQL_TXN_READ_COMMITTED(%ld)"),Param);break;
				case SQL_TXN_REPEATABLE_READ:		_stprintf(buf,_T("SQL_TXN_REPEATABLE_READ(%ld)"),Param);break;
				case SQL_TXN_SERIALIZABLE:			_stprintf(buf,_T("SQL_TXN_SERIALIZABLE(%ld)"),Param);break;
			}
			break;

		case SQL_ODBC_CURSORS:
			switch (Param)
			{
			case SQL_CUR_USE_IF_NEEDED:			_stprintf(buf,_T("SQL_CUR_USE_IF_NEEDED(%ld)"),Param);break;
			case SQL_CUR_USE_ODBC:					_stprintf(buf,_T("SQL_CUR_USE_ODBC(%ld)"),Param);break;
			case SQL_CUR_USE_DRIVER:				_stprintf(buf,_T("SQL_CUR_USE_DRIVER(%ld)"),Param);break;
			}
			break;

		case SQL_PACKET_SIZE:
			_stprintf(buf,_T("%ld seconds"),Param);
			break;

		case SQL_GET_BOOKMARK:
            _stprintf(buf,_T("SQL_GET_BOOKMARK(%ld)"),Param);break;
		case SQL_ROW_NUMBER:
            _stprintf(buf,_T("SQL_ROW_NUMBER(%ld)"),Param);break;
		case SQL_MAX_ROWS:
            _stprintf(buf,_T("SQL_MAX_ROWS(%ld)"),Param);break;
		case SQL_MAX_LENGTH:
            _stprintf(buf,_T("SQL_MAX_LENGTH(%ld)"),Param);break;
		case SQL_KEYSET_SIZE:
            _stprintf(buf,_T("SQL_KEYSET_SIZE(%ld)"),Param);break;
		case SQL_ROWSET_SIZE:
            _stprintf(buf,_T("SQL_ROWSET_SIZE(%ld)"),Param);break;
			//_ltot(Param,buf,10);

		default:
            _stprintf(buf,_T("Unknown SQL Parameter(%ld)"),Param);break;
			//_ltot(Param,buf,10);
	}
	return buf;
}

/****************************************************************
** SQLCTypeToChar()
**
** This function will attempt to convert a SQLType value from an
** ODBC function call into a more user friendly character string.
** If the CType isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *SQLCTypeToChar(SWORD CType, TCHAR *buf)
{
   switch (CType) {
      case SQL_C_CHAR:			_stprintf (buf,_T("SQL_C_CHAR(%d)"),CType);break;
      case SQL_C_WCHAR:			_stprintf (buf,_T("SQL_C_WCHAR(%d)"),CType);break;
	  case SQL_C_LONG:			_stprintf (buf,_T("SQL_C_LONG(%d)"),CType);break;
      case SQL_C_SHORT:			_stprintf (buf,_T("SQL_C_SHORT(%d)"),CType);break;
      case SQL_C_FLOAT:			_stprintf (buf,_T("SQL_C_FLOAT(%d)"),CType);break;
      case SQL_C_DOUBLE:		_stprintf (buf,_T("SQL_C_DOUBLE(%d)"),CType);break;
      case SQL_C_NUMERIC:		_stprintf (buf,_T("SQL_C_NUMERIC(%d)"),CType);break;
      case SQL_C_DEFAULT:		_stprintf (buf,_T("SQL_C_DEFAULT(%d)"),CType);break;
      case SQL_C_DATE:			_stprintf (buf,_T("SQL_C_DATE(%d)"),CType);break;
      case SQL_C_TIME:			_stprintf (buf,_T("SQL_C_TIME(%d)"),CType);break;
      case SQL_C_TIMESTAMP:			_stprintf (buf,_T("SQL_C_TIMESTAMP(%d)"),CType);break;
      case SQL_C_TYPE_DATE:			_stprintf (buf,_T("SQL_C_TYPE_DATE(%d)"),CType);break;
      case SQL_C_TYPE_TIME:			_stprintf (buf,_T("SQL_C_TYPE_TIME(%d)"),CType);break;
      case SQL_C_TYPE_TIMESTAMP:		_stprintf (buf,_T("SQL_C_TYPE_TIMESTAMP(%d)"),CType);break;
      case SQL_C_INTERVAL_YEAR:		_stprintf (buf,_T("SQL_C_INTERVAL_YEAR(%d)"),CType);break;
      case SQL_C_INTERVAL_MONTH:		_stprintf (buf,_T("SQL_C_INTERVAL_MONTH(%d)"),CType);break;
      case SQL_C_INTERVAL_DAY:		_stprintf (buf,_T("SQL_C_INTERVAL_DAY(%d)"),CType);break;
      case SQL_C_INTERVAL_HOUR:		_stprintf (buf,_T("SQL_C_INTERVAL_HOUR(%d)"),CType);break;
      case SQL_C_INTERVAL_MINUTE:	_stprintf (buf,_T("SQL_C_INTERVAL_MINUTE(%d)"),CType);break;
      case SQL_C_INTERVAL_SECOND:	_stprintf (buf,_T("SQL_C_INTERVAL_SECOND(%d)"),CType);break;
      case SQL_C_INTERVAL_YEAR_TO_MONTH:		_stprintf (buf,_T("SQL_C_INTERVAL_YEAR_TO_MONTH(%d)"),CType);break;
      case SQL_C_INTERVAL_DAY_TO_HOUR:			_stprintf (buf,_T("SQL_C_INTERVAL_DAY_TO_HOUR(%d)"),CType);break;
      case SQL_C_INTERVAL_DAY_TO_MINUTE:		_stprintf (buf,_T("SQL_C_INTERVAL_DAY_TO_MINUTE(%d)"),CType);break;
      case SQL_C_INTERVAL_DAY_TO_SECOND:		_stprintf (buf,_T("SQL_C_INTERVAL_DAY_TO_SECOND(%d)"),CType);break;
      case SQL_C_INTERVAL_HOUR_TO_MINUTE:		_stprintf (buf,_T("SQL_C_INTERVAL_HOUR_TO_MINUTE(%d)"),CType);break;
      case SQL_C_INTERVAL_HOUR_TO_SECOND:		_stprintf (buf,_T("SQL_C_INTERVAL_HOUR_TO_SECOND(%d)"),CType);break;
      case SQL_C_INTERVAL_MINUTE_TO_SECOND:	_stprintf (buf,_T("SQL_C_INTERVAL_MINUTE_TO_SECOND(%d)"),CType);break;
      case SQL_C_BINARY:		_stprintf (buf,_T("SQL_C_BINARY(%d)"),CType);break;
      case SQL_C_BIT:			_stprintf (buf,_T("SQL_C_BIT(%d)"),CType);break;
      case SQL_C_SBIGINT:		_stprintf (buf,_T("SQL_C_SBIGINT(%d)"),CType);break;
      case SQL_C_UBIGINT:		_stprintf (buf,_T("SQL_C_UBIGINT(%d)"),CType);break;
      case SQL_C_TINYINT:		_stprintf (buf,_T("SQL_C_TINYINT(%d)"),CType);break;
      case SQL_C_SLONG:			_stprintf (buf,_T("SQL_C_SLONG(%d)"),CType);break;
      case SQL_C_SSHORT:		_stprintf (buf,_T("SQL_C_SSHORT(%d)"),CType);break;
      case SQL_C_STINYINT:		_stprintf (buf,_T("SQL_C_STINYINT(%d)"),CType);break;
      case SQL_C_ULONG:			_stprintf (buf,_T("SQL_C_ULONG(%d)"),CType);break;
      case SQL_C_USHORT:		_stprintf (buf,_T("SQL_C_USHORT(%d)"),CType);break;
      case SQL_C_UTINYINT:		_stprintf (buf,_T("SQL_C_UTINYINT(%d)"),CType);break;
      default:
         _itot(CType,buf,10);
	}
	return buf;
}


/****************************************************************
** CharToSQLCType()
**
** This function will attempt to convert a SQLType value from an
** ODBC function call into a more user friendly character string.
** If the CType isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
SWORD	CharToSQLCType(TCHAR *buffer)
{
	SWORD	SQLCType = 999;
	
	if (_tcsicmp(buffer,_T("SQL_C_TCHAR")) == 0)
	{
		SQLCType = SQL_C_TCHAR;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_LONG")) == 0)
	{
		SQLCType = SQL_C_LONG;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_SHORT")) == 0)
	{
		SQLCType = SQL_C_SHORT;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_FLOAT")) == 0)
	{
		SQLCType = SQL_C_FLOAT;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_DOUBLE")) == 0)
	{
		SQLCType = SQL_C_DOUBLE;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_NUMERIC")) == 0)
	{
		SQLCType = SQL_C_NUMERIC;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_DEFAULT")) == 0)
	{
		SQLCType = SQL_C_DEFAULT;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_DATE")) == 0)
	{
		SQLCType = SQL_C_DATE;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_TIME")) == 0)
	{
		SQLCType = SQL_C_TIME;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_TIMESTAMP")) == 0)
	{
		SQLCType = SQL_C_TIMESTAMP;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_TYPE_DATE")) == 0)
	{
		SQLCType = SQL_C_TYPE_DATE;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_TYPE_TIME")) == 0)
	{
		SQLCType = SQL_C_TYPE_TIME;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_TYPE_TIMESTAMP")) == 0)
	{
		SQLCType = SQL_C_TYPE_TIMESTAMP;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_YEAR")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_YEAR;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_MONTH")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_MONTH;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_DAY")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_DAY;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_HOUR")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_HOUR;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_MINUTE")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_MINUTE;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_SECOND")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_SECOND;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_YEAR_TO_MONTH")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_YEAR_TO_MONTH;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_DAY_TO_HOUR")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_DAY_TO_HOUR;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_DAY_TO_MINUTE")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_DAY_TO_MINUTE;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_DAY_TO_SECOND")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_DAY_TO_SECOND;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_HOUR_TO_MINUTE")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_HOUR_TO_MINUTE;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_HOUR_TO_SECOND")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_HOUR_TO_SECOND;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_INTERVAL_MINUTE_TO_SECOND")) == 0)
	{
		SQLCType = SQL_C_INTERVAL_MINUTE_TO_SECOND;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_BINARY")) == 0)
	{
		SQLCType = SQL_C_BINARY;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_BIT")) == 0)
	{
		SQLCType = SQL_C_BIT;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_SBIGINT")) == 0)
	{
		SQLCType = SQL_C_SBIGINT;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_UBIGINT")) == 0)
	{
		SQLCType = SQL_C_UBIGINT;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_TINYINT")) == 0)
	{
		SQLCType = SQL_C_TINYINT;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_SLONG")) == 0)
	{
		SQLCType = SQL_C_SLONG;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_SSHORT")) == 0)
	{
		SQLCType = SQL_C_SSHORT;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_STINYINT")) == 0)
	{
		SQLCType = SQL_C_STINYINT;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_ULONG")) == 0)
	{
		SQLCType = SQL_C_LONG;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_USHORT")) == 0)
	{
		SQLCType = SQL_C_USHORT;
	}
	else if (_tcsicmp(buffer,_T("SQL_C_UTINYINT")) == 0)
	{
		SQLCType = SQL_C_UTINYINT;
	}
	return SQLCType;
}


/****************************************************************
** InfoTypeToChar()
**
** This function will attempt to convert a SQLGetInfoType value
** into a more user friendly character string.
** If the SQLGetInfoType isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *InfoTypeToChar( long InfoType, TCHAR *buf )
{
	switch( InfoType )
	{
	case SQL_ACTIVE_CONNECTIONS:		_stprintf(buf,_T("SQL_ACTIVE_CONNECTIONS(%ld)"),InfoType);break;
	case SQL_ACTIVE_STATEMENTS:         _stprintf(buf,_T("SQL_ACTIVE_STATEMENTS(%ld)"),InfoType);break;
	case SQL_ASYNC_MODE:				_stprintf(buf,_T("SQL_ASYNC_MODE(%ld)"),InfoType);break;
	case SQL_CATALOG_NAME:		        _stprintf(buf,_T("SQL_CATALOG_NAME(%ld)"),InfoType);break;
	case SQL_CATALOG_NAME_SEPARATOR:	_stprintf(buf,_T("SQL_CATALOG_NAME_SEPARATOR(%ld)"),InfoType);break;
	case SQL_CATALOG_TERM:				_stprintf(buf,_T("SQL_CATALOG_TERM(%ld)"),InfoType);break;
	case SQL_COLLATION_SEQ:             _stprintf(buf,_T("SQL_COLLATION_SEQ(%ld)"),InfoType);break;
	case SQL_CURSOR_SENSITIVITY:        _stprintf(buf,_T("SQL_CURSOR_SENSITIVITY(%ld)"),InfoType);break;
	case SQL_DATA_SOURCE_NAME:          _stprintf(buf,_T("SQL_DATA_SOURCE_NAME(%ld)"),InfoType);break;
	case SQL_DESCRIBE_PARAMETER:		_stprintf(buf,_T("SQL_DESCRIBE_PARAMETER(%ld)"),InfoType);break;
	case SQL_DM_VER:				    _stprintf(buf,_T("SQL_DM_VER(%ld)"),InfoType);break;
	case SQL_DRIVER_HDBC:				_stprintf(buf,_T("SQL_DRIVER_HDBC(%ld)"),InfoType);break;
	case SQL_DRIVER_HENV:				_stprintf(buf,_T("SQL_DRIVER_HENV(%ld)"),InfoType);break;
	case SQL_DRIVER_HLIB:				_stprintf(buf,_T("SQL_DRIVER_HLIB(%ld)"),InfoType);break;
	case SQL_DRIVER_HSTMT:				_stprintf(buf,_T("SQL_DRIVER_HSTMT(%ld)"),InfoType);break;
	case SQL_DRIVER_NAME:               _stprintf(buf,_T("SQL_DRIVER_NAME(%ld)"),InfoType);break;
	case SQL_DRIVER_VER:                _stprintf(buf,_T("SQL_DRIVER_VER(%ld)"),InfoType);break;
	case SQL_DYNAMIC_CURSOR_ATTRIBUTES1:_stprintf(buf,_T("SQL_DYNAMIC_CURSOR_ATTRIBUTES1(%ld)"),InfoType);break;
	case SQL_DYNAMIC_CURSOR_ATTRIBUTES2:_stprintf(buf,_T("SQL_DYNAMIC_CURSOR_ATTRIBUTES2(%ld)"),InfoType);break;
	case SQL_FETCH_DIRECTION:           _stprintf(buf,_T("SQL_FETCH_DIRECTION(%ld)"),InfoType);break;
	case SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1:_stprintf(buf,_T("SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES1(%ld)"),InfoType);break;
	case SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES2:_stprintf(buf,_T("SQL_FORWARD_ONLY_CURSOR_ATTRIBUTES2(%ld)"),InfoType);break;
	case SQL_KEYSET_CURSOR_ATTRIBUTES1: _stprintf(buf,_T("SQL_KEYSET_CURSOR_ATTRIBUTES1(%ld)"),InfoType);break;
	case SQL_KEYSET_CURSOR_ATTRIBUTES2:	_stprintf(buf,_T("SQL_KEYSET_CURSOR_ATTRIBUTES2(%ld)"),InfoType);break;
	case SQL_ODBC_API_CONFORMANCE:      _stprintf(buf,_T("SQL_ODBC_API_CONFORMANCE(%ld)"),InfoType);break;
	case SQL_ODBC_VER:                  _stprintf(buf,_T("SQL_ODBC_VER(%ld)"),InfoType);break;
	case SQL_ROW_UPDATES:               _stprintf(buf,_T("SQL_ROW_UPDATES(%ld)"),InfoType);break;
	case SQL_ODBC_SAG_CLI_CONFORMANCE:  _stprintf(buf,_T("SQL_ODBC_SAG_CLI_CONFORMANCE(%ld)"),InfoType);break;
	case SQL_SERVER_NAME:               _stprintf(buf,_T("SQL_SERVER_NAME(%ld)"),InfoType);break;
	case SQL_SEARCH_PATTERN_ESCAPE:     _stprintf(buf,_T("SQL_SEARCH_PATTERN_ESCAPE(%ld)"),InfoType);break;
	case SQL_ODBC_SQL_CONFORMANCE:      _stprintf(buf,_T("SQL_ODBC_SQL_CONFORMANCE(%ld)"),InfoType);break;
	case SQL_DBMS_NAME:                 _stprintf(buf,_T("SQL_DBMS_NAME(%ld)"),InfoType);break;
	case SQL_DBMS_VER:                  _stprintf(buf,_T("SQL_DBMS_VER(%ld)"),InfoType);break;
	case SQL_ACCESSIBLE_TABLES:         _stprintf(buf,_T("SQL_ACCESSIBLE_TABLES(%ld)"),InfoType);break;
	case SQL_ACCESSIBLE_PROCEDURES:     _stprintf(buf,_T("SQL_ACCESSIBLE_PROCEDURES(%ld)"),InfoType);break;
	case SQL_PROCEDURES:                _stprintf(buf,_T("SQL_PROCEDURES(%ld)"),InfoType);break;
	case SQL_CONCAT_NULL_BEHAVIOR:      _stprintf(buf,_T("SQL_CONCAT_NULL_BEHAVIOR(%ld)"),InfoType);break;
	case SQL_CURSOR_COMMIT_BEHAVIOR:    _stprintf(buf,_T("SQL_CURSOR_COMMIT_BEHAVIOR(%ld)"),InfoType);break;
	case SQL_CURSOR_ROLLBACK_BEHAVIOR:  _stprintf(buf,_T("SQL_CURSOR_ROLLBACK_BEHAVIOR(%ld)"),InfoType);break;
	case SQL_DATA_SOURCE_READ_ONLY:     _stprintf(buf,_T("SQL_DATA_SOURCE_READ_ONLY(%ld)"),InfoType);break;
	case SQL_DATABASE_NAME:				_stprintf(buf,_T("SQL_DATABASE_NAME(%ld)"),InfoType);break;
	case SQL_DEFAULT_TXN_ISOLATION:     _stprintf(buf,_T("SQL_DEFAULT_TXN_ISOLATION(%ld)"),InfoType);break;
	case SQL_EXPRESSIONS_IN_ORDERBY:    _stprintf(buf,_T("SQL_EXPRESSIONS_IN_ORDERBY(%ld)"),InfoType);break;
	case SQL_IDENTIFIER_CASE:           _stprintf(buf,_T("SQL_IDENTIFIER_CASE(%ld)"),InfoType);break;
	case SQL_IDENTIFIER_QUOTE_CHAR:     _stprintf(buf,_T("SQL_IDENTIFIER_QUOTE_CHAR(%ld)"),InfoType);break;
	case SQL_MAX_ASYNC_CONCURRENT_STATEMENTS:_stprintf(buf,_T("SQL_MAX_ASYNC_CONCURRENT_STATEMENTS(%ld)"),InfoType);break;
	case SQL_MAX_COLUMN_NAME_LEN:       _stprintf(buf,_T("SQL_MAX_COLUMN_NAME_LEN(%ld)"),InfoType);break;
	case SQL_MAX_CURSOR_NAME_LEN:       _stprintf(buf,_T("SQL_MAX_CURSOR_NAME_LEN(%ld)"),InfoType);break;
	case SQL_MAX_IDENTIFIER_LEN:        _stprintf(buf,_T("SQL_MAX_IDENTIFIER_LEN(%ld)"),InfoType);break;
	case SQL_MAX_SCHEMA_NAME_LEN:       _stprintf(buf,_T("SQL_MAX_SCHEMA_NAME_LEN(%ld)"),InfoType);break;
	case SQL_MAX_PROCEDURE_NAME_LEN:    _stprintf(buf,_T("SQL_MAX_PROCEDURE_NAME_LEN(%ld)"),InfoType);break;
	case SQL_MAX_CATALOG_NAME_LEN:		_stprintf(buf,_T("SQL_MAX_CATALOG_NAME_LEN(%ld)"),InfoType);break;
	case SQL_MAX_TABLE_NAME_LEN:        _stprintf(buf,_T("SQL_MAX_TABLE_NAME_LEN(%ld)"),InfoType);break;
	case SQL_MULT_RESULT_SETS:          _stprintf(buf,_T("SQL_MULT_RESULT_SETS(%ld)"),InfoType);break;
	case SQL_MULTIPLE_ACTIVE_TXN:       _stprintf(buf,_T("SQL_MULTIPLE_ACTIVE_TXN(%ld)"),InfoType);break;
	case SQL_OUTER_JOINS:               _stprintf(buf,_T("SQL_OUTER_JOINS(%ld)"),InfoType);break;
	case SQL_SCHEMA_TERM:               _stprintf(buf,_T("SQL_SCHEMA_TERM(%ld)"),InfoType);break;
	case SQL_PROCEDURE_TERM:            _stprintf(buf,_T("SQL_PROCEDURE_TERM(%ld)"),InfoType);break;
	case SQL_SCROLL_CONCURRENCY:        _stprintf(buf,_T("SQL_SCROLL_CONCURRENCY(%ld)"),InfoType);break;
	case SQL_SCROLL_OPTIONS:            _stprintf(buf,_T("SQL_SCROLL_OPTIONS(%ld)"),InfoType);break;
	case SQL_STATIC_CURSOR_ATTRIBUTES1: _stprintf(buf,_T("SQL_STATIC_CURSOR_ATTRIBUTES1(%ld)"),InfoType);break;
	case SQL_STATIC_CURSOR_ATTRIBUTES2: _stprintf(buf,_T("SQL_STATIC_CURSOR_ATTRIBUTES2(%ld)"),InfoType);break;
	case SQL_TABLE_TERM:                _stprintf(buf,_T("SQL_TABLE_TERM(%ld)"),InfoType);break;
	case SQL_TXN_CAPABLE:               _stprintf(buf,_T("SQL_TXN_CAPABLE(%ld)"),InfoType);break;
	case SQL_USER_NAME:                 _stprintf(buf,_T("SQL_USER_NAME(%ld)"),InfoType);break;
	case SQL_CONVERT_FUNCTIONS:         _stprintf(buf,_T("SQL_CONVERT_FUNCTIONS(%ld)"),InfoType);break;
	case SQL_NUMERIC_FUNCTIONS:         _stprintf(buf,_T("SQL_NUMERIC_FUNCTIONS(%ld)"),InfoType);break;
	case SQL_STRING_FUNCTIONS:          _stprintf(buf,_T("SQL_STRING_FUNCTIONS(%ld)"),InfoType);break;
	case SQL_SYSTEM_FUNCTIONS:          _stprintf(buf,_T("SQL_SYSTEM_FUNCTIONS(%ld)"),InfoType);break;
	case SQL_TIMEDATE_FUNCTIONS:        _stprintf(buf,_T("SQL_TIMEDATE_FUNCTIONS(%ld)"),InfoType);break;
	case SQL_CONVERT_BIGINT:            _stprintf(buf,_T("SQL_CONVERT_BIGINT(%ld)"),InfoType);break;
	case SQL_CONVERT_BIT:               _stprintf(buf,_T("SQL_CONVERT_BIT(%ld)"),InfoType);break;
	case SQL_CONVERT_CHAR:              _stprintf(buf,_T("SQL_CONVERT_CHAR(%ld)"),InfoType);break;
	case SQL_CONVERT_DATE:              _stprintf(buf,_T("SQL_CONVERT_DATE(%ld)"),InfoType);break;
	case SQL_CONVERT_DECIMAL:           _stprintf(buf,_T("SQL_CONVERT_DECIMAL(%ld)"),InfoType);break;
	case SQL_CONVERT_DOUBLE:            _stprintf(buf,_T("SQL_CONVERT_DOUBLE(%ld)"),InfoType);break;
	case SQL_CONVERT_FLOAT:             _stprintf(buf,_T("SQL_CONVERT_FLOAT(%ld)"),InfoType);break;
	case SQL_CONVERT_INTEGER:           _stprintf(buf,_T("SQL_CONVERT_INTEGER(%ld)"),InfoType);break;
	case SQL_CONVERT_INTERVAL_DAY_TIME: _stprintf(buf,_T("SQL_CONVERT_INTERVAL_DAY_TIME(%ld)"),InfoType);break;
	case SQL_CONVERT_INTERVAL_YEAR_MONTH:_stprintf(buf,_T("SQL_CONVERT_INTERVAL_YEAR_MONTH(%ld)"),InfoType);break;
	case SQL_CONVERT_LONGVARCHAR:       _stprintf(buf,_T("SQL_CONVERT_LONGVARCHAR(%ld)"),InfoType);break;
	case SQL_CONVERT_NUMERIC:           _stprintf(buf,_T("SQL_CONVERT_NUMERIC(%ld)"),InfoType);break;
	case SQL_CONVERT_REAL:              _stprintf(buf,_T("SQL_CONVERT_REAL(%ld)"),InfoType);break;
	case SQL_CONVERT_SMALLINT:          _stprintf(buf,_T("SQL_CONVERT_SMALLINT(%ld)"),InfoType);break;
	case SQL_CONVERT_TIME:              _stprintf(buf,_T("SQL_CONVERT_TIME(%ld)"),InfoType);break;
	case SQL_CONVERT_TIMESTAMP:         _stprintf(buf,_T("SQL_CONVERT_TIMESTAMP(%ld)"),InfoType);break;
	case SQL_CONVERT_TINYINT:           _stprintf(buf,_T("SQL_CONVERT_TINYINT(%ld)"),InfoType);break;
	case SQL_CONVERT_VARCHAR:           _stprintf(buf,_T("SQL_CONVERT_VARCHAR(%ld)"),InfoType);break;
	case SQL_CONVERT_BINARY:            _stprintf(buf,_T("SQL_CONVERT_BINARY(%ld)"),InfoType);break;
	case SQL_CONVERT_VARBINARY:         _stprintf(buf,_T("SQL_CONVERT_VARBINARY(%ld)"),InfoType);break;
	case SQL_CONVERT_LONGVARBINARY:     _stprintf(buf,_T("SQL_CONVERT_LONGVARBINARY(%ld)"),InfoType);break;
	case SQL_CONVERT_WCHAR:             _stprintf(buf,_T("SQL_CONVERT_WCHAR(%ld)"),InfoType);break;
	case SQL_CONVERT_WLONGVARCHAR:      _stprintf(buf,_T("SQL_CONVERT_WLONGVARCHAR(%ld)"),InfoType);break;
	case SQL_CONVERT_WVARCHAR:          _stprintf(buf,_T("SQL_CONVERT_WVARCHAR(%ld)"),InfoType);break;
	case SQL_TXN_ISOLATION_OPTION:      _stprintf(buf,_T("SQL_TXN_ISOLATION_OPTION(%ld)"),InfoType);break;
	case SQL_ODBC_SQL_OPT_IEF:          _stprintf(buf,_T("SQL_ODBC_SQL_OPT_IEF(%ld)"),InfoType);break;
	case SQL_CORRELATION_NAME:          _stprintf(buf,_T("SQL_CORRELATION_NAME(%ld)"),InfoType);break;
	case SQL_NON_NULLABLE_COLUMNS:      _stprintf(buf,_T("SQL_NON_NULLABLE_COLUMNS(%ld)"),InfoType);break;
	case SQL_DRIVER_ODBC_VER:           _stprintf(buf,_T("SQL_DRIVER_ODBC_VER(%ld)"),InfoType);break;
	case SQL_LOCK_TYPES:                _stprintf(buf,_T("SQL_LOCK_TYPES(%ld)"),InfoType);break;
	case SQL_POS_OPERATIONS:            _stprintf(buf,_T("SQL_POS_OPERATIONS(%ld)"),InfoType);break;
	case SQL_POSITIONED_STATEMENTS:     _stprintf(buf,_T("SQL_POSITIONED_STATEMENTS(%ld)"),InfoType);break;
	case SQL_GETDATA_EXTENSIONS:        _stprintf(buf,_T("SQL_GETDATA_EXTENSIONS(%ld)"),InfoType);break;
	case SQL_BOOKMARK_PERSISTENCE:      _stprintf(buf,_T("SQL_BOOKMARK_PERSISTENCE(%ld)"),InfoType);break;
	case SQL_STATIC_SENSITIVITY:        _stprintf(buf,_T("SQL_STATIC_SENSITIVITY(%ld)"),InfoType);break;
	case SQL_FILE_USAGE:                _stprintf(buf,_T("SQL_FILE_USAGE(%ld)"),InfoType);break;
	case SQL_NULL_COLLATION:            _stprintf(buf,_T("SQL_NULL_COLLATION(%ld)"),InfoType);break;
	case SQL_ALTER_TABLE:               _stprintf(buf,_T("SQL_ALTER_TABLE(%ld)"),InfoType);break;
	case SQL_COLUMN_ALIAS:              _stprintf(buf,_T("SQL_COLUMN_ALIAS(%ld)"),InfoType);break;
	case SQL_GROUP_BY:                  _stprintf(buf,_T("SQL_GROUP_BY(%ld)"),InfoType);break;
	case SQL_KEYWORDS:                  _stprintf(buf,_T("SQL_KEYWORDS(%ld)"),InfoType);break;
	case SQL_ORDER_BY_COLUMNS_IN_SELECT:_stprintf(buf,_T("SQL_ORDER_BY_COLUMNS_IN_SELECT(%ld)"),InfoType);break;
	case SQL_SCHEMA_USAGE:              _stprintf(buf,_T("SQL_SCHEMA_USAGE(%ld)"),InfoType);break;
	case SQL_CATALOG_USAGE:				_stprintf(buf,_T("SQL_CATALOG_USAGE(%ld)"),InfoType);break;
	case SQL_QUOTED_IDENTIFIER_CASE:    _stprintf(buf,_T("SQL_QUOTED_IDENTIFIER_CASE(%ld)"),InfoType);break;
	case SQL_SPECIAL_CHARACTERS:        _stprintf(buf,_T("SQL_SPECIAL_CHARACTERS(%ld)"),InfoType);break;
	case SQL_SUBQUERIES:                _stprintf(buf,_T("SQL_SUBQUERIES(%ld)"),InfoType);break;
	case SQL_UNION:                     _stprintf(buf,_T("SQL_UNION(%ld)"),InfoType);break;
	case SQL_MAX_COLUMNS_IN_GROUP_BY:   _stprintf(buf,_T("SQL_MAX_COLUMNS_IN_GROUP_BY(%ld)"),InfoType);break;
	case SQL_MAX_COLUMNS_IN_INDEX:      _stprintf(buf,_T("SQL_MAX_COLUMNS_IN_INDEX(%ld)"),InfoType);break;
	case SQL_MAX_COLUMNS_IN_ORDER_BY:   _stprintf(buf,_T("SQL_MAX_COLUMNS_IN_ORDER_BY(%ld)"),InfoType);break;
	case SQL_MAX_COLUMNS_IN_SELECT:     _stprintf(buf,_T("SQL_MAX_COLUMNS_IN_SELECT(%ld)"),InfoType);break;
	case SQL_MAX_COLUMNS_IN_TABLE:      _stprintf(buf,_T("SQL_MAX_COLUMNS_IN_TABLE(%ld)"),InfoType);break;
	case SQL_MAX_INDEX_SIZE:            _stprintf(buf,_T("SQL_MAX_INDEX_SIZE(%ld)"),InfoType);break;
	case SQL_MAX_ROW_SIZE_INCLUDES_LONG:_stprintf(buf,_T("SQL_MAX_ROW_SIZE_INCLUDES_LONG(%ld)"),InfoType);break;
	case SQL_MAX_ROW_SIZE:              _stprintf(buf,_T("SQL_MAX_ROW_SIZE(%ld)"),InfoType);break;
	case SQL_MAX_STATEMENT_LEN:         _stprintf(buf,_T("SQL_MAX_STATEMENT_LEN(%ld)"),InfoType);break;
	case SQL_MAX_TABLES_IN_SELECT:      _stprintf(buf,_T("SQL_MAX_TABLES_IN_SELECT(%ld)"),InfoType);break;
	case SQL_MAX_USER_NAME_LEN:         _stprintf(buf,_T("SQL_MAX_USER_NAME_LEN(%ld)"),InfoType);break;
	case SQL_MAX_CHAR_LITERAL_LEN:      _stprintf(buf,_T("SQL_MAX_CHAR_LITERAL_LEN(%ld)"),InfoType);break;
	case SQL_TIMEDATE_ADD_INTERVALS:    _stprintf(buf,_T("SQL_TIMEDATE_ADD_INTERVALS(%ld)"),InfoType);break;
	case SQL_TIMEDATE_DIFF_INTERVALS:   _stprintf(buf,_T("SQL_TIMEDATE_DIFF_INTERVALS(%ld)"),InfoType);break;
	case SQL_NEED_LONG_DATA_LEN:        _stprintf(buf,_T("SQL_NEED_LONG_DATA_LEN(%ld)"),InfoType);break;
	case SQL_MAX_BINARY_LITERAL_LEN:    _stprintf(buf,_T("SQL_MAX_BINARY_LITERAL_LEN(%ld)"),InfoType);break;
	case SQL_LIKE_ESCAPE_CLAUSE:        _stprintf(buf,_T("SQL_LIKE_ESCAPE_CLAUSE(%ld)"),InfoType);break;
	case SQL_CATALOG_LOCATION:			_stprintf(buf,_T("SQL_CATALOG_LOCATION(%ld)"),InfoType);break;
	case SQL_OJ_CAPABILITIES:			_stprintf(buf,_T("SQL_OJ_CAPABILITIES(%ld)"),InfoType);break;
	case SQL_ACTIVE_ENVIRONMENTS:		_stprintf(buf,_T("SQL_ACTIVE_ENVIRONMENTS(%ld)"),InfoType);break;
	case SQL_ALTER_DOMAIN:				_stprintf(buf,_T("SQL_ALTER_DOMAIN(%ld)"),InfoType);break;
	case SQL_SQL_CONFORMANCE:			_stprintf(buf,_T("SQL_SQL_CONFORMANCE(%ld)"),InfoType);break;
	case SQL_DATETIME_LITERALS:			_stprintf(buf,_T("SQL_DATETIME_LITERALS(%ld)"),InfoType);break;
	case SQL_BATCH_ROW_COUNT:			_stprintf(buf,_T("SQL_BATCH_ROW_COUNT(%ld)"),InfoType);break;
	case SQL_BATCH_SUPPORT:				_stprintf(buf,_T("SQL_BATCH_SUPPORT(%ld)"),InfoType);break;
	case SQL_CREATE_ASSERTION:			_stprintf(buf,_T("SQL_CREATE_ASSERTION(%ld)"),InfoType);break;
	case SQL_CREATE_CHARACTER_SET:		_stprintf(buf,_T("SQL_CREATE_CHARACTER_SET(%ld)"),InfoType);break;
	case SQL_CREATE_COLLATION:			_stprintf(buf,_T("SQL_CREATE_COLLATION(%ld)"),InfoType);break;
	case SQL_CREATE_DOMAIN:				_stprintf(buf,_T("SQL_CREATE_DOMAIN(%ld)"),InfoType);break;
	case SQL_CREATE_SCHEMA:				_stprintf(buf,_T("SQL_CREATE_SCHEMA(%ld)"),InfoType);break;
	case SQL_CREATE_TABLE:				_stprintf(buf,_T("SQL_CREATE_TABLE(%ld)"),InfoType);break;
	case SQL_CREATE_TRANSLATION:		_stprintf(buf,_T("SQL_CREATE_TRANSLATION(%ld)"),InfoType);break;
	case SQL_CREATE_VIEW:				_stprintf(buf,_T("SQL_CREATE_VIEW(%ld)"),InfoType);break;
	case SQL_DRIVER_HDESC:				_stprintf(buf,_T("SQL_DRIVER_HDESC(%ld)"),InfoType);break;
	case SQL_DROP_ASSERTION:			_stprintf(buf,_T("SQL_DROP_ASSERTION(%ld)"),InfoType);break;
	case SQL_DROP_CHARACTER_SET:		_stprintf(buf,_T("SQL_DROP_CHARACTER_SET(%ld)"),InfoType);break;
	case SQL_DROP_COLLATION:			_stprintf(buf,_T("SQL_DROP_COLLATION(%ld)"),InfoType);break;
	case SQL_DROP_DOMAIN:				_stprintf(buf,_T("SQL_DROP_DOMAIN(%ld)"),InfoType);break;
	case SQL_DROP_SCHEMA:				_stprintf(buf,_T("SQL_DROP_SCHEMA(%ld)"),InfoType);break;
	case SQL_DROP_TABLE:				_stprintf(buf,_T("SQL_DROP_TABLE(%ld)"),InfoType);break;
	case SQL_DROP_TRANSLATION:			_stprintf(buf,_T("SQL_DROP_TRANSLATION(%ld)"),InfoType);break;
	case SQL_DROP_VIEW:					_stprintf(buf,_T("SQL_DROP_VIEW(%ld)"),InfoType);break;
	case SQL_INDEX_KEYWORDS:			_stprintf(buf,_T("SQL_INDEX_KEYWORDS(%ld)"),InfoType);break;
	case SQL_INFO_SCHEMA_VIEWS:			_stprintf(buf,_T("SQL_INFO_SCHEMA_VIEWS(%ld)"),InfoType);break;
	case SQL_ODBC_INTERFACE_CONFORMANCE:_stprintf(buf,_T("SQL_ODBC_INTERFACE_CONFORMANCE(%ld)"),InfoType);break;
	case SQL_PARAM_ARRAY_ROW_COUNTS:	_stprintf(buf,_T("SQL_PARAM_ARRAY_ROW_COUNTS(%ld)"),InfoType);break;
	case SQL_PARAM_ARRAY_SELECTS:		_stprintf(buf,_T("SQL_PARAM_ARRAY_SELECTS(%ld)"),InfoType);break;
	case SQL_SQL92_DATETIME_FUNCTIONS:	_stprintf(buf,_T("SQL_SQL92_DATETIME_FUNCTIONS(%ld)"),InfoType);break;
	case SQL_SQL92_FOREIGN_KEY_DELETE_RULE:_stprintf(buf,_T("SQL_SQL92_FOREIGN_KEY_DELETE_RULE(%ld)"),InfoType);break;
	case SQL_SQL92_FOREIGN_KEY_UPDATE_RULE:_stprintf(buf,_T("SQL_SQL92_FOREIGN_KEY_UPDATE_RULE(%ld)"),InfoType);break;
	case SQL_SQL92_GRANT:				_stprintf(buf,_T("SQL_SQL92_GRANT(%ld)"),InfoType);break;
	case SQL_SQL92_NUMERIC_VALUE_FUNCTIONS:_stprintf(buf,_T("SQL_SQL92_NUMERIC_VALUE_FUNCTIONS(%ld)"),InfoType);break;
	case SQL_SQL92_PREDICATES:			_stprintf(buf,_T("SQL_SQL92_PREDICATES(%ld)"),InfoType);break;
	case SQL_SQL92_RELATIONAL_JOIN_OPERATORS:_stprintf(buf,_T("SQL_SQL92_RELATIONAL_JOIN_OPERATORS(%ld)"),InfoType);break;
	case SQL_SQL92_REVOKE:				_stprintf(buf,_T("SQL_SQL92_REVOKE(%ld)"),InfoType);break;
	case SQL_SQL92_ROW_VALUE_CONSTRUCTOR:_stprintf(buf,_T("SQL_SQL92_ROW_VALUE_CONSTRUCTOR(%ld)"),InfoType);break;
	case SQL_SQL92_STRING_FUNCTIONS:	_stprintf(buf,_T("SQL_SQL92_STRING_FUNCTIONS(%ld)"),InfoType);break;
	case SQL_SQL92_VALUE_EXPRESSIONS:	_stprintf(buf,_T("SQL_SQL92_VALUE_EXPRESSIONS(%ld)"),InfoType);break;
	case SQL_STANDARD_CLI_CONFORMANCE:	_stprintf(buf,_T("SQL_STANDARD_CLI_CONFORMANCE(%ld)"),InfoType);break;
	case SQL_AGGREGATE_FUNCTIONS:		_stprintf(buf,_T("SQL_AGGREGATE_FUNCTIONS(%ld)"),InfoType);break;
	case SQL_DDL_INDEX:					_stprintf(buf,_T("SQL_DDL_INDEX(%ld)"),InfoType);break;
	case SQL_INSERT_STATEMENT:			_stprintf(buf,_T("SQL_INSERT_STATEMENT(%ld)"),InfoType);break;
	case SQL_XOPEN_CLI_YEAR:			_stprintf(buf,_T("SQL_XOPEN_CLI_YEAR(%ld)"),InfoType);break;
	default:
		_ltot(InfoType,buf,10);
	}
	return buf;
}

/****************************************************************
** StrFunctionToString()
**
** This function will attempt to convert a String Fuction bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *StrFunctionToString(long StrFunction, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(StrFunction&SQL_FN_STR_ASCII){
		_tcscat (buf,_T("SQL_FN_STR_ASCII "));
		StrFunction=StrFunction^SQL_FN_STR_ASCII;
		}
	if(StrFunction&SQL_FN_STR_BIT_LENGTH){
		_tcscat (buf,_T("SQL_FN_STR_BIT_LENGTH "));
		StrFunction=StrFunction^SQL_FN_STR_BIT_LENGTH;
		}
	if(StrFunction&SQL_FN_STR_CHAR){
		_tcscat (buf,_T("SQL_FN_STR_CHAR "));
		StrFunction=StrFunction^SQL_FN_STR_CHAR;
		}
	if(StrFunction&SQL_FN_STR_CHAR_LENGTH){
		_tcscat (buf,_T("SQL_FN_STR_CHAR_LENGTH "));
		StrFunction=StrFunction^SQL_FN_STR_CHAR_LENGTH;
		}
	if(StrFunction&SQL_FN_STR_CHARACTER_LENGTH){
		_tcscat (buf,_T("SQL_FN_STR_CHARACTER_LENGTH "));
		StrFunction=StrFunction^SQL_FN_STR_CHARACTER_LENGTH;
		}
	if(StrFunction&SQL_FN_STR_CONCAT){
		_tcscat (buf,_T("SQL_FN_STR_CONCAT "));
		StrFunction=StrFunction^SQL_FN_STR_CONCAT;
		}
	if(StrFunction&SQL_FN_STR_DIFFERENCE){
		_tcscat (buf,_T("SQL_FN_STR_DIFFERENCE "));
		StrFunction=StrFunction^SQL_FN_STR_DIFFERENCE;
		}
	if(StrFunction&SQL_FN_STR_INSERT){
		_tcscat (buf,_T("SQL_FN_STR_INSERT "));
		StrFunction=StrFunction^SQL_FN_STR_INSERT;
		}
	if(StrFunction&SQL_FN_STR_LCASE){
		_tcscat (buf,_T("SQL_FN_STR_LCASE "));
		StrFunction=StrFunction^SQL_FN_STR_LCASE;
		}
	if(StrFunction&SQL_FN_STR_LEFT){
		_tcscat (buf,_T("SQL_FN_STR_LEFT "));
		StrFunction=StrFunction^SQL_FN_STR_LEFT;
		}
	if(StrFunction&SQL_FN_STR_LENGTH){
		_tcscat (buf,_T("SQL_FN_STR_LENGTH "));
		StrFunction=StrFunction^SQL_FN_STR_LENGTH;
		}
	if(StrFunction&SQL_FN_STR_LOCATE){
		_tcscat (buf,_T("SQL_FN_STR_LOCATE "));
		StrFunction=StrFunction^SQL_FN_STR_LOCATE;
		}
	if(StrFunction&SQL_FN_STR_LOCATE_2){
		_tcscat (buf,_T("SQL_FN_STR_LOCATE_2 "));
		StrFunction=StrFunction^SQL_FN_STR_LOCATE_2;
		}
	if(StrFunction&SQL_FN_STR_LTRIM){ 
		_tcscat (buf,_T("SQL_FN_STR_LTRIM "));
		StrFunction=StrFunction^SQL_FN_STR_LTRIM;
		}
	if(StrFunction&SQL_FN_STR_OCTET_LENGTH){ 
		_tcscat (buf,_T("SQL_FN_STR_OCTET_LENGTH "));
		StrFunction=StrFunction^SQL_FN_STR_OCTET_LENGTH;
		}
	if(StrFunction&SQL_FN_STR_POSITION){
		_tcscat (buf,_T("SQL_FN_STR_POSITION "));
		StrFunction=StrFunction^SQL_FN_STR_POSITION;
		}
	if(StrFunction&SQL_FN_STR_REPEAT){
		_tcscat (buf,_T("SQL_FN_STR_REPEAT "));
		StrFunction=StrFunction^SQL_FN_STR_REPEAT;
		}
	if(StrFunction&SQL_FN_STR_REPLACE){
		_tcscat (buf,_T("SQL_FN_STR_REPLACE "));
		StrFunction=StrFunction^SQL_FN_STR_REPLACE;
		}
	if(StrFunction&SQL_FN_STR_RIGHT){
		_tcscat (buf,_T("SQL_FN_STR_RIGHT "));
		StrFunction=StrFunction^SQL_FN_STR_RIGHT;
		}
	if(StrFunction&SQL_FN_STR_RTRIM){
		_tcscat (buf,_T("SQL_FN_STR_RTRIM "));
		StrFunction=StrFunction^SQL_FN_STR_RTRIM;
		}
	if(StrFunction&SQL_FN_STR_SOUNDEX){
		_tcscat (buf,_T("SQL_FN_STR_SOUNDEX "));
		StrFunction=StrFunction^SQL_FN_STR_SOUNDEX;
		}
	if(StrFunction&SQL_FN_STR_SPACE){
		_tcscat (buf,_T("SQL_FN_STR_SPACE "));
		StrFunction=StrFunction^SQL_FN_STR_SPACE;
		}
	if(StrFunction&SQL_FN_STR_SUBSTRING){
		_tcscat (buf,_T("SQL_FN_STR_SUBSTRING "));
		StrFunction=StrFunction^SQL_FN_STR_SUBSTRING;
		}
	if(StrFunction&SQL_FN_STR_UCASE){
		_tcscat (buf,_T("SQL_FN_STR_UCASE "));
		StrFunction=StrFunction^SQL_FN_STR_UCASE;
		}
	
	// Should be zero unless there are undefined bits
	if(StrFunction){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),StrFunction);
		_tcscat(buf,TempBuf);
		}

	return buf;
	}
		
/****************************************************************
** TimeFunctionToString()
**
** This function will attempt to convert a Time Function bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *TimeFunctionToString(long TimeFunction, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
if(TimeFunction&SQL_FN_TD_CURRENT_DATE){
		_tcscat (buf,_T("SQL_FN_TD_CURRENT_DATE "));
		TimeFunction=TimeFunction^SQL_FN_TD_CURRENT_DATE;
		}
if(TimeFunction&SQL_FN_TD_CURRENT_TIME){
		_tcscat (buf,_T("SQL_FN_TD_CURRENT_TIME "));
		TimeFunction=TimeFunction^SQL_FN_TD_CURRENT_TIME;
		}
if(TimeFunction&SQL_FN_TD_CURRENT_TIMESTAMP){
		_tcscat (buf,_T("SQL_FN_TD_CURRENT_TIMESTAMP "));
		TimeFunction=TimeFunction^SQL_FN_TD_CURRENT_TIMESTAMP;
		}
if(TimeFunction&SQL_FN_TD_CURDATE){
		_tcscat (buf,_T("SQL_FN_TD_CURDATE "));
		TimeFunction=TimeFunction^SQL_FN_TD_CURDATE;
		}
if(TimeFunction&SQL_FN_TD_CURTIME){ 
		_tcscat (buf,_T("SQL_FN_TD_CURTIME "));
		TimeFunction=TimeFunction^SQL_FN_TD_CURTIME;
		}
if(TimeFunction&SQL_FN_TD_DAYNAME){
		_tcscat (buf,_T("SQL_FN_TD_DAYNAME "));
		TimeFunction=TimeFunction^SQL_FN_TD_DAYNAME;
		}
if(TimeFunction&SQL_FN_TD_DAYOFMONTH){
		_tcscat (buf,_T("SQL_FN_TD_DAYOFMONTH "));
		TimeFunction=TimeFunction^SQL_FN_TD_DAYOFMONTH;
		}
if(TimeFunction&SQL_FN_TD_DAYOFWEEK){
		_tcscat (buf,_T("SQL_FN_TD_DAYOFWEEK "));
		TimeFunction=TimeFunction^SQL_FN_TD_DAYOFWEEK;
		}
if(TimeFunction&SQL_FN_TD_DAYOFYEAR){ 
		_tcscat (buf,_T("SQL_FN_TD_DAYOFYEAR "));
		TimeFunction=TimeFunction^SQL_FN_TD_DAYOFYEAR;
		}
if(TimeFunction&SQL_FN_TD_EXTRACT){
		_tcscat (buf,_T("SQL_FN_TD_EXTRACT "));
		TimeFunction=TimeFunction^SQL_FN_TD_EXTRACT;
		}
if(TimeFunction&SQL_FN_TD_HOUR){
		_tcscat (buf,_T("SQL_FN_TD_HOUR "));
		TimeFunction=TimeFunction^SQL_FN_TD_HOUR;
		}
if(TimeFunction&SQL_FN_TD_MINUTE){
		_tcscat (buf,_T("SQL_FN_TD_MINUTE "));
		TimeFunction=TimeFunction^SQL_FN_TD_MINUTE;
		}
if(TimeFunction&SQL_FN_TD_MONTH){
		_tcscat (buf,_T("SQL_FN_TD_MONTH "));
		TimeFunction=TimeFunction^SQL_FN_TD_MONTH;
		}
if(TimeFunction&SQL_FN_TD_MONTHNAME){
		_tcscat (buf,_T("SQL_FN_TD_MONTHNAME "));
		TimeFunction=TimeFunction^SQL_FN_TD_MONTHNAME;
		}
if(TimeFunction&SQL_FN_TD_NOW){
		_tcscat (buf,_T("SQL_FN_TD_NOW "));
		TimeFunction=TimeFunction^SQL_FN_TD_NOW;
		}
if(TimeFunction&SQL_FN_TD_QUARTER){
		_tcscat (buf,_T("SQL_FN_TD_QUARTER "));
		TimeFunction=TimeFunction^SQL_FN_TD_QUARTER;
		}
if(TimeFunction&SQL_FN_TD_SECOND){
		_tcscat (buf,_T("SQL_FN_TD_SECOND "));
		TimeFunction=TimeFunction^SQL_FN_TD_SECOND;
		}
if(TimeFunction&SQL_FN_TD_TIMESTAMPADD){
		_tcscat (buf,_T("SQL_FN_TD_TIMESTAMPADD "));
		TimeFunction=TimeFunction^SQL_FN_TD_TIMESTAMPADD;
		}
if(TimeFunction&SQL_FN_TD_TIMESTAMPDIFF){
		_tcscat (buf,_T("SQL_FN_TD_TIMESTAMPDIFF "));
		TimeFunction=TimeFunction^SQL_FN_TD_TIMESTAMPDIFF;
		}
if(TimeFunction&SQL_FN_TD_WEEK){
		_tcscat (buf,_T("SQL_FN_TD_WEEK "));
		TimeFunction=TimeFunction^SQL_FN_TD_WEEK;
		}
if(TimeFunction&SQL_FN_TD_YEAR){
		_tcscat (buf,_T("SQL_FN_TD_YEAR "));
		TimeFunction=TimeFunction^SQL_FN_TD_YEAR;
		}

	// Should be zero unless there are undefined bits
	if(TimeFunction){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),TimeFunction);
		_tcscat(buf,TempBuf);
		}

	return buf;
	}

/****************************************************************
** TimeIntToString()
**
** This function will attempt to convert a Time Interval bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *TimeIntToString(long TimeInt, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(TimeInt&SQL_FN_TSI_FRAC_SECOND){
		_tcscat (buf,_T("SQL_FN_TSI_FRAC_SECOND "));
		TimeInt=TimeInt^SQL_FN_TSI_FRAC_SECOND;
		}
	if(TimeInt&SQL_FN_TSI_SECOND){
		_tcscat (buf,_T("SQL_FN_TSI_SECOND "));
		TimeInt=TimeInt^SQL_FN_TSI_SECOND;
		}
	if(TimeInt&SQL_FN_TSI_MINUTE){
		_tcscat (buf,_T("SQL_FN_TSI_MINUTE "));
		TimeInt=TimeInt^SQL_FN_TSI_MINUTE;
		}
	if(TimeInt&SQL_FN_TSI_HOUR){
		_tcscat (buf,_T("SQL_FN_TSI_HOUR "));
		TimeInt=TimeInt^SQL_FN_TSI_HOUR;
		}
	if(TimeInt&SQL_FN_TSI_DAY){
		_tcscat (buf,_T("SQL_FN_TSI_DAY "));
		TimeInt=TimeInt^SQL_FN_TSI_DAY;
		}
	if(TimeInt&SQL_FN_TSI_WEEK){
		_tcscat (buf,_T("SQL_FN_TSI_WEEK "));
		TimeInt=TimeInt^SQL_FN_TSI_WEEK;
		}
	if(TimeInt&SQL_FN_TSI_MONTH){
		_tcscat (buf,_T("SQL_FN_TSI_MONTH "));
		TimeInt=TimeInt^SQL_FN_TSI_MONTH;
		}
	if(TimeInt&SQL_FN_TSI_QUARTER){
		_tcscat (buf,_T("SQL_FN_TSI_QUARTER "));
		TimeInt=TimeInt^SQL_FN_TSI_QUARTER;
		}
	if(TimeInt&SQL_FN_TSI_YEAR){
		_tcscat (buf,_T("SQL_FN_TSI_YEAR "));
		TimeInt=TimeInt^SQL_FN_TSI_YEAR;
		}

	// Should be zero unless there are undefined bits
	if(TimeInt){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),TimeInt);
		_tcscat(buf,TempBuf);
		}

	return buf;
	}

/****************************************************************
** OJToString()
**
** This function will attempt to convert an Outer Join Capabilities bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *OJToString(long OJ, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(OJ&SQL_OJ_LEFT){
		_tcscat (buf,_T("SQL_OJ_LEFT "));
		OJ=OJ^SQL_OJ_LEFT;
		}
	if(OJ&SQL_OJ_RIGHT){
		_tcscat (buf,_T("SQL_OJ_RIGHT "));
		OJ=OJ^SQL_OJ_RIGHT;
		}
	if(OJ&SQL_OJ_FULL){
		_tcscat (buf,_T("SQL_OJ_FULL "));
		OJ=OJ^SQL_OJ_FULL;
		}
	if(OJ&SQL_OJ_NESTED){
		_tcscat (buf,_T("SQL_OJ_NESTED "));
		OJ=OJ^SQL_OJ_NESTED;
		}
	if(OJ&SQL_OJ_NOT_ORDERED){
		_tcscat (buf,_T("SQL_OJ_NOT_ORDERED "));
		OJ=OJ^SQL_OJ_NOT_ORDERED;
		}
	if(OJ&SQL_OJ_INNER){
		_tcscat (buf,_T("SQL_OJ_INNER "));
		OJ=OJ^SQL_OJ_INNER;
		}
	if(OJ&SQL_OJ_ALL_COMPARISON_OPS){ 
		_tcscat (buf,_T("SQL_OJ_ALL_COMPARISON_OPS "));
		OJ=OJ^SQL_OJ_ALL_COMPARISON_OPS;
		}

	// Should be zero unless there are undefined bits
	if(OJ){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),OJ);
		_tcscat(buf,TempBuf);
		}

	return buf;
	}

/****************************************************************
** GDExtToString()
**
** This function will attempt to convert a GetData Extensions bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *GDExtToString(long GDExt, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(GDExt&SQL_GD_ANY_COLUMN){
		_tcscat (buf,_T("SQL_GD_ANY_COLUMN "));
		GDExt=GDExt^SQL_GD_ANY_COLUMN;
		}
	if(GDExt&SQL_GD_ANY_ORDER){
		_tcscat (buf,_T("SQL_GD_ANY_ORDER "));
		GDExt=GDExt^SQL_GD_ANY_ORDER;
		}
	if(GDExt&SQL_GD_BLOCK){
		_tcscat (buf,_T("SQL_GD_BLOCK "));
		GDExt=GDExt^SQL_GD_BLOCK;
		}
	if(GDExt&SQL_GD_BOUND){
		_tcscat (buf,_T("SQL_GD_BOUND "));
		GDExt=GDExt^SQL_GD_BOUND;
		}

	// Should be zero unless there are undefined bits
	if(GDExt){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),GDExt);
		_tcscat(buf,TempBuf);
		}

	return buf;
	}

/****************************************************************
** NumFunctionToString()
**
** This function will attempt to convert a Numeric Fuction bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *NumFunctionToString(long NumFunction, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(NumFunction&SQL_FN_NUM_ABS){
		_tcscat (buf,_T("SQL_FN_NUM_ABS "));
		NumFunction=NumFunction^SQL_FN_NUM_ABS;
		}
	if(NumFunction&SQL_FN_NUM_ACOS){
		_tcscat (buf,_T("SQL_FN_NUM_ACOS "));
		NumFunction=NumFunction^SQL_FN_NUM_ACOS;
		}
	if(NumFunction&SQL_FN_NUM_ASIN){
		_tcscat (buf,_T("SQL_FN_NUM_ASIN "));
		NumFunction=NumFunction^SQL_FN_NUM_ASIN;
		}
	if(NumFunction&SQL_FN_NUM_ATAN){
		_tcscat (buf,_T("SQL_FN_NUM_ATAN "));
		NumFunction=NumFunction^SQL_FN_NUM_ATAN;
		}
	if(NumFunction&SQL_FN_NUM_ATAN2){
		_tcscat (buf,_T("SQL_FN_NUM_ATAN2 "));
		NumFunction=NumFunction^SQL_FN_NUM_ATAN2;
		}
	if(NumFunction&SQL_FN_NUM_CEILING){
		_tcscat (buf,_T("SQL_FN_NUM_CEILING "));
		NumFunction=NumFunction^SQL_FN_NUM_CEILING;
		}
	if(NumFunction&SQL_FN_NUM_COS){
		_tcscat (buf,_T("SQL_FN_NUM_COS "));
		NumFunction=NumFunction^SQL_FN_NUM_COS;
		}
	if(NumFunction&SQL_FN_NUM_COT){
		_tcscat (buf,_T("SQL_FN_NUM_COT "));
		NumFunction=NumFunction^SQL_FN_NUM_COT;
		}
	if(NumFunction&SQL_FN_NUM_DEGREES){
		_tcscat (buf,_T("SQL_FN_NUM_DEGREES "));
		NumFunction=NumFunction^SQL_FN_NUM_DEGREES;
		}
	if(NumFunction&SQL_FN_NUM_EXP){
		_tcscat (buf,_T("SQL_FN_NUM_EXP "));
		NumFunction=NumFunction^SQL_FN_NUM_EXP;
		}
	if(NumFunction&SQL_FN_NUM_FLOOR){
		_tcscat (buf,_T("SQL_FN_NUM_FLOOR "));
		NumFunction=NumFunction^SQL_FN_NUM_FLOOR;
		}
	if(NumFunction&SQL_FN_NUM_LOG){
		_tcscat (buf,_T("SQL_FN_NUM_LOG "));
		NumFunction=NumFunction^SQL_FN_NUM_LOG;
		}
	if(NumFunction&SQL_FN_NUM_LOG10){
		_tcscat (buf,_T("SQL_FN_NUM_LOG10 "));
		NumFunction=NumFunction^SQL_FN_NUM_LOG10;
		}
	if(NumFunction&SQL_FN_NUM_MOD){
		_tcscat (buf,_T("SQL_FN_NUM_MOD "));
		NumFunction=NumFunction^SQL_FN_NUM_MOD;
		}
	if(NumFunction&SQL_FN_NUM_PI){
		_tcscat (buf,_T("SQL_FN_NUM_PI "));
		NumFunction=NumFunction^SQL_FN_NUM_PI;
		}
	if(NumFunction&SQL_FN_NUM_POWER){
		_tcscat (buf,_T("SQL_FN_NUM_POWER "));
		NumFunction=NumFunction^SQL_FN_NUM_POWER;
		}
	if(NumFunction&SQL_FN_NUM_RADIANS){
		_tcscat (buf,_T("SQL_FN_NUM_RADIANS "));
		NumFunction=NumFunction^SQL_FN_NUM_RADIANS;
		}
	if(NumFunction&SQL_FN_NUM_RAND){
		_tcscat (buf,_T("SQL_FN_NUM_RAND "));
		NumFunction=NumFunction^SQL_FN_NUM_RAND;
		}
	if(NumFunction&SQL_FN_NUM_ROUND){
		_tcscat (buf,_T("SQL_FN_NUM_ROUND "));
		NumFunction=NumFunction^SQL_FN_NUM_ROUND;
		}
	if(NumFunction&SQL_FN_NUM_SIGN){
		_tcscat (buf,_T("SQL_FN_NUM_SIGN "));
		NumFunction=NumFunction^SQL_FN_NUM_SIGN;
		}
	if(NumFunction&SQL_FN_NUM_SIN){
		_tcscat (buf,_T("SQL_FN_NUM_SIN "));
		NumFunction=NumFunction^SQL_FN_NUM_SIN;
		}
	if(NumFunction&SQL_FN_NUM_SQRT){
		_tcscat (buf,_T("SQL_FN_NUM_SQRT "));
		NumFunction=NumFunction^SQL_FN_NUM_SQRT;
		}
	if(NumFunction&SQL_FN_NUM_TAN){
		_tcscat (buf,_T("SQL_FN_NUM_TAN "));
		NumFunction=NumFunction^SQL_FN_NUM_TAN;
		}
	if(NumFunction&SQL_FN_NUM_TRUNCATE){
		_tcscat (buf,_T("SQL_FN_NUM_TRUNCATE "));
		NumFunction=NumFunction^SQL_FN_NUM_TRUNCATE;
		}

	// Should be zero unless there are undefined bits
	if(NumFunction){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),NumFunction);
		_tcscat(buf,TempBuf);
		}

	return buf;
	}
		
/****************************************************************
** CatalogUsageToString()
**
** This function will attempt to convert a catalog usage bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *CatalogUsageToString(long CatUsage, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(CatUsage&SQL_CU_DML_STATEMENTS){
		_tcscat (buf,_T("SQL_CU_DML_STATEMENTS "));
		CatUsage=CatUsage^SQL_CU_DML_STATEMENTS;
		}
	if(CatUsage&SQL_CU_PROCEDURE_INVOCATION){
		_tcscat (buf,_T("SQL_CU_PROCEDURE_INVOCATION "));
		CatUsage=CatUsage^SQL_CU_PROCEDURE_INVOCATION;
		}
	if(CatUsage&SQL_CU_TABLE_DEFINITION){
		_tcscat (buf,_T("SQL_CU_TABLE_DEFINITION "));
		CatUsage=CatUsage^SQL_CU_TABLE_DEFINITION;
		}
	if(CatUsage&SQL_CU_INDEX_DEFINITION){
		_tcscat (buf,_T("SQL_CU_INDEX_DEFINITION "));
		CatUsage=CatUsage^SQL_CU_INDEX_DEFINITION;
		}
	if(CatUsage&SQL_CU_PRIVILEGE_DEFINITION){
		_tcscat (buf,_T("SQL_CU_PRIVILEGE_DEFINITION "));
		CatUsage=CatUsage^SQL_CU_PRIVILEGE_DEFINITION;
		}

	// Should be zero unless there are undefined bits
	if(CatUsage){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),CatUsage);
		_tcscat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** SchemaUsageToString()
**
** This function will attempt to convert a schema usage bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *SchemaUsageToString(long SchemaUsage, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(SchemaUsage&SQL_SU_DML_STATEMENTS){
		_tcscat (buf,_T("SQL_SU_DML_STATEMENTS "));
		SchemaUsage=SchemaUsage^SQL_SU_DML_STATEMENTS;
		}
	if(SchemaUsage&SQL_SU_PROCEDURE_INVOCATION){
		_tcscat (buf,_T("SQL_SU_PROCEDURE_INVOCATION "));
		SchemaUsage=SchemaUsage^SQL_SU_PROCEDURE_INVOCATION;
		}
	if(SchemaUsage&SQL_SU_TABLE_DEFINITION){
		_tcscat (buf,_T("SQL_SU_TABLE_DEFINITION "));
		SchemaUsage=SchemaUsage^SQL_SU_TABLE_DEFINITION;
		}
	if(SchemaUsage&SQL_SU_INDEX_DEFINITION){
		_tcscat (buf,_T("SQL_SU_INDEX_DEFINITION "));
		SchemaUsage=SchemaUsage^SQL_SU_INDEX_DEFINITION;
		}
	if(SchemaUsage&SQL_SU_PRIVILEGE_DEFINITION){
		_tcscat (buf,_T("SQL_SU_PRIVILEGE_DEFINITION "));
		SchemaUsage=SchemaUsage^SQL_SU_PRIVILEGE_DEFINITION;
		}

	// Should be zero unless there are undefined bits
	if(SchemaUsage){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),SchemaUsage);
		_tcscat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** GroupByToString()
**
** This function will attempt to convert a Group By value
** into a more user friendly character string.
** If the value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *GroupByToString(SWORD GroupBy, TCHAR *buf)
{
   switch (GroupBy) {
		case SQL_GB_COLLATE:							_tcscpy (buf,_T("SQL_GB_COLLATE"));break;
		case SQL_GB_NOT_SUPPORTED:					_tcscpy (buf,_T("SQL_GB_NOT_SUPPORTED"));break;
		case SQL_GB_GROUP_BY_EQUALS_SELECT:		_tcscpy (buf,_T("SQL_GB_GROUP_BY_EQUALS_SELECT"));break;
		case SQL_GB_GROUP_BY_CONTAINS_SELECT:	_tcscpy (buf,_T("SQL_GB_GROUP_BY_CONTAINS_SELECT"));break;
		case SQL_GB_NO_RELATION:					_tcscpy (buf,_T("SQL_GB_NO_RELATION"));break;
      default:
         _itot(GroupBy,buf,10);
		}
	return buf;
}


/****************************************************************
** CaseToString()
**
** This function will attempt to convert an Identifier Case value
** into a more user friendly character string.
** If the value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *CaseToString(SWORD CaseValue, TCHAR *buf)
{
   switch (CaseValue) {
		case SQL_IC_UPPER:		_tcscpy (buf,_T("SQL_IC_UPPER"));break;
		case SQL_IC_LOWER:		_tcscpy (buf,_T("SQL_IC_LOWER"));break;
		case SQL_IC_SENSITIVE:	_tcscpy (buf,_T("SQL_IC_SENSITIVE"));break;
		case SQL_IC_MIXED:		_tcscpy (buf,_T("SQL_IC_MIXED"));break;
      default:
         _itot(CaseValue,buf,10);
		}
	return buf;
}

/****************************************************************
** ConcatNullToString()
**
** This function will attempt to convert a concat null behavior value
** into a more user friendly character string.
** If the concat null behavior value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *ConcatNullToString(SWORD ConcatNull, TCHAR *buf)
{
   switch (ConcatNull) {
		case SQL_CB_NULL:			_tcscpy (buf,_T("SQL_CB_NULL"));break;
		case SQL_CB_NON_NULL:	_tcscpy (buf,_T("SQL_CB_NON_NULL"));break;
      default:
         _itot(ConcatNull,buf,10);
		}
	return buf;
}

/****************************************************************
** CA1ToString()
**
** This function will attempt to convert a Cursor Attribute bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *CA1ToString(long CAValue, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(CAValue&SQL_CA1_NEXT){
		_tcscat(buf,_T("SQL_CA1_NEXT "));
		CAValue=CAValue^SQL_CA1_NEXT;
		}
	if(CAValue&SQL_CA1_ABSOLUTE){
		_tcscat(buf,_T("SQL_CA1_ABSOLUTE "));
		CAValue=CAValue^SQL_CA1_ABSOLUTE;
		}
	if(CAValue&SQL_CA1_RELATIVE){
		_tcscat(buf,_T("SQL_CA1_RELATIVE "));
		CAValue=CAValue^SQL_CA1_RELATIVE;
		}
	if(CAValue&SQL_CA1_BOOKMARK){
		_tcscat(buf,_T("SQL_CA1_BOOKMARK "));
		CAValue=CAValue^SQL_CA1_BOOKMARK;
		}
	if(CAValue&SQL_CA1_LOCK_NO_CHANGE){
		_tcscat(buf,_T("SQL_CA1_LOCK_NO_CHANGE "));
		CAValue=CAValue^SQL_CA1_LOCK_NO_CHANGE;
		}
	if(CAValue&SQL_CA1_LOCK_EXCLUSIVE){
		_tcscat(buf,_T("SQL_CA1_LOCK_EXCLUSIVE "));
		CAValue=CAValue^SQL_CA1_LOCK_EXCLUSIVE;
		}
	if(CAValue&SQL_CA1_LOCK_UNLOCK){
		_tcscat(buf,_T("SQL_CA1_LOCK_UNLOCK "));
		CAValue=CAValue^SQL_CA1_LOCK_UNLOCK;
		}
	if(CAValue&SQL_CA1_POS_POSITION){
		_tcscat(buf,_T("SQL_CA1_POS_POSITION "));
		CAValue=CAValue^SQL_CA1_POS_POSITION;
		}
	if(CAValue&SQL_CA1_POS_UPDATE){
		_tcscat(buf,_T("SQL_CA1_POS_UPDATE "));
		CAValue=CAValue^SQL_CA1_POS_UPDATE;
		}
	if(CAValue&SQL_CA1_POS_DELETE){
		_tcscat(buf,_T("SQL_CA1_POS_DELETE "));
		CAValue=CAValue^SQL_CA1_POS_DELETE;
		}
	if(CAValue&SQL_CA1_POS_REFRESH){
		_tcscat(buf,_T("SQL_CA1_POS_REFRESH "));
		CAValue=CAValue^SQL_CA1_POS_REFRESH;
		}
	if(CAValue&SQL_CA1_POSITIONED_UPDATE){
		_tcscat(buf,_T("SQL_CA1_POSITIONED_UPDATE "));
		CAValue=CAValue^SQL_CA1_POSITIONED_UPDATE;
		}
	if(CAValue&SQL_CA1_POSITIONED_DELETE){
		_tcscat(buf,_T("SQL_CA1_POSITIONED_DELETE "));
		CAValue=CAValue^SQL_CA1_POSITIONED_DELETE;
		}
	if(CAValue&SQL_CA1_SELECT_FOR_UPDATE){
		_tcscat(buf,_T("SQL_CA1_SELECT_FOR_UPDATE "));
		CAValue=CAValue^SQL_CA1_SELECT_FOR_UPDATE;
		}
	if(CAValue&SQL_CA1_BULK_ADD){
		_tcscat(buf,_T("SQL_CA1_BULK_ADD "));
		CAValue=CAValue^SQL_CA1_BULK_ADD;
		}
	if(CAValue&SQL_CA1_BULK_UPDATE_BY_BOOKMARK){
		_tcscat(buf,_T("SQL_CA1_BULK_UPDATE_BY_BOOKMARK "));
		CAValue=CAValue^SQL_CA1_BULK_UPDATE_BY_BOOKMARK;
		}
	if(CAValue&SQL_CA1_BULK_DELETE_BY_BOOKMARK){
		_tcscat(buf,_T("SQL_CA1_BULK_DELETE_BY_BOOKMARK "));
		CAValue=CAValue^SQL_CA1_BULK_DELETE_BY_BOOKMARK;
		}
	if(CAValue&SQL_CA1_BULK_FETCH_BY_BOOKMARK){
		_tcscat(buf,_T("SQL_CA1_BULK_FETCH_BY_BOOKMARK "));
		CAValue=CAValue^SQL_CA1_BULK_FETCH_BY_BOOKMARK;
		}
	
	// Should be zero unless there are undefined bits
	if(CAValue){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),CAValue);
		_tcscat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** CA2ToString()
**
** This function will attempt to convert a Cursor Attribute bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *CA2ToString(long CAValue, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(CAValue&SQL_CA2_READ_ONLY_CONCURRENCY){
		_tcscat(buf,_T("SQL_CA2_READ_ONLY_CONCURRENCY "));
		CAValue=CAValue^SQL_CA2_READ_ONLY_CONCURRENCY;
		}
	if(CAValue&SQL_CA2_LOCK_CONCURRENCY){
		_tcscat(buf,_T("SQL_CA2_LOCK_CONCURRENCY "));
		CAValue=CAValue^SQL_CA2_LOCK_CONCURRENCY;
		}
	if(CAValue&SQL_CA2_OPT_ROWVER_CONCURRENCY){
		_tcscat(buf,_T("SQL_CA2_OPT_ROWVER_CONCURRENCY "));
		CAValue=CAValue^SQL_CA2_OPT_ROWVER_CONCURRENCY;
		}
	if(CAValue&SQL_CA2_OPT_VALUES_CONCURRENCY){
		_tcscat(buf,_T("SQL_CA2_OPT_VALUES_CONCURRENCY "));
		CAValue=CAValue^SQL_CA2_OPT_VALUES_CONCURRENCY;
		}
	if(CAValue&SQL_CA2_SENSITIVITY_ADDITIONS){
		_tcscat(buf,_T("SQL_CA2_SENSITIVITY_ADDITIONS "));
		CAValue=CAValue^SQL_CA2_SENSITIVITY_ADDITIONS;
		}
	if(CAValue&SQL_CA2_SENSITIVITY_DELETIONS){
		_tcscat(buf,_T("SQL_CA2_SENSITIVITY_DELETIONS "));
		CAValue=CAValue^SQL_CA2_SENSITIVITY_DELETIONS;
		}
	if(CAValue&SQL_CA2_SENSITIVITY_UPDATES){
		_tcscat(buf,_T("SQL_CA2_SENSITIVITY_UPDATES "));
		CAValue=CAValue^SQL_CA2_SENSITIVITY_UPDATES;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_SELECT){
		_tcscat(buf,_T("SQL_CA2_MAX_ROWS_SELECT "));
		CAValue=CAValue^SQL_CA2_MAX_ROWS_SELECT;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_INSERT){
		_tcscat(buf,_T("SQL_CA2_MAX_ROWS_INSERT "));
		CAValue=CAValue^SQL_CA2_MAX_ROWS_INSERT;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_DELETE){
		_tcscat(buf,_T("SQL_CA2_MAX_ROWS_DELETE "));
		CAValue=CAValue^SQL_CA2_MAX_ROWS_DELETE;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_UPDATE){
		_tcscat(buf,_T("SQL_CA2_MAX_ROWS_UPDATE "));
		CAValue=CAValue^SQL_CA2_MAX_ROWS_UPDATE;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_CATALOG){
		_tcscat(buf,_T("SQL_CA2_MAX_ROWS_CATALOG "));
		CAValue=CAValue^SQL_CA2_MAX_ROWS_CATALOG;
		}
	if(CAValue&SQL_CA2_MAX_ROWS_AFFECTS_ALL){
		_tcscat(buf,_T("SQL_CA2_MAX_ROWS_AFFECTS_ALL "));
		CAValue=CAValue^SQL_CA2_MAX_ROWS_AFFECTS_ALL;
		}
	if(CAValue&SQL_CA2_CRC_EXACT){
		_tcscat(buf,_T("SQL_CA2_CRC_EXACT "));
		CAValue=CAValue^SQL_CA2_CRC_EXACT;
		}
	if(CAValue&SQL_CA2_CRC_APPROXIMATE){
		_tcscat(buf,_T("SQL_CA2_CRC_APPROXIMATE "));
		CAValue=CAValue^SQL_CA2_CRC_APPROXIMATE;
		}
	if(CAValue&SQL_CA2_SIMULATE_NON_UNIQUE){
		_tcscat(buf,_T("SQL_CA2_SIMULATE_NON_UNIQUE "));
		CAValue=CAValue^SQL_CA2_SIMULATE_NON_UNIQUE;
		}
	if(CAValue&SQL_CA2_SIMULATE_TRY_UNIQUE){
		_tcscat(buf,_T("SQL_CA2_SIMULATE_TRY_UNIQUE "));
		CAValue=CAValue^SQL_CA2_SIMULATE_TRY_UNIQUE;
		}
	if(CAValue&SQL_CA2_SIMULATE_UNIQUE){
		_tcscat(buf,_T("SQL_CA2_SIMULATE_UNIQUE "));
		CAValue=CAValue^SQL_CA2_SIMULATE_UNIQUE;
		}
	
	// Should be zero unless there are undefined bits
	if(CAValue){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),CAValue);
		_tcscat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** ConvertValueToString()
**
** This function will attempt to convert a Convert Value bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *ConvertValueToString(long ConvertValue, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(ConvertValue&SQL_CVT_BIGINT){
		_tcscat(buf,_T("SQL_CVT_BIGINT "));
		ConvertValue=ConvertValue^SQL_CVT_BIGINT;
		}
	if(ConvertValue&SQL_CVT_BINARY){
		_tcscat(buf,_T("SQL_CVT_BINARY "));
		ConvertValue=ConvertValue^SQL_CVT_BINARY;
		}
	if(ConvertValue&SQL_CVT_BIT){
		_tcscat(buf,_T("SQL_CVT_BIT ")); 
		ConvertValue=ConvertValue^SQL_CVT_BIT;
		}
	if(ConvertValue&SQL_CVT_CHAR){
		_tcscat(buf,_T("SQL_CVT_CHAR ")); 
		ConvertValue=ConvertValue^SQL_CVT_CHAR;
		}
	if(ConvertValue&SQL_CVT_DATE){
		_tcscat(buf,_T("SQL_CVT_DATE "));
		ConvertValue=ConvertValue^SQL_CVT_DATE;
		}
	if(ConvertValue&SQL_CVT_DECIMAL){
		_tcscat(buf,_T("SQL_CVT_DECIMAL "));
		ConvertValue=ConvertValue^SQL_CVT_DECIMAL;
		}
	if(ConvertValue&SQL_CVT_DOUBLE){
		_tcscat(buf,_T("SQL_CVT_DOUBLE "));
		ConvertValue=ConvertValue^SQL_CVT_DOUBLE;
		}
	if(ConvertValue&SQL_CVT_FLOAT){
		_tcscat(buf,_T("SQL_CVT_FLOAT "));
		ConvertValue=ConvertValue^SQL_CVT_FLOAT;
		}
	if(ConvertValue&SQL_CVT_INTEGER){
		_tcscat(buf,_T("SQL_CVT_INTEGER "));
		ConvertValue=ConvertValue^SQL_CVT_INTEGER;
		}
	if(ConvertValue&SQL_CVT_INTERVAL_YEAR_MONTH){
		_tcscat(buf,_T("SQL_CVT_INTERVAL_YEAR_MONTH "));
		ConvertValue=ConvertValue^SQL_CVT_INTERVAL_YEAR_MONTH;
		}
	if(ConvertValue&SQL_CVT_INTERVAL_DAY_TIME){
		_tcscat(buf,_T("SQL_CVT_INTERVAL_DAY_TIME "));
		ConvertValue=ConvertValue^SQL_CVT_INTERVAL_DAY_TIME;
		}
	if(ConvertValue&SQL_CVT_LONGVARBINARY){
		_tcscat(buf,_T("SQL_CVT_LONGVARBINARY "));
		ConvertValue=ConvertValue^SQL_CVT_LONGVARBINARY;
		}
	if(ConvertValue&SQL_CVT_LONGVARCHAR){
		_tcscat(buf,_T("SQL_CVT_LONGVARCHAR "));
		ConvertValue=ConvertValue^SQL_CVT_LONGVARCHAR;
		}
	if(ConvertValue&SQL_CVT_NUMERIC){
		_tcscat(buf,_T("SQL_CVT_NUMERIC "));
		ConvertValue=ConvertValue^SQL_CVT_NUMERIC;
		}
	if(ConvertValue&SQL_CVT_REAL){
		_tcscat(buf,_T("SQL_CVT_REAL "));
		ConvertValue=ConvertValue^SQL_CVT_REAL;
		}
	if(ConvertValue&SQL_CVT_SMALLINT){
		_tcscat(buf,_T("SQL_CVT_SMALLINT "));
		ConvertValue=ConvertValue^SQL_CVT_SMALLINT;
		}
	if(ConvertValue&SQL_CVT_TIME){
		_tcscat(buf,_T("SQL_CVT_TIME "));
		ConvertValue=ConvertValue^SQL_CVT_TIME;
		}
	if(ConvertValue&SQL_CVT_TIMESTAMP){
		_tcscat(buf,_T("SQL_CVT_TIMESTAMP "));
		ConvertValue=ConvertValue^SQL_CVT_TIMESTAMP;
		}
	if(ConvertValue&SQL_CVT_TINYINT){
		_tcscat(buf,_T("SQL_CVT_TINYINT "));
		ConvertValue=ConvertValue^SQL_CVT_TINYINT;
		}
	if(ConvertValue&SQL_CVT_VARBINARY){
		_tcscat(buf,_T("SQL_CVT_VARBINARY "));
		ConvertValue=ConvertValue^SQL_CVT_VARBINARY;
		}
	if(ConvertValue&SQL_CVT_VARCHAR){
		_tcscat(buf,_T("SQL_CVT_VARCHAR "));
		ConvertValue=ConvertValue^SQL_CVT_VARCHAR;
		}
	if(ConvertValue&SQL_CVT_WCHAR){
		_tcscat(buf,_T("SQL_CVT_WCHAR "));
		ConvertValue=ConvertValue^SQL_CVT_WCHAR;
		}
	if(ConvertValue&SQL_CVT_WLONGVARCHAR){
		_tcscat(buf,_T("SQL_CVT_WLONGVARCHAR "));
		ConvertValue=ConvertValue^SQL_CVT_WLONGVARCHAR;
		}
	if(ConvertValue&SQL_CVT_WVARCHAR){
		_tcscat(buf,_T("SQL_CVT_WVARCHAR "));
		ConvertValue=ConvertValue^SQL_CVT_WVARCHAR;
		}

	// Should be zero unless there are undefined bits
	if(ConvertValue){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),ConvertValue);
		_tcscat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** CvtFunctionToString()
**
** This function will attempt to convert a Convert Function bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *CvtFunctionToString(long CvtFunction, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(CvtFunction&SQL_FN_CVT_CAST){
		_tcscat (buf,_T("SQL_FN_CVT_CAST "));
		CvtFunction=CvtFunction^SQL_FN_CVT_CAST;
		}
	if(CvtFunction&SQL_FN_CVT_CONVERT){
		_tcscat(buf,_T("SQL_FN_CVT_CONVERT "));
		CvtFunction=CvtFunction^SQL_FN_CVT_CONVERT;
		}

	// Should be zero unless there are undefined bits
	if(CvtFunction){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),CvtFunction);
		_tcscat(buf,TempBuf);
		}
	return buf;
}

/****************************************************************
** AggregateTableToString()
**
** This function will attempt to convert an Aggregate Funcions option bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *AggregateToString(long AggregateOption, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(AggregateOption&SQL_AF_AVG){
		_tcscat(buf,_T("SQL_AF_AVG "));
		AggregateOption=AggregateOption^SQL_AF_AVG;
		}
	if(AggregateOption&SQL_AF_COUNT){
		_tcscat(buf,_T("SQL_AF_COUNT "));
		AggregateOption=AggregateOption^SQL_AF_COUNT;
		}
	if(AggregateOption&SQL_AF_MAX){
		_tcscat(buf,_T("SQL_AF_MAX "));
		AggregateOption=AggregateOption^SQL_AF_MAX;
		}
	if(AggregateOption&SQL_AF_MIN){
		_tcscat(buf,_T("SQL_AF_MIN "));
		AggregateOption=AggregateOption^SQL_AF_MIN;
		}
	if(AggregateOption&SQL_AF_SUM){
		_tcscat(buf,_T("SQL_AF_SUM "));
		AggregateOption=AggregateOption^SQL_AF_SUM;
		}
	if(AggregateOption&SQL_AF_DISTINCT){
		_tcscat(buf,_T("SQL_AF_DISTINCT "));
		AggregateOption=AggregateOption^SQL_AF_DISTINCT;
		}
	if(AggregateOption&SQL_AF_ALL){
		_tcscat(buf,_T("SQL_AF_ALL "));
		AggregateOption=AggregateOption^SQL_AF_ALL;
		}

	// Should be zero unless there are undefined bits
	if(AggregateOption){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),AggregateOption);
		_tcscat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** AlterTableToString()
**
** This function will attempt to convert an Alter Table option bit-mask
** into a more user friendly character string representing all the bit flags.
****************************************************************/
TCHAR *AlterTableToString(long AlterOption, TCHAR *buf)
{
	TCHAR TempBuf[MAX_STRING_SIZE];

	buf[0]=NULL_STRING;
	if(AlterOption&SQL_AT_ADD_COLUMN){
		_tcscat(buf,_T("SQL_AT_ADD_COLUMN "));
		AlterOption=AlterOption^SQL_AT_ADD_COLUMN;
		}
	if(AlterOption&SQL_AT_DROP_COLUMN){
		_tcscat(buf,_T("SQL_AT_DROP_COLUMN "));
		AlterOption=AlterOption^SQL_AT_DROP_COLUMN;
		}
	if(AlterOption&SQL_AT_CONSTRAINT_NON_DEFERRABLE){
		_tcscat(buf,_T("SQL_AT_CONSTRAINT_NON_DEFERRABLE "));
		AlterOption=AlterOption^SQL_AT_CONSTRAINT_NON_DEFERRABLE;
		}
	if(AlterOption&SQL_AT_CONSTRAINT_DEFERRABLE){
		_tcscat(buf,_T("SQL_AT_CONSTRAINT_DEFERRABLE "));
		AlterOption=AlterOption^SQL_AT_CONSTRAINT_DEFERRABLE;
		}
	if(AlterOption&SQL_AT_CONSTRAINT_INITIALLY_IMMEDIATE){
		_tcscat(buf,_T("SQL_AT_CONSTRAINT_INITIALLY_IMMEDIATE "));
		AlterOption=AlterOption^SQL_AT_CONSTRAINT_INITIALLY_IMMEDIATE;
		}
	if(AlterOption&SQL_AT_CONSTRAINT_INITIALLY_DEFERRED){
		_tcscat(buf,_T("SQL_AT_CONSTRAINT_INITIALLY_DEFERRED "));
		AlterOption=AlterOption^SQL_AT_CONSTRAINT_INITIALLY_DEFERRED;
		}
	if(AlterOption&SQL_AT_CONSTRAINT_NAME_DEFINITION){
		_tcscat(buf,_T("SQL_AT_CONSTRAINT_NAME_DEFINITION "));
		AlterOption=AlterOption^SQL_AT_CONSTRAINT_NAME_DEFINITION;
		}
	if(AlterOption&SQL_AT_DROP_TABLE_CONSTRAINT_RESTRICT){
		_tcscat(buf,_T("SQL_AT_DROP_TABLE_CONSTRAINT_RESTRICT "));
		AlterOption=AlterOption^SQL_AT_DROP_TABLE_CONSTRAINT_RESTRICT;
		}
	if(AlterOption&SQL_AT_DROP_TABLE_CONSTRAINT_CASCADE){
		_tcscat(buf,_T("SQL_AT_DROP_TABLE_CONSTRAINT_CASCADE "));
		AlterOption=AlterOption^SQL_AT_DROP_TABLE_CONSTRAINT_CASCADE;
		}
	if(AlterOption&SQL_AT_ADD_TABLE_CONSTRAINT){
		_tcscat(buf,_T("SQL_AT_ADD_TABLE_CONSTRAINT "));
		AlterOption=AlterOption^SQL_AT_ADD_TABLE_CONSTRAINT;
		}
	if(AlterOption&SQL_AT_DROP_COLUMN_RESTRICT){
		_tcscat(buf,_T("SQL_AT_DROP_COLUMN_RESTRICT "));
		AlterOption=AlterOption^SQL_AT_DROP_COLUMN_RESTRICT;
		}
	if(AlterOption&SQL_AT_DROP_COLUMN_CASCADE){
		_tcscat(buf,_T("SQL_AT_DROP_COLUMN_CASCADE "));
		AlterOption=AlterOption^SQL_AT_DROP_COLUMN_CASCADE;
		}
	if(AlterOption&SQL_AT_DROP_COLUMN_DEFAULT){
		_tcscat(buf,_T("SQL_AT_DROP_COLUMN_DEFAULT "));
		AlterOption=AlterOption^SQL_AT_DROP_COLUMN_DEFAULT;
		}
	if(AlterOption&SQL_AT_SET_COLUMN_DEFAULT){
		_tcscat(buf,_T("SQL_AT_SET_COLUMN_DEFAULT "));
		AlterOption=AlterOption^SQL_AT_SET_COLUMN_DEFAULT;
		}
	if(AlterOption&SQL_AT_ADD_COLUMN_COLLATION){
		_tcscat(buf,_T("SQL_AT_ADD_COLUMN_COLLATION "));
		AlterOption=AlterOption^SQL_AT_ADD_COLUMN_COLLATION;
		}
	if(AlterOption&SQL_AT_ADD_COLUMN_DEFAULT){
		_tcscat(buf,_T("SQL_AT_ADD_COLUMN_DEFAULT "));
		AlterOption=AlterOption^SQL_AT_ADD_COLUMN_DEFAULT;
		}
	if(AlterOption&SQL_AT_ADD_COLUMN_SINGLE){
		_tcscat(buf,_T("SQL_AT_ADD_COLUMN_SINGLE "));
		AlterOption=AlterOption^SQL_AT_ADD_COLUMN_SINGLE;
		}
	if(AlterOption&SQL_AT_ADD_CONSTRAINT){
		_tcscat(buf,_T("SQL_AT_ADD_CONSTRAINT "));
		AlterOption=AlterOption^SQL_AT_ADD_CONSTRAINT;
		}

	// Should be zero unless there are undefined bits
	if(AlterOption){
		_stprintf(TempBuf,_T("<UndefinedBits:0x%08lX>"),AlterOption);
		_tcscat(buf,TempBuf);
		}

	return buf;
}

/****************************************************************
** CorrelationToString()
**
** This function will attempt to convert a Correlation Name value
** into a more user friendly character string.
** If the concat null behavior value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *CorrelationToString(SWORD Correl, TCHAR *buf)
{
   switch (Correl) {
		case SQL_CN_NONE:			_tcscpy (buf,_T("SQL_CN_NONE"));break;
		case SQL_CN_DIFFERENT:	_tcscpy (buf,_T("SQL_CN_DIFFERENT"));break;
		case SQL_CN_ANY:			_tcscpy (buf,_T("SQL_CN_ANY"));break;
      default:
         _itot(Correl,buf,10);
		}
	return buf;
}

/****************************************************************
** CursorBehaviorToString()
**
** This function will attempt to convert a Cursor Behavior value
** into a more user friendly character string.
** If the concat null behavior value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *CursorBehaviorToString(SWORD CursorB, TCHAR *buf)
{
   switch (CursorB) {
		case SQL_CB_DELETE:		_tcscpy (buf,_T("SQL_CB_DELETE"));break;
		case SQL_CB_CLOSE:		_tcscpy (buf,_T("SQL_CB_CLOSE"));break;
		case SQL_CB_PRESERVE:	_tcscpy (buf,_T("SQL_CB_PRESERVE"));break;
      default:
         _itot(CursorB,buf,10);
		}
	return buf;
}

/****************************************************************
** TxnIsolationToString()
**
** This function will attempt to convert a Transaction Isolation
** value into a more user friendly character string.
** If the value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *TxnIsolationToString(SDWORD TxnIsolation, TCHAR *buf)
{
   switch (TxnIsolation) {
		case SQL_TXN_READ_UNCOMMITTED:	_tcscpy (buf,_T("SQL_TXN_READ_UNCOMMITTED"));break;
		case SQL_TXN_READ_COMMITTED:		_tcscpy (buf,_T("SQL_TXN_READ_COMMITTED"));break;
		case SQL_TXN_REPEATABLE_READ:		_tcscpy (buf,_T("SQL_TXN_REPEATABLE_READ"));break;
		case SQL_TXN_SERIALIZABLE:			_tcscpy (buf,_T("SQL_TXN_SERIALIZABLE"));break;
      default:
         _itot(TxnIsolation,buf,10);
		}
	return buf;
}

/****************************************************************
** FileUsageToString()
**
** This function will attempt to convert a File Usage
** value into a more user friendly character string.
** If the value isn't one of the standard values then this
** function converts it into a numeric string.
****************************************************************/
TCHAR *FileUsageToString(SDWORD FileUsage, TCHAR *buf)
{
   switch (FileUsage) {
		case SQL_FILE_NOT_SUPPORTED:	_tcscpy (buf,_T("SQL_FILE_NOT_SUPPORTED"));break;
		case SQL_FILE_TABLE:			_tcscpy (buf,_T("SQL_FILE_TABLE"));break;
		case SQL_FILE_CATALOG:			_tcscpy (buf,_T("SQL_FILE_CATALOG"));break;
        default:						_itot(FileUsage,buf,10);
		}
	return buf;
}
              
/**************************************************************
** CheckReturnCode()
**
** This function is used to compare an actual return code from
** an ODBC function to an expected value.  It will log a message
** if the expected return code was not correct. It should never 
** be called directly.  It should always be invoked through the
** CHECKRC macro found in "common.h".
***************************************************************/
TrueFalse CheckReturnCode(
   RETCODE expected,
   RETCODE actual,
   TCHAR *FunctionName,
   TCHAR *SourceFile,
   short LineNum)
{
	TCHAR exp[30];
	TCHAR act[30];
    // this is a fix for freestatement since SQL returns SQL_SUCCESS_WITH_INFO for more than one stmt while closing.
	if ((actual == SQL_SUCCESS_WITH_INFO) && (expected == SQL_SUCCESS))
			actual = SQL_SUCCESS;
    // end change.

   if(expected==actual) return(TRUE);
   LogMsg(NONE,_T(""));
   LogMsg(ERRMSG+SHORTTIMESTAMP,_T("%s: Expected: %s Actual: %s\n"),
		FunctionName,ReturncodeToChar(expected,exp),ReturncodeToChar(actual,act));
   LogMsg(NONE,_T("   File: %s   Line: %d\n"),SourceFile,LineNum);
   return(FALSE);
}

TrueFalse DriverConnectNoPrompt(TestInfo *pTestInfo)
{
   RETCODE returncode;
   TCHAR ConnectStringOut[MAX_CONNECT_STRING];
   short Conn_tcslengthOut;
   TCHAR ConnectStringIn[MAX_CONNECT_STRING];
   TCHAR *pString;
   TCHAR *pTempString;
   TCHAR TempString[MAX_CONNECT_STRING];
   SQLHANDLE henv;
   SQLHANDLE hdbc;
   int InStringLen;

   // Initialize the basic handles needed by ODBC 
   returncode = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle")) return(FALSE);

   returncode = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER) SQL_OV_ODBC3, 0);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetEnvAttr"))
   {
	   // Cleanup. No need to check return codes since we are already failing
	   SQLFreeHandle(SQL_HANDLE_ENV, henv);
	   return (FALSE);
   }

   returncode = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
   {
	   // Cleanup.  No need to check return codes since we are already failing
	   SQLFreeHandle(SQL_HANDLE_ENV, henv);
	   return(FALSE);
   }
   
   _tcscpy(ConnectStringIn,_T(""));
   _stprintf(ConnectStringIn, _T("DSN=%s;UID=%s;PWD=%s;"),pTestInfo->DataSource,pTestInfo->UserID,pTestInfo->Password);
   
   
   InStringLen=_tcslen(ConnectStringIn);
//#endif
   returncode = SQLDriverConnect(hdbc,NULL,(SQLTCHAR*)ConnectStringIn, InStringLen,
                                 (SQLTCHAR*)ConnectStringOut,sizeof(ConnectStringOut),&Conn_tcslengthOut,
                                 SQL_DRIVER_NOPROMPT);
   /*
   returncode = SQLConnect(hdbc,pTestInfo->DataSource,_tcslen(pTestInfo->DataSource)*2,
		   pTestInfo->UserID,_tcslen(pTestInfo->UserID)*2,
		   pTestInfo->Password,_tcslen(pTestInfo->Password)*2);
		   */
   // changed this since some ODBC drivers return SQL_SUCCESS_WITH_INFO like SQLSERVER
   if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))
   {
	   LogAllErrors(henv,hdbc,(SQLHANDLE)NULL);
	   LogMsg(LINEAFTER,_T("\n   The InConnectionString is: =\"%s\"\n"),ConnectStringIn);
	   LogMsg(LINEAFTER,_T("\n   Returned ConnectString=\"%s\"\n"),ConnectStringOut);
	   
	   // Cleanup.  No need to check return codes since we are already failing
	   SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
	   SQLFreeHandle(SQL_HANDLE_ENV, henv);
	   return(FALSE);
   }                               
      
   // Strip out DSN from connection string. 
   pString = _tcsstr(ConnectStringOut,_T("DSN="));
   if (pString != NULL)
   {
	   pString += 4;           // skip past 'DSN='
	   pTempString = TempString;
	   while((*pString != ';') && (*pString != (TCHAR)NULL)) 
	   {
		   *pTempString = *pString;
		   pTempString++;
		   pString++;
	   }
	   *pTempString = (TCHAR)NULL;
	   _tcscpy(pTestInfo->DataSource,TempString);
   }
   else
	   _tcscpy(pTestInfo->DataSource,_T(""));
   
   // Strip out SERVER from connection string.
   pString = _tcsstr(ConnectStringOut,_T("SERVER="));
   if (pString != NULL)
   {
	   pString += 7;           // skip past 'SERVER='
	   pTempString = TempString;
	   while((*pString != '/') && (*pString != (TCHAR)NULL))
	   {
		   *pTempString = *pString;
		   pTempString++;
		   pString++;
	   }
	   *pTempString = (TCHAR)NULL;
	   _tcscpy(pTestInfo->Server,TempString);
   }
   else
	   _tcscpy(pTestInfo->Server,_T(""));

  // Strip out /PortNumber from connection string.
  pString = _tcsstr(ConnectStringOut,_T("/"));
  if (pString != NULL)
  {
      pString += 1;           // skip past '/'
      pTempString = TempString;
      while ((*pString != ';') && (*pString != (TCHAR)NULL)){
		  *pTempString = *pString;
		  pTempString++;
		  pString++;
	  }         
      *pTempString = (TCHAR)NULL;
      _tcscpy(pTestInfo->Port,TempString);
  }
  else 
	  _tcscpy(pTestInfo->Port,_T(""));

   
   // Strip out UID from connection string.
   pString = _tcsstr(ConnectStringOut,_T("UID="));
   if (pString != NULL)
   {
	   pString += 4;           // skip past 'UID='
	   pTempString = TempString;
	   while((*pString != ';') && (*pString != (TCHAR)NULL))
	   {
		   *pTempString = *pString;
		   pTempString++;
		   pString++;
	   }
	   *pTempString = (TCHAR)NULL;
	   _tcscpy(pTestInfo->UserID,TempString);
   }
   else
	   _tcscpy(pTestInfo->UserID,_T(""));
   
   // Strip out PWD from connection string.
   pString = _tcsstr(ConnectStringOut,_T("PWD="));
   if (pString != NULL)
   {
	   pString += 4;           // skip past 'PWD='
	   pTempString = TempString;
	   while((*pString != ';') && (*pString != (TCHAR)NULL))
	   {
		   *pTempString = *pString;
		   pTempString++;
		   pString++;
	   }
	   *pTempString = (TCHAR)NULL;
	   _tcscpy((TCHAR *)pTestInfo->Password,TempString);
   }
   else
	   _tcscpy((TCHAR *)pTestInfo->Password,_T(""));
   
   // Strip out DBQ from connection string.
   pString = _tcsstr(ConnectStringOut,_T("DBQ="));
   if (pString != NULL)
   {
	   pString += 4;           // skip past 'DBQ='
	   pTempString = TempString;
	   while ((*pString != ';') && (*pString != (TCHAR)NULL))
	  {
		  *pTempString = *pString;
		  pTempString++;
		  pString++;
	  }
	  *pTempString = (TCHAR)NULL;
	  _tcscpy((TCHAR *)pTestInfo->Database,TempString);
  }
  else
	  _tcscpy((TCHAR *)pTestInfo->Database,_T("MASTER"));

  // Strip out CATALOG from connection string.
  pString = _tcsstr(ConnectStringOut,_T("CATALOG="));
  if (pString != NULL)
  {
	  pString += 8;           // skip past 'CATALOG=' 
	  pTempString = TempString;
	   while((*pString != ';') && (*pString != (TCHAR)NULL))
	  {
		  *pTempString = *pString;
		  pTempString++;
		  pString++;
	  }
	  *pTempString = (TCHAR)NULL;
	   _tcscpy((TCHAR *)pTestInfo->Catalog,TempString);
  }
  else
	  _tcscpy((TCHAR *)pTestInfo->Catalog,_T("TRAFODION"));

  // Strip out SCHEMA from connection string.
  pString = _tcsstr(ConnectStringOut,_T("SCHEMA="));
  if (pString != NULL)
  {
	  pString += 7;           // skip past 'SCHEMA=' 
	  pTempString = TempString;
	  while((*pString != ';') && (*pString != (TCHAR)NULL))
	  {
		  *pTempString = *pString;
		  pTempString++;
		  pString++;
	  }
	  *pTempString = (TCHAR)NULL;
	  /* Now check to see if there is catalog in the name */
	  pString = _tcsstr(TempString, _T("."));
	  if (pString != NULL)
	  {
		  pString++; // skip catalog and ".".  Only take the schema part.
		  _tcscpy (TempString, pString);
	  }

	   _tcscpy((TCHAR *)pTestInfo->Schema,TempString);
  }
  //else
  //	   _tcscpy((TCHAR *)pTestInfo->Schema,pTestInfo->Schema);

  // send the current handles to the caller 
  pTestInfo->henv = henv;
  pTestInfo->hdbc = hdbc;
  
  return(TRUE);
}

/**************************************************************
** FullConnect()
** 
** This function will attempt to establish a full connection
** based upon the information within the structure passed in to it.
***************************************************************/                         
TrueFalse FullConnect(TestInfo *pTestInfo)
{
   RETCODE returncode;
   SQLHANDLE henv;
   SQLHANDLE hdbc;
   SQLUINTEGER onoff = 1;
   
   /* Initialize the basic handles needed by ODBC */
   returncode = SQLAllocEnv(&henv);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")) return(FALSE);

   returncode = SQLAllocConnect(henv,&hdbc);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
	   /* Cleanup.  No need to check return codes since we are already failing */
	   DisplaySqlErr(henv, SQL_HANDLE_ENV);
	   
	   SQLFreeEnv(henv);
	   return(FALSE);
   }

   /* 6-5-00:
      Need to turn Autocommit off since SQL/MX will close all open cursors that are
      open if the end of ANY of the cursors is reached. */
   /*returncode = SQLSetConnectOption(hdbc, SQL_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
	   // Cleanup.  No need to check return codes since we are already failing
	   SQLFreeEnv(henv);
	   return(FALSE);
   }*/

   //Turn fetch ahead feature 'ON'
   /*
   returncode = SQLSetConnectAttr(hdbc, SQL_ATTR_FETCHAHEAD, (SQLPOINTER)onoff, SQL_IS_POINTER);
   if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
	   // Cleanup.  No need to check return codes since we are already failing
	   SQLFreeEnv(henv);
	   return(FALSE);
   }
   */

   returncode = SQLConnect(hdbc,
                           (SQLTCHAR*)pTestInfo->DataSource,(SWORD)_tcslen(pTestInfo->DataSource),
                           (SQLTCHAR*)pTestInfo->UserID,(SWORD)_tcslen(pTestInfo->UserID),
                           (SQLTCHAR*)pTestInfo->Password,(SWORD)_tcslen(pTestInfo->Password)
                           );
   
   if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))
   {
	   /* Cleanup.  No need to check return codes since we are already failing */
	   //DisplaySqlErr(hdbc, SQL_HANDLE_DBC);
	   
	   SQLFreeConnect(hdbc);
	   SQLFreeEnv(henv);
	   return(FALSE);
   }
   
   pTestInfo->henv = (SQLHANDLE)henv;
   pTestInfo->hdbc = (SQLHANDLE)hdbc;
   
   /* Connection established */
   return(TRUE);
}  /* FullConnect() */
   
/**************************************************************
** FullConnectWithOptions()
** 
** This function will attempt to establish a full connection
** based upon the information within the structure passed in to it.
***************************************************************/                         
TrueFalse FullConnectWithOptions(TestInfo *pTestInfo, int Options)
{
	RETCODE returncode;
	SQLHANDLE henv;
	SQLHANDLE hdbc;

	assert( (Options&CONNECT_ODBC_VERSION_2) || (Options&CONNECT_ODBC_VERSION_3) );

	/* Initialize the basic handles needed by ODBC */
	if (Options&CONNECT_ODBC_VERSION_2)
	{
		returncode = SQLAllocEnv(&henv);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")) return(FALSE);
		
		returncode = SQLAllocConnect(henv,&hdbc);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
			/* Cleanup.  No need to check return codes since we are already failing */
			SQLFreeEnv(henv);
			return(FALSE);
		}
	}
	if (Options&CONNECT_ODBC_VERSION_3)
	{
		returncode = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle")) return(FALSE);

		returncode = SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER) SQL_OV_ODBC3, 0);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLSetEnvAttr"))
		{
			/* Cleanup. No need to check return codes since we are already failing */
			SQLFreeHandle(SQL_HANDLE_ENV, henv);
			return (FALSE);
		}

		returncode = SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle")){
			/* Cleanup. No need to check return codes since we are already failing */
			SQLFreeHandle(SQL_HANDLE_ENV, henv);
			return(FALSE);
		}
	}

	// Handle Autocommit_Off Option
	if (Options&CONNECT_AUTOCOMMIT_OFF)
	{
		returncode = SQLSetConnectOption(hdbc, SQL_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
			// Cleanup.  No need to check return codes since we are already failing
			SQLFreeEnv(henv);
			return(FALSE);
		}
	}

	returncode = SQLConnect(hdbc,
                           (SQLTCHAR*)pTestInfo->DataSource,(SWORD)_tcslen(pTestInfo->DataSource),
                           (SQLTCHAR*)pTestInfo->UserID,(SWORD)_tcslen(pTestInfo->UserID),
                           (SQLTCHAR*)pTestInfo->Password,(SWORD)_tcslen(pTestInfo->Password)
                           );

	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))
	{
		// Free up handles since we hit a problem.
		if (Options&CONNECT_ODBC_VERSION_2)
		{
			/* Cleanup.  No need to check return codes since we are already failing */
			SQLFreeConnect(hdbc);
			SQLFreeEnv(henv);
			return(FALSE);
		}
		if (Options&CONNECT_ODBC_VERSION_3)
		{
			/* Cleanup.  No need to check return codes since we are already failing */		   
			SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
			SQLFreeHandle(SQL_HANDLE_ENV, henv);
		}
	}
	
	pTestInfo->henv = (SQLHANDLE)henv;
	pTestInfo->hdbc = (SQLHANDLE)hdbc;
	
	/* Connection established */
	return(TRUE);
}  /* FullConnectWithOptions() */

TrueFalse FullDisconnectVer(TestInfo *pTestInfo, int iODBCVer)
{
	if (iODBCVer == SQL_OV_ODBC3)	// ODBC version 3.x
		return FullDisconnect3(pTestInfo);
	else // default for V2 and below (e.g. SQL_OV_ODBC2)
		return FullDisconnect(pTestInfo);
}

/**************************************************************
** FullDisconnect()
**
** This function disconnects a single connection based upon the
** information passed in to it.  If this function returns FALSE
** it does not always mean the disconnect did not happen.  For
** FALSE, the disconnect might have happened and there might have
** been some other error. For ODBC version 2.x and below.
***************************************************************/                         
TrueFalse FullDisconnect(TestInfo *pTestInfo)
{
  RETCODE returncode;                        
  TrueFalse Result;
  
  Result=TRUE;
   
  /* Disconnect from the data source.  If errors, still go on and */
  /* try to free the handles */
  returncode = SQLDisconnect((SQLHANDLE)pTestInfo->hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDisconnect")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}
   
  /* Free up all handles used by this connection */
  returncode = SQLFreeConnect((SQLHANDLE)pTestInfo->hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeConnect")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}

   
  returncode = SQLFreeEnv((SQLHANDLE)pTestInfo->henv);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeEnv")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}
   
  return(Result);
}  /* FullDisconnect() */

/**************************************************************
** FullDisconnect3()
**
** This function disconnects a single connection based upon the
** information passed in to it.  If this function returns FALSE
** it does not always mean the disconnect did not happen.  For
** FALSE, the disconnect might have happened and there might have
** been some other error. For ODBC version 3.x.
***************************************************************/                         
TrueFalse FullDisconnect3(TestInfo *pTestInfo)
{
  RETCODE returncode;                        
  TrueFalse Result;
  
  Result=TRUE;
   
  /* Disconnect from the data source.  If errors, still go on and */
  /* try to free the handles */
  returncode = SQLDisconnect((SQLHANDLE)pTestInfo->hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLDisconnect")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}
   
  /* Free up all handles used by this connection */
  returncode = SQLFreeHandle(SQL_HANDLE_DBC, (SQLHANDLE)pTestInfo->hdbc);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeHandle")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}

  returncode = SQLFreeHandle(SQL_HANDLE_ENV, (SQLHANDLE)pTestInfo->henv);
  if(!CHECKRC(SQL_SUCCESS,returncode,"SQLFreeEnv")) {
		Result=FALSE;	
		LogAllErrors(pTestInfo->henv,pTestInfo->hdbc,pTestInfo->hstmt);
	}
   
  return(Result);
}  /* FullDisconnect3() */

/**************************************************************
** LogAllErrors()
**                          
** This function loops through calls to SQLError() building strings
** for all error messages that might be there and writes them out
** the the log file.
***************************************************************/                         
void LogAllErrors(SQLHANDLE henv,
                  SQLHANDLE hdbc,
                  SQLHANDLE hstmt)
{             
    TCHAR	buf[MAX_STRING_SIZE];
    TCHAR	State[STATE_SIZE];
	SDWORD	NativeError;
    RETCODE returncode;
	BOOL MsgDisplayed;

	MsgDisplayed=FALSE;

   /* Log any henv error messages */
   returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
      LogPrintf(_T("   State: %s\n   Native Error: %ld\n   Error: %s\n"),State,NativeError,buf);
		MsgDisplayed=TRUE;
      returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
   }

   /* Log any hdbc error messages */
   returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)hdbc, (SQLHANDLE)NULL, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
        LogPrintf(_T("   State: %s\n   Native Error: %ld\n   Error: %s\n"),State,NativeError,buf);
		MsgDisplayed=TRUE;
      returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)hdbc, (SQLHANDLE)NULL, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
   }

   /* Log any hstmt error messages */
   returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLHANDLE)hstmt, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
        LogPrintf(_T("   State: %s\n   Native Error: %ld\n   Error: %s\n"),State,NativeError,buf);
		MsgDisplayed=TRUE;
      returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLHANDLE)hstmt, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
   }

   /* if no error messages were displayed then display a message */
   if(!MsgDisplayed)
		LogMsg(NONE,_T("There were no error messages for SQLError() to display\n"));
}                     

/**************************************************************
** LogAllErrorsver3()
**                          
** This function loops through calls to SQLError() building strings
** for all error messages that might be there and writes them out
** the the log file.
***************************************************************/        

void LogAllErrorsVer3(SQLHANDLE henv,
                  SQLHANDLE hdbc,
                  SQLHANDLE hstmt)
{             
  SQLTCHAR		buf[MAX_STRING_SIZE];
  SQLTCHAR		State[STATE_SIZE];
  SQLINTEGER	NativeError;
  RETCODE returncode;
  BOOL MsgDisplayed;
  SQLSMALLINT	ErrorMsglen;
  SQLSMALLINT i =1;

  MsgDisplayed=FALSE;
   /* Log any henv error messages */
   returncode = SQLGetDiagRec(SQL_HANDLE_ENV, (SQLHANDLE)henv,i, State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, &ErrorMsglen);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
      LogPrintf(_T("   State: %s\n   Native Error: %ld\n   Error: %s\n"),State,NativeError,buf);
    	MsgDisplayed=TRUE;
		i++;
		returncode = SQLGetDiagRec(SQL_HANDLE_ENV, (SQLHANDLE)henv,i, State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, &ErrorMsglen);
      }

   /* Log any hdbc error messages */
   i =1;
   returncode = SQLGetDiagRec(SQL_HANDLE_DBC, (SQLHANDLE)hdbc,i, State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, &ErrorMsglen);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
      LogPrintf(_T("   State: %s\n   Native Error: %ld\n   Error: %s\n"),State,NativeError,buf);
		MsgDisplayed=TRUE;
		i++;
	   returncode = SQLGetDiagRec(SQL_HANDLE_DBC, (SQLHANDLE)hdbc,i, State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, &ErrorMsglen);
      }

   /* Log any hstmt error messages */
   i =1;
   returncode = SQLGetDiagRec(SQL_HANDLE_STMT,(SQLHANDLE)hstmt,i, State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, &ErrorMsglen);
   while((returncode == SQL_SUCCESS) ||
         (returncode == SQL_SUCCESS_WITH_INFO)){
		State[STATE_SIZE-1]=NULL_STRING;
	    LogPrintf(_T("   State: %s\n   Native Error: %ld\n   Error: %s\n"),State,NativeError,buf);
		MsgDisplayed=TRUE;
		i++;
	  returncode = SQLGetDiagRec(SQL_HANDLE_STMT, (SQLHANDLE)hstmt,i, State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, &ErrorMsglen);
      }

   /* if no error messages were displayed then display a message */
	if(!MsgDisplayed){
		LogMsg(NONE,_T("There were no error messages for SQLError() to display\n"));
		}
	
}

/**************************************************************
 ** DisplaySqlErr()
 **                                         
 ** This function will loop through all possible errors that within
 ** the passed in handle of specified handle type, and display the 
 ** errors on the stantard output (screen by default). This is only 
 ** used for debug purpose, not recommended in regular test cases.
 ***************************************************************/                         
void DisplaySqlErr(SQLHANDLE hdl, SQLSMALLINT HdlType)
{
	SQLRETURN rc;
	SQLINTEGER NativeErr;
	SQLSMALLINT iRec;
	SQLSMALLINT msgLen;

	TCHAR buf[MAX_STRING_SIZE];
	TCHAR SqlState[SQL_SQLSTATE_SIZE];

	iRec=1;
	rc=SQLGetDiagRec(HdlType, hdl, iRec, (SQLTCHAR*)SqlState, &NativeErr, (SQLTCHAR*)buf, MAX_STRING_SIZE, &msgLen);
	while(rc==SQL_SUCCESS || rc==SQL_SUCCESS_WITH_INFO)
	{
		_tprintf(_T("State:      %S\r\nNative Error:  %ld\r\nError:     %S\r\n"), SqlState, NativeErr, buf);
		iRec++;
		rc=SQLGetDiagRec(HdlType, hdl, iRec, (SQLTCHAR*)SqlState, &NativeErr, (SQLTCHAR*)buf, MAX_STRING_SIZE, &msgLen);
	}
}

/**************************************************************
 ** FindError()
 **                                         
 ** This function will loop through all possible errors that might
 ** have occurred looking to see if the one specified in <FindState>
 ** occurred or not. 
 ***************************************************************/                         
TrueFalse FindError(TCHAR *FindMsg, SQLHANDLE henv, SQLHANDLE hdbc, SQLHANDLE hstmt)
{                 
	TCHAR			buf[MAX_STRING_SIZE];
	RETCODE		returncode;
	TCHAR			State[STATE_SIZE];
	SDWORD		NativeError;
	TrueFalse found;
	BOOL			MsgDisplayed;

	found = FALSE;
	MsgDisplayed=FALSE;

  // Log any henv error messages 
  returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
  while(((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO)) && !found)
	{
		State[STATE_SIZE-1]=NULL_STRING;
		// scan henv, hdbc, and hstmt for errors of the specified state 
		MsgDisplayed=TRUE;
		if (_tcsstr(FindMsg,State) != NULL)
		{
			found = TRUE;
		}
		else
		{
			found = FALSE;
			LogPrintf(_T("   State: %s\nNativeError: %ld\n%s\n"),State,NativeError,buf);
		}
		returncode = SQLError((SQLHANDLE)henv, (SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
	}

   /* Log any hdbc error messages */
  returncode = SQLError((SQLHANDLE)NULL,(SQLHANDLE)hdbc, (SQLHANDLE)NULL, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
  while(((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO)) && !found)
	{
		State[STATE_SIZE-1]=NULL_STRING;
		MsgDisplayed=TRUE;
		// scan henv, hdbc, and hstmt for errors of the specified state 
		if (_tcsstr(FindMsg,State) != NULL)
		{
			found = TRUE;
		}
		else
		{
			found = FALSE;
			LogPrintf(_T("   State: %s\nNativeError: %ld\n%s\n"),State,NativeError,buf);
		}
		returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)hdbc, (SQLHANDLE)NULL, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
	}

   /* Log any hstmt error messages */
	returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLHANDLE)hstmt, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
  while(((returncode == SQL_SUCCESS) || (returncode == SQL_SUCCESS_WITH_INFO)) && !found)
	{
		State[STATE_SIZE-1]=NULL_STRING;
		MsgDisplayed=TRUE;
		// scan henv, hdbc, and hstmt for errors of the specified state 
		if (_tcsstr(FindMsg,State) != NULL)
		{
			found = TRUE;
		}
		else
		{
			found = FALSE;
			LogPrintf(_T("   State: %s\nNativeError: %ld\n%s\n"),State,NativeError,buf);
		}
		returncode = SQLError((SQLHANDLE)NULL, (SQLHANDLE)NULL, (SQLHANDLE)hstmt, (SQLTCHAR*)State, &NativeError, (SQLTCHAR*)buf, MAX_STRING_SIZE, NULL);
	}

   /* if no error messages were displayed then display a message */
	if(!MsgDisplayed)
	{
		LogMsg(ENDLINE,_T("There were no error messages for SQLError() to display\n"));
	}
	return (found);
}       
              
/**************************************************************
** GetDataAll()
** fetches all the data returned from a statement
** and places it at address buf up to cbBuf characters
** 
** Number of 
** bytes of data available is placed in cbAvail.  
** NOTE: the return value will be true even if the buffer was 
** not large enough for all the data, so 'pRetCode' must be 
** examined to determine if the SQL_SUCCESS_WITH_INFO was 
** received and more data remains to be fetched.
****************************************************************/

TrueFalse GetDataAll( TestInfo* ti, void *buffer, SQLULEN cbBuf, 
			SQLULEN* pcbAvail, RETCODE *pRetCode, SQLULEN cbMaxCol)
{
	SWORD		iNumCols,	/* number of columns in table */
				iCol;	    /*	column index into table   */
	SQLULEN		cbColName;	/* actual number of bytes in column name*/
	SDWORD		iNumChars;	/* number of characters returned */
	SQLULEN		cbWritten = 0L;
	TCHAR		outStr[MAX_ROW_LEN];
    TCHAR		tempStr[MAX_STRING_SIZE];
	ColumnInfo* Cols;
	SQLULEN		i;
    TCHAR*		buf;
	
	TFILE *fp = (TFILE*)NULL;  /* NULL to write to buf instead */
	
	if (! cbBuf )
	    fp = (TFILE*) buffer;	
    else
		buf = (TCHAR*)buffer;

	*pcbAvail = 0;
	/* get number of columns in result */
	*pRetCode = SQLNumResultCols( (SQLHANDLE)ti->hstmt, &iNumCols );
	
	/* allocate storage for ColumnInfo structures */
	if ( (void *)NULL == 
		 (Cols = (ColumnInfo *)malloc( iNumCols*sizeof( ColumnInfo ) ) ) )
	{
		_stprintf( tempStr,
			_T("GetDataAll:Could not allocate memory for %d columns"), iNumCols );
		LogMsg( ERRMSG, tempStr);
		return FALSE;
	}

	for (iCol = 0; iCol < iNumCols; iCol++ )
	{
		*pRetCode = SQLDescribeCol( (SQLHANDLE)ti->hstmt, 
			(UWORD)(iCol+1), Cols[iCol].Name,MAX_COLUMN_NAME, 
			(SWORD FAR*)&cbColName, &(Cols[iCol].SqlType),
			&(Cols[iCol].Prec),
			&(Cols[iCol].Scale), &(Cols[iCol].Nullable ));
	}

	/* now build string for header */
	_tcscpy( outStr,_T("") );
	for (iCol = 0; iCol < iNumCols; iCol++ )
	{
		_stprintf( tempStr,_T("%s"), Cols[iCol].Name );
	
		if (_tcslen( tempStr ) + _tcslen( outStr ) <
					MAX_ROW_LEN )
		{
			if (iCol)
				_tcscat( outStr, _T(",") );
			_tcscat( outStr, tempStr );
		}   
		else
		{
			LogMsg( ERRMSG, _T("Row too long") );
			free (Cols);
			return FALSE;
		}
	}
	/* write Header string to file or buffer */
	
	if (fp)
		_fputts( outStr, fp );
	else
	{
		_stprintf( buf, _T("%s\n\n"), outStr );
	}
	
	cbWritten += _tcslen(outStr);
	cbWritten++;	/*allow for newline TCHAR */

	/* build string for divider line */
	for (i = 0; i < cbWritten-1; i++)
		outStr[i] = '-';

	/* write divider line to file or buffer */
	if (fp)
	{
		_fputts( outStr, fp );
		_fputts( _T("\n"), fp );
	}
	else
	{
		_stprintf( buf+cbWritten, _T("%s\n"), outStr );
	}
	cbWritten += cbWritten;
	/* new line character already allotted for in cbWritten value */
	/* while there are more rows fetch data   */
	/* fetch all SQL data types as SQL_C_TCHAR */
	while ( SQLFetch((SQLHANDLE) ti->hstmt ) != SQL_NO_DATA_FOUND )
	{
	  _tcscpy(outStr, _T("")); /* new row */
	  /* build a row column by column */
	  for ( iCol = 0; iCol < iNumCols; iCol++ )
	  {
		    /* get data for column */
		  	*pRetCode = SQLGetData((SQLHANDLE) ti->hstmt, (UWORD)(iCol+1), 
				SQL_C_TCHAR, tempStr, 
				MAX_STRING_SIZE-1, (SQLLEN*)&iNumChars ); // sushil
			/* check for NULL data case */
			if  (iNumChars == SQL_NULL_DATA)
			{
				_tcscpy( tempStr, _T("<NULL>"));
			}
			else if (( SQL_SUCCESS != *pRetCode ) && 
					 (SQL_SUCCESS_WITH_INFO != *pRetCode ) )
			{
				_stprintf( tempStr, _T("GetDataAll:Col%d %s"),
					iCol+1, Cols[iCol].Name );
				LogMsg( ERRMSG, tempStr);					
				free (Cols);
				return FALSE;
			}
          /* write column data to outStr if sufficient buffer space */
		  if( (!fp) && 
			  ( cbWritten + _tcslen(tempStr) > (SQLULEN)cbBuf ))
		  { /* out of buffer space */  
	 		cbBuf   =  0;
			*pcbAvail += (_tcslen(tempStr)+1);
		  } 
		  else
		  { 
			/* sufficient buffer space */
			if (iCol)
			{	
				_tcscat( outStr, _T(",") );
				_tcscat( outStr, tempStr );
			}
			else
				_tcscpy( outStr, tempStr);   
		  } /* end else (sufficient buffer space) */
		}	/* end "for iCol", row completed */

		/* write row to file or buffer */
		if (fp)
		{
			/* write to file */
			_fputts( outStr, fp );
			cbWritten += _tcslen(outStr);
			cbWritten++;
		}
		else	/* write to buffer, space permitting */
			if (cbBuf) 
			{
			    /* space left */
				_stprintf( buf+cbWritten, _T("%s\n\n"), outStr );
				cbWritten += _tcslen(outStr);
				cbWritten++;
			}
			else
			{
				/* no space left */
	
			}
	 }  /* end while SQLFetch not returning SQL_NO_DATA_FOUND */

*pcbAvail += cbWritten;/* add bytes written to total available */
/* cleanup */
free( Cols );

SQLFreeStmt((SQLHANDLE) ti->hstmt, SQL_CLOSE );
return TRUE;
}

/*************************************************
**   LogDataAll()
**   Performs GetDataAll and writes results to log
**   pointed to by hlog.  If hlog is -1, then writes
**   to main log file
****************************************************/
#define BUF_SIZE 10000
TrueFalse LogDataAll( TestInfo *ti, HLOGT hlog )
{	
	TCHAR		*buf;
	TrueFalse	rslt;
	SQLULEN		cbAvail;
	RETCODE		retcode;

	    /* try GetDataAll with a buffer of BUF_SIZE */
	    if( !(buf = (TCHAR *)malloc( BUF_SIZE*sizeof(TCHAR) )))
		{
			LogMsg( ERRMSG, _T("LogDataAll:Memory Allocation error"));
			return FALSE;
		}
		rslt = GetDataAll( ti, buf, BUF_SIZE, 
					&cbAvail, &retcode, MAX_COLUMN_NAME );

		if (!rslt)
		{
			LogMsg( ERRMSG, _T("GetDataAll returned FALSE") );
			return FALSE;
		}
		if ( cbAvail > BUF_SIZE )
		{	
			/* need to allocate larger buffer */
			free(buf);
			if (!(buf = (TCHAR *)malloc( cbAvail*sizeof(TCHAR) )))
			{
				LogMsg( ERRMSG, _T("Memory Allocation error") );
				return FALSE;
			}
			rslt = GetDataAll( ti, buf, BUF_SIZE, 
					&cbAvail, &retcode, MAX_COLUMN_NAME );
			if (!rslt)
			{
				LogMsg( ERRMSG, _T("GetDataAll returned FALSE") );
				return FALSE;
			}
		}	/*end if cbAvail > BUF_SIZE */
//			if ( hlog == (HLOGT)(-1) )
			/* print to main log */
			LogPrintf( _T("%s"), buf );
//		else
//		{
//			AuxLogPrintf( hlog, "%s", buf );
//		}

	return TRUE;
}

SQLTCHAR *StmtQueries(long QueryType, TCHAR *name, TCHAR *buf )
{

	switch (QueryType) 
	{
		case CREATE_TABLE:						_stprintf(buf,_T("create table %s (c1 char(10),c2 varchar(10),c3 decimal(10,5),c4 numeric(10,5),c5 smallint,c6 integer,c7 real,c8 float,c9 double precision,c10 date,c11 time,c12 timestamp,c13 bigint) NO PARTITION"),name);break;
		case DROP_TABLE:							_stprintf(buf,_T("drop table %s"),name);break;
		case INSERT_TABLE:						_stprintf(buf,_T("insert into %s values ('0123456789','0123456789',1234.56789,1234.56789,1200,12000,123.45E2,123.45E3,123.45E4,{d '1993-07-01'},{t '09:45:30'},{ts '1993-08-02 08:44:31.001'},120000)"),name);break;
		case INSERT_TABLE_WITH_PARAM:	_stprintf(buf,_T("insert into %s values (?,?,?,?,?,?,?,?,?,?,?,?,?)"),name);break;
		case SELECT_TABLE:						_stprintf(buf,_T("select c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13 from %s"),name);break;
		default:
			_stprintf(buf,_T("invalid QueryType %s"),name);
	}

	return (SQLTCHAR*)buf;
}

TCHAR *CreateTableForConversion(int SQLDataType, TCHAR *TableName, TCHAR *cprec, TCHAR *vcprec, TCHAR *lvcprec,TCHAR *decprec, TCHAR *numprec, TCHAR *buf )
{
	switch (SQLDataType)
	{
		case MX_DT_ALL:
			_stprintf(buf,_T("create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar,c4 decimal(%s),c5 numeric(%s),c6 smallint,c7 integer,c8 bigint,c9 real,c10 float,c11 double precision,c12 date,c13 time,c14 timestamp) NO PARTITION"),TableName,cprec,vcprec,decprec,numprec);
			break;
		case MP_DT_ALL:
			_stprintf(buf,_T("create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar(%s),c4 decimal(%s),c5 numeric(%s),c6 bit,c7 tinyint,c8 smallint,c9 integer,c10 bigint,c11 real,c12 float,c13 double precision,c14 date,c15 time,c16 timestamp,c17 binary(%s),c18 varbinary(%s),c19 long varbinary(%s)) NO PARTITION"),TableName,cprec,vcprec,lvcprec,decprec,numprec,cprec,vcprec,lvcprec);
			break;
		case MX_DT_EXCEPT_DATETIME:
			_stprintf(buf,_T("create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar,c4 decimal(%s),c5 numeric(%s),c6 smallint,c6 integer,c7 bigint,c8 real,c9 float,c10 double precision) NO PARTITION"),TableName,cprec,vcprec,decprec,numprec);
			break;
		case MP_DT_EXCEPT_DATETIME:
			_stprintf(buf,_T("create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar(%s),c4 decimal(%s),c5 numeric(%s),c6 bit,c7 tinyint,c8 smallint,c9 integer,c10 bigint,c11 real,c12 float,c13 double precision,c14 binary(%s),c15 varbinary(%s),c16 long varbinary(%s)) NO PARTITION"),TableName,cprec,vcprec,lvcprec,decprec,numprec,cprec,vcprec,lvcprec);
			break;
		case MX_DT_DATE:
			_stprintf(buf,_T("create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar,c4 date,c5 timestamp) NO PARTITION"),TableName,cprec,vcprec);
			break;
		case MX_DT_TIME:
			_stprintf(buf,_T("create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar,c4 time,c6 timestamp) NO PARTITION"),TableName,cprec,vcprec);
			break;
		case MX_DT_TIMESTAMP:
			_stprintf(buf,_T("create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar,c4 date,c5 time,c6 timestamp) NO PARTITION"),TableName,cprec,vcprec);
			break;
		case MP_DT_DATE:
			_stprintf(buf,_T("create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar(%s),c4 date,c5 timestamp) NO PARTITION"),TableName,cprec,vcprec,lvcprec);
			break;
		case MP_DT_TIME:
			_stprintf(buf,_T("create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar(%s),c4 time,c6 timestamp) NO PARTITION"),TableName,cprec,vcprec,lvcprec);
			break;
		case MP_DT_TIMESTAMP:
			_stprintf(buf,_T("create table %s (c1 char(%s),c2 varchar(%s),c3 long varchar(%s),c4 date,c5 time,c6 timestamp) NO PARTITION"),TableName,cprec,vcprec,lvcprec);
			break;
		default:
			_stprintf(buf,_T("invalid QueryType"));
			break;
	}

	return buf;
}

TCHAR *PerformanceQueries(long QueryType, TCHAR *name, TCHAR *buf )
{

	switch (QueryType) 
	{
		case CREATE_TABLE:						_stprintf(buf,_T("create table %s (c1 char(10),c2 varchar(10),c3 decimal(10,5),c4 numeric(10,5),c5 smallint,c6 integer,c7 real,c8 float,c9 double precision) NO PARTITION"),name);break;
		case DROP_TABLE:							_stprintf(buf,_T("drop table %s"),name);break;
		case INSERT_TABLE:						_stprintf(buf,_T("insert into %s values ('0123456789','0123456789',1234.56789,1234.56789,1200,12000,123.45E2,123.45E3,123.45E4)"),name);break;
		case INSERT_TABLE_WITH_PARAM:	_stprintf(buf,_T("insert into %s values (?,?,?,?,?,?,?,?,?)"),name);break;
		case SELECT_TABLE:						_stprintf(buf,_T("select c1,c2,c3,c4,c5,c6,c7,c8,c9 from %s"),name);break;
		default:
			_stprintf(buf,_T("invalid QueryType %s"),name);
	}

	return buf;
}

void LogResults(void)
{
	LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,_T("Total Tests=%d  Failed=%d\n"),_gTestCount - _gTestIndvCount,_gTestFailedCount - _gTestFailedIndvCount);
	_gTestIndvCount = _gTestCount;
	_gTestFailedIndvCount = _gTestFailedCount;
}

void LogResultsTest(TCHAR *ProcName)
{
// SEAQUEST	LogMsg(LINEBEFORE+LINEAFTER+SHORTTIMESTAMP,_T("\t%s \t--> \tTotal Tests=\t%d  \tFailed=\t%d\n"),ProcName, _gTestCount - _gTestIndvCount,_gTestFailedCount - _gTestFailedIndvCount);
	LogMsg(LINEBEFORE+LINEAFTER,_T("%-35s TEST RESULT: %s Cases=%d Failed=%d\n"), ProcName, ((_gTestFailedCount - _gTestFailedIndvCount) ? _T("FAIL") : _T("PASS")), _gTestCount - _gTestIndvCount, _gTestFailedCount - _gTestFailedIndvCount);
	_gTestIndvCount = _gTestCount;
	_gTestFailedIndvCount = _gTestFailedCount;
}

TCHAR *ReturnColumnDefinition(TCHAR *InsStr, short ColNum)
{
	//TCHAR	colseps[]   = _T(",");
	TCHAR	*colseps   = _T(",");
	TCHAR	*coltoken;

	TCHAR   TmpCrtCol[4050];
	//UChar	TmpCrtCol[4050] = (UChar*)((UChar*)(L" ")+1); 
	//TCHAR    TmpCrtCol[4050] = _T(" ");

	_tcscpy(TmpCrtCol, InsStr);

	ColumnDefinition[0] = '\0';
	if (ColNum == 0)
	{
		if (_tcsstr(_tcsupr(TmpCrtCol),_T("CREATE")) != NULL)
			_tcscpy(column_string,_tcschr(TmpCrtCol,'('));
		else
			_tcscpy(column_string,TmpCrtCol);
		coltoken = _tcstok(column_string, colseps);
	}
	else
	{
		coltoken = _tcstok(NULL, colseps);
	}

	if(coltoken != NULL)
	{
		if ((_tcsstr(_tcsupr(coltoken),_T("NUMERIC")) != NULL) || (_tcsstr(_tcsupr(coltoken),_T("DECIMAL")) != NULL))
		{
			_tcscpy(ColumnDefinition,coltoken);
			_tcscat(ColumnDefinition,_T(","));
			coltoken = _tcstok(NULL, colseps);
			if(coltoken != NULL)
				_tcscat(ColumnDefinition,coltoken);
		}
		else
			_tcscpy(ColumnDefinition,coltoken);
	}
	else
	{
		_tcscpy(ColumnDefinition,_T("INVALID COLUMN DEFINITION"));
	}
	return (ColumnDefinition);

}

void LogInfo(TestInfo *pTestInfo)
{
 	RETCODE				returncode;
 	SQLHANDLE 			henv;
 	SQLHANDLE 			hdbc;
 	SQLHANDLE			hstmt;
	TCHAR szData[500];
	SQLLEN cbData;
	TCHAR	*ShowCntl = _T("SHOWCONTROL ALL");

	//Log DSN Info
	LogMsg(NONE, _T("Data Source : %s\n"), pTestInfo->DataSource);
	LogMsg(NONE, _T("Server : %s\n"), pTestInfo->Server);
	LogMsg(NONE, _T("Port : %s\n"), pTestInfo->Port);
	LogMsg(NONE, _T("UserID : %s\n"), pTestInfo->UserID);
	LogMsg(NONE, _T("Database : %s\n"), pTestInfo->Database);
	LogMsg(NONE, _T("Catalog : %s\n"), pTestInfo->Catalog);
	LogMsg(NONE, _T("Schema : %s\n"), pTestInfo->Schema);

	//Log SHOWCONTROL ALL OUTPUT
	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*) ShowCntl, SQL_NTS);
	if (returncode != SQL_ERROR)
	{
		while (returncode != SQL_NO_DATA_FOUND)
  		{
   			returncode = SQLFetch(hstmt);
   			if (returncode != SQL_NO_DATA_FOUND) {
       			if ( returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO )
   				{
					memset(szData, '\0', 500*sizeof(TCHAR));
    				returncode=SQLGetData(hstmt, 1, SQL_C_TCHAR, szData, 200, &cbData);
    				LogMsg(NONE, _T("%s\n"), szData);
   				} 
				else
   				{
      				LogMsg(NONE, _T("An unexpected error occurred when calling SQLFetch() in common.c. \n") );
      				LogMsg(NONE, _T("Log SHOWCONTROL ALL error. Expected SQL_SUCCESS, returned %d\n"), returncode);
					LogAllErrors(henv,hdbc,hstmt);
					break;
   				}
			}
  		}
	}
	returncode=SQLFreeStmt(hstmt,SQL_CLOSE);
	isUCS2 = specialMode(hstmt, _T("ISO_MAPPING"), _T("UTF8"));
}


/*There functions are added for Character Sets testing
Added by HP
*/

int next_line(TCHAR *lineOut, TFILE *scriptFD) {
	int p = 0, c = 0;
	TCHAR buff[5120];
	_tcscpy(lineOut,_T(""));
	while (_fgetts (buff , 5120 , scriptFD) != NULL) {
		//trim
		p = _tcslen(buff)-1;
		while (buff[p] == ' ' || buff[p] == '\n' || buff[p] == '\r' || buff[p] == '\t') p--;
		buff[p+1] = '\0';

		p = 0;
		while (buff[p] == ' ' || buff[p] == '\n'  || buff[p] == '\r' || buff[p] == '\t') p++;
		if (buff[p] == '\0') continue;
		if (buff[p] == '-' && buff[p+1] == '-') continue;

		//copy to buffer
		c = 0;
		do {
			lineOut[c++] = buff[p];
		}
		while (buff[p++] != '\0');

		return TRUE;
	}
	return FALSE;
}

var_list_t* load_api_vars(TCHAR *api, TCHAR *textFile) {
	TCHAR		line[5120];
	TFILE		*scriptFD;
	var_list_t *my_var_list = NULL;
	int i, p, num_vars = 0;
	int found = FALSE;
	TCHAR strAPI[256];
	TCHAR *seps   = _T("\"");
	TCHAR *token;

	if ((scriptFD = _tfopen(textFile, _T("r"))) == NULL) {
		_tprintf(_T("Error open script file %s\n"), textFile);
		return NULL;
	}

	//Find the API block in text file
	_stprintf(strAPI, _T("[%s "), api);
	while (next_line(line, scriptFD)) {
		if (_tcsnicmp(strAPI, line, _tcslen(strAPI)) == 0) {
			num_vars = _tstoi(line + _tcslen(strAPI));
			found = TRUE;
			break;
		}
	}
	if (!found) {
		_tfclose(scriptFD);
		_tprintf(_T("Could not find API name %s in the text file %s!\n"), api, textFile);
		return NULL;
	}

	if (!found || num_vars == 0) {
		_tfclose(scriptFD);
		_tprintf(_T("Can not find API %s. Or number of variables is %d\n"), api, num_vars);
		return NULL;
	}

	//Allocate mem for variables
	my_var_list = (var_list_t*)malloc(num_vars*sizeof(var_list_t));
	if (my_var_list == NULL) {
		_tfclose(scriptFD);
		_tprintf(_T("Malloc memory error!\n"));
		return NULL;
	}

	//Scan each vars and load to memory
	_stprintf(strAPI, _T("[END]"));
	i = 0; found = FALSE;
	while (next_line(line, scriptFD)) {
		if (_tcsnicmp(strAPI, line, _tcslen(strAPI)) == 0) {
			found = TRUE;
			break;
		}
		if (i>=num_vars) {
			i++;
			break;
		}

		token = _tcstok(_tcsdup(line), seps);
		my_var_list[i].value = _tcsdup(line + _tcslen(token) + 1);
		p = _tcslen(my_var_list[i].value)-1;
		if (my_var_list[i].value[p] == '"') {
			my_var_list[i].value[p] = '\0';
		}
		else {
			_tfclose(scriptFD);
			_tprintf(_T("File format error! Variable string must be ended by a double quote. :::%c:::\n"), my_var_list[i].value[p]);
			_tprintf(_T("File name: %s\nAPI block: %s\nVariable ID: %s\n"), textFile, api, token);
			return NULL;
		}
		
		p = _tcslen(token)-1;
		while (token[p] == ' ' || token[p] == '\t') p--;
		token[p+1] = '\0';
		my_var_list[i].var_name = _tcsdup(token);

		if (i == (num_vars-1)) my_var_list[i].last = TRUE;
		else my_var_list[i].last = FALSE;

		i++;
	}

	if(i != num_vars) {
		_tfclose(scriptFD);
		_tprintf(_T("The number specified for API %s doesn't match with number of variables declared!\n"), api);
		return NULL;
	}
	if (!found) {
		_tfclose(scriptFD);
		_tprintf(_T("The variable block of API %s is not teminated by a marker [END].\n OR the text file %s is in wrong format!\n"), api, textFile);
		return NULL;
	}

	_tfclose(scriptFD);
	return my_var_list;
}

void print_list (var_list_t *var_list) {
	int i=0;
	if (var_list == NULL) return;
	do {
		_tprintf(_T("Name: :%s:\n"), var_list[i].var_name);
		_tprintf(_T("Value: :%s:\n"), var_list[i].value);
		_tprintf(_T("Last: %i\n"), var_list[i].last);
	} while(!var_list[i++].last);
	_tprintf(_T("=============================================\n"));
}

void free_list (var_list_t *var_list) {
	int i=0;
	if (var_list == NULL) return;
	do {
		free(var_list[i].var_name);
		free(var_list[i].value);
	} while(!var_list[i++].last);

	free(var_list);
}

TCHAR* var_mapping(TCHAR *var_name, var_list_t *var_list) {
	int i=0;
	if (var_list == NULL) return NULL;
	do {
		if(_tcsicmp(var_name, var_list[i].var_name) == 0) {
			return var_list[i].value;
		}
	} while(!var_list[i++].last);
	_tprintf(_T("Mapping error: Can not find variable name %s\n"), var_name);
	return NULL;
}

/*
 *  Charset adaptive _tcscmp and _tcsicmp for COAST
 */
int cwcscmp(TCHAR* str1, TCHAR* str2, BOOL ignoreCase) {
	int ret = -1;
	if(isCharSet == TRUE) {
	    if((_tcsstr(str1,str2) != NULL && _tcslen(str1) == (_tcslen(str2)+2)) || 
			(_tcsstr(str2,str1) != NULL && _tcslen(str2) == (_tcslen(str1)+2)) ||
			_tcscmp(str1,str2) == 0) 
			ret = 0;
	} else {
		if(ignoreCase == TRUE) 
			ret = _tcsicmp(str1, str2);
		else                   
			ret = _tcscmp (str1, str2);
	}
	return ret;
}

/*
 *  Charset adaptive _tcsncmp and _tcsnicmp for COAST
 */
int cstrncmp(TCHAR* expect, TCHAR* actual, BOOL ignoreCase, int size) {
	int ret = -1;
	TCHAR act[300];
	TCHAR exp[300];
	if((isCharSet==TRUE) && (_tcslen(actual) != _tcslen(expect))) {
		_tcsncpy(act, actual, size-2);
		act[size-2]='\0';
		_tcsncpy(exp, expect+1,size-2); 
		exp[size-2]='\0';
		ret = _tcscmp(exp,act);
	} else {
		if(ignoreCase == TRUE)
			ret = _tcsnicmp(expect, actual, size);
		else
			ret = _tcsncmp (expect, actual, size);
	}
	return ret;
}

TCHAR* printSymbol(TCHAR* input, TCHAR* output) {
	TCHAR temp[2048];
	int i = 0, j = 0, len = 0;
	if(input != NULL) {
		output = removeQuotes(input,output);
		len = _tcslen(output);
		if(len > 0) {
			while(j<len) {
				if(output[j]!='%')
					temp[i++] = output[j++];
				else {
					temp[i++] = output[j];
					temp[i++] = output[j++];
				}
			}
			temp[i] = '\0';
			_tcscpy (output,temp);
        } else if (len == 0 ) {
			_stprintf(output, _T("<empty>"));
		} else {
			_tcscpy (output,input);
        }
        return output;
    } else {
	    return NULL;
    }
}

TCHAR* removeQuotes(TCHAR* in, TCHAR* output) {
	TCHAR temp[2048];
	int len = 0;
	if(in != NULL) {
		len = _tcslen(in);
		if(isCharSet && (in[0]=='"') && (in[len-1]=='"') && (len > 1)) {
			_tcsncpy(temp,in+1,len-2);
			temp[len-2] = '\0';
            _tcscpy(output, temp);
		} else {
			_tcscpy(output,in);
		}
        return output;
    } else {
	    return NULL;
    }
}

BOOL specialMode(SQLHANDLE hstmt, TCHAR* cqd, TCHAR* mode) {
    SQLRETURN ret;
    SQLTCHAR data[256];
    SQLLEN dataPtr = SQL_NTS;
	TCHAR temp[1024];

    ret = SQLExecDirect(hstmt, (SQLTCHAR*)_T("CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'ON'"), SQL_NTS);
	_stprintf(temp, _T("SHOWCONTROL DEFAULT %s, MATCH FULL, NO HEADER"), cqd);
    ret = SQLExecDirect(hstmt, (SQLTCHAR*)temp, SQL_NTS);
    ret = SQLBindCol(hstmt, 1, SQL_C_TCHAR, (SQLPOINTER) data, 256, &dataPtr); 
    ret = SQLFetch(hstmt);
    if (ret == SQL_SUCCESS || ret == SQL_SUCCESS_WITH_INFO) {
        if(_tcscmp((const char*)data, (const char*)mode) == 0) {
			ret = SQLFreeStmt(hstmt, SQL_CLOSE);
            ret = SQLExecDirect(hstmt, (SQLTCHAR*)_T("CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF'"), SQL_NTS);
			return TRUE;
		}
    }
    ret = SQLFreeStmt(hstmt, SQL_CLOSE);
    ret = SQLExecDirect(hstmt, (SQLTCHAR*)_T("CONTROL QUERY DEFAULT SHOWCONTROL_UNEXTERNALIZED_ATTRS 'OFF'"), SQL_NTS);
    return FALSE;
}

/*Type: 1: Convert to UTF-8, truncate to lenght "len" in byte, then convert back mbs
		2: Convert to UCS2, truncate to lenght "len" in byte, then convert back mbs
*/
int mbs_truncate(TCHAR* in_mbsstr, TCHAR* out_mbsstr, int len, int type) {
	int requiredSize = 0, size = 0, i,j;
	unsigned char uft8str[1024];//This buffer is just for debugging
	wchar_t *pwc;

#ifndef UNICODE
	requiredSize = mbstowcs(NULL, in_mbsstr, 0); // C4996
    //pwc = (wchar_t *)malloc( (requiredSize + 1) * sizeof( wchar_t ));
    pwc = new wchar_t[requiredSize + 1];
    if (! pwc) {
		_tprintf(_T("Memory allocation failure, at line: %d\n"), __LINE__);
        return -1;
    }
    size = mbstowcs( pwc, in_mbsstr, requiredSize + 1); // C4996
    if (size == -1) {
		_tprintf(_T("Couldn't convert string--invalid multibyte character, at line: %d\n"), __LINE__);
	 	free(pwc);
		return -1;
    }
#else
    //pwc = (wchar_t *)malloc( (_tcslen(in_mbsstr) + 1) * sizeof( wchar_t ));
    pwc = new wchar_t[_tcslen(in_mbsstr) + 1];
    if (! pwc) {
		_tprintf(_T("Memory allocation failure, at line: %d\n"), __LINE__);
        return -1;
    }
	_tcscpy(pwc, in_mbsstr);
	requiredSize = _tcslen(pwc);
#endif

	switch (type) {
		case 1:
			j = 0;
			for(i=0;i<requiredSize;i++){
				if(pwc[i] < 0x80){
					uft8str[j++] = pwc[i];
				}
				else if(pwc[i] < 0x0800) {
					uft8str[j++] = pwc[i]>> 6 | 0xC0;
					uft8str[j++] = pwc[i] & 0x3F | 0x80;
				}
				else if(pwc[i] < 0x10000) {
					uft8str[j++] = pwc[i]>> 12 | 0xE0;
					uft8str[j++] = pwc[i]>> 6 & 0x3F | 0x80;
					uft8str[j++] = pwc[i] & 0x3F | 0x80;
				}
				else {
					uft8str[j++] = pwc[i]>> 18 | 0xF0;
					uft8str[j++] = pwc[i]>> 12 & 0x3F | 0x80;
					uft8str[j++] = pwc[i]>> 6 & 0x3F | 0x80;
					uft8str[j++] = pwc[i] & 0x3F | 0x80;
				}
				if (j>len) break;
			}
			uft8str[j] = '\0';
			pwc[i] = '\0';
			break;
		case 2:
#ifdef UNICODE
			pwc[(int)(len/sizeof(wchar_t))] = '\0';
#else
			pwc[(int)(len*2/sizeof(wchar_t))] = '\0';
#endif
			break;
		default:
			printf("Internal error, at line %d\n", __LINE__);
			break;
	}

#ifndef UNICODE
	requiredSize = wcstombs( NULL, pwc, 0);
	size = wcstombs(out_mbsstr, pwc, requiredSize+1);
	if (size == -1)
	{
		printf("Couldn't convert string, at line %d\n", __LINE__);
	}
#else
	_tcscpy(out_mbsstr, pwc);
	size = _tcslen(out_mbsstr)*sizeof(TCHAR);
#endif

//	free(pwc);
	delete[] pwc;

	return size;
}
