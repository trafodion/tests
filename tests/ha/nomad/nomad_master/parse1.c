#include "defines.h"
#include "tokens.h"
#include "include.h"
#include "table.h"
#include "sqlproc.h"
#include "globals.h"

extern short next_token(void);
extern void init_testid(void);


/***********************************/
/* function prototype declarations */
/***********************************/
short do_command(list_desc *list_ptr,short *loop_number);

/***********************************************************************
** std_err()
**
** This function prints the more standard error messages (those which
** can occur in several different places throughout the parser).
************************************************************************/
void std_err(short error_code)
{
   switch(error_code){
      case MISSING_EQUALS:
         printf("%s Missing equals '=' sign.\n",g_errstr);
         break;
      case MISSING_SEMI_COLON:
         printf("%s Missing semi-colon ';'.  A semi-colon must appear at\n",
                g_errstr);
         printf("the end of each command.\n");
         break;
      case MISSING_COLON:
         printf("%s Missing colon ':'.\n",g_errstr);
         break;
      default:
         printf("%s Internal error.  Invalid <error_code> passed to\n",
                g_errstr);
         printf("the function std_err().  <error_code> was %d.\n",
                error_code);
         break;
      } /* end: switch(error_code) */
   } /* end: std_err() */

/***********************************************************************
** valid_disk()
**
** This function will verify that the string passed to it is a valid
** disk drive name.  It will also verify that the disk exists.
************************************************************************/
short valid_disk(char *diskname)
{
/*   short error;

   error=DEVICE_GETINFOBYNAME_(diskname,(short)strlen(diskname));

   if(error) return(FAILURE);
*/
   return(SUCCESS);
   } /* end: valid_disk() */


/***********************************************************************
** AllocateAndCopyTableDesc()
**
** This function will allocate and copy the information from the
** TableDesc structure.
************************************************************************/
TableDescription *AllocateAndCopyTableDesc(TableDescription *FromPtr)
{
   TableDescription *ToPtr;

   ToPtr=InitializeTableDesc(FromPtr->TableInfoPtr->NumOfCol,
                             FromPtr->TableInfoPtr->KeyColCount,
                             0, /* FromPtr->TableInfoPtr->NumOfPartitions */
                             FromPtr->TableInfoPtr->IndexCount,
                             0,  /* IndexColumnCount */
                             0); /* IndexPartitionCount*/

   memcpy(ToPtr->NomadInfoPtr,FromPtr->NomadInfoPtr,sizeof(NomadInfo));
   CopyTableInfo(ToPtr->TableInfoPtr,FromPtr->TableInfoPtr);
	ToPtr->henv=FromPtr->henv;
	ToPtr->hdbc=FromPtr->hdbc;
	ToPtr->hstmt=FromPtr->hstmt;

   return(ToPtr);
   } /* end: AllocateAndCopyTableDesc() */



/***********************************************************************
** add_table()
**
** This function will check the current list of tables to see if a
** table already exists.  If it does, the table's table number is returned.
** If it doesn't then the table's format is checked to see if it meets our
** requirements and then an entry is created and added to the list of
** tables.
************************************************************************/
short add_table(char *table_name)
{
   TableDescription *table_ptr;
   short i;
   ReturnStatus *RSPtr;

   /* search table list to see if table is already in it */
   for(i=0;i<g_info.table_count;i++){

      /* if found then return its table number */
      if(strcmp(table_name,g_info.table_ptr[i]->TableInfoPtr->TableName)==0) return(i);
      }

   /* if not found then get table's information (this will return NULL... */
   /* ...if table does not meet our requirements) */
	table_ptr=GetExistingTableDesc(ghdbc,table_name,&RSPtr);
   if(table_ptr==NULL) {
   	LogReturnStatus(RSPtr);
   	return(FAILURE);
   }

   /* add new table entry to table list */
   g_info.table_ptr[g_info.table_count]=table_ptr;
   g_info.table_count++;

   /* return its table number */
   return((short)(g_info.table_count-1));
   } /* end: add_table() */


/***********************************************************************
** do_create()
**
** This function handles parsing for the CREATE command.  It sets the
** information parsed into the appropriate structure variables.  Syntax
** of the CREATE command is as follows:
**
**   CREATE [ <count> ] ( <table-spec> )
**                      ( PROCESS(ES)  )
**      <count> is:
**         optional and must be an integer from 1 to 999.
**      <table-spec> is:
** [TABLE(S) [ LIKE <existing-table> ]                                   ]
** [TABLE(S) [ WITH <column-count> COLUMNS ] ]
**      <column-count> is:
**         an integer from 4 to maximum number of columns allowed by SQL
**
************************************************************************/
short do_create(void)
{
   short i;
   short count;
   short CreateFailureCount;
   short file_type;
   short Audited;
   short ColumnCount;
   ReturnStatus *RSPtr;
   TableDescription *temp_ptr;

   file_type=0;
   Audited=RANDOM;

   /* check if optional repetition count was specified */
   if(next_token()==NUMBER) {
      count=atoi(g_token_string);
      next_token();
      }
   else count=1;

   /* determine if we're creating tables or processes */
   if(g_current_token==PROCESS){

      /* create processes */
      g_info.process_count+=count;
      if(g_info.process_count>MAX_PROCESSES) {
         printf("%s maximum number of processes exceeded. Maximum=%d\n",
                g_errstr,MAX_PROCESSES);
         return(FAILURE);
         }
      for(i=g_info.process_count-count;
          i<g_info.process_count;i++) {
         g_info.process_ptr[i]=
            (process_info *)malloc(sizeof(process_info));
         memset(g_info.process_ptr[i],0,sizeof(process_info));
         }
      }

   else{

      /* create tables */
      if(g_current_token==TABLE){
         g_info.table_count+=count; /* add to any previous tables... */
                                    /* ...that were created */
         if(g_info.table_count>MAX_TABLES) {
            printf("%s maximum number of tables exceeded. Maximum=%d\n",
                   g_errstr,MAX_TABLES);
            return(FAILURE);
            }
         }
      else {
         printf("%s expecting TABLE\n",g_errstr);
         return(FAILURE);
         }

      switch(next_token()){
         case LIKE:
				next_token();
				temp_ptr=GetExistingTableDesc(ghdbc,g_token_string,&RSPtr);
				if(temp_ptr==NULL) return(FAILURE);
				strcpy(temp_ptr->NomadInfoPtr->like_name,
						 temp_ptr->TableInfoPtr->TableName);
            break;

         case WITH:
            if((next_token()!=NUMBER)||
               (atoi(g_token_string)<NOMAD_MIN_COLUMN_COUNT)) {
               printf("%s invalid number of columns.  Minimum is %d.\n",
                      g_errstr,NOMAD_MIN_COLUMN_COUNT);
               return(FAILURE);
               }

            ColumnCount=atoi(g_token_string);
            temp_ptr=InitializeTableDesc(
                        ColumnCount,  /* number of columns */
                        (short)RANDOM_NUM1(ColumnCount-3),/* number of keys */
                        0,     /* number of partitions */
                        0,     /* number of indexes */
                        0,     /* number of index columns per index */
                        0);    /* number of partitions per index */

            if(file_type==0) file_type=KEY_SEQ;
            temp_ptr->TableInfoPtr->Organization=file_type;

            if(next_token()!=COLUMNS) {
               printf("%s expecting COLUMNS keyword.\n",g_errstr);
               return(FAILURE);
               }
            break;

         case SEMI_COLON:
            ColumnCount=RANDOM_RANGE(NOMAD_MIN_COLUMN_COUNT,
                                     SQL_MAX_COLUMNS);
            temp_ptr=InitializeTableDesc(
                        ColumnCount,
                        (short)RANDOM_NUM1(ColumnCount-3),/* number of keys */
                        0,      /* number of partitions */
                        0,      /* number of indexes */
                        0,      /* number of index columns per index */
                        0);     /* number of partitions per index */

            if(file_type==0) file_type=KEY_SEQ;
            temp_ptr->TableInfoPtr->Organization=file_type;
            break;

         default:
            printf("%s '%s' is invalid, expecting LIKE, WITH, or semi-"
                   "colon.\n",g_errstr,g_token_string);
            return(FAILURE);
         } /* end: switch(next_token()) */


      /* allocate space for each tables information and initialize... */
      /* ...it, then create the table */
      CreateFailureCount=0;
      i=g_info.table_count-count;
		temp_ptr->henv=ghenv;
		temp_ptr->hdbc=ghdbc;
		temp_ptr->hstmt=ghstmt;
      while((i<g_info.table_count)&&(CreateFailureCount<3)){

         g_info.table_ptr[i]=AllocateAndCopyTableDesc(temp_ptr);

         if(temp_ptr->NomadInfoPtr->like_name[0]==NULL){
            FillTableDesc(g_info.table_ptr[i]);
            }
         sprintf(g_info.table_ptr[i]->TableInfoPtr->TCatalog,"TRAFODION");
         sprintf(g_info.table_ptr[i]->TableInfoPtr->SchemaName,"%s_SCHEMA",
					  g_info.testid);
         sprintf(g_info.table_ptr[i]->TableInfoPtr->TableName,"%s.%s.%s_T%03d",
					  g_info.table_ptr[i]->TableInfoPtr->TCatalog,
                 g_info.table_ptr[i]->TableInfoPtr->SchemaName,
                 g_info.testid,i);
         sprintf(g_info.table_ptr[i]->TableInfoPtr->ShortTableName,"%s_T%03d",
                 g_info.testid,i);
         if(CreateSQLTable(g_info.table_ptr[i])!=0){
            FreeTableDesc(g_info.table_ptr[i]);
            CreateFailureCount++;
            }
         else{
            i++;
            CreateFailureCount=0;
            }
         }

      FreeTableDesc(temp_ptr);
      if(CreateFailureCount>0) return(FAILURE);

      } /* end: else */

   if(g_current_token!=SEMI_COLON){
      if(next_token()!=SEMI_COLON){
         std_err(MISSING_SEMI_COLON);
         return(FAILURE);
         }
      }
   return(SUCCESS);
   } /* end: do_create() */


