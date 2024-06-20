# *************************************************************
# Original Autor:  M. Thaler (Modul BSY)
# *************************************************************

CMP=        gcc
CMPFLAGS=   -Wall
LDFLAGS=
EXENAMES=   aaaa.e
FNAME=      ProcA6
LIBNAME=

$(EXENAMES):	$(FNAME).o
	$(CMP)  $(FNAME).o $(LIBNAME) $(LDFLAGS) -o $@

.c.o:
	$(CMP) -c $(CMPFLAGS) $<

.cc.o:
	$(CMP) -c $(CMPFLAGS) $<

clean:
	rm -f *.o $(EXENAMES)

all:
	@make clean
	@make

