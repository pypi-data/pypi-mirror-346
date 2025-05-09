from QBenchAnalyzer.literal import METRIC_NUMBER_QUBITS, METRIC_NUMBER_GATES, METRIC_NUMBER_2_GATES, METRIC_DEPTH, \
    METRIC_CONSECUTIVE_2_GATES, METRIC_AVG_2_GATES_X_QUBIT, METRIC_PARALLELISM, METRIC_CRITICAL_DEPTH, \
    METRIC_ENTANGLEMENT_RATIO, METRIC_PROGRAM_COMMUNICATION, METRIC_ENTANGLEMENT_VARIANCE
from QBenchAnalyzer.metrics_generator import generate_metrics
from qiskit import QuantumCircuit
import pytest
import math

pytestmark = pytest.mark.parametrize("circuit,expected_metrics",
                                     [
                                         ("qaoa_vanilla_03", {
                                             METRIC_NUMBER_QUBITS: 3,
                                             METRIC_NUMBER_GATES: 15,
                                             METRIC_NUMBER_2_GATES: 6,
                                             METRIC_DEPTH: 11,
                                             METRIC_CONSECUTIVE_2_GATES: 2,
                                             METRIC_AVG_2_GATES_X_QUBIT: 4.0,
                                             METRIC_PARALLELISM: 2/11,
                                             METRIC_CRITICAL_DEPTH: 1,
                                             METRIC_ENTANGLEMENT_RATIO: 6/15,
                                             METRIC_PROGRAM_COMMUNICATION: 1,
                                             METRIC_ENTANGLEMENT_VARIANCE: 0,
                                         }),
                                         ("qaoa_vanilla_04", {
                                             METRIC_NUMBER_QUBITS: 4,
                                             METRIC_NUMBER_GATES: 26,
                                             METRIC_NUMBER_2_GATES: 12,
                                             METRIC_DEPTH: 17,
                                             METRIC_CONSECUTIVE_2_GATES: 3,
                                             METRIC_AVG_2_GATES_X_QUBIT: 6.0,
                                             METRIC_PARALLELISM: 3/17,
                                             METRIC_CRITICAL_DEPTH: 5/6,
                                             METRIC_ENTANGLEMENT_RATIO: 12/26,
                                             METRIC_PROGRAM_COMMUNICATION: 1,
                                             METRIC_ENTANGLEMENT_VARIANCE: 0,
                                         }),
                                         ("hamiltonian_04", {
                                             METRIC_NUMBER_QUBITS: 4,
                                             METRIC_NUMBER_GATES: 25,
                                             METRIC_NUMBER_2_GATES: 6,
                                             METRIC_DEPTH: 13,
                                             METRIC_CONSECUTIVE_2_GATES: 2,
                                             METRIC_AVG_2_GATES_X_QUBIT: 3.0,
                                             METRIC_PARALLELISM: 4/13,
                                             METRIC_CRITICAL_DEPTH: 1,
                                             METRIC_ENTANGLEMENT_RATIO: 6/25,
                                             METRIC_PROGRAM_COMMUNICATION: 0.5,
                                             METRIC_ENTANGLEMENT_VARIANCE: math.log(5, 10) / 4,
                                         }),
                                         ("hamiltonian_05", {
                                             METRIC_NUMBER_QUBITS: 5,
                                             METRIC_NUMBER_GATES: 32,
                                             METRIC_NUMBER_2_GATES: 8,
                                             METRIC_DEPTH: 16,
                                             METRIC_CONSECUTIVE_2_GATES: 2,
                                             METRIC_AVG_2_GATES_X_QUBIT: 3.2,
                                             METRIC_PARALLELISM: 1/4,
                                             METRIC_CRITICAL_DEPTH: 1,
                                             METRIC_ENTANGLEMENT_RATIO: 8/32,
                                             METRIC_PROGRAM_COMMUNICATION: 0.4,
                                             METRIC_ENTANGLEMENT_VARIANCE: math.log(5.8, 10) / 5,
                                         }),
                                         ("grover_noancilla_1reg_2", {
                                             METRIC_NUMBER_QUBITS: 2,
                                             METRIC_NUMBER_GATES: 6,
                                             METRIC_NUMBER_2_GATES: 0,
                                             METRIC_DEPTH: 4,
                                             METRIC_CONSECUTIVE_2_GATES: 0,
                                             METRIC_AVG_2_GATES_X_QUBIT: 0,
                                             METRIC_PARALLELISM: 0.5,
                                             METRIC_CRITICAL_DEPTH: 0,
                                             METRIC_ENTANGLEMENT_RATIO: 0,
                                             METRIC_PROGRAM_COMMUNICATION: 0,
                                             METRIC_ENTANGLEMENT_VARIANCE: 0,
                                         }),
                                         ("grover_noancilla_1reg_4", {
                                             METRIC_NUMBER_QUBITS: 4,
                                             METRIC_NUMBER_GATES: 142,
                                             METRIC_NUMBER_2_GATES: 52,
                                             METRIC_DEPTH: 93,
                                             METRIC_CONSECUTIVE_2_GATES: 2,
                                             METRIC_AVG_2_GATES_X_QUBIT: 26,
                                             METRIC_PARALLELISM: 49/279,
                                             METRIC_CRITICAL_DEPTH: 48/52,
                                             METRIC_ENTANGLEMENT_RATIO: 52/142,
                                             METRIC_PROGRAM_COMMUNICATION: 1,
                                             METRIC_ENTANGLEMENT_VARIANCE: math.log(81, 10) / 4,
                                         })
                                     ])


