/************************************************************************
** sqlutil.c
**
** This source module contains a collection of routines which determine the
** record format of an SQL table and dynamically allocate the structures
** describing the record format.
**
************************************************************************/

/******************
** include files **
******************/
#include "include.h"
#include "defines.h"
#include "ODBCcommon.h"
#include "table.h"
#include "struct.h"
#include "commonglobals.h"
#include "sqlutil.h"
#include "rtnstat.h"


/**************************************************************
** FindError()
**
** This function will loop through all possible errors that might
** have occurred looking to see if the one specified in <FindState>
** occurred or not.
***************************************************************/
Boolean FindError(char *FindMsg,
                    HENV henv,
                    HDBC hdbc,
                    HSTMT hstmt)
{
   char buf[MAX_STRING_SIZE];
   RETCODE returncode;
   char State[STATE_SIZE];
	SQLINTEGER NatErr;
   Boolean found;

   found = FALSE;

   /* scan henv, hdbc, and hstmt for errors of the specified state */
   returncode = SQLError(henv, hdbc, hstmt, State, &NatErr, buf, MAX_STRING_SIZE, NULL);
   while(!found &&
         ((returncode == SQL_SUCCESS) ||
          (returncode == SQL_SUCCESS_WITH_INFO))){
		found = (strcmp(buf, FindMsg) == 0);
		returncode = SQLError(henv, hdbc, hstmt, State, &NatErr, buf, MAX_STRING_SIZE, NULL);
//      if(strstr(FindMsg,buf) != NULL){
//			found = TRUE;
//			returncode = SQLError(henv, hdbc, hstmt, State, &NatErr, buf, MAX_STRING_SIZE, NULL);
//			}
      }

	return(found);
}


/*************************************************************************
** AllocateValueBuffer()
**
** This function takes a given ODBC SQL data type and allocates
** the data buffer of appropriate length to hold its value.
**
** Returns: SUCCESS or FAILURE
*************************************************************************/
short AllocateValueBuffer(ColumnInfo *pColumn)
{
   long memory_required;       /* buffer size to be allocate */

   switch(pColumn->DataType){

      /* for character and binary data types add one to length to allow */
      /* for a NULL terminator */
      case SQL_LONGVARCHAR:
      case SQL_BINARY:
      case SQL_VARBINARY:
      case SQL_LONGVARBINARY:
      case SQL_CHAR:
      case SQL_VARCHAR:
         memory_required=pColumn->DataTypeLen+1;
         break;

      /*  All other data types */
      default:
         memory_required=pColumn->DataTypeLen;
         break;
      } /* end of switch */

   /* allocate memory for the column data value */
	if(memory_required<sizeof(long)) memory_required=sizeof(long);
   pColumn->Value.pChar=(char *)malloc(memory_required);
   if(pColumn->Value.pChar==NULL) return(FAILURE);
strcpy(pColumn->Value.pChar,"AABB");
   return(SUCCESS);
   }

/********************************************************************
** Function: ScanTableColumns()
**
** This function will scan the given TableInfo structure looking for
** a column of the specified data type and return its column number.
** The scan begins with <start_column>.
********************************************************************/
short ScanTableColumns(TableInfo *pTable,
                       short ODBCDataType,
                       short start_column)
{
   short i;
   ColumnInfo *pTemp;

   pTemp=pTable->ColPtr;
	pTemp+=start_column;
   for(i=start_column;i<pTable->NumOfCol;i++){
      if(pTemp->DataType==ODBCDataType) return(i);
      pTemp++;
      }
   return(-1);
   }

/********************************************************************
** Function: ScanTableColumnsForNondatetime()
**
** This function will scan the given TableInfo structure looking for
** any column othe than a date, time, or timestamp and returns its column
** number.  The scan begins with <start_column>.
********************************************************************/
short ScanTableColumnsForNondatetime(TableInfo *pTable,short start_column)
{
   short i;
   ColumnInfo *pTemp;

   pTemp=pTable->ColPtr;
	pTemp+=start_column;
   for(i=start_column;i<pTable->NumOfCol;i++){
      if((pTemp->DataType!=SQL_DATE) &&
         (pTemp->DataType!=SQL_TIME) &&
         (pTemp->DataType!=SQL_TIMESTAMP)){
         return(i);
         }
      pTemp++;
      }

   return(-1);
   }

