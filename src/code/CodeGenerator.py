from data.FileHandler import FileHandler
from data.ARFF import ARFF, Attribute
from weka.Weka import WEKA
from data.CSV import CSV

class CodeGenerator:
	def __init__(self):
		""

	def float2String(self, _float):
		return str(_float)


	def unrollMultiplication(self, _name, _in, _weights):
		lIn = len(_weights)
		lOut = len(_weights[0])

		code = "\tfloat " + _name + "[" + str(lOut) + "] = {"
		for n in range(lOut):
			for m in range(lIn):
				code += _in + "[" + CodeGenerator().float2String(m) + "]*" + CodeGenerator().float2String(_weights[m][n])
				if m<lIn-1:
					code += "+"
				elif n<lOut-1:
					code += ", "
		code += "};\n"

		return code
		

	def generateDummyMain(self, _callType, _numIn):
		code = "\nint main(void)\n{\n"
		code += "\t" + _callType + " r = " + self.generateFunctionCall("predict", ["1.2"]*_numIn) + ";\n\t"
		code += "return r;\n}\n"

		return code


	def generateForLoop(self, _layer, _itType, _itName, _start, _end):
		tab = "\t"*_layer
		code = tab + _itType  + " " + _itName + ";\n"
		code += tab + "for(" + _itName + "=" + str(_start) + "; " + _itName + "<" + str(_end) + "; " + _itName + "++)\n"

		return code


	def generateFunctionHeader(self, _name, _attributes):
		code = ""
		vNames = list(_attributes.keys())
		for i in range(0, len(_attributes)):
			vName = vNames[i]
			vType = _attributes[vName]

			if i==0:
				code += vType + " " + _name + "("
			else:
				code += vType + " " + vName
				if i<len(_attributes)-1:
					code += ","
		code += ")"

		return code


	def generateFunctionCall(self, _name, _attributes):
		code = _name + "(" + ", ".join(_attributes) + ")"
		
		return code


	def generateArray(self, _type, _name, _values): # CAUTION: string array
		code = _type + " " + _name + "[" + str(len(_values)) + "] = {";
		for i in range(0, len(_values)):
			code += _values[i]
			if i<len(_values)-1:
				code += ", "

		code += "};"

		return code 


	def generateMatrix(self, _type, _name, _values): # CAUTION: float array
		yMax = len(_values)
		xMax = len(_values[0])
		code = _type + " " + _name + "[" + str(yMax) + "][" + str(xMax) +"] = {\n";

		for y in range(0, yMax):
			code += "\t{"
			for x in range(0, xMax):
				code += str(_values[y][x])
				if x<xMax-1:
					code += ", "
			if y<yMax-1:
				code += "},\n"
			else:
				code += "}\n"
		code += "};"
		return code


	def findMax(self, _type):
		code = "unsigned int findMax(" + _type + " *_values, unsigned int _size)\n{\n"
		code += "\t" + _type + " max = _values[0];\n"
		code += "\tunsigned int index = 0;\n" 
		code += self.generateForLoop(1, "unsigned int", "i", 1, "_size") + "\t{\n"
		code += "\t\tif(_values[i]>max)\n\t\t{\n"
		code += "\t\t\tmax = _values[i];\n"
		code += "\t\t\tindex = i;\n\t\t}\n"
		code += "\t}\n"
		code += "\treturn index;\n"
		code += "}"

		return code


	def export(self, _training, _model, _id, _out):
		csv = CSV()
		csv.load(_training)
		csv.convertToARFF("tmp/train_arff.arff", False)		
		attributes = csv.findAttributes(0)

		WEKA().train(_model, "tmp/train_arff.arff", "_" + _id)
		data = "\n".join(FileHandler().read("tmp/raw_" + _id + ".txt"))

		_model.exportCode(data, csv, attributes, _out, _training)