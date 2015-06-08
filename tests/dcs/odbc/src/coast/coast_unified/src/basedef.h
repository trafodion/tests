#ifndef __BASEDEFH      /* this prevents multiple copies of this... */
#define __BASEDEFH      /* ...include file from being #included... */
/**************************************
** the basic constants and typedefs 
**************************************/

#define SUCCESS       0
#define FAILURE      -1

#define NULL_STRING  '\0'

// extension for master files of correct results
#define MASTER_EXT   "ref"

#define MAX_FILENAME_LENGTH      256

#define DIVIDER_STRING "*===============================================*\n"
typedef short HLOGT;

typedef short TrueFalse;                         

typedef enum PassFail {PASSED, FAILED} PassFail;



#endif
