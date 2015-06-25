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
