import numpy as np
import pylab
from qiskit.quantum_info import SparsePauliOp
from qiskit import QuantumCircuit
from qiskit import Aer
from qiskit.circuit.library import NLocal, CCXGate, CRZGate, RXGate, TwoLocal
from qiskit.circuit import Parameter
from qiskit.quantum_info import Statevector
from qiskit_ibm_runtime import QiskitRuntimeService, Estimator
from qiskit.algorithms.optimizers import SPSA
from math import pi

reference_circuit = TwoLocal(2, "rx", "cz", entanglement="linear", reps=1)
theta_list = [pi / 2, pi / 3, pi / 3, pi / 2]

reference_circuit = reference_circuit.bind_parameters(theta_list)

theta = Parameter("θ")
var_ = NLocal(
    num_qubits=5,
    rotation_blocks=[RXGate(theta), CRZGate(theta)],
    entanglement_blocks=CCXGate(),
    entanglement=[ [0, 1, 2], [0, 2, 3], [4, 2, 1], [3, 1, 0] ],
    reps=2,
    insert_barriers=True,
)

variational_form=var_.assign_parameters(np.random.random(ansatz.num_parameters))
Statevector.from_instruction(ran_ansatz)

def cost_function_vqe(theta):
    observable = SparsePauliOp.from_list([("XX", -1/2), ("YY", -1/2),("ZZ", -1/2)])

    reference_circuit = TwoLocal(2, "rx", "cz", entanglement="linear", reps=1)
    theta_list = [pi / 2, pi / 3, pi / 3, pi / 2]

    reference_circuit = reference_circuit.bind_parameters(theta_list)

    ansatz = reference_circuit.compose(variational_form)

    backend = service.backend("ibmq_qasm_simulator")
    
    estimator = Estimator(session=backend)
    job = estimator.run(ansatz, observable, theta)
    values = job.result().values

    return values



initial_theta = np.ones(2)
optimizer = SPSA()

optimizer_result = optimizer.minimize(fun=cost_function_vqe, x0=initial_theta)

optimal_parameters = optimizer_result.x
print(optimal_parameters)