/********************************************************************
** Function: ScanTableColumnsForNumber()
**
** This function will scan the given TableInfo structure looking for
** any column of a number data type and return its column number.
** The scan begins with <start_column>.
********************************************************************/
short ScanTableColumnsForNumber(TableInfo *pTable,short start_column)
{
   short i;
   ColumnInfo *pTemp;

   pTemp=pTable->ColPtr;
	pTemp+=start_column;
   for(i=start_column;i<pTable->NumOfCol;i++){
      switch(pTemp->DataType){
         case SQL_BIGINT:
         case SQL_TINYINT:
//         case SQL_NUMERIC:
         case SQL_INTEGER:
         case SQL_SMALLINT:
         case SQL_FLOAT:
         case SQL_REAL:
         case SQL_DOUBLE:
            return(i);
         } /* end switch */
		pTemp++;
      } /* end for loop */

   return(-1);
   }


/*************************************************************************
** GetColumnInfo()
**
** This function returns all the detail information about a column by
** doing repetative calls to SQLColAttributes().
*************************************************************************/
ColumnInfo *GetColumnInfo(HSTMT hstmt,
                           short ColumnPosition,
                           ColumnInfo *pColumn,
                           ReturnStatus **RSPtr)
{
   RETCODE returncode;
   SQLLEN TempInt;
   char TempBuffer[4096];
   short ActualSize;

   /* get all the various column attributes and package it into our */
   /* column structure */

   /* Auto Increment */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_AUTO_INCREMENT,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=FALSE;
      }
   pColumn->AutoIncrement=(short)TempInt;

   /* Case Sensitive */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_CASE_SENSITIVE,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=FALSE;
      }
   pColumn->CaseSensitive=(short)TempInt;

   /* Display Size */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_DISPLAY_SIZE,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=FALSE;
      }
   pColumn->DisplaySize=TempInt;

   /* Label */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_LABEL,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   TempBuffer[ActualSize]=NULL;
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempBuffer[0]=NULL;
      }

   strcpy(pColumn->CHeading,TempBuffer);

   /* Length */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_LENGTH,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=0;
      }
   pColumn->DataTypeLen=TempInt;

   /* Money */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_MONEY,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=FALSE;
      }
   pColumn->Money=(short)TempInt;

   /* name */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_NAME,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   TempBuffer[ActualSize]=NULL;
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempBuffer[0]=NULL;
      }
   strcpy(pColumn->CName,TempBuffer);

   /* Nullable */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_NULLABLE,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=SQL_NULLABLE_UNKNOWN;
      }
   pColumn->Nullable=(short)TempInt;

   /* Precision */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_PRECISION,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=0;
      }
   pColumn->DataTypePrecision=(short)TempInt;

   /* Scale */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_SCALE,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=0;
      }
   pColumn->DataTypeScale=(short)TempInt;

   /* Searchable */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_SEARCHABLE,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=FALSE;
      }
   pColumn->Searchable=(short)TempInt;

   /* Type */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_TYPE,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=0;
      }
   pColumn->DataType=FindODBCType((short)TempInt);
	pColumn->pTypeInfo=FindSQLTypeInfo(pColumn->DataType);

   /* Type Name */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_TYPE_NAME,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   TempBuffer[ActualSize]=NULL;
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempBuffer[0]=NULL;
      }
   strcpy(pColumn->pTypeInfo->TypeName,TempBuffer);

   /* Unsigned */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_UNSIGNED,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=FALSE;
      }
   pColumn->UnsignedColumn=(short)TempInt;

   /* Updatable */
   returncode=SQLColAttributes(hstmt,ColumnPosition,SQL_COLUMN_UPDATABLE,
                               TempBuffer,sizeof(TempBuffer),&ActualSize,
                               &TempInt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      TempInt=SQL_ATTR_READWRITE_UNKNOWN;
      }
   pColumn->Updatable=(short)TempInt;

   /* allocate storage to hold the actual value */
   if(AllocateValueBuffer(pColumn)==FAILURE){
      *RSPtr=BuildReturnStatusChain(RT_ODBC,FAILURE,*RSPtr,
             "AllocateValueBuffer() failed\n",NULL);
      }

   return(pColumn);
   } /* end GetColumnInfo() */