/***********************************************************************
** do_max_records()
**
** This function will parse the MAXIMUM_RECORDS keyword which has the
** following syntax:
**
** MAXIMUM_RECORDS [ FOR { #TABLEn               } ] = <integer>
**                 [     { <existing-table-name> } ]
**
** If neither #TABLEn or <existing-table> is specified then the value for
** record range will be applied to all tables.
************************************************************************/
short do_max_records(void)
{
   short i;
   short table_num;
   Boolean found;
   long max;
   char* end_ptr;

   table_num=-1;  /* default to use all tables from process's USE command */

   next_token();

   /* check for the FOR keyword clause */
   if(g_current_token==FOR_KW){
      next_token();
      if(g_current_token==TABLE_N){

         /* get and validate table number */
         sscanf(g_token_string,"#TABLE%hd",&table_num);
         if(table_num>=g_info.table_count){
            printf("%s only %d tables defined, %s is not defined\n",g_errstr,
                   g_info.table_count,g_token_string);
            return(FAILURE);
            }
         next_token();
         }
      else if(g_current_token==STRING){

         /* look for existing table in table list */
         found=FALSE;
         for(i=0;i<g_info.table_count;i++){
            if(strcmp(g_token_string,
                      g_info.table_ptr[i]->TableInfoPtr->TableName)==0){
               found=TRUE;
               table_num=i;
               }
            }
         if(!found){
            printf("%s %s must be specified in a USE TABLE command\n",
                   g_errstr,g_token_string);
            return(FAILURE);
            }
         next_token();
         }
      else {
         printf("%s expecting either #TABLEn or existing table name\n",
                g_errstr);
         return(FAILURE);
         }
      } /* end if(g_current_token==FOR) */

   if(g_current_token!=EQUALS){
      std_err(MISSING_EQUALS);
      return(FAILURE);
      }

   if(next_token()!=NUMBER){
      printf("%s expecting a number greater than or equal to zero\n",g_errstr);
      return(FAILURE);
      }
   max=strtol(g_token_string,&end_ptr,10);
   if(next_token()!=SEMI_COLON){
      std_err(MISSING_SEMI_COLON);
      return(FAILURE);
      }

   /* apply record maximum, to all tables or a single table as appropriate */
   if(table_num==-1){

      /* apply to all tables */
      for(i=0;i<g_info.table_count;i++){
         g_info.table_ptr[i]->NomadInfoPtr->max_records=max;
         }
      }
   else {
      /* apply to single specified table */
      g_info.table_ptr[table_num]->NomadInfoPtr->max_records=max;
      }
   return(SUCCESS);
   } /* end: do_max_records() */


/***********************************************************************
** do_library()
**
** This function will parse the RUN_TIME_LIBRARY keyword who's syntax is:
**         RUN_TIME_LIBRARY = <existing-library-file>
************************************************************************/
short do_library(void)
{
/*
   short error;
   short fullname_length;
   short item_list[1];
   short item_count;
   struct{
      short filecode;
      } result;

   if(next_token()!=EQUALS) {std_err(MISSING_EQUALS); return(FAILURE);}

   if(next_token()==STRING){

      // make name into fully-qualified name, if it already isn't
      error=FILENAME_RESOLVE_(g_token_string,(short)strlen(g_token_string),
                              g_info.library,
                              (short)sizeof(g_info.library),
                              &fullname_length);
      g_info.library[fullname_length]=NULL_STR;
      if(error){
         printf("%s File System error %d returned from FILENAME_RESOLVE_\n",
                g_errstr,error);
         return(FAILURE);
         }

      // get the file code for this file
      item_list[0]=FILE_CODE;
      item_count=1;
      error=FILE_GETINFOLISTBYNAME_(g_info.library,
                                    (short)strlen(g_info.library),
                                    item_list,item_count,
                                    (short *)&result,(short)sizeof(result));
      //>>> should check error
      // sanity check to make sure it is at least an object file
      if(result.filecode!=OBJECT_FILECODE){
         printf("%s %s is NOT a valid run-time library\n",g_errstr,
                g_info.library);
         return(FAILURE);
         }

      } // end: if STRING
   else {
      printf("%s expecting a valid run-time library filename.\n",g_errstr);
      return(FAILURE);
      }

   if(next_token()!=SEMI_COLON){std_err(MISSING_SEMI_COLON);return(FAILURE);}
*/
   return(SUCCESS);
   } // end: do_check_interval()


