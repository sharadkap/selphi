@rem | Downloads the test run method identifiers from HipTest, then runs the python script that applies them to the results file,
@rem | (Assuming that the test suite has already been run), then finally, uploads the newly-converted file to HipTest again. 
@rem | To use: run this, and input the Test Run ID when prompted.

@set /p testid="Enter Test Run ID for this run: "

ruby -v
call hiptest-publisher --config=config.txt --test-run-id=%testid%
python hipnabler.py
call hiptest-publisher --config=config.txt --test-run-id=%testid% --push=REGR.tap

echo "(Zero Tests Imported usually means an incorrect Test Run ID or a Formatting error.)"

pause