/*************************************************************************
** GetTableInfo()
**
** this function accepts a table or view name as input and returns one
** pointer to a TableInfo structure which describes each of the
** fields in the records in the table.  The TableInfo structure is allocated
** dynamically and initialized by this function.
**
** This function uses a "SELECT * FROM <table_name>" SQL statement to
** determine the record format of the table or view.  However, no CURSOR
** or FETCH statements are used to actually retrieve any records.
**
** Returns:  TableInfo pointer
**           ReturnStatus pointer as a parameter
**
**           if errors, NULL is returned and ReturnStatus Pointer is set
*************************************************************************/
TableInfo *GetTableInfo(HDBC hdbc,
                        char *table_name,
                        Boolean syskey,
                        ReturnStatus **RSPtr)
{
   TableInfo *pTable;
	short  NumOfCol;
   char command_line[SQL_MAX_COMMAND_LENGTH];
   HSTMT hstmt;
   RETCODE returncode;
	ColumnInfo *pTempCol;
	short i;
	Boolean SyskeyFound;
	KeyDef *pKeyInfo;
	char KeyColumnName[SQL_MAX_COL_NAME+1];
	char TempTableName[SQL_MAX_TABLE_NAME_LEN];

   *RSPtr=NULL;
	SyskeyFound=FALSE;

   /* see if caller wants SYSKEY field returned as part of TableInfo if */
   /* SYSKEY exists */
   if(syskey) {

      /* build SELECT statement assuming the SYSKEY field is defined */
      sprintf(command_line,"SELECT SYSKEY,* FROM %s",table_name);

      /* PREPARE the SQL statement */
      returncode=SQLAllocStmt(hdbc,&hstmt);
      if(returncode!=SQL_SUCCESS){
         *RSPtr=BuildReturnStatusODBC(returncode,NULL,hdbc,NULL,*RSPtr);
         return(NULL);
         }
      returncode=SQLPrepare(hstmt,command_line,SQL_NTS);
      if(returncode!=SQL_SUCCESS){

         /* if SYSKEY field was not present then build SELECT statement */
         /* without SYSKEY */
         if(FindError(SQL_COLUMN_NOT_FOUND,NULL,hdbc,hstmt)){
            sprintf(command_line,"SELECT * FROM %s",table_name);

            /* PREPARE the SQL statement */
            returncode=SQLPrepare(hstmt,command_line,SQL_NTS);
            if(returncode!=SQL_SUCCESS){
               *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
               return(NULL);
               }
            }
         /* if PREPARE failed for some other reason then return error */
         else {
            *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
            return(NULL);
            }
         }
		SyskeyFound=TRUE;
      }

   /* Caller does not want SYSKEY field included in TableInfo */
   else {

      /* build SELECT statement without SYSKEY */
      sprintf(command_line,"SELECT * FROM %s",table_name);

      /* PREPARE the SQL statement */
      returncode=SQLAllocStmt(hdbc,&hstmt);
      if(returncode!=SQL_SUCCESS){
         *RSPtr=BuildReturnStatusODBC(returncode,NULL,hdbc,NULL,*RSPtr);
         return(NULL);
         }
      returncode=SQLPrepare(hstmt,command_line,SQL_NTS);
      if((returncode!=SQL_SUCCESS) && (returncode!=SQL_SUCCESS_WITH_INFO)){
         *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
         return(NULL);
         }
      }

   /* allocate TableInfo buffer */
   returncode=SQLNumResultCols(hstmt,&NumOfCol);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      return(NULL);
      }

   pTable=InitializeTableInfo(NumOfCol,0);//>>> need a way to figure out the number of keys
   if(pTable==NULL){
      *RSPtr=BuildReturnStatusMALLOC;
      return(NULL);
      }

	// set the table name
	strcpy(pTable->TableName,table_name);

	// Catalog, Schema, and ShortTableName must be parsed out of full tablename
	// >>>>(because the SQLColAttributes(SQL_QUALIFIER_NAME) type calls don't work)
   strcpy(TempTableName,pTable->TableName);
	strcpy(pTable->TCatalog,strtok(TempTableName,"."));
	strcpy(pTable->SchemaName,strtok(NULL,"."));
	strcpy(pTable->ShortTableName,strtok(NULL,"."));

   /* get information on fields in table's record format */
   pTempCol=pTable->ColPtr;
   for(i=1;i<=NumOfCol;i++){
      GetColumnInfo(hstmt,i,pTempCol,RSPtr);
      pTempCol++;
      }

	// get info on all key fields
   returncode=SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,hdbc,NULL,*RSPtr);
      return(NULL);
      }
   returncode=SQLAllocHandle(SQL_HANDLE_STMT,hdbc,&hstmt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,hdbc,NULL,*RSPtr);
      return(NULL);
      }
   returncode=SQLPrimaryKeys(hstmt,pTable->TCatalog,SQL_NTS,pTable->SchemaName,SQL_NTS,
										pTable->ShortTableName,SQL_NTS);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      FreeTableInfo(pTable);
      return(NULL);
      }

	pTable->KeyColCount=0;
	pKeyInfo=pTable->KeyPtr;
	returncode=SQLFetch(hstmt);
	while(returncode==SQL_SUCCESS){
		returncode=SQLGetData(hstmt,4,SQL_C_CHAR,KeyColumnName,SQL_MAX_COL_NAME+1,NULL);
      if(returncode!=SQL_SUCCESS){
         *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
         return(NULL);
			}
		pKeyInfo->ColNum=GetColumnNumber(pTable,KeyColumnName)-1;
		pKeyInfo++;
		pTable->KeyColCount++;
		returncode=SQLFetch(hstmt);
		}
   if(returncode!=SQL_NO_DATA_FOUND){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,NULL,hstmt,*RSPtr);
      FreeTableInfo(pTable);
      return(NULL);
      }

   returncode=SQLFreeHandle(SQL_HANDLE_STMT,hstmt);
   if(returncode!=SQL_SUCCESS){
      *RSPtr=BuildReturnStatusODBC(returncode,NULL,hdbc,NULL,*RSPtr);
      return(NULL);
      }

	if(SyskeyFound) {
		if(pTable->KeyColCount==0){
			pTable->KeyType=SYSTEM_KEY;
			pTable->KeyColCount=1;
			pKeyInfo->ColNum=1;
			}
		else {
			pTable->KeyType=CLUSTERING_KEY; 	//>>> is it possible to have CLUSTERING_KEY
														//>>> in SQL/MX without a SYSKEY?
			pTable->KeyColCount++;
			pKeyInfo++;
			pKeyInfo->ColNum=1;
			}
		}
	else{
		if(pTable->KeyColCount>0) pTable->KeyType=PRIMARY_KEY;
		else pTable->KeyType=SYSTEM_KEY;
		}

   /* return successful */
   return(pTable);
   }  /* end of GetTableInfo() */