/***********************************************************************
** do_fill()
**
** This function will parse the command line which specifies how full
** to start a given set of tables with.  Syntax is as follows:
**
** FILL [ <table-list> ] { RANDOMLY     } { WITH <count> RECORDS }
**                       { SEQUENTIALLY } { TO <percent>         }
**
************************************************************************/
short do_fill(void)
{
   NomadInfo *NPtr;
   short table_num;
   Boolean found;
   short i;
   long InitialRecordCount;
	short InitialFillMethod;
   short percent;

   percent=-1;
   table_num=-1;
   next_token();
   if(g_current_token==RANDOM_KW || g_current_token==SEQUENTIAL ){

      }
   else {
      if(g_current_token==TABLE_N){

         /* get and validate table number */
         sscanf(g_token_string,"#TABLE%hd",&table_num);
         if(table_num>=g_info.table_count){
            printf("%s only %d tables defined, %s is not defined\n",g_errstr,
                   g_info.table_count,g_token_string);
            return(FAILURE);
            }
         next_token();
         }
      else if(g_current_token==STRING){

         /* look for existing table in table list */
         found=FALSE;
         for(i=0;i<g_info.table_count;i++){
            if(strcmp(g_token_string,
                      g_info.table_ptr[i]->TableInfoPtr->TableName)==0){
               found=TRUE;
               table_num=i;
               }
            }
         if(!found){
            printf("%s %s must be specified in a USE TABLE command\n",
                   g_errstr,g_token_string);
            return(FAILURE);
            }
         next_token();
         }
      else {
         printf("%s expecting either #TABLEn or an existing table name\n",
                g_errstr);
         return(FAILURE);
         }
      }

   switch(g_current_token){
      case RANDOM_KW: InitialFillMethod=FILLRANDOMLY; break;
      case SEQUENTIAL: InitialFillMethod=FILLSEQUENTIALLY; break;
      default:
         printf("%s expecting either RANDOMLY or SEQUENTIALLY\n",g_errstr);
         return(FAILURE);
      }

   switch(next_token()){
      case WITH:
         if(next_token()!=NUMBER){
            printf("%s expecting a number greater than or equal to zero\n",g_errstr);
            return(FAILURE);
            }
         InitialRecordCount=atoi(g_token_string);
         if(next_token()!=RECORD){
            printf("%s expecting RECORD\n",g_errstr);
            return(FAILURE);
            }
         break;

      case TO_KW:
         if(next_token()!=NUMBER){
            printf("%s expecting a number greater than or equal to zero\n",g_errstr);
            return(FAILURE);
            }
         percent=atoi(g_token_string);
         if(percent>100){
            printf("%s expecting a percentage from 0%% to 100%%\n",g_errstr);
            return(FAILURE);
            }
         next_token();
         if(strcmp(g_token_string,"%")!=0){
            printf("%s expecting a percent sign '%%'\n",g_errstr);
            return(FAILURE);
            }

         break;

      default:
         printf("%s expecting WITH or TO \n",g_errstr);
         return(FAILURE);
      }
   /* apply record fill, to all tables or a single table as appropriate */
   if(table_num==-1){

      /* apply to all tables */
      for(i=0;i<g_info.table_count;i++){
         NPtr=g_info.table_ptr[i]->NomadInfoPtr;
			NPtr->InitialFillMethod=InitialFillMethod;
         if(NPtr->max_records==0){
            printf("%s somewhere before this FILL statement, MAX_RECORDS\n"
                   "for this table must be specified\n",g_errstr);
            return(FAILURE);
            }
         if(percent==-1){
            NPtr->InitialRecordCount=InitialRecordCount;
            if(NPtr->max_records<NPtr->InitialRecordCount){
               printf("%s expecting a number from 0 to %ld (MAX_RECORDS)\n",
                      g_errstr,NPtr->max_records);
               return(FAILURE);
               }
            }
         else{
            /* the divide by 100 needs to be done last as this is integer */
            /* variables done with integer math */
            NPtr->InitialRecordCount=NPtr->max_records*percent/100;
            }
         }
      }
   else {

      /* apply to single specified table */
      NPtr=g_info.table_ptr[table_num]->NomadInfoPtr;
		NPtr->InitialFillMethod=InitialFillMethod;
      if(NPtr->max_records==0){
         printf("%s somewhere before this FILL statement, MAX_RECORDS\n"
                "for this table must be specified\n",g_errstr);
         return(FAILURE);
         }
      if(percent==-1){
         NPtr->InitialRecordCount=InitialRecordCount;
         if(NPtr->max_records<NPtr->InitialRecordCount){
            printf("%s expecting a number from 0 to %ld (MAX_RECORDS)\n",
                   g_errstr,NPtr->max_records);
            return(FAILURE);
            }
         }
      else{
         /* the divide by 100 needs to be done last as this is integer */
         /* variables done with integer math */
         NPtr->InitialRecordCount=NPtr->max_records*percent/100;
         }
      }

   if(next_token()!=SEMI_COLON){
      std_err(MISSING_SEMI_COLON);
      return(FAILURE);
      }

   return(SUCCESS);

   } /* end: do_fill() */


