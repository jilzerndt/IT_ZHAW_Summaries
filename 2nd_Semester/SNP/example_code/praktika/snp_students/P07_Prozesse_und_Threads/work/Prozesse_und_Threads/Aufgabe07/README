
Enable core dumps     ->   ulimit -c unlimited
Disable core dumps    ->   ulimit -c 0

Das core File lesen mit gdb:

	gdb -c core ChildProgA8.e


!!!! Wichtig !!!!

Wenn sie ein Linux benutzen, das standardmaessig ABRT (Automatic Bug
Reporting Tool) verwendet (z.B. Fedora, Centos, etc.), muss 
/proc/sys/kernel/core_pattern auf "core" gesetzt werden, damit ein 
core File erzeugt wird

    echo core > /proc/sys/kernel/core_pattern

Wenn ihr System SE-Linux verwendet (z.B. Fedora) , laesst sich core_pattern
nicht auf einfache Art setzen, verzichten sie in diesem Fall auf die
Erzeugung des "core" Files. 
