START /b python orderer.py 

timeout 1
START /b python fmixer.py
timeout 1
START /b python steamer.py 
timeout 1
START /b python mixer.py 
timeout 1
START /b python pipeline.py 
timeout 1
START /b python dryer.py 
timeout 1
START /b python belt.py 
timeout 1
START /b python lift.py 
timeout 1
START /b python scale.py 
timeout 1
START /b python cooler.py 
timeout 1
START /b python silos.py 

timeout 1
START python logger.py