/***********************************************************************
** do_use()
**
** This function will parse the USE command which has the following syntax:
**
**      USE TABLE(S) <table-list>
**         <table-list> is:
**            { <existing-table>                                        }
**            { ( <existing-table> [ , <existing-table> ] ... )         }
**            { #TABLE<table-number>                                    }
**            { ( #TABLE<table-number> [ , #TABLE<table-number> ] ... ) }
**
** All tables must already exist and/or must reference a table from a
** previous CREATE TABLE command.
************************************************************************/
short do_use(process_info *proc_ptr)
{
   Boolean list;
   short table_num;
   table *temp_ptr;

   if(next_token()!=TABLE){
      printf("%s expecting TABLE(S) keyword.\n",g_errstr);
      return(FAILURE);
      }
   if(next_token()==BEGIN_LIST) {
      list=TRUE;
      next_token();
      }
   else list=FALSE;

   switch(g_current_token){
      case STRING:
         /* add the table name to the list (if it's already in... */
         /* ...the list then only its number is returned) */
         table_num=add_table(g_token_string);
         if(table_num<0) {
         	printf("%s Problem with table '%s'\n",g_errstr,g_token_string);
         	return(FAILURE);
         }
         break;

      case TABLE_N:
         /* verify table number is defined */
         table_num=atoi(&g_token_string[6]);
         if(table_num>=g_info.table_count) {
            printf("%s %s is undefined.\n",g_errstr,g_token_string);
            return(FAILURE);
            }
         break;

      default:
         printf("%s invalid table name '%s' in USE TABLE list\n",
                g_errstr,g_token_string);
         return(FAILURE);
      } /* end: switch(g_current_token) */

   if(proc_ptr!=NULL){

      /* link table number to front of process's table list */
      /*>>>> need to free any default table lists already allocated */
      temp_ptr=(table *)malloc(sizeof(table));
      memset(temp_ptr,0,sizeof(table));
      temp_ptr->num=table_num;
      proc_ptr->table_ptr=temp_ptr;
      proc_ptr->table_count=1;
      g_info.table_ptr[table_num]->NomadInfoPtr->process_count++;
      }

   /* process remaining list of tables (if any) */
   if(list){
      while(next_token()!=END_LIST){
         if(g_current_token!=COMMA){
            std_err(MISSING_COMMA);
            return(FAILURE);
            }
         switch(next_token()){
            case STRING:
               /* add the table name to the list (if it's already in... */
               /* ...the list then only its number is returned) */
               table_num=add_table(g_token_string);
               if(table_num<0) return(FAILURE);
               break;

            case TABLE_N:
               /* verify table number is defined */
               table_num=atoi(&g_token_string[6]);
               if(table_num>=g_info.table_count) {
                  printf("%s %s is undefined.\n",g_errstr,g_token_string);
                  return(FAILURE);
                  }
               break;

            default:
               printf("%s invalid table name '%s' in USE TABLE list\n",
                      g_errstr,g_token_string);
               return(FAILURE);
            } /* end: switch(next_token()) */

         if(proc_ptr!=NULL){

            /* link table number to front of process's table list */
            temp_ptr=(table *)malloc(sizeof(table));
            memset(temp_ptr,0,sizeof(table));
            temp_ptr->next_ptr=proc_ptr->table_ptr;
            temp_ptr->num=table_num;
            proc_ptr->table_ptr=temp_ptr;
            proc_ptr->table_count++;
            g_info.table_ptr[table_num]->NomadInfoPtr->process_count++;
            }

         } /* end: while(next_token... */
      } /* end: if(list) */

   if(next_token()!=SEMI_COLON){
      std_err(MISSING_SEMI_COLON);
      return(FAILURE);
      }

   return(SUCCESS);
   } /* end: do_use() */

/***********************************************************************
** do_stop_on_error()
**
** This function will parse the STOP_ON_ERROR keyword which has the following syntax:
**      STOP_ON_ERROR = { YES | NO }
************************************************************************/
short do_stop_on_error(void)
{
   if(next_token()!=EQUALS) {std_err(MISSING_EQUALS); return(FAILURE);}

   switch(next_token()){
      case STRING:
      	toupper_s(g_token_string);
      	if(strcmp(g_token_string,"YES")==0){
           	gStopOnError=TRUE;
      	}
      	else if(strcmp(g_token_string,"NO")==0){
           	gStopOnError=FALSE;
      	}
      	else {
            printf("%s expecting YES or NO\n",g_errstr);
            return(FAILURE);
      	}
      	break;
      default:
         printf("%s expecting YES or NO\n",g_errstr);
         return(FAILURE);
      } /* end: switch */

   if(next_token()!=SEMI_COLON){std_err(MISSING_SEMI_COLON);return(FAILURE);}

   return(SUCCESS);
   } /* end: do_stop_on_error() */

/***********************************************************************
** get_startup_info()
**
**
************************************************************************/
short get_startup_info(void)
{
   short temp_token;
   short error;

   /* check for colon which should follow keyword */
   next_token();
   if(strcmp(g_token_string,":")!=0){
      std_err(MISSING_COLON);
      return(FAILURE);
      }

   /* first command in STARTUP: section must be 'TESTID' */
   if(next_token()==TESTID) {

      /* process TESTID keyword */
      if(next_token()!=EQUALS) {
         std_err(MISSING_EQUALS);
         return(FAILURE);
         }
      if((next_token()!=STRING) || (strlen(g_token_string)!=2)){
         printf("%s TESTID must be two letters. '%s' is invalid.\n",
         g_errstr,g_token_string);
         return(FAILURE);
         }
      strcpy(g_info.testid,g_token_string);
      if(next_token()!=SEMI_COLON) {
         std_err(MISSING_SEMI_COLON);
         return(FAILURE);
         }
      }
   else {
      printf("%s 'TESTID' must be first command in STARTUP: section.\n",
             g_errstr);
      return(FAILURE);
      }

   /* parse work_vol and table_vol here because it needs to appear before */
   /* any CREATE commands so we can create table on the correct volume */
   next_token();
   if((g_current_token==WORK_VOL)||(g_current_token==TABLE_VOL)){
      temp_token=g_current_token;
      if(next_token()!=EQUALS){
         std_err(MISSING_EQUALS);
         return(FAILURE);
         }
      next_token();
      if(valid_disk(g_token_string)!=0){
         printf("%s Invalid volume name or volume does not exist.\n",
                g_errstr);
         return(FAILURE);
         }
      switch(temp_token){
         case WORK_VOL:
            strcpy(g_info.work_volume,g_token_string);
            break;
         case TABLE_VOL:
            strcpy(g_info.catalog,g_token_string);
            break;
         } /* end: switch(temp_token) */
      if(next_token()!=SEMI_COLON){
         std_err(MISSING_SEMI_COLON);
         return(FAILURE);
         }
      next_token();
      }

   /* initialize this testid's stuff */
   init_testid();

   /* loop processing all commands in the STARTUP section until we hit... */
   /* ...another section name or the EOF */
   while((g_current_token!=EOF) && (g_current_token!=CLEANUP) &&
         (g_current_token!=ALL_PROCESSES) && (g_current_token!=PROCESS_N)){
      switch(g_current_token) {
         case CREATE_KW: do_create(); break;

         case USE: do_use(NULL); break;

         case LIBRARY: do_library(); break;

         case MAX_RECORDS: error=do_max_records(); break;

         case FILL: error=do_fill(); break;

         case STOP_ON_ERROR_KW: error=do_stop_on_error(); break;

         case WORK_VOL:
         case TABLE_VOL:
            printf("%s WORK_VOLUME and TABLE_VOLUME must precede any"
                   " CREATE command\n",g_errstr);
            return(FAILURE);
         default:
            printf("%s Unknown command '%s' or command not "
                   "allowed in STARTUP section.\n\n",g_errstr,g_token_string);
            return(FAILURE);
         } /* end: switch(g_current_token) */
      next_token();
      } /* end: while((g_current_token... */
   return(SUCCESS);
   } /* end: get_startup_info() */


