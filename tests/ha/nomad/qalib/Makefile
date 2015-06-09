#------------------------------------------------
# Makefile to create QA's libraries
#------------------------------------------------

# distribution directories
DISTROOT = $(PWD)
LIB = $(DISTROOT)/lib
OBJ = $(DISTROOT)/obj
#------------------------------------------------

CREATE_PATH ?= mkdir -p $(@D)

SRC = .
INCDIRS =	-I $(SRC) -I /usr/include -I /usr/include/odbc

TARGETS =	$(LIB)/libqa.so

CPP_COMPILER = g++
C_FLAGS = -O0 -g -DDEBUG -DNA_LINUX -fPIC -Wno-write-strings
CPP_FLAGS = $(C_FLAGS)
LIBDIRS = -L $(LIB)
LIBS =
LINK_FLAGS =

C_COMPILE_LINK		= gcc -o $@ $(C_FLAGS) $(INCDIRS) $<
CPP_COMPILE_LINK	= $(CPP_COMPILER) $(CPP_FLAGS) -o $@  $(INCDIRS) $(LIBDIRS) $(LIBS) \
					-L $(LIB) $<
C_COMPILE_ONLY    = gcc -c -o $@ $(C_FLAGS) $(INCDIRS) $<
CPP_COMPILE_ONLY  = $(CPP_COMPILER) -c -o $@ $(CPP_FLAGS) $(INCDIRS) $<

LINK_SHARED_LIB = $(CPP_COMPILER) -shared -o $@ $(LINK_FLAGS) $(LIBDIRS) $(LIBS)
LINK_STATIC_LIB = ar -cvq $@

#---------------------------------------------------
all: $(TARGETS)

# build the QA shared library
$(LIB)/libqa.so: \
	$(OBJ)/bitlib.o \
	$(OBJ)/log.o \
	$(OBJ)/ODBCcommon.o \
	$(OBJ)/rtnstat.o \
	$(OBJ)/sqlutil.o \
	$(OBJ)/table.o \
	$(OBJ)/util.o
		@$(CREATE_PATH)
		@echo '*** Creating library $(@F) ***'
		@$(LINK_SHARED_LIB) \
			$(OBJ)/bitlib.o $(OBJ)/log.o $(OBJ)/ODBCcommon.o \
			$(OBJ)/rtnstat.o $(OBJ)/sqlutil.o $(OBJ)/table.o $(OBJ)/util.o

# compile all the object files
$(OBJ)/bitlib.o: $(SRC)/bitlib.c $(SRC)/bitlib.h
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/log.o: $(SRC)/log.c $(SRC)/log.h
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/ODBCcommon.o: $(SRC)/ODBCcommon.c $(SRC)/ODBCcommon.h
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/rtnstat.o: $(SRC)/rtnstat.c $(SRC)/rtnstat.h
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/util.o: $(SRC)/util.c $(SRC)/util.h
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/sqlutil.o: $(SRC)/sqlutil.c $(SRC)/sqlutil.h
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)

$(OBJ)/table.o: $(SRC)/table.c $(SRC)/table.h
		@$(CREATE_PATH)
		@echo '*** Compiling $(<F) ***'
		@$(C_COMPILE_ONLY)


# >>>This should be replaced by automatically generating dependence
# >>>files using some form of the follow:
# >>>CC_DEPEND_IT     = cd $(@D); $(CC_CC) -WM $(CC_CFLAGS) $(ALL_INCLUDEDIR_LIST) \
# >>>                   $< | sed -e 's@\(.*\)/.o:@$(@D)/\1.o $(@D)/\1.d:@' >$@

#---------------------------------------------------
clean:
	@echo '***** Cleaning *****'
	-rm $(LIB)/libqa.so \
		$(OBJ)/bitlib.o \
		$(OBJ)/log.o \
		$(OBJ)/ODBCcommon.o \
		$(OBJ)/rtnstat.o \
		$(OBJ)/sqlutil.o \
		$(OBJ)/table.o \
		$(OBJ)/util.o
