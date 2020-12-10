START /b python orderer.py > nul

timeout 1
START /b python fmixer.py > nul
timeout 1
START /b python steamer.py > nul
timeout 1
START /b python mixer.py > nul
timeout 1
START /b python pipeline.py > nul
timeout 1
START /b python dryer.py > nul
timeout 1
START /b python belt.py > nul
timeout 1
START /b python lift.py > nul
timeout 1
START /b python scale.py > nul
timeout 1
START /b python cooler.py > nul
timeout 1
START /b python silos.py > nul

timeout 1
START python logger.py