/***********************************************************************
** do_record_action()
**
**
************************************************************************/
item_desc *do_record_action(void)
{
   item_desc *item_ptr;

   /* allocate new item descriptor */
   item_ptr=(item_desc *)malloc(sizeof(item_desc));

   switch(g_current_token){
      case RANDOM_KW:
         switch(next_token()){
            case INSERT: item_ptr->code=RANDOM_INSERT; break;
            case DELETE_ROW: item_ptr->code=RANDOM_DELETE; break;
            case UPDATE: item_ptr->code=RANDOM_UPDATE; break;
            case SELECT: item_ptr->code=RANDOM_SELECT; break;
            default:
               printf("%s RAND expecting INSERT, DELETE, UPDATE, or SELECT\n"
                     ,g_errstr);
               free(item_ptr);
               return(NULL);
            } /* end: switch */
         break;
      case SEQUENTIAL:
         switch(next_token()){
            case INSERT: item_ptr->code=SEQ_INSERT; break;
            case DELETE_ROW: item_ptr->code=SEQ_DELETE; break;
            case UPDATE: item_ptr->code=SEQ_UPDATE; break;
            case SELECT: item_ptr->code=SEQ_SELECT; break;
            default:
               printf("%s SEQ expecting INSERT, DELETE, UPDATE, or SELECT\n",
                      g_errstr);
               free(item_ptr);
               return(NULL);
            } /* end: switch */
         break;
      case VSBB:
         switch(next_token()){
            case INSERT: item_ptr->code=VSBB_INSERT; break;
            case UPDATE: item_ptr->code=VSBB_UPDATE; break;
            case SELECT: item_ptr->code=VSBB_SELECT; break;
            default:
               printf("%sVSBB expecting INSERT, UPDATE, or SELECT\n",
                      g_errstr);
               printf("%s VSBB DELETEs are not supported\n",g_indent);
               free(item_ptr);
               return(NULL);
            } /* end: switch */
         break;
/*       case ALTER_KW:
            if (next_token()==TABLE)
              switch (next_token())     {
                    case ADD:
                            if (next_token()==COLUMN)   {
                              item_ptr->code = ALTER_ADD_COL;
                              break;
                             }
                    default:
                  printf("***INTERNAL ERROR: Invalid ALTER statement in %s\n",
                           "do_record_action");
                     free(item_ptr);
                     return (NULL);
                }
*/ /* end switch */
/*        else    {
                  printf("***INTERNAL ERROR: Invalid ALTER  statement in %s\n",
                                         "do_record_action");
              free(item_ptr);
              return (NULL);
            }
        break;
*/
      default:
         printf("*** INTERNAL ERROR: Invalid token in do_record_action()\n");
         printf("***                 token=%d  string=%s\n",g_current_token,
                g_token_string);
         free(item_ptr);
         return(NULL);
      } /* end: switch */

   /* parse the repetition factor */
   switch(next_token()){
      case ALL:
         item_ptr->number=1;
         switch(item_ptr->code){
            case SEQ_INSERT: item_ptr->code=SEQ_INSERT_ALL; break;
            case SEQ_UPDATE: item_ptr->code=SEQ_UPDATE_ALL; break;
            case SEQ_DELETE: item_ptr->code=SEQ_DELETE_ALL; break;
            case SEQ_SELECT: item_ptr->code=SEQ_SELECT_ALL; break;
            case VSBB_INSERT: item_ptr->code=VSBB_INSERT_ALL; break;
            case VSBB_UPDATE: item_ptr->code=VSBB_UPDATE_ALL; break;
            case VSBB_SELECT: item_ptr->code=VSBB_SELECT_ALL; break;
            default:
               printf("%s ALL option not allowed on this action\n",
                      g_errstr);
               return(NULL);
            } /* end: switch */
         break;
      case NUMBER:
         item_ptr->number=atoi(g_token_string);
         if(item_ptr->number<=0){
            printf("%s expecting a number greater than 0\n",g_errstr);
            free(item_ptr);
            return(NULL);
            }
         break;
      }

   /* record actions are distinguished from percent action by being...*/
   /*...negative */
   item_ptr->code=-item_ptr->code;

   item_ptr->list_ptr=NULL;
   item_ptr->next_ptr=NULL;

   if(next_token()!=SEMI_COLON){
      std_err(MISSING_SEMI_COLON);
      return(NULL);
      }

   return(item_ptr);
   } /* end: do_record_action() */


/***********************************************************************
** do_percent_action()
**
**
************************************************************************/
item_desc *do_percent_action(void)
{
   item_desc *item_ptr;

   /* allocate new item descriptor */
   item_ptr=(item_desc *)malloc(sizeof(item_desc));

   /* get and validate percentage number */
   item_ptr->number=atoi(g_token_string);
   if((item_ptr->number<0)||(item_ptr->number>100)){
      printf("%s expecting a percentage from 0%% to 100%%\n",g_errstr);
      free(item_ptr);
      return(NULL);
      }
   next_token();
   if(strcmp(g_token_string,"%")!=0){
      printf("%s expecting a percent sign '%%'\n",g_errstr);
      free(item_ptr);
      return(NULL);
      }

   switch(next_token()){
      case RANDOM_KW:
         switch(next_token()){
            case INSERT: item_ptr->code=RANDOM_INSERT; break;
            case DELETE_ROW: item_ptr->code=RANDOM_DELETE; break;
            case UPDATE: item_ptr->code=RANDOM_UPDATE; break;
            case SELECT: item_ptr->code=RANDOM_SELECT; break;
            default:
               printf("%s expecting INSERTS, DELETES, UPDATES, or SELECTS\n",
                      g_errstr);
               return(NULL);
            } /* end: switch */
         break;
      case SEQUENTIAL:
         switch(next_token()){
            case INSERT: item_ptr->code=SEQ_INSERT; break;
            case DELETE_ROW: item_ptr->code=SEQ_DELETE; break;
            case UPDATE: item_ptr->code=SEQ_UPDATE; break;
            case SELECT: item_ptr->code=SEQ_SELECT; break;
            default:
               printf("%s expecting INSERTS, DELETES, UPDATES, or SELECTS\n",
                      g_errstr);

               free(item_ptr);
               return(NULL);
            } /* end: switch */
         break;
      case VSBB:
         switch(next_token()){
            case INSERT: item_ptr->code=VSBB_INSERT; break;
            case UPDATE: item_ptr->code=VSBB_UPDATE; break;
            case SELECT: item_ptr->code=VSBB_SELECT; break;
            default:
               printf("%s expecting INSERT, UPDATE, or SELECT\n",
                      g_errstr);
               printf("%s VSBB DELETEs are not supported\n",g_indent);
               free(item_ptr);
               return(NULL);
            } /* end: switch */
         break;
/*      case ALTER_KW:
            if (next_token()==TABLE)
              switch (next_token())     {
                    case ADD:
                            if (next_token()==COLUMN)   {
                              item_ptr->code = ALTER_ADD_COL;
                              break;
                             }
                    default:
                     printf("***INTERNAL ERROR: Invalid ALTER TABLE statement in %s\n",
                                         "do_percent_action");
                     free(item_ptr);
                     return (NULL);
                }
        else    {
                  printf("***INTERNAL ERROR: Invalid ALTER  statement in %s\n",
                                         "do_percent_action");
              free(item_ptr);
              return (NULL);
            }
        break;
*/
      default:
         printf("%s expecting RANDOM or SEQUENTIAL or ALTER\n",g_errstr);
         free(item_ptr);
         return(NULL);
      } /* end: switch */

   item_ptr->list_ptr=NULL;
   item_ptr->next_ptr=NULL;

   if(next_token()!=SEMI_COLON){
      std_err(MISSING_SEMI_COLON);
      return(NULL);
      }

   return(item_ptr);
   } /* end: do_percent_action() */


