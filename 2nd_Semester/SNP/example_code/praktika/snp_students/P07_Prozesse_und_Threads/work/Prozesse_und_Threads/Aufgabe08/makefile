# *************************************************************
# Original Autor:  M. Thaler (Modul BSY)
# *************************************************************

CMP=        gcc -std=gnu99
CMPFLAGS=   -Wall
LDFLAGS=
EXENAME1=   ProcA8_1.e
FNAM1=      ProcA8_1.o
EXENAME2=   ProcA8_2.e
FNAM2=      ProcA8_2.o 
EXENAME3=   ProcA8_3.e 
FNAM3=      ProcA8_3.o workerUtils.o
LIBNAME=

compile:	$(EXENAME1) $(EXENAME2) $(EXENAME3)

$(EXENAME1):	$(FNAM1)
	$(CMP)  $(CMPFLAGS) $(FNAM1) $(LIBNAME) $(LDFLAGS) -o $@

$(EXENAME2):	$(FNAM2)
	$(CMP)  $(CMPFLAGS) $(FNAM2) $(LIBNAME) $(LDFLAGS) -o $@

$(EXENAME3):	$(FNAM3)
	$(CMP)  $(CMPFLAGS) $(FNAM3) $(LIBNAME) $(LDFLAGS) -o $@

.c.o:
	$(CMP) -c $(CMPFLAGS) $<

.cc.o:
	$(CMP) -c $(CMPFLAGS) $<

clean:
	rm -f *.o $(EXENAME1) $(EXENAME2) $(EXENAME3) 

all:
	@make clean
	@make
