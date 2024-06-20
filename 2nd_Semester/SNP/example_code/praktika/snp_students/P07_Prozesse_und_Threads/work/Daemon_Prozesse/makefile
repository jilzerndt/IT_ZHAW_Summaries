# *************************************************************
# Original Autor:  M. Thaler (Modul BSY)
# *************************************************************

CMP=        gcc
CMPFLAGS=   -Wall -g -std=gnu99
EXENAMES=   MrTimeDaemon.e
EXENAMEC=   WhatsTheTimeMr.e
EXENAMEP=   PlapperMaul.e
LIBNAME=    

compile:    $(EXENAMES) $(EXENAMEC) $(EXENAMEP)

$(EXENAMES):    MrTimeDaemon.o IPsockCom.o Daemonizer.o TimeDaemon.o
	$(CMP) $(CMPFLAGS) MrTimeDaemon.o IPsockCom.o Daemonizer.o TimeDaemon.o $(LIBNAME) -o $(EXENAMES)

$(EXENAMEC):    WhatsTheTimeMr.o IPsockCom.o
	$(CMP) $(CMPFLAGS) WhatsTheTimeMr.o IPsockCom.o $(LIBNAME) -o $(EXENAMEC)

$(EXENAMEP):    PlapperMaul.o
	$(CMP) $(CMPFLAGS) PlapperMaul.o $(LIBNAME) -o $(EXENAMEP)

.c.o:
	$(CMP) -c $(CMPFLAGS) $<

.cc.o:
	$(CMP) -c $(CMPFLAGS) $<

clean:
	rm -f $(EXENAMEC) $(EXENAMES)  $(EXENAMEP)
	rm -f *.o

all:
	@make clean
	@make