/***********************************************************************
** get_int_range()
**
** This function parses the strings "= <integer1>;" and
** "= ( <integer1>,<integer2> );" and returns the values of the integer(s).
** In the case of a single integer both <num1> and <num2> are set to the
** same value.
************************************************************************/
short get_int_range(short *num1,short *num2)
{

   if(g_current_token!=EQUALS) {std_err(MISSING_EQUALS); return(FAILURE);}

   if(next_token()!=BEGIN_LIST){
      if(g_current_token!=NUMBER){
         printf("%s expecting an integer >= 0\n",g_errstr);
         return(FAILURE);
         }
      *num1=atoi(g_token_string);
      *num2=*num1;
      } /* end: if not BEGIN_LIST */
   else{
      if(next_token()!=NUMBER){
         printf("%s expecting an integer >= 0\n",g_errstr);
         return(FAILURE);
         }
      *num1=atoi(g_token_string);

      if(next_token()!=COMMA) {std_err(MISSING_COMMA); return(FAILURE);}

      if(next_token()!=NUMBER){
         printf("%s expecting an integer >= 0\n",g_errstr);
         return(FAILURE);
         }
      *num2=atoi(g_token_string);

      if(next_token()!=END_LIST){std_err(MISSING_CLOSE_PAREN);return(FAILURE);}
      } /* end: else BEGIN_LIST */

   if(next_token()!=SEMI_COLON){std_err(MISSING_SEMI_COLON);return(FAILURE);}

   return(SUCCESS);
   } /* end: get_int_range() */


/***********************************************************************
** do_record_range()
**
** This function will parse the RECORD_RANGE keyword which has the
** following syntax:
**
** RECORD_RANGE [ FOR { #TABLEn               } ] = "(" <low> , <high> ")"
**              [     { <existing-table-name> } ]
**
** If neither #TABLEn or <existing-table is specified then the values for
** record range will be applied to all tables the process uses.
************************************************************************/
short do_record_range(process_info *proc_ptr)
{
   short i;
   short table_num;
   table *table_ptr;
   Boolean found;
   short low,high;

   table_num=-1;  /* default to use all tables from process's USE command */

   next_token();

   /* check for the FOR keyword clause */
   if(g_current_token==FOR_KW){
      next_token();
      if(g_current_token==TABLE_N){

         /* get and validate table number */
         sscanf(g_token_string,"#TABLE%hd",&table_num);
         table_ptr=proc_ptr->table_ptr;
         found=FALSE;
         for(i=0;i<proc_ptr->table_count;i++){
            if(table_num==table_ptr->num) found=TRUE;
            table_ptr=table_ptr->next_ptr;
            }
         if(!found){
            printf("%s %s must be specified in a USE TABLE command for this"
                   "process\n",g_errstr,g_token_string);
            return(FAILURE);
            }
         next_token();
         }
      else if(g_current_token==STRING){

         /* look for existing table in process's table list */
         found=FALSE;
         table_ptr=proc_ptr->table_ptr;
         for(i=0;i<proc_ptr->table_count;i++){
            if(strcmp(g_token_string,
                      g_info.table_ptr[table_ptr->num]->TableInfoPtr->TableName)==0){
               found=TRUE;
               table_num=table_ptr->num;
               }
            table_ptr=table_ptr->next_ptr;
            }
         if(!found){
            printf("%s %s must be specified in a USE TABLE command for this"
                   "process\n",g_errstr,g_token_string);
            return(FAILURE);
            }
         next_token();
         }
      else {
         printf("%s expecting either #TABLEn or existing table name\n",
                g_errstr);
         return(FAILURE);
         }
      } /* end if(g_current_token==FOR) */

   if(get_int_range(&low,&high)==FAILURE) return(FAILURE);

   /* apply record range to all tables or a single table as appropriate */
   table_ptr=proc_ptr->table_ptr;
   if(table_num==-1){

      /* apply to all tables */
      while(table_ptr!=NULL){
         table_ptr->min_range=low;
         table_ptr->max_range=high;
         table_ptr=table_ptr->next_ptr;
         }
      }
   else {

      /* apply to single specified table */
      for(i=0;i<proc_ptr->table_count;i++){
         if(table_num==table_ptr->num){
            table_ptr->min_range=low;
            table_ptr->max_range=high;
            }
         table_ptr=table_ptr->next_ptr;
         }
      }
   return(SUCCESS);
   } /* end: do_record_range() */


/***********************************************************************
** do_check_interval()
**
** This function will parse the CHECK_INTERVAL keyword who's syntax is:
**         CHECK_INTERVAL = <integer> { MINUTE[S] | HOUR[S] }
************************************************************************/
short do_check_interval(process_info *proc_ptr)
{
   if(next_token()!=EQUALS) {std_err(MISSING_EQUALS); return(FAILURE);}

   if(next_token()==NUMBER){
      proc_ptr->consist_check=atoi(g_token_string);
      switch(next_token()){
         case MINUTES:
            break;
         case HOURS:
            proc_ptr->consist_check*=60;
            break;
         default:
            printf("%s expecting MINUTES or HOURS\n",g_errstr);
            return(FAILURE);
         } /* end: switch */
      } /* end: if NUMBER */
   else {
      printf("%s expecting an integer >= 0\n",g_errstr);
      return(FAILURE);
      }

   if(next_token()!=SEMI_COLON){std_err(MISSING_SEMI_COLON);return(FAILURE);}

   return(SUCCESS);
   } /* end: do_check_interval() */


/***********************************************************************
** do_runtime()
**
** This function will parse the RUN_TIME keyword which has the following
** syntax:
**          RUNTIME = { <integer> { MINUTE[S] } }
**                    {           { HOUR[S]   } }
**                    { FOREVER                 }
**                    { UNTIL_DONE              }
**
************************************************************************/
short do_runtime(process_info *proc_ptr)
{
   if(next_token()!=EQUALS) {std_err(MISSING_EQUALS); return(FAILURE);}

   switch(next_token()){
      case NUMBER:
         switch(next_token()){
            case MINUTES:
               proc_ptr->list.duration=atoi(g_token_string);
               break;
            case HOURS:
               proc_ptr->list.duration=atoi(g_token_string)*60;
               break;
            default:
               printf("%s expecting MINUTES or HOURS\n",g_errstr);
               return(FAILURE);
            } /* end: switch */
         break;
      case FOREVER: proc_ptr->list.duration=0; break;
      case UNTIL_DONE: proc_ptr->list.duration=-1; break;
      default:
         printf("%s expecting an integer, FOREVER, or UNTIL_DONE\n",
                g_errstr);
         return(FAILURE);
      } /* end: switch */

   if(next_token()!=SEMI_COLON){std_err(MISSING_SEMI_COLON);return(FAILURE);}

   return(SUCCESS);
   } /* end: do_runtime() */


