import sys, os, struct, shutil, re

print sys.argv

if (len(sys.argv) != 2):
	quit()

data = sys.argv[1]
dataMacrodetails = os.path.join(data, "targets", "macrodetails")

def ensureDirectory(path):
	directory = os.path.dirname(path)

	if not os.path.exists(directory):
		os.makedirs(directory)

def importMakehumanData(path):
	if os.path.isdir(path):
		for sub in os.listdir(path):
			importMakehumanData(os.path.join(path, sub))
	else:
		if path.endswith("base.obj") or path.endswith(".png"):
			newPath = os.path.join("data", path[len(data) + 1:])

			print newPath

			ensureDirectory(newPath)
			shutil.copyfile(path, newPath)
		elif path.startswith(dataMacrodetails) and path.endswith(".target"):
			newPath = os.path.join("data", path[len(data) + 1:] + "b")

			print newPath

			ensureDirectory(newPath)

			inputFile = open(path, "r")
			outputFile = open(newPath, "wb")

			try:
				lines = inputFile.readlines()

				for line in lines:
					if not line.startswith("#"):
						values = line.split()
						outputFile.write(struct.pack("<i", int(values[0])))
						outputFile.write(struct.pack("<f", float(values[1])))
						outputFile.write(struct.pack("<f", float(values[2])))
						outputFile.write(struct.pack("<f", float(values[3])))
			except:
				print "Unexpected error:", sys.exc_info()
			finally:
				inputFile.close()
				outputFile.close()

importMakehumanData(data)
