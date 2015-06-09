#include "defines.h"
#include "include.h"
//#include "QALib.h"
#include "table.h"
#include "struct.h"
#include "globals.h"
#include "sqlutil.h"
#include "sqlutil2.h"
#include "ODBCcommon.h"

/*************************************************************************
** Function: do_delete()
**
** Attempts to delete the record(s) specified, beginning with
** <starting_record> for <record_count> number of records.
**
** NOTE: Because of the zero sum consistency method used, this function
**       will re-insert the last deleted record.  In the case where only
**       a single record was deleted it can appear that nothing happened
**       because the deleted record will be reinserted.
*************************************************************************/
short do_delete(table_description *tab_ptr,Bitmap *bitmap_ptr,long starting_record,
					 long record_count,Boolean abort_flag)
{
   short i;
   long last_record_num;
   char *key_column_name;
   char *zerosum_column_name;
   char select_str[SQL_MAX_COMMAND_LENGTH];
   char delete_str[SQL_MAX_COMMAND_LENGTH];
   char parm_string[80];
   char fields[80];
	Bitmap *bmap_ptr;
   ReturnStatus *RSPtr;
   char command_line[SQL_MAX_COMMAND_LENGTH];
   long zerosum_adjustment;
	ColumnInfo *pCol;
	TableInfo *pTable;
	SQLHENV	henv;
	SQLHDBC	hdbc;
	SQLHSTMT	hstmt;
	RETCODE rc;
	SQLLEN NullIndicator;

   henv=tab_ptr->henv;
   hdbc=tab_ptr->hdbc;
   hstmt=tab_ptr->hstmt;
	bmap_ptr=bitmap_ptr;
	pTable=tab_ptr->pTable;

   LogMsg(TIMESTAMP+INFOMSG,"Deleting %lu records starting from %lu\n",
   		record_count,starting_record);

	/* build the SELECT statement used to adjust the zerosum column... */
   /* ...and the DELETE statement used to delete the records */
	pCol=&(pTable->ColPtr[tab_ptr->key_column_used]);
   strcpy(select_str,"SELECT SUM(%s) FROM %s WHERE %s>=?p1");
   strcpy(delete_str,"DELETE FROM %s WHERE %s>=?p1");

	rc=SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_LONG,
								pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
								&starting_record,0,NULL);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
      return(-1);
      }

   /* check if record range should wrap around to beginning */
   last_record_num=starting_record+record_count-1;
   if(last_record_num>tab_ptr->max_records-1){

      /* record range wraps */
      last_record_num-=tab_ptr->max_records;
      strcat(select_str," OR %s<=?p2");
      strcat(delete_str," OR %s<=?p2");
      }

   else {

      /* record range doesn't wrap */
      strcat(select_str," AND %s<=?p2");
      strcat(delete_str," AND %s<=?p2");
      }

	rc=SQLBindParameter(hstmt,2,SQL_PARAM_INPUT,SQL_C_LONG,
								pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
								&last_record_num,0,NULL);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
      return(-1);
      }

	if(gTrace&TRACE_SQL) LogMsg(NONE,"   Parameter1=%ld,  Parameter2=%ld\n",starting_record,last_record_num);

   strcat(select_str," FOR REPEATABLE ACCESS");

   key_column_name=pCol->CName;

	pCol=&(pTable->ColPtr[tab_ptr->zerosum_column]);
   zerosum_column_name=pCol->CName;

   /* PREPARE the SELECT statement */
   sprintf(command_line,select_str,zerosum_column_name,pTable->TableName,
           key_column_name,key_column_name);

   if(gTrace&TRACE_SQL) LogMsg(0,"   %s\n",command_line);

	rc=SQLPrepare(hstmt,command_line,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLPrepare")){
		LogMsg(0,"   %s\n",command_line);
		LogAllErrors(henv,hdbc,hstmt);
      return(-1);
      }

   /* build the DELETE statement */
   sprintf(command_line,delete_str,pTable->TableName,
           key_column_name,key_column_name);

   if(gTrace&TRACE_SQL) LogMsg(0,"   %s\n",command_line);

	// bind all result columns
	rc=SQLBindCol(hstmt,1,SQL_C_LONG,&zerosum_adjustment,0,&NullIndicator);

   /* do the previously prepared SELECT statement to find out the... */
   /* ...total of the zerosum column in the records to be deleted */
	rc=SQLExecute(hstmt);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecute")){
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }

	rc=SQLFetch(hstmt);
	if(NullIndicator <0) zerosum_adjustment=0;
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLFetch")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
		return(FAILURE);
		}

	rc=SQLFreeStmt(hstmt,SQL_CLOSE);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLFreeStmt")){
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }

   /* EXECUTE the DELETE statement */
	rc=SQLExecDirect(hstmt,command_line,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecDirect")){
		LogMsg(0,"   %s\n",command_line);
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }

