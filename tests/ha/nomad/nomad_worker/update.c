#include "defines.h"
#include "include.h"
#include "ODBCcommon.h"
#include "table.h"
#include "struct.h"
#include "globals.h"
#include "sqlutil.h"

/*************************************************************************
** Function: do_update()
**
** Randomly chooses a record or subset of sequential records to be
** updated from the specified table and then attempts to update them.
*************************************************************************/
short do_update(table_description *tab_ptr,Bitmap *bmap_ptr,
					 long requested_record_count,Boolean abort_flag)
{
   long record_num;
   long record_count;
   long last_record_num;
   char *key_column_name;
   char *abort_column_name;
   char update_str[SQL_MAX_COMMAND_LENGTH];
   char command_line[SQL_MAX_COMMAND_LENGTH];
	TableInfo *pTable;
	ColumnInfo *pCol;
	ColumnInfo *pCol2;
	HENV	henv;
	HDBC	hdbc;
	HSTMT	hstmt;
	RETCODE rc;

	pTable=tab_ptr->pTable;
	henv=tab_ptr->henv;
	hdbc=tab_ptr->hdbc;
	hstmt=tab_ptr->hstmt;

	LogMsg(NONE,"\n");

   /* search bitmap for a full block of the right size */
   record_num=find_next_bitblock(BIT_ON,(bitmap *)bmap_ptr->MapPtr,
                                 tab_ptr->max_range-1,
                                 LongRandRange(tab_ptr->min_range,tab_ptr->max_range),
                                 CIRCULAR_SEARCH,
                                 requested_record_count,&record_count);
   /* if no records to read then nothing can be done */
   if(record_num==BIT_NOT_FOUND) {
      if(gTrace){
         LogMsg(0,"No records to update in %s\n",pTable->TableName);
         }
      return(0);
      }

   /* build the UPDATE statement */
	pCol=&(tab_ptr->pTable->ColPtr[tab_ptr->key_column_used]);
   strcpy(update_str,"UPDATE %s SET %s=%d WHERE %s>=?p1");

	rc=SQLBindParameter(hstmt,1,SQL_PARAM_INPUT,SQL_C_LONG,
								pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
								&record_num,0,NULL);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
      return(-1);
      }

   last_record_num=record_num+record_count-1;
   if(last_record_num>tab_ptr->max_records-1){
      strcat(update_str," OR %s<=?p2");
      last_record_num-=tab_ptr->max_records;
      }
   else {
      strcat(update_str," AND %s<=?p2");
      }

   LogMsg(TIMESTAMP+INFOMSG,"Updating %lu records from %lu to %lu\n",
   		record_count,record_num,last_record_num);

	rc=SQLBindParameter(hstmt,2,SQL_PARAM_INPUT,SQL_C_LONG,
								pCol->pTypeInfo->SQLDataType,pCol->DataTypeLen,0,
								&last_record_num,0,NULL);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLBindParameter")){
		LogAllErrors(henv,hdbc,hstmt);
      if(gDebug) assert(FALSE);
      return(-1);
      }

   /*>>> support update zerosum column, someday (maybe other columns as well */
   /*>>> instead of just abort column */

   key_column_name=pCol->CName;
	pCol2=&(pTable->ColPtr[tab_ptr->abort_column]);
   abort_column_name=pCol2->CName;
   sprintf(command_line,update_str,pTable->TableName,
           abort_column_name,abort_flag,
           key_column_name,key_column_name);

	if(gTrace){
		LogMsg(NONE,"   Parameter1=%ld,  Parameter2=%ld\n",record_num,last_record_num);
		LogMsg(0,"   %s\n",command_line);
		}

   /* EXECUTE the UPDATE statement */
	rc=SQLExecDirect(hstmt,command_line,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecDirect")){
		LogAllErrors(henv,hdbc,hstmt);
      return(FAILURE);
      }

   return(0);
   }


