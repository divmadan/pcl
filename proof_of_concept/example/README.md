Some pointers:

- Swig can be used to generate bindings from multiple languages using the `example.i` interpreted file, which we can configure to support our header files.
- Currently, the `Makefile` generates bindings for Python, Javascript and Octave, can add more.

- Run `make` to generate bindings from the `example.i` file.
- For Javascript:
    - Javascript requires node-gyp build tool: `sudo npm install -g node-gyp`
    - To use the extension you need to 'require' it in the Javascript source file: `require("./build/Release/example")`
- For octave, it makes use of `mkoctfile`
- The repo also contains some output files.
- Files to look into: `example.i`,  `Makefile`
- Website link, for documentation, download, etc.: [link](http://www.swig.org/)
- For full list of supported languages: [link](http://www.swig.org/compat.html#SupportedLanguages)
