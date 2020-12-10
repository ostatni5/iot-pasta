

START /b python fmixer.py > nul

START /b python steamer.py > nul

START /b python mixer.py > nul
timeout 1
START /b python pipeline.py > nul

START /b python dryer.py > nul

START /b python belt.py > nul

START /b python lift.py > nul
timeout 1
START /b python scale.py > nul

START /b python cooler.py > nul
timeout 1
START /b python orderer.py > nul

@REM START /b python silos.py > nul
@REM timeout 1
@REM START python logger.py


