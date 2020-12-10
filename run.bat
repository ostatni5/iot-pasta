START /b python orderer.py 

ping 127.0.0.1 -n 2 > nul
START /b python fmixer.py
ping 127.0.0.1 -n 2 > nul 
START /b python steamer.py 
ping 127.0.0.1 -n 2 > nul 
START /b python mixer.py 
ping 127.0.0.1 -n 2 > nul 
START /b python pipeline.py 
ping 127.0.0.1 -n 2 > nul 
START /b python dryer.py 
ping 127.0.0.1 -n 2 > nul 
START /b python belt.py 
ping 127.0.0.1 -n 2 > nul 
START /b python lift.py 
ping 127.0.0.1 -n 2 > nul 
@REM START /b python scale.py 
@REM START /b python cooler.py 
@REM START /b python silos.py 

ping 127.0.0.1 -n 2 > nul 
START python logger.py