/***********************************************************************
** do_seed()
**
** This function will parse the SEED keyword which has the following syntax:
**                    SEED = { integer | RANDOM }
************************************************************************/
short do_seed(process_info *proc_ptr)
{
   if(next_token()!=EQUALS) {std_err(MISSING_EQUALS); return(FAILURE);}

   switch(next_token()){
      case NUMBER: proc_ptr->seed=atoi(g_token_string); break;
      case RANDOM_KW: proc_ptr->seed=rand(); break;
      default:
         printf("%s expecting an integer or RANDOM\n",g_errstr);
         return(FAILURE);
      } /* end: switch */

   if(next_token()!=SEMI_COLON){std_err(MISSING_SEMI_COLON);return(FAILURE);}

   return(SUCCESS);
   } /* end: do_seed() */

/***********************************************************************
** do_repeat()
**
** This function will parse the REPEAT command block which has the following
** following syntax:
**
**    REPEAT ( <count> TIMES             )  "{" <action-list> "}"
**           ( FOR <integer> { MINUTES } )
**           (               { HOURS   } )
**           ( FOREVER                   )
**
**   <action-list> is:
**  { <record-action>|<REPEAT-block> [ ; <record-action>|<REPEAT-block> ]...}
**  { <percent-action> [ ; <percent-action> ] ...                           }
**
************************************************************************/
item_desc *do_repeat(short *loop_number)
{
   list_desc *list_ptr;
   item_desc *item_ptr;

   /* allocate item description to be returned */
   item_ptr=(item_desc *)malloc(sizeof(item_desc));
   item_ptr->code=REPEAT_LOOP;
   (*loop_number)++;
   item_ptr->number=(*loop_number);
   item_ptr->next_ptr=NULL;

   /* allocate space for new list (loop) */
   list_ptr=(list_desc *)malloc(sizeof(list_desc));
   memset(list_ptr,0,sizeof(list_desc));
   item_ptr->list_ptr=list_ptr;

   /* parse remainder of REPEAT statement */
   switch(next_token()){
      case NUMBER:
         list_ptr->duration=-atoi(g_token_string);
         if(next_token()!=TIMES){
            printf("%s expecting TIMES keyword\n",g_errstr);
            free(list_ptr);
            free(item_ptr);
            return(NULL);
            }
         break;
      case FOR_KW:
         if(next_token()!=NUMBER){
            printf("%s expecting an integer number.\n",g_errstr);
            free(list_ptr);
            free(item_ptr);
            return(NULL);
            }
         list_ptr->duration=atoi(g_token_string);
         if(list_ptr->duration<=0){
            printf("%s time limit must be a positive integer.\n",g_errstr);
            free(list_ptr);
            free(item_ptr);
            return(NULL);
            }
         switch(next_token()){
            case HOURS: list_ptr->duration*=60; break;
            case MINUTES: break;
            default:
               printf("%s expecting either HOURS or MINUTES.\n",g_errstr);
               free(list_ptr);
               free(item_ptr);
               return(NULL);
            } /* end: switch */
         break;
      case FOREVER:
         list_ptr->duration=0;
         break;
      default:
         printf("%s expecting a time limit or repetition number.\n",
                g_errstr);
         free(list_ptr);
         free(item_ptr);
         return(NULL);
      } /* end: switch */

   if(next_token()!=BEGIN_BLOCK){
      printf("%s expecting '{' (open brace)\n",g_errstr);
      free(list_ptr);
      free(item_ptr);
      return(NULL);
      }

   /* process the action statements within this loop */
   while(next_token()!=END_BLOCK){
      if(do_command(list_ptr,loop_number)!=0){
         free(list_ptr);
         free(item_ptr);
         return(NULL);
         }
      } /* end: while */

   return(item_ptr);

   } /* end: do_repeat() */


/***********************************************************************
** do_command()
**
** This function adds items to a list descriptor creating a series of
** actions.
************************************************************************/
short do_command(list_desc *list_ptr,short *loop_number)
{
   item_desc *item_ptr;

   item_ptr=NULL;

   /* call the appropriate parse function based on the command */
   switch(g_current_token){
      case RANDOM_KW:
      case SEQUENTIAL:
      case VSBB:
      case ALTER_KW:
         item_ptr=do_record_action();
         break;
      case NUMBER:
         item_ptr=do_percent_action();
         break;
      case REPEAT:
         item_ptr=do_repeat(loop_number);
         break;
      default:
         printf("*** INTERNAL ERROR: invalid token in do_command()\n");
         printf("***                 token=%d  string='%s'\n",
                g_current_token,g_token_string);
      } /* end switch */

   /* check if the command just parsed was valid, if not then return */
   if(item_ptr==NULL) return(FAILURE);

   /* if first item in list then set up first and last pointers */
   if(list_ptr->first_item_ptr==NULL){
      list_ptr->first_item_ptr=item_ptr;
      list_ptr->last_item_ptr=item_ptr;
      }
   /* otherwise, add item to end of action item chain */
   else {
      list_ptr->last_item_ptr->next_ptr=item_ptr;
      list_ptr->last_item_ptr=item_ptr;
      }
   list_ptr->item_count++;
   return(SUCCESS);
   } /* end: do_command() */

/***********************************************************************
** init_all_processes()
**
** This function sets the default values for a processes info structure.
** It is really only used to set the ALL_PROCESSES info which is in turn
** used to initialize any individual process's structures
************************************************************************/
void init_all_processes(process_info *proc_ptr)
{
   /* initialize to zeroes */
   memset(proc_ptr,0,sizeof(process_info));

   /* set default values */

   proc_ptr->min_subset_size=1;
   proc_ptr->max_subset_size=5;
   proc_ptr->min_vsbb_size=10;
   proc_ptr->max_vsbb_size=20;
   proc_ptr->abort_percent=0;
   proc_ptr->dtc_percent=0;
   proc_ptr->min_concurrent_trans=1;
   proc_ptr->max_concurrent_trans=5;
   proc_ptr->min_trans_size=1;
   proc_ptr->max_trans_size=5;
   proc_ptr->trace_options=0;
   proc_ptr->debug_options=0;

   } /* end: init_all_processes() */


void init_process_n(process_info *default_ptr,process_info *proc_ptr)
{
   short i;
   Boolean first_time;
   table *dt_ptr;
   table *pt_ptr;
   table *previous_pt_ptr;

   memcpy(proc_ptr,default_ptr,sizeof(process_info));

	/* default all table info */
   first_time=TRUE;
   for(i=0;i<default_ptr->table_count;i++){
      if(first_time){
         proc_ptr->table_ptr=(table *)malloc(sizeof(table));
         pt_ptr=proc_ptr->table_ptr;
         dt_ptr=default_ptr->table_ptr;
         memcpy(pt_ptr,dt_ptr,sizeof(table));
         previous_pt_ptr=pt_ptr;
         first_time=FALSE;
         }
      else {
         pt_ptr=(table *)malloc(sizeof(table));
         dt_ptr=dt_ptr->next_ptr;
         memcpy(pt_ptr,dt_ptr,sizeof(table));
         previous_pt_ptr->next_ptr=pt_ptr;
         previous_pt_ptr=pt_ptr;
         }
      }

   } /* end:init_process_n() */

