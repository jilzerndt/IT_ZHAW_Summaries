# *************************************************************
# Original Autor:  M. Thaler (Modul BSY)
# *************************************************************

CMP=        gcc
CMPFLAGS=   -Wall -g
LDFLAGS=
EXENAME=    ProcA7.e
FNAME=      ProcA7
EXENAMC=    ChildProcA7.e
FNAMC=      ChildProcA7
LIBNAME=
LIBNAME=

compile: $(EXENAME) $(EXENAMC)

$(EXENAME): $(FNAME).o
	$(CMP)  $(FNAME).o $(LIBNAME) $(LDFLAGS) -o $@

$(EXENAMC):	$(FNAMC).o
	$(CMP)  $(FNAMC).o $(LIBNAME) $(LDFLAGS) -o $@

.c.o:
	$(CMP) -c $(CMPFLAGS) $<

.cc.o:
	$(CMP) -c $(CMPFLAGS) $<

clean:
	rm -f core *.o $(EXENAME) $(EXENAMC)

all:
	@make clean
	@make
