## Assembler
Given a path to a file written in assembly, `Assembler.py` creates a file in the same directory that is in binary code. The binary code is executable on the "Hack Plattform" hardware built in the hardware part of the course described in ch.1-5 of <a href='http://www.nand2tetris.org/book.php'>this course</a>.

The assembly language here is a simple language described <a href='http://www.nand2tetris.org/chapters/chapter%2004.pdf'>here</a>. Files in this language have extension `.asm`. Binary output files have the same name, and the extension '.hack'.

To run:

```
python Assembler.py path/to/file.asm
```
This should result in a new executable binary file `path/to/file.hack`