//   if((sqlcode!=0) && (sqlcode!=SQL_NO_ROWS_WARNING)) {
//
//      /* DELETE from Entry Seq. table not allowed, make sure we got an error */
//      if(tab_ptr->file_type==ENTRY_SEQ){
//         if(sqlcode==SQL_NO_DELETE_FROM_ES) return(SUCCESS);
//         else {
//            LogMsg(ERRMSG,
//                   "Attempted a DELETE from an entry seq. table and did"
//                   "NOT get an error.\n");
//            return(FAILURE);
//            }
//         }
//
//      if(EvaluateSQLError(SQL_CLOSE,tab_ptr)!=0) return(FAILURE);
//      }

   /* once sucessfully deleted (or hit allowable error) then mark bit(s)... */
   /* ...in bitmap for this table */
   SetBitBlock(BIT_OFF,bmap_ptr,starting_record,record_count);

   /* >>> might want to make this an UPDATE instead of an INSERT since */
   /* >>> the INSERT just undoes the DELETE, although an UPDATE might */
   /* >>> not have any records to update if last record was just deleted */
   /* >>> need to change "(*)" if ALTER ADD COLUMN is ever supported */

   /* Do INSERT of last record deleted to adjust the zerosum column */
   if(strcmp(pTable->ColPtr[0].CName,"SYSKEY")==0){
      strcpy(fields,"SYSKEY,*");
      }
   else strcpy(fields,"*");
   sprintf(command_line,"INSERT INTO %s (%s) VALUES(?p1",
           pTable->TableName,fields);
   for(i=1;i<pTable->NumOfCol;i++){
      sprintf(parm_string,",?p%d",i+1);
      strncat(command_line,parm_string,6);
      }
   strncat(command_line,")",2);

	rc=SQLPrepare(hstmt,command_line,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLPrepare")){
		LogMsg(0,"   %s\n",command_line);
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }

   /* randomly fill values into all columns */
	RSPtr=BindAndFillAllParams(hstmt,pTable);
   if(RSPtr!=NULL){
      LogMsg(ERRMSG+LINEAFTER,
             "couldn't generate random data values for all columns\n"
             "probable cause: row contains an unsupported data type\n"
             "I will continue, inserting the row as is\n");
      FreeReturnStatus(RSPtr);
      }

   /* set key-column */
   RSPtr=SetKeyColumnValue(tab_ptr,last_record_num);
   if(RSPtr!=NULL){
      LogMsg(ERRMSG+LINEAFTER,
             "couldn't set data value for all key columns\n"
             "probable cause: row contains an unsupported data type\n"
             "I will continue, inserting the row as is\n");
      FreeReturnStatus(RSPtr);
      }

   /* set abort-column */
	pCol=&(pTable->ColPtr[tab_ptr->abort_column]);
	rc=SQLBindParameter(hstmt,(short)(tab_ptr->abort_column+1),SQL_PARAM_INPUT,SQL_C_CHAR,
								pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
								&abort_flag,1,NULL);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
      return(FAILURE);
      }

   /* set zerosum-column */
	pCol=&(pTable->ColPtr[tab_ptr->zerosum_column]);
	rc=SQLBindParameter(hstmt,(short)(tab_ptr->zerosum_column+1),SQL_PARAM_INPUT,SQL_C_LONG,
								pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
								&zerosum_adjustment,0,NULL);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
      return(FAILURE);
      }

   /* EXECUTE the previously prepared INSERT statement */
   if(gTrace&TRACE_SQL) LogMsg(NONE,"   %s\n",command_line);
	rc=SQLExecute(hstmt);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecute")){
		LogAllErrors(henv,hdbc,hstmt);
		if(rc!=SQL_SUCCESS_WITH_INFO) return(FAILURE);
      }

   /* once sucessfully inserted (or hit allowable error) then mark bit... */
   /* ...in bitmap for this table */
   SetBit(BIT_ON,bmap_ptr,last_record_num);

   return(SUCCESS);
   }