class ITest:
    def generate_path_file(self, file_name):
        return f"./test/circuits/{file_name}.qasm"

    def generate_metrics(self, circuit):
        qc = QuantumCircuit.from_qasm_file(self.generate_path_file(circuit))
        metrics = generate_metrics(qc)
        return metrics

    def assert_metric(self, circuit, expected_metrics, metric):
        metrics = self.generate_metrics(circuit)
        assert round(metrics[metric], 9) == round(expected_metrics[metric], 9)


class TestBasicMetrics(ITest):
    def test_n_qubits_metrics(self, circuit, expected_metrics):
        self.assert_metric(circuit, expected_metrics, METRIC_NUMBER_QUBITS)

    def test_n_gates_metrics(self, circuit, expected_metrics):
        self.assert_metric(circuit, expected_metrics, METRIC_NUMBER_GATES)

    def test_n_2gates_metrics(self, circuit, expected_metrics):
        self.assert_metric(circuit, expected_metrics, METRIC_NUMBER_2_GATES)

    def test_depth_metrics(self, circuit, expected_metrics):
        self.assert_metric(circuit, expected_metrics, METRIC_DEPTH)

    def test_consecutive_2gates_metrics(self, circuit, expected_metrics):
        self.assert_metric(circuit, expected_metrics, METRIC_CONSECUTIVE_2_GATES)

    def test_avg_2gates_x_qubit_metrics(self, circuit, expected_metrics):
        self.assert_metric(circuit, expected_metrics, METRIC_AVG_2_GATES_X_QUBIT)


class TestDerivedMetrics(ITest):
    def test_parallelism_metric(self, circuit, expected_metrics):
        self.assert_metric(circuit, expected_metrics, METRIC_PARALLELISM)

    def test_critical_depth_metric(self, circuit, expected_metrics):
        self.assert_metric(circuit, expected_metrics, METRIC_CRITICAL_DEPTH)

    def test_entanglement_ratio_metric(self, circuit, expected_metrics):
        self.assert_metric(circuit, expected_metrics, METRIC_ENTANGLEMENT_RATIO)

    def test_program_communication_metric(self, circuit, expected_metrics):
        self.assert_metric(circuit, expected_metrics, METRIC_PROGRAM_COMMUNICATION)

    def test_entanglement_variance_metric(self, circuit, expected_metrics):
        self.assert_metric(circuit, expected_metrics, METRIC_ENTANGLEMENT_VARIANCE)
