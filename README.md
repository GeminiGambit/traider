# traider

To make the shell scripts executable, you must run for the first time:
chmod +x build_traider
chmod +x traider
export PATH=$PATH:$PWD

then download intraday free historical data and install dependencies
./build_traider -I -s -i

To run:
./traider
