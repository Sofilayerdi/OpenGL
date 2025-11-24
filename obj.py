class Obj(object):
	def __init__(self, filename):
		# Asumiendo que el archivo es un formato .obj
		with open(filename, "r") as file:
			lines = file.read().splitlines()
			
		self.vertices = []
		self.texCoords = []
		self.normals = []
		self.faces = []
		
		for line in lines:
			# Si la linea no cuenta con un prefijo y un valor,
			# seguimos a la siguiente la linea

			line = line.rstrip()

			try:
				prefix, value = line.split(" ", 1)
			except:
				continue
			
			# Dependiendo del prefijo, parseamos y guardamos
			# la informacion en el contenedor correcto
			
			if prefix == "v": # Vertices
				vert = list(map(float, filter(None, value.split(" "))))
				self.vertices.append(vert)
				
			elif prefix == "vt": # Coordenadas de textura
				vts = list(map(float,value.split(" ")))
				self.texCoords.append([vts[0],vts[1]])
				
			elif prefix == "vn": # Normales
				norm = list(map(float,value.split(" ")))
				self.normals.append(norm)
				
			elif prefix == "f":  # Caras
				face = []
				verts = value.split()
				for vert in verts:
					if not vert:
						continue

					parts = vert.split("/")

					v = int(parts[0]) if parts[0] != "" else 0

					if len(parts) > 1 and parts[1] != "":
						vt = int(parts[1])
					else:
						vt = 0  # 0 = sin UV

					if len(parts) > 2 and parts[2] != "":
						vn = int(parts[2])
					else:
						vn = 0  # 0 = sin normal

					face.append([v, vt, vn])

				self.faces.append(face)
