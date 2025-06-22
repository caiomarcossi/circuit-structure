import numpy as np

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
				print(f"Connected to node {neighbor} with: ")
				for comp in components:
					comp_type=comp.get("type")
					value=comp.get("value")
					print(f"Type: {comp_type}. Value: {value}.")

	def solve(self, referenceNode):
		nodeIndex={}
		i=0
		for node in self.nodesList.keys():
			if not node==referenceNode:
				nodeIndex[node]=i
				i+=1
		nodeIndex[referenceNode]=i
		numNodes=len(self.nodesList)
		conductanceArray=np.zeros((numNodes, numNodes))
		voltageVector=np.zeros(numNodes)
		for node1 in self.nodesList:
			for node2, components in self.nodesList[node1].items():
				index1=nodeIndex[node1]
				index2=nodeIndex[node2]
				if index1 >= index2:
					continue
				for component in components:
					if component['type'].lower()=='r':
						conductance=1/component['value']
						if not node1==referenceNode:
							conductanceArray[index1][index1]+=conductance
						if not node2==referenceNode:
							conductanceArray[index2][index2]+=conductance
						if not node1==referenceNode and not node2==referenceNode:
							conductanceArray[index1][index2] -= conductance
							conductanceArray[index2][index1] -= conductance
		for node1 in self.nodesList:
			for node2, components in self.nodesList[node1].items():
				for component in components:
					if component['type'].lower()=='v':
						if node1==referenceNode and not node2==referenceNode:
							index2=nodeIndex[node2]
							voltageVector[index2]=component['value']
							conductanceArray[index2, :]=0
							conductanceArray[index2][index2]=1
						elif node2==referenceNode and not node1==referenceNode:
							index1=nodeIndex[node1]
							voltageVector[index1]=component['value']
							conductanceArray[index1, :]=0
							conductanceArray[index1][index1]=1
						else:
							raise NotImplementedError("Voltage sources between non-reference nodes not supported yet")
		refIndex=nodeIndex[referenceNode]
		reducedArray=np.delete(conductanceArray, refIndex, axis=0)
		reducedArray=np.delete(reducedArray, refIndex, axis=1)
		reducedVector=np.delete(voltageVector, refIndex)

		# Resolução do sistema
		solution=np.linalg.solve(reducedArray, reducedVector)

		voltages={}
		i=0
		for node in self.nodesList.keys():
			if not node==referenceNode:
				voltages[node]=solution[i]
				i+=1
			else:
				voltages[node]=0

		# Cálculo das correntes
		currents={}
		for node1 in self.nodesList:
			for node2, components in self.nodesList[node1].items():
				index1=nodeIndex[node1]
				index2=nodeIndex[node2]
				if index1>index2:
					continue
				for i,component in enumerate(components):
					if component['type'].lower()=='r':
						currents[(node1, node2, i)]=(voltages[node1] - voltages[node2])/component['value']
					elif component['type'].lower()=='v':
						currents[(node1, node2, i)]=None

		return voltages, currents
