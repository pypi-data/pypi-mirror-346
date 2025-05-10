# Quantum Noise Analysis
**Note**
The project is still under development. Please be patient for now and raise any query or feature directly to mail joshimohit@bhu.ac.in

## Resource estimation with the package
```python
from qiskit_noise_analysis import ResourceEstimation

resource_estimation = ResourceEstimation()
report = resource_estimation.get_estimation(
    circuits = [ circ1, circ2, ....], 
    basis_gates= [''].
    circuit_names= ['circ1', 'circ2'])

```


### Implementation Example
```python
# create quantum circuit
def generate_random_circuit(n_qubits, depth, random_seed=42):
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

resource_estimation = ResourceEstimation()
report = resource_estimation.get_estimation(circuits = [ generate_random_circuit(4,5, 42) , generate_random_circuit(4,5,43) ], circuit_names= ['circ1', 'circ2'])
resource_estimation.plot()


```