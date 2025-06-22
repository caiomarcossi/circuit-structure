from circuit import Circuit
import sys

def get_int_input(prompt):
	while True:
		try:
			return int(input(prompt))
		except ValueError:
			print("Invalid number. Please enter a valid integer.")

def get_float_input(prompt):
	while True:
		try:
			return float(input(prompt))
		except ValueError:
			print("Invalid value. Please enter a valid number.")

def get_component_type(prompt):
	while True:
		comp_type=input(prompt).strip().upper()
		if comp_type in ["R", "V"]:
			return comp_type
		else:
			print("Invalid type. Use 'R' for resistor or 'V' for voltage source.")

circuit=Circuit()

nodes=get_int_input("How many nodes does the circuit have? ")
for i in range(1, nodes + 1):
	for j in range(i + 1, nodes + 1):
		has_connection=input(f"Is there any connection between node {i} and node {j}? (y/n) ").strip().lower()
		if has_connection=="y":
			components_count=get_int_input(f"How many components are between node {i} and node {j}? ")
			components=[]
			for k in range(1, components_count + 1):
				comp_type=get_component_type(f"Component {k}. Type 'R' for resistor, 'V' for voltage source: ")
				comp_value=get_float_input("Value: ")
				components.append({"type": comp_type, "value": comp_value})
			circuit.addConnection(i, j, components)
print("\nCircuit connections:")
circuit.showCircuit()
while True:
	try:
		ref_node=int(input("Choose the reference node (default is 0): "))
		if ref_node in circuit.nodesList:
			break
		else:
			print(f"Node {ref_node} is not in the circuit. Try again.")
	except ValueError:
		ref_node=0
		break
print("\nSolving circuit")
try:
	voltages, currents=circuit.solve(referenceNode=ref_node)
	print("\nNode voltages:")
	for node, voltage in voltages.items():
		print(f"  Node {node}: {voltage:.2f} V")
	print("\nComponent currents:")
	for (node1, node2, idx), current in currents.items():
		comp=circuit.nodesList[node1][node2][idx]
		comp_type=comp["type"]
		comp_value=comp["value"]
		if comp_type.lower()=="r":
			voltage_drop=voltages[node1] - voltages[node2]
			print(f"Resistor of {comp_value}Ω between nodes {node1} and {node2}:")
			print(f"  Voltage drop: {voltage_drop:.2f} V")
			print(f"  Current: {current:.2f} A")
		elif comp_type.lower()=="v":
			print(f"Voltage source of {comp_value}V between nodes {node1} and {node2}:")
			print(f"  Voltage drop: {comp_value:.2f} V")
			print("  Current: not calculated")
except Exception as e:
	print(f"Error solving circuit: {e}")