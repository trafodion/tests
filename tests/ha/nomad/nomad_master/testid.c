#include "defines.h"
#include "include.h"
#include "table.h"
#include "mstruct.h"
#include "globals.h"
#include "sqlproc.h"
#include "ODBCcommon.h"

/***********************************************************************
** put_testid_info()
**
** This function creates the testid file and writes the various pieces
** of information to it.
************************************************************************/
void put_testid_info()
{
   char testid_file[_MAX_PATH];
   FILE *fp;

   sprintf(testid_file,"%s/%s_NOMAD/TEST%s.txt",g_info.work_volume,
           g_info.testid,g_info.testid);
   fp=fopen(testid_file,"w");
   if(fp==NULL){
      /*>>> handle error somehow */
      printf("%s unable to open %s\n",g_errstr,testid_file);
      return;
      }
   fprintf(fp,"%d process count\n",g_info.process_count);
   fprintf(fp,"%d tables created\n",g_info.table_count);
   fprintf(fp,"%s.SEABASE.%sT table prefix\n",g_info.catalog,
           g_info.testid);

   /*>>> have to do something about listing tables that weren't... */
   /*>>> ... created by NOMAD but were used */
   fprintf(fp,"0 tables used (for now always zero)\n");
   fprintf(fp,"%s  SQL catalog name\n",g_info.catalog);
   fprintf(fp,"SEABASE  SQL schema name\n");
   fprintf(fp,"%s  command file for this test\n",getenv("STDIN"));

   fclose(fp);
   } /* end: put_testid_info() */


/***********************************************************************
** get_testid_info()
**
** This function returns a pointer to the testid info structure.  It will
** search the TESTIDS file for an entry matching the supplied testid and
** return the information found in the TESTIDS file for that testid.  If
** the testid is not found then a NULL pointer is returned.
************************************************************************/
testid_info *get_testid_info(char *testid)
{
   FILE *fp;
   Boolean found;
   char volume[_MAX_PATH];
   char testid_file[_MAX_PATH];
   testid_info *ptr;
   char temp_testid[3];

   /* open TESTIDS file */
   fp=fopen(g_testid_file,"r+");

   /* if file doesn't exist, testid can't be in it so, return NULL pointer */
   if(fp==NULL) return(NULL);

   /* scan it for the current testid */
   found=FALSE;
   fget_s(g_input_line,MAX_LINE,fp);
   while(!feof(fp)){
	   sscanf(g_input_line,"%s",temp_testid);
      sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s",volume);

      /* if found, then allocate and return testid_info structure */
      if(strcmp(testid,temp_testid)==0){
         found=TRUE;
         ptr=(testid_info *)malloc(sizeof(testid_info));
         fclose(fp);
         strcpy(ptr->test_vol,volume);
         sprintf(testid_file,"%s/%s_NOMAD/TEST%s.txt",volume,testid,testid);
         fp=fopen(testid_file,"r");

         if(fp==NULL){

            /* we're unable to open this testid's file eventhough it has */
            /* an entry in NOMAD's list of all testids so, something is */
            /* out of whack here.  it'll be fixed by resetting this testid */
            /* and deleting any old files that might be lying around */
            printf("%s unable to open %s\n",g_errstr,testid_file);
            printf("%s Resetting testid '%s'\n",g_indent,testid);
//            cleanup_testid(testid);
            return(NULL);
            }

         sscanf(fget_s(g_input_line,MAX_LINE,fp),"%hd ",&ptr->process_count);
         sscanf(fget_s(g_input_line,MAX_LINE,fp),"%hd ",&ptr->tables_created);
         sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s ",ptr->table_prefix);
         sscanf(fget_s(g_input_line,MAX_LINE,fp),"%hd ",&ptr->tables_used);
         /*>>> have to do something about listing tables that weren't... */
         /*>>> ... created by NOMAD but were used */
         sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s ",ptr->sql_catalog);
         sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s ",ptr->sql_schema);
         sscanf(fget_s(g_input_line,MAX_LINE,fp),"%s ",ptr->infile);
         fclose(fp);
         return(ptr);
         }

      fget_s(g_input_line,MAX_LINE,fp);
      }

   /* if not found, then return a NULL pointer */
   fclose(fp);
   return(NULL);
   } /* end: get_testid_info() */


