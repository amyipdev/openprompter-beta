echo "Welcome to OpenPrompter. The current directory is $(pwd). Ensuring directory is set correctly..."
cd $(dirname "${BASH_SOURCE[0]}")
echo "Directory has been reset to $(pwd)."
echo "Loading venv..."
source ../venv/bin/activate
echo "Loading server..."
ts=$(python3 -c "import datetime; print(int(datetime.datetime.timestamp(datetime.datetime.utcnow())),end='')")
echo "Time logged as $ts. Launching discov..."
python3 discov.py > "discov-$ts.log" 2>&1 &
echo "Started discov. Launching app..."
python3 app.py > "app-$ts.log" 2>&1 &
echo "Started app. Launching pygame as interactive..."
python3 pygsets.py 2>&1 | tee "pyg-$ts.log"
echo "Something happened. Check pygame logs..."
kill $(jobs -p)
