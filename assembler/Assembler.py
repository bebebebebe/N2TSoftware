from os import path
from sys import argv
import re

import AssemblerConstants

script, filename = argv

class Assembler():
	def __init__(self, filepath):
		self.filepath = filepath
		self.outputPath = None

		self.symbolTable = {}
		self.storeL = 0
		self.storeA = 16

		self.setOutputPath()
		self.buildSymbolTable()
		self.writeOutput()

	def setOutputPath(self):
		filepath, fileext = path.splitext(self.filepath)
		self.outputPath = filepath + '.hack'

	def buildSymbolTable(self):
		file = open(self.filepath)
		for line in file:
			command = self.cleanLine(line)
			if command == '': continue

			parsed = self.parse(command)
			if parsed['type'] == 'L':
				self.symbolTable[parsed['symbol']] = self.storeL
			else:
				self.storeL += 1

		file.close()

	def writeOutput(self):
		file = open(self.filepath)
		output = open(self.outputPath, 'w')

		for line in file:
			command = self.cleanLine(line)
			if command == '': continue

			parsed = self.parse(command)
			if parsed['type'] == 'L': continue
			binary = self.toBinary(parsed)
			outputLine = binary + '\n'
			output.write(outputLine)

		file.close()
		output.close()

	def toBinaryC(self, parsed):
		binary = '111' + AssemblerConstants.comp(parsed['comp']) + AssemblerConstants.dest(parsed['dest']) + AssemblerConstants.jump(parsed['jump'])

		return binary

	def toBinaryA(self, parsed):
		if parsed['symbol']:
			string = parsed['symbol']
			digits = self.symToNum(parsed['symbol'])
		else:
			digits = parsed['number']

		binary = bin(int(digits))
		binary = binary[2:] # remove leading '0b'

		return '0' * (16 - len(binary)) + binary

# check: returns a string or a number?
	def symToNum(self, symbol):
		if symbol in AssemblerConstants.reservedSym:
			return AssemblerConstants.reservedSym[symbol]

		if symbol in self.symbolTable:
			return self.symbolTable[symbol]

		self.symbolTable[symbol] = self.storeA
		self.storeA += 1
		return self.symbolTable[symbol]

	def toBinary(self, parsed):
		if parsed['type'] == 'C':
			return self.toBinaryC(parsed)
		
		if parsed['type'] == 'A':
			return self.toBinaryA(parsed)

	def cleanLine(self, line):
		line = line.partition('//')[0]
		return line.strip()

	def parse(self, string):
		pattern_L = re.compile(AssemblerConstants.REGEX_L)
		pattern_A = re.compile(AssemblerConstants.REGEX_A)
		pattern_C = re.compile(AssemblerConstants.REGEX_C)

		L_COMMAND = pattern_L.match(string)
		if L_COMMAND:
			return {
				'type': 'L',
				'symbol': L_COMMAND.group('symbol')
			}

		A_COMMAND = pattern_A.match(string)
		if A_COMMAND:
			return {
				'type': 'A',
				'symbol': A_COMMAND.group('symbol'),
				'number': A_COMMAND.group('number')
				}

		C_COMMAND = pattern_C.match(string)
		if C_COMMAND:
			comp = C_COMMAND.group('comp')
			dest = C_COMMAND.group('dest') if C_COMMAND.group('dest') else 'null'
			jump = C_COMMAND.group('jump') if C_COMMAND.group('jump') else 'null'

			return {
				'type': 'C',
				'dest': dest,
				'comp': comp,
				'jump': jump
			}

		raise Exception('invalid syntax: ', string)

a = Assembler(filename)
