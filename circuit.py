class Circuit:
	def __init__(self):
		self.nodesList={}

	def addConnection(self, node1, node2, components):
		if node1 not in self.nodesList:
			self.nodesList[node1]={}
		if node2 not in self.nodesList:
			self.nodesList[node2]={}
		self.nodesList[node1][node2]=components
		self.nodesList[node2][node1]=components

	def showCircuit(self):
		for node, connections in self.nodesList.items():
			print(f"node {node}")
			for neighbor, components in connections.items():
				print("Connected to node {neighbor} with: \n")
				for comp in components:
					print(comp+"\n")