# Quantum Noise Analysis
**Note**
The project is still under development. Please raise any query or feature request directly to mail joshimohit@bhu.ac.in.

## Resource estimation with the package
```python
from qiskit_noise_analysis import resource_estimation

report = resource_estimation.get_estimation(
    circuits = [ circ1, circ2, ....], 
    basis_gates= ["id", "rz", "sx", "x", "cx"],
    circuit_names= ['circ1', 'circ2'])

```


### Implementation Example
```python
from qiskit_noise_analysis import resource_estimation

from qiskit import QuantumCircuit

qc1 = QuantumCircuit(4)
qc1.h([0,1,2,3])
qc1.cx(0,1)
qc1.t([1,2,3])

qc2 = QuantumCircuit(4)
qc2.t([0,1,2,3])
qc2.cx(0,1)

report = resource_estimation.get_estimation(circuits=[qc1, qc2], circuit_names =['qc1','qc2'])

```

You can also use resource_estimation.demo() to see the comparison of two random circuits.