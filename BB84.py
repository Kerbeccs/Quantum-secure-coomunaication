import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import random
from math import pi

class QuantumSecureCommunication:
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')
    
    def generate_bb84_key(self, n_bits=8):
        alice_bits = [random.randint(0, 1) for _ in range(n_bits)]
        alice_bases = [random.randint(0, 1) for _ in range(n_bits)]
        bob_bases = [random.randint(0, 1) for _ in range(n_bits)]
        
        qubits = []
        for i in range(n_bits):
            qr = QuantumRegister(1)
            cr = ClassicalRegister(1)
            qc = QuantumCircuit(qr, cr)
            
            if alice_bits[i] == 1:
                qc.x(0)
            
            if alice_bases[i] == 1:
                qc.h(0)
                
            if bob_bases[i] == 1:
                qc.h(0)
            
            qc.measure(0, 0)
            qubits.append(qc)
        
        job = execute(qubits, self.backend, shots=1)
        results = job.result()
        
        bob_results = []
        for i in range(n_bits):
            counts = results.get_counts(qubits[i])
            measured_bit = int(list(counts.keys())[0])
            bob_results.append(measured_bit)
        
        shared_key = ""
        for i in range(n_bits):
            if alice_bases[i] == bob_bases[i]:
                shared_key += str(alice_bits[i])
        
        return shared_key
    
    def quantum_teleportation(self, message_bit, shared_key_bit):
        qr = QuantumRegister(3)
        cr = ClassicalRegister(2)
        crBob = ClassicalRegister(1)
        qc = QuantumCircuit(qr, cr, crBob)
        
        if message_bit == 1:
            qc.x(0)
        
        if shared_key_bit == 1:
            qc.x(0)
        
        qc.h(1)
        qc.cx(1, 2)
        
        qc.cx(0, 1)
        qc.h(0)
        qc.measure([0, 1], [0, 1])
        
        qc.cx(1, 2).c_if(cr, 1)
        qc.cz(0, 2).c_if(cr, 2)
        
        if shared_key_bit == 1:
            qc.x(2)
        
        qc.measure(2, 2)
        
        job = execute(qc, self.backend, shots=1)
        result = job.result()
        counts = result.get_counts()
        measured_result = list(counts.keys())[0]
        received_bit = int(measured_result[-1])
        
        return received_bit, qc
    
    def secure_quantum_communication(self, message_bits):
        shared_key = self.generate_bb84_key(len(message_bits))
        shared_key_bits = [int(bit) for bit in shared_key]
        
        received_message = []
        circuits = []
        
        for i in range(len(message_bits)):
            if i < len(shared_key_bits):
                received_bit, circuit = self.quantum_teleportation(message_bits[i], shared_key_bits[i])
                received_message.append(received_bit)
                circuits.append(circuit)
            else:
                break
        
        return received_message, circuits, shared_key_bits

def run_demonstration():
    qsc = QuantumSecureCommunication()
    
    message = [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]
    print(f"Original message bits: {message}")
    
    received_message, circuits, key_bits = qsc.secure_quantum_communication(message)
    print(f"Shared key bits: {key_bits}")
    print(f"Received message bits: {received_message}")
    
    if len(message) == len(received_message):
        success = all(message[i] == received_message[i] for i in range(len(message)))
        print(f"Transmission successful: {success}")
    else:
        print("Transmission incomplete: Key length was insufficient.")
    
    if circuits:
        print("Example quantum teleportation circuit:")
        print(circuits[0])

if __name__ == "__main__":
    run_demonstration()