/***********************************************************************
** BindAndFillAllParams()
**
** This function generates random data values for each column in a table.
** It then does an SQLBindParameter for each column.
************************************************************************/
ReturnStatus *BindAndFillAllParams(HSTMT hstmt,TableInfo *pTable)
{
	short CDataType;
	ReturnStatus *pReturnStatus;
	short i;
	ColumnInfo *pCol;
	RETCODE rc;
	char *pMessage;

	pReturnStatus=NULL;
	for(i=0;i<pTable->NumOfCol;i++){
		pCol=&(pTable->ColPtr[i]);
		switch(pCol->pTypeInfo->SQLDataType){
			case SQL_CHAR:
			case SQL_VARCHAR:
			case SQL_LONGVARCHAR:
				CDataType=SQL_C_CHAR;
				if(pCol->Value.pChar!=NULL) free(pCol->Value.pChar);
				pCol->Value.pChar=RandomString((short)RANDOM_NUM1((short)pCol->DataTypeLen));
				break;
			case SQL_NUMERIC:
			case SQL_DECIMAL:
				CDataType=SQL_C_CHAR;
				if(pCol->Value.pChar!=NULL) free(pCol->Value.pChar);
				pCol->Value.pChar=RandomDecimalString((short)pCol->DataTypePrecision,pCol->DataTypeScale);
				break;
			case SQL_SMALLINT:
				CDataType=SQL_C_SHORT;
				*(pCol->Value.pSmallint)=RANDOM_NUM0(32767);
				break;
			case SQL_TINYINT:
				CDataType=SQL_C_SHORT;
				*(pCol->Value.pSmallint)=RANDOM_NUM0(127);
				break;
			case SQL_BIT:
				CDataType=SQL_C_SHORT;
				*(pCol->Value.pSmallint)=RANDOM_NUM0(1);
				break;
			case SQL_BIGINT:
			case SQL_INTEGER:
			case SQL_FLOAT:
			case SQL_REAL:
			case SQL_DOUBLE:
				CDataType=SQL_C_LONG;
				*(pCol->Value.pInteger)=LongRand(65534);
				break;
			case SQL_DATE:
				CDataType=SQL_C_CHAR;
				if(pCol->Value.pChar!=NULL) free(pCol->Value.pChar);
				pCol->Value.pChar=RandomODBCDateTimeString(TYPE_DATE);
				break;
			case SQL_TIME:
				CDataType=SQL_C_CHAR;
				if(pCol->Value.pChar!=NULL) free(pCol->Value.pChar);
				pCol->Value.pChar=RandomODBCDateTimeString(TYPE_TIME);
				break;
			case SQL_TIMESTAMP:
				CDataType=SQL_C_CHAR;
				if(pCol->Value.pChar!=NULL) free(pCol->Value.pChar);
				pCol->Value.pChar=RandomODBCDateTimeString(TYPE_TIMESTAMP);
				break;
			case SQL_BINARY:
			case SQL_VARBINARY:
			case SQL_LONGVARBINARY:
				//>>> need to code random data generator for these fields
				break;
			default:
				break;
			}

		rc=SQLBindParameter(hstmt,(SQLUSMALLINT)(i+1),SQL_PARAM_INPUT,CDataType,
									pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
									pCol->Value.pChar,0,NULL);
	   pMessage=CHECKRC_STR(SQL_SUCCESS,rc,"SQLBindParameter");
		if(pMessage!=NULL){
			pReturnStatus=BuildReturnStatusChain(RT_ODBC,rc,pReturnStatus,pMessage,NULL);
			free(pMessage);
			if(gDebug) assert(FALSE);
			return(pReturnStatus);
			}
		}
	return(pReturnStatus);
	}


/***********************************************************************
** BuildReturnStatusODBC()
**
** This function  is a shell to simplify making calls to GetAllErrors
** followed by a call to BuildReturnStatus().
************************************************************************/
ReturnStatus *BuildReturnStatusODBC(short ODBCReturnCode,
                                    HENV henv,
                                    HDBC hdbc,
                                    HSTMT hstmt,
                                    ReturnStatus *RS_Ptr)
{
   char *pMessage;
   ReturnStatus *pRS;

	pMessage=GetAllErrors(henv,hdbc,hstmt);
   pRS=BuildReturnStatusChain(RT_ODBC,ODBCReturnCode,RS_Ptr,pMessage,NULL);
   free(pMessage);
   return(pRS);

   } /* end: BuildReturnStatusSQL() */

