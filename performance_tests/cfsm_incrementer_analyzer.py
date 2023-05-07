import time
import csv
import os
import numpy as np
from performance_tests.cfsm_incrementer import CFSMIncrementer


class CFSMIncrementerAnalyzer:

    def __init__(self, initial_cfsm, initial_index, results_path, size=2, max_points=30, randomize_times=10):
        self.initial_cfsm = initial_cfsm
        self.initial_index = initial_index
        self.size = size
        self.max_points = max_points
        self.randomize_times = randomize_times

        self.path = f'{results_path}/{max_points}_points_{randomize_times}_times'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.incrementer = CFSMIncrementer()

    def calculate_bisimulation_with_simple_increment_strategy(self):
        writer = self.CSVWriter(f'{self.path}/increment_strategy.csv')
        writer.create()
        metrics = self.calculate_bisimulation_for_with_strategy(self.incrementer.increment, writer)
        return metrics

    def calculate_bisimulation_with_increment_splitting_transitions_strategy(self):
        writer = self.CSVWriter(f'{self.path}/increment_splitting_transitions.csv')
        writer.create()
        metrics = self.calculate_bisimulation_for_with_strategy(self.incrementer.increment_splitting_transitions, writer)
        return metrics

    def calculate_bisimulation_with_increment_splitting_transitions_in_new_states_strategy(self):
        writer = self.CSVWriter(f'{self.path}/increment_splitting_transitions_in_new_states.csv')
        writer.create()
        metrics = self.calculate_bisimulation_for_with_strategy(self.incrementer.increment_splitting_transitions_in_new_states, writer)
        return metrics

    def calculate_bisimulation_for_with_strategy(self, increment_strategy, writer):
        metrics = []
        cfsm = self.initial_cfsm
        index = self.initial_index

        for i in range(self.max_points):
            if i != 0:
                cfsm, index = increment_strategy(cfsm, self.size, index)

            size = self.size_of_cfsm(cfsm)
            print(f'Calculating: {i+1} metric, size: {size}')
            avg_time = self.calculate_bisimulation_time_for(cfsm)

            metric = {'size': size, 'avg_time': avg_time}
            print(metric)
            print('')
            metrics.append(metric)
            writer.write([size, avg_time])

        return metrics

    def calculate_bisimulation_time_for(self, cfsm):
        times = []
        for i in range(self.randomize_times):
            print(f'  {i+1} randomize')
            randomized_cfsm = self.incrementer.randomize(cfsm)

            start_time = time.time()
            cfsm.calculate_bisimulation_with(randomized_cfsm)
            end_time = time.time()

            # Cancelar el temporizador si el código se ejecutó dentro del límite de tiempo

            print(f'{end_time - start_time} seconds')

            times.append(end_time - start_time)

        return np.mean(times)

    def size_of_cfsm(self, cfsm):
        states = len(cfsm.states)
        transitions = sum(len(transitions) for transitions in cfsm.transitions_by_source_id.values())
        return states * transitions

    class CSVWriter:

        def __init__(self, csv_path):
            self.csv_path = csv_path

        def create(self):
            if not os.path.exists(self.csv_path):
                self.write(['size', 'avg_time'])

        def write_line_result(self, data):
            self.write(data)

        def write(self, data):
            with open(self.csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data)