/*************************************************************************
** Function: do_vsbb_update()
**
** Randomly chooses a subset of sequential records to be updated
** from the specified table and then attempts to update them.
*************************************************************************/
/*
short do_vsbb_update(tab_ptr,bmap_ptr,requested_record_count,abort_flag)
exec sql begin declare section;
table_description *tab_ptr;
exec sql end declare section;
bitmap *bmap_ptr;
short requested_record_count;
Boolean abort_flag;
{
   long record_num;
   long TempRecordNumber;
   long last_record_num;
   long actual_record_count;
   long record_count;
   char *key_column_name;
   char *abort_column_name;
   char fields[80];
   char *StringValuePtr;
   char select_str[SQL_MAX_COMMAND_LENGTH];
   char update_str[SQL_MAX_COMMAND_LENGTH];
   exec sql begin declare section;
   char command_line[SQL_MAX_COMMAND_LENGTH];
   exec sql end declare section;

   abort_flag=abort_flag;

   // search bitmap for a full block of the right size
   record_num=find_next_bitblock(BIT_ON,bmap_ptr,tab_ptr->max_records,
                                 0,SEARCH_UNTIL_END,
                                 requested_record_count,&record_count);

   // if no records to read then nothing can be done
   if(record_num==BIT_NOT_FOUND) {
      if(gTrace){
         LogMsg(0,"No records in %s to VSBB-UPDATE.\n",tab_ptr->table_name);
         }
      return(0);
      }

   // set the CONTROL table option for VSBB updates
   sprintf(command_line,"CONTROL TABLE %s SEQUENTIAL UPDATE ON",
           tab_ptr->table_name);

   // provide trace information if flag set
   if(gTrace) LogMsg(0,"   %s\n",command_line);

   blank_pad(command_line,SQL_MAX_COMMAND_LENGTH);
   exec sql EXECUTE IMMEDIATE :command_line;
   if(sqlcode!=0){
      if(EvaluateSQLError(SQL_CONTROL_TABLE,tab_ptr)!=0) return(-1);
      }

   // build the SELECT statement used to read the records
   strcpy(select_str,"SELECT %s FROM %s WHERE %s>=");
   StringValuePtr=SetColumnValueString(tab_ptr->sqlda_ptr,
                  tab_ptr->key_column_used,record_num);
   strcat(select_str,StringValuePtr);
   free(StringValuePtr);

   last_record_num=record_num+record_count-1;
   if(last_record_num>tab_ptr->max_records){
      strcat(select_str," OR %s<=");
      last_record_num-=tab_ptr->max_records;
      }
   else {
      strcat(select_str," AND %s<=");
      }

   StringValuePtr=SetColumnValueString(tab_ptr->sqlda_ptr,
                  tab_ptr->key_column_used,last_record_num);
   strcat(select_str,StringValuePtr);
   free(StringValuePtr);

   strcat(select_str," FOR UPDATE OF %s");

   key_column_name=tab_ptr->name_ptr[tab_ptr->key_column_used];
   abort_column_name=tab_ptr->name_ptr[tab_ptr->abort_column];

   switch(tab_ptr->file_type){
      case ENTRY_SEQ:
      case KEY_SEQ:
         strcpy(fields,"*");
         break;
      case RELATIVE:
         strcpy(fields,"SYSKEY,*");
         break;
      }

   // PREPARE the SELECT statement
   sprintf(command_line,select_str,fields,tab_ptr->table_name,
           key_column_name,
           key_column_name,abort_column_name);

   // provide trace information if flag set
   if(gTrace) LogMsg(0,"   %s\n",command_line);

   blank_pad(command_line,SQL_MAX_COMMAND_LENGTH);

   exec sql PREPARE select_statement from :command_line;
   if(sqlcode!=0){
      if(EvaluateSQLError(SQL_PREPARE,tab_ptr)!=0) return(-1);
      }

   // build the UPDATE statement
   strcpy(update_str,"UPDATE %s SET %s=%d WHERE CURRENT OF C1");
   sprintf(command_line,update_str,tab_ptr->table_name,
           abort_column_name,abort_flag);

   // provide trace information if flag set
   if(gTrace) LogMsg(0,"   %s\n",command_line);

   blank_pad(command_line,SQL_MAX_COMMAND_LENGTH);

   // do the prepared SELECT statement to read each record
   exec sql DECLARE C1 CURSOR FOR select_statement;
   if(sqlcode!=0){
      if(EvaluateSQLError(SQL_DECLARE,tab_ptr)!=0) return(-1);
      }
   exec sql OPEN C1;
   if(sqlcode!=0){
      if(EvaluateSQLError(SQL_OPEN,tab_ptr)!=0) return(-1);
      }
   actual_record_count=0;
   TempRecordNumber=record_num;

   // Assume the records are not there until we have actually updated
   // them.  So, clear the range in our bitmap and turn them back on
   // one at a time as they are updated.
   set_bitblock(BIT_OFF,bmap_ptr,record_num,tab_ptr->max_records,
                record_count);

   exec sql FETCH C1 USING DESCRIPTOR :*tab_ptr->sqlda_ptr;

   while((sqlcode>=0)&&(sqlcode!=SQL_EOF)){

      // EXECUTE the UPDATE statement
      exec sql EXECUTE IMMEDIATE :command_line;
      if(sqlcode!=0){
         if(EvaluateSQLError(SQL_UPDATE,tab_ptr)!=0) return(-1);
         }

      actual_record_count++;

      // once sucessfully updated then mark bit in bitmap
      // (just in case its out-of-date)
      set_bit(BIT_ON,bmap_ptr,TempRecordNumber);
      TempRecordNumber++;

      exec sql FETCH C1 USING DESCRIPTOR :*tab_ptr->sqlda_ptr;
      }

   if(sqlcode!=SQL_EOF){
      if(EvaluateSQLError(SQL_FETCH,tab_ptr)!=0) return(-1);
      }

   // check that no more than the records requested were read (sanity check)
   // This is only true if there is not a clustering key
   if((sqlcode==SQL_EOF)&&
      (actual_record_count>record_count)&&
      (tab_ptr->key_type!=CLUSTERING_KEY)){
      LogMsg(ERRMSG,"SELECT read %d but, should have read %d records\n",
             actual_record_count,record_count);
      if(debug_option) DEBUG();
      }
   exec sql CLOSE C1;
   if(sqlcode!=0){
      if(EvaluateSQLError(SQL_CLOSE,tab_ptr)!=0) return(-1);
      }

   if(gTrace){
      LogMsg(0,"   -- %ld records updated with VSBB\n",actual_record_count);
      }

   // reset the CONTROL table option (this really isn't necessary since...
   //...the CONTROL TABLE is supposed to only be in effect for SQL...
   //...statements within this function but, just in case the manual...
   //...was wrong, I reset it here)
   sprintf(command_line,"CONTROL TABLE %s",
           tab_ptr->table_name);

   // provide trace information if flag set
   if(gTrace) LogMsg(0,"   %s\n",command_line);

   blank_pad(command_line,SQL_MAX_COMMAND_LENGTH);
   exec sql EXECUTE IMMEDIATE :command_line;
   if(sqlcode!=0){
      if(EvaluateSQLError(SQL_PREPARE,tab_ptr)!=0) return(-1);
      }

   return(0);
   }

*/

/************************************************************************
** Function: do_seq_update_all()
**
** Attempts to update all records for the process's record range for the
** table specified.  Updates are done sequentially.
************************************************************************
short do_seq_update_all(tab_ptr,bmap_ptr,abort_flag)
{
   tab_ptr=tab_ptr;
   bmap_ptr=bmap_ptr;
   abort_flag=abort_flag;
   return(0);
   } // end: do_seq_update_all()
*/
/************************************************************************
** Function: do_vsbb_update_all()
**
** Attempts to update all records for the process's record range for the
** table specified.  Updates are attempted to be done with VSBB but, due
** to other processes or the layout of the table VSBB might not always be
** done.
************************************************************************
short do_vsbb_update_all(tab_ptr,bmap_ptr,abort_flag)
{
   tab_ptr=tab_ptr;
   bmap_ptr=bmap_ptr;
   abort_flag=abort_flag;
   return(0);
   } // end: do_vsbb_update_all()

*/
