# minimal required settings
SNP_TESTLIB   := $(if $(SNP_TESTLIB),$(SNP_TESTLIB),$(wildcard ~/snp/testlib))
SNP_DOXYFILE  := $(if $(SNP_DOXYFILE),$(SNP_DOXYFILE),$(wildcard ~/snp/Doxyfile))

# directories to create (and remove upon cleanup)
CREATEDIRS    := bin doc

# list of derived file names from the source names
OBJECTS       := $(SOURCES:%.c=%.o)    # list of gcc -c  ... produced *.o files
DEPS          := $(SOURCES:%.c=%.d)    # list of gcc -MD ... produced *.d files
TSTOBJECTS    := $(TSTSOURCES:%.c=%.o) # list of gcc -c  ... produced *.o files
TSTDEPS       := $(TSTSOURCES:%.c=%.d) # list of gcc -MD ... produced *.d files
TSTTARGET     := $(CURDIR)/tests/runtest

# shared libs
TSTLIBDIR := $(SNP_TESTLIB)/lib
TSTINCDIR := $(SNP_TESTLIB)/include

# full path to the target
FULLTARGET    := $(CURDIR)/$(TARGET)

# commands and flags
CC            = gcc
CFLAGS        = -std=c99 -Wall -pedantic -g
CPPFLAGS      = -MD -Isrc -Itests -I$(TSTINCDIR) -DTARGET=$(FULLTARGET)
LDFLAGS       = -static

# targets which get always visited (without checking any up-to-date state)
.PHONY: default clean test doc install mkdir

# targets
default: $(FULLTARGET)
	@echo "#### $< built ####"

$(FULLTARGET): mkdir $(OBJECTS) Makefile
	$(LINK.c) -o $@ $(OBJECTS) $(LIBS)

clean:
	$(RM) $(TARGET) $(OBJECTS) $(DEPS) $(TSTTARGET) $(TSTOBJECTS) $(TSTDEPS) $(wildcard */*~ *~ tests/*.txt)
	$(RM) -r $(CREATEDIRS)
	@echo "#### $@ done ####"

doc:
	doxygen $(SNP_DOXYFILE) > /dev/null
	@echo "#### $@ done ####"

test: $(TSTTARGET)
	(cd tests; $(TSTTARGET))
	@echo "#### $< executed ####"

$(TSTTARGET): $(FULLTARGET) $(TSTOBJECTS)
	$(LINK.c) -o $(TSTTARGET) $(TSTOBJECTS) $(LIBS) -lcunit -L$(TSTLIBDIR) -lsnptest
	@echo "#### $@ built ####"


# create needed directories (ignoring any error)
mkdir:
	-mkdir -p $(CREATEDIRS)

# read in the gcc -MD ... produced dependencies (ignoring any error)
-include $(DEPS) $(TSTDEPS)
