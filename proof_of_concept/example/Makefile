# standard compile options for the c++ executable
FLAGS = -fPIC

# the python interface through swig
PYTHONI = -I/usr/include/python3.6/
PYTHONL = -Xlinker -export-dynamic

# default super-target
all: 
	g++ -fPIC -c example.cpp -o example.o
	swig -c++ -python -o example_wrap.cxx example.i 
	g++ $(FLAGS) $(PYTHONI) -c example_wrap.cxx -o example_wrap.o
	g++ $(PYTHONL) $(LIBFLAGS) -shared example.o example_wrap.o -o _example.so

	#javascript
	node-gyp configure
	swig -c++ -javascript -node example.i
	node-gyp build

	#octave
	swig -octave -c++ -o example_wrap.cxx example.i
	mkoctfile example_wrap.cxx example.cpp -o example.oct
