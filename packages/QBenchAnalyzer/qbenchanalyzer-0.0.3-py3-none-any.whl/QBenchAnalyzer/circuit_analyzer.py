from .literal import METRIC_PROGRAM_COMMUNICATION, METRIC_ENTANGLEMENT_VARIANCE, METRIC_ENTANGLEMENT_RATIO, \
    METRIC_CRITICAL_DEPTH, METRIC_PARALLELISM
from .metrics_generator import generate_metrics
import matplotlib.pyplot as plt

MARKERS = ['o', '^', 's', 'd', 'X']


def analyze_circuit_group_structural(circuit_generator, min_num_qubits, max_num_qubits, img_file_name="test.png",
                                     img_file_path="test/images/"):
    interval = range(min_num_qubits, max_num_qubits+1)
    all_metrics = [generate_metrics(circuit_generator.generate_qiskit_circuit(i)) for i in interval]
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.set_xticks(interval)
    ax.set_xticklabels(map(str, interval))
    metrics_to_analyze = [METRIC_PROGRAM_COMMUNICATION, METRIC_ENTANGLEMENT_VARIANCE, METRIC_ENTANGLEMENT_RATIO,
                          METRIC_CRITICAL_DEPTH, METRIC_PARALLELISM]
    for i in range(len(metrics_to_analyze)):
        metric = metrics_to_analyze[i]
        marker = MARKERS[i]
        ax.plot(interval, [metrics[metric] for metrics in all_metrics], marker=marker, label=metric)
    ax.legend()
    ax.set_xlabel("Number of qubits")
    ax.set_ylabel("Metric value")
    fig.suptitle(circuit_generator.name, fontsize=14)
    fig.savefig(img_file_path + img_file_name)