/***********************************************************************
** cleanup_testid()
**
** This function will first stop any process from the given testid which
** might still be executing, then reports to the user anything out of
** the ordinary.  It will then delete all files and SQL tables created for
** the testid.
************************************************************************/
void cleanup_testid(char *testid)
{
   short i;
//   short error;
//   boolean done;
   char search_pattern[_MAX_PATH];
//   char filename[_MAX_PATH];
//   short filename_len;
//   short searchid;
   testid_info *ptr;
   char command_line[SQL_MAX_COMMAND_LENGTH];
	RETCODE rc;

   printf("***INFO: dropping all tables/views/indexes for testid '%s'\n",
          testid);

   printf("***INFO: dropping SQL schema '%s.%s_SCHEMA'\n",
   		g_info.catalog,testid);
   printf("***WARNING: using CLEANUP because of bugs in DROP SCHEMA CASCADE\n");
   sprintf(command_line,"CLEANUP SCHEMA %s.%s_SCHEMA",
   		g_info.catalog,testid);
	rc=SQLExecDirect(ghstmt,command_line,SQL_NTS);
	// display any errors but ignore them and keep running
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecDirect")){
		printf("%s return code=%d on %s\n",g_errstr,rc,command_line);
		LogAllErrors(ghenv,ghdbc,ghstmt);
		}

   // purge all files on the NOMAD directory for this testid
   sprintf(search_pattern,"%s/%s_NOMAD/*.*",g_info.work_volume,testid);
   printf("***INFO: purging all files in '%s'\n",search_pattern);
   sprintf(search_pattern,"rm -rf %s/%s_NOMAD",g_info.work_volume,testid);
   system(search_pattern);

   } // end: delete_testid()


/***********************************************************************
** init_testid()
**
** This function performs some initializations for a testid.  If it is
** a reuse of a previously used testid then some clean-up is done and
** the testid is reset.  An SQL schema is created for the testid.
************************************************************************/
void init_testid()
{
   char command_line[SQL_MAX_COMMAND_LENGTH];
	testid_info *ptr;
	RETCODE rc;
	char TempDir[_MAX_PATH];
	int status;
	errno=0;

   /* get information on testid */
   //ptr=get_testid_info(g_info.testid);

   /* if the testid doesn't already exist then add it */
   //if(ptr==NULL) add_testid(g_info.testid);
   //else delete_testid(g_info.testid);

   // otherwise cleanup everything associated with the
   // previous run of this testid and reset it
   cleanup_testid(g_info.testid);

   printf("***INFO: using SQL catalog '%s'\n",g_info.catalog);

   /* create SQL schema */
   printf("***INFO: creating SQL schema '%s.%s_SCHEMA'\n",
		g_info.catalog);
   sprintf(command_line,"CREATE SCHEMA %s.%s_SCHEMA",
      g_info.catalog,g_info.testid);
	rc=SQLExecDirect(ghstmt,command_line,SQL_NTS);
	if(!CHECKRC(SQL_SUCCESS,rc,"SQLExecDirect")){
		LogAllErrors(ghenv,ghdbc,ghstmt);
      }

   /* create Work directory for this test ID */
	sprintf(TempDir,"%s/%s_NOMAD",g_info.work_volume,g_info.testid);
   printf("***INFO: creating work directory '%s'\n",TempDir);
	if(mkdir(TempDir,S_IRWXU|S_IRWXG|S_IRWXO)!=0){
		printf("***ERROR:  unable to create NOMAD's directory '%s'  errno='%s'\n",
			TempDir,strerror(errno));
		}
} /* end: init_testid() */