/***********************************************************************
** get_proc_info()
**
** This function gets the information about what a specific process is
** supposed to do according to any user supplied commands.
************************************************************************/
short get_proc_info(process_info *proc_ptr)
{
   short error;
   short dummy;  /* place holder used for get_int_range() calls */
   Boolean first_time;

   /* check for colon which should follow keyword */
   next_token();
   if(strcmp(g_token_string,":")!=0){
      std_err(MISSING_COLON);
      return(FAILURE);
      }

   /* LIKE PROCESSn statement (if used) must be first statement */
   next_token();
   if(g_current_token==LIKE){
      if(next_token()==PROCESS_N){
         sscanf(g_token_string,"#PROCESS%hd",&proc_ptr->like_process);

         /* validate the like process number */
         if(proc_ptr->like_process>=g_info.process_count){
            printf("%s only %d processes created, '#PROCESS%d' is not defined\n",
                   g_errstr,g_info.process_count,g_current_token);
            return(FAILURE);
            }

         /* initialize process to LIKEd process */
         init_process_n(g_info.process_ptr[proc_ptr->like_process],
                        proc_ptr);

         /* check for semi-colon which should end the LIKE statement */
         next_token();
         if(strcmp(g_token_string,";")!=0){
            std_err(MISSING_SEMI_COLON);
            return(FAILURE);
            }
      }

      else {
         printf("%s expecting #PROCESSn where 'n' is a defined process"
                " number\n",g_errstr);
         return(FAILURE);
         }
      next_token();
      }

   /* process the statements */
   first_time=TRUE;
   while((g_current_token!=PROCESS_N)&&(g_current_token!=CLEANUP)&&
         (g_current_token!=EOF)){
      switch(g_current_token){
         case ABORT_KW:
            next_token();
            if(g_current_token!=EQUALS){
            	std_err(MISSING_EQUALS);
            	return(FAILURE);
            }
            if(next_token()!=NUMBER){
               printf("%s expecting a percentage from 0%% to 100%%\n",g_errstr);
               return(FAILURE);
               }
            proc_ptr->abort_percent=atoi(g_token_string);
            if(proc_ptr->abort_percent>100){
               printf("%s expecting a percentage from 0%% to 100%%\n",g_errstr);
               return(FAILURE);
               }
            next_token();
            if(strcmp(g_token_string,"%")!=0){
               printf("%s expecting a percent sign '%%'\n",g_errstr);
               return(FAILURE);
               }
            if(next_token()!=SEMI_COLON){std_err(MISSING_SEMI_COLON);return(FAILURE);}
            break;
         case DTC_TRANSACTIONS:
            next_token();
            error=get_int_range(&proc_ptr->dtc_percent,&dummy);
            break;
         case TRANSACTION_SIZE:
            next_token();
            error=get_int_range(&proc_ptr->min_trans_size,
                                &proc_ptr->max_trans_size);
            break;
         case CONCURRENT_CONNECTIONS:
            next_token();
            error=get_int_range(&proc_ptr->min_concurrent_trans,
                                &proc_ptr->max_concurrent_trans);
            break;
         case SUBSET_SIZE:
            next_token();
            error=get_int_range(&proc_ptr->min_subset_size,
                                &proc_ptr->max_subset_size);
            break;
         case VSBB_SIZE:
            next_token();
            error=get_int_range(&proc_ptr->min_vsbb_size,
                                &proc_ptr->max_vsbb_size);
            break;
         case USE: error=do_use(proc_ptr); break;
         case RECORD_RANGE: error=do_record_range(proc_ptr); break;
         case RUNTIME: error=do_runtime(proc_ptr); break;
         case SEED: error=do_seed(proc_ptr); break;
         case CHECK_INTERVAL: error=do_check_interval(proc_ptr); break;
//			case SETTESTPOINT: error=do_SetTestpoint(

         case RANDOM_KW:
         case SEQUENTIAL:
         case NUMBER:
         case REPEAT:
            if(first_time){
               proc_ptr->list_count=0;
               /*>>>> really need to free() all list item's storage */
               memset(&proc_ptr->list,0,sizeof(list_desc));
               proc_ptr->list.duration=-1; /* default to UNTIL_DONE */
               first_time=FALSE;
               }
            error=do_command(&proc_ptr->list,&proc_ptr->list_count);
            break;

         default:
            printf("%s Unknown command '%s' or command not allowed in this "
                   "section.\n",g_errstr,g_token_string);
            error=TRUE;
            break;
         } /* end: switch(g_current_token) */

      if(error) return(FAILURE);
      next_token();
      } /* end: while */

   if(g_current_token==EOF) return(EOF);
   return(SUCCESS);
   } /* end: get_proc_info() */

/**********************************************************************
** parse_commands()
**
** This function will read in the user's command file and parse all
** commands and keywords found in it.  All information is stored in
** globals structures dynamically allocated by functions called
** from this function.
***********************************************************************/
short parse_commands()
{
   process_info all_processes;
   short i;
   short proc_num;

   /* first token must be 'STARTUP' section name */
   if(next_token()!=STARTUP) {
      printf("%s 'STARTUP' section name must be before any other "
             "commands.\n",g_errstr);
      return(FAILURE);
      }

   /* process STARTUP: section */
   if(get_startup_info()==FAILURE) return(FAILURE);

   /* create SQL tables, allocate work files, etc. */
/* if(init_startup()!=0) return(FAILURE);
*/
   /* set process defaults */
   init_all_processes(&all_processes);

   /* next, check for the optional ALL_PROCESSES section and handle it */
   if(g_current_token==ALL_PROCESSES) {
      if(get_proc_info(&all_processes)==FAILURE) return(FAILURE);
      } /* end: if ALL_PROCESSES */

   /* initialize all PROCESS_N structures with ALL_PROCESSES structure */
   for(i=0;i<g_info.process_count;i++){
      init_process_n(&all_processes,g_info.process_ptr[i]);
      }

   /* next, check for any PROCESSn sections and loop handling each one */
   while(g_current_token==PROCESS_N){

      /* get the process number */
      sscanf(g_token_string,"#PROCESS%hd",&proc_num);
      if(proc_num>=g_info.process_count){
         printf("%s only %d processes created, '#PROCESS%d' is not defined\n",
                g_errstr,g_info.process_count,g_current_token);
         return(FAILURE);
         }

      /* get all the information supplied by the user for the process */
      if(get_proc_info(g_info.process_ptr[proc_num])==FAILURE) {
         return(FAILURE);
         }
      } /* end: while PROCESS_N */

   /* handle the LIKE PROCESS N statements here */
   for(i=0;i<g_info.process_count;i++){
      proc_num=g_info.process_ptr[i]->like_process;
      if(proc_num!=0){

         /* copy the 'like process' into this processes info structure */
         memcpy(g_info.process_ptr[i],g_info.process_ptr[proc_num],
                sizeof(process_info));
         }
      } /* end: for */

   /* lastly, check for the optional CLEANUP section and process it */
   if(g_current_token==CLEANUP){
		// >>> Currently, there is no clean-up processing
      } /* end: if CLEANUP */

   /*>>>> need to handle extra tokens as errors */

   return(SUCCESS);
   } /* end: parse_commands() */
