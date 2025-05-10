

# def resource_estimation(circuits, basis_gates=None, resource_set=None, circuit_names=None):

#     res_est = ResourceEstimation()
#     # report = res_est.get_estimation(circuits, basis_gates=None, resource_set=None, circuit_names=None)

#     return res_est



class ResourceEstimation:
    """
    Class to estimate the resource of the circuit

    Methods
    -------
    __init__()
        Return None

    generate_report(circuits, basis_gates, resources)
        Return None

    transpile(circ, basis_gates)
        Return transpiled_circuit

    estimate(transpiled_circ, resources):
        Return estimation

    demo()
        Return None
   
    """
    def __init__(self):
        """
        
        """
        self.estimation = []

        # storing intermediate data for debugging purpose
        self.circuits = []
        self.transpiled_circuits = []


        # default values
        self.default_circuits = [self.generate_random_circuit(4,5,42), self.generate_random_circuit(4,5,43), self.generate_random_circuit(4,5,44)]
        self.default_basis_gates = ["rz", "sx", "x", "cx"]   # Note 'reset', 'delay' and 'measure' are always present in transpilation
        # self.default_basis_gates = ['id', 'x', 'y', 'z', 'h', 's', 'sdg', 'cx', 'cy', 'cz', 'swap', 'i']
        self.default_resource_set = self.default_basis_gates
        self.clifford_gates = {'id', 'x', 'y', 'z', 'h', 's', 'sdg', 'cx', 'cy', 'cz', 'swap', 'i'} # verify the set and expand accordingly


        # used in estimate fucntion

    def update_estimation(self, estimation):
        self.estimation = estimation

    def get_raw_result(self):   
        return self.estimation
    
    def get_transpiled_circuits(self):
        return self.transpiled_circuits 
    
    def update_transpiled_circuits(self, transpiled_circuits):
        self.transpiled_circuits = transpiled_circuits
    
    def get_circuits(self):
        return self.circuits
    
    def update_circuits(self, circuits):
        self.circuits = circuits
    
    def generate_random_circuit(self, n_qubits, depth, random_seed=42):
        from qiskit.circuit.random import random_circuit
        max_operands = 2

        qc = random_circuit(
            num_qubits=n_qubits,
            depth=depth,
            max_operands=2,
            measure=True,
            seed=random_seed  
        )

        return qc

    def demo(self, n_circuits=3):
        """
        a demo function to show the functionality of class
        """
        circuit_list = [self.generate_random_circuit(4,5,42+i) for i in range(n_circuits)]
        self.get_estimation(circuit_list, self.default_basis_gates, self.default_resource_set)


            

    def validate_circuit_list(self, circuits):
        """
        Validate circuit (Implement Later)    
        """
        from qiskit import QuantumCircuit

        for circ_name, circ in circuits.items():
            if not isinstance(circ, QuantumCircuit):
                raise ValueError(f'{circ_name} is not a valid quantum circuit.')
            
        return True
    
    def validate_gate_list(self,  gates):
        """
        Validate basis gates (Implement Later)    
        maybe valid gate by transpiling in basis set
        """
        # from qiskit.circuit import Instruction

        # for gate in gates:
        #     if not isinstance(gate, Instruction):
        #         raise ValueError(f'{gate} is not a valid quantum gate.')
            
        return True
    
    def transpile(self, circ, basis_gates):
        from qiskit.providers.fake_provider import GenericBackendV2, generic_backend_v2
        from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

        # used in transpile function
        optimization_level = {'no_opt':0, 'light':1,'heavy':2,'vheavy':3}    # acc to generate preset manager

        backend = GenericBackendV2(num_qubits=circ.num_qubits, basis_gates=basis_gates )
        transpiled_circ = generate_preset_pass_manager(optimization_level['heavy'], backend=backend).run(circ)

        return transpiled_circ

    def is_clifford(self, gate):
        """Check if a single gate is Clifford."""
        from qiskit.quantum_info import Clifford
        from qiskit import QuantumCircuit


        temp_qc = QuantumCircuit(gate.num_qubits, gate.num_clbits)
        temp_qc.append(gate, qargs = [i for i in range(gate.num_qubits)], cargs=None)
    
        try:
            Clifford(temp_qc)
            return True
        except Exception:
            return False

    def estimate(self, circ, resource_set):
        gate_count = 0
        for gate, count in circ.count_ops().items():
            gate_count +=count
        estimation = {'depth': circ.depth(), 'gate_count':gate_count}
        estimation['gates'] = {}

        estimation['gates'].update({gates : 0 for gates in resource_set})
        estimation['gates']['others'] = {}
        estimation['resource_count'] = {'clifford':0, 'non_clifford':0, 'total':0}

        for instr in circ.data:
            gate = instr.operation

            gate_name = gate.name
            if gate_name == 'measure': continue

            if gate_name in resource_set:
                estimation['gates'][gate_name] += 1
            else: 
                if gate_name in estimation['gates']['others'].keys():
                    estimation['gates']['others'][gate_name] += 1
                else:
                    estimation['gates']['others'][gate_name] = 1   

            # checking clifford and non-clifford resources
            if self.is_clifford(gate):
                estimation['resource_count']['clifford'] += 1
            elif not self.is_clifford(gate):
                estimation['resource_count']['non_clifford'] +=1
            estimation['resource_count']['total'] += 1


        return estimation


    def prepare_visualization_dict(self, estimation):
        import pandas as pd

        # Build a flat dictionary for each circuit
        flattened = {}

        for circ_name, circ_data in estimation.items():
            flat = {}

            # Add depth and gate_count
            flat['depth'] = circ_data['depth']
            # flat['gate_count'] = circ_data['gate_count']

            # Add resource counts
            flat.update(circ_data['resource_count'])

            # # Add gates (exclude 'others')
            # flat.update({k: v for k, v in circ_data['gates'].items() if k != 'others'})
            # flat.update(circ_data['gates']['others'])

            # Store
            flattened[circ_name] = flat

        # Convert to DataFrame
        df = pd.DataFrame(flattened)

        # Reset index to have 'Resources' column
        df = df.reset_index().rename(columns={'index': 'Resources'})

        # Filter out rows where both circ1 and circ2 are zero (implement later)
        # df = df[~((df['circ1'] == 0) & (df['circ2'] == 0))]
        # # Select columns that start with 'circ'
        # circuit_cols = [col for col in df.columns if col.startswith('circ')]

        # # Keep rows where at least one circuit column is not zero
        # df = df[(df[circuit_cols] != 0).any(axis=1)]


        return df



    def describe(self, estimation):
        print(self.prepare_visualization_dict(estimation))


    def plot(self, estimation=None):
        if estimation is None:
            estimation = self.get_raw_result()
        
        import matplotlib.pyplot as plt

        # Convert to DataFrame
        # df = pd.DataFrame(self.prepare_visualization_dict(self.estimation))

        # Reset index to have 'Resources' column
        # df = df.reset_index().rename(columns={'index': 'Resources'})

        # Filter out rows where all circuits are zero
        # df = df.loc[~(df.drop(columns='Resources') == 0).all(axis=1)]

        df = self.prepare_visualization_dict(self.get_raw_result())

        # Set Resources as index for plotting
        df_plot = df.set_index('Resources')

        # Plot
        ax = df_plot.plot(kind='bar', figsize=(10, 6))
        plt.title('Comparison of Circuit Resources')
        plt.ylabel('Count')
        plt.xlabel('Resources')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.legend(title='Circuit')
        plt.show()


        
    def get_estimation(self, circuits= None, circuit_fn=None, basis_gates=None, resource_set=None, circuit_names=None):

        """
        Generates resource estimation report and stores in self.raw_report()

        Args:
            circuits (list) : list of circuits
            basis_gate (list) : list of basis gates in which circuit will be transpiled
            resources (list) : list of resources for which estimation will be done i.e. how much of each resources are their in given circuit

        Return:
            None

        Raise: 
            ValueError: If input is not correct

        """
        # check for necessary argument
        if circuits is None and circuit_fn is None:
            raise ValueError('Give either one circuit or circuit fn to compare')
        
        # think of way to give circuit and circuit_fn in one input

        # initialize the inputs with defaults inputs (if necessary)
        basis_gates = basis_gates if basis_gates is not None else self.default_basis_gates
        resource_set = resource_set if resource_set is not None else self.default_resource_set 
        circuit_names = circuit_names if circuit_names is not None else [f'circ{i}' for i in range(len(circuits))]

        circuits = dict(zip(circuit_names, circuits))
        self.update_circuits(circuits)
        

        # validate the input (check for each circuit)
        self.validate_circuit_list(circuits)     # make it work with circuit fn also where all the parameters are checked.
        self.validate_gate_list(basis_gates)
        self.validate_gate_list(resource_set)        

        # process circuit 
        transpiled_circuits = {circ_name: self.transpile(circ, basis_gates) for circ_name, circ in circuits.items()}
        self.update_transpiled_circuits(transpiled_circuits)

        # estimate resources
        estimation = {circ_name: self.estimate(transpiled_circ, resource_set) for circ_name, transpiled_circ in transpiled_circuits.items()}
        self.update_estimation(estimation)

        self.plot(estimation)

        return self.describe(estimation)



resource_estimation = ResourceEstimation()
        
