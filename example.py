from circuit import *

circuit=Circuit()
nodes=int(input("How many nodes does have in the circuit?"))
for i in range(1, nodes+1):
	for j in range(i+1, nodes+1):
		hasConnection=input(f"Is there any connection between node {i} and node {j}? y/n").strip().lower()
		if hasConnection=="y":
			try:
				componentsCount=int(input(f"How many components are between node {i} and node {j}?"))
			except:
				print("erro de valor")
				sys.exit()
			components=[]
			for k in range(1, componentsCount+1):
				comp=input(f"component {k}")
				components.append(comp)
			circuit.addConnection(i, j, components)

circuit.showCircuit()