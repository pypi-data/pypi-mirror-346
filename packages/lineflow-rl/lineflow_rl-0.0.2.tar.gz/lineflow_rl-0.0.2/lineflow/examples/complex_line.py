import numpy as np
import random
from lineflow.simulation import (
    Line,
    Sink,
    Source,
    Assembly,
    Magazine,
    Switch,
    WorkerPool,
)

def index_for_waiting_time(waiting_times, waiting_time):
    return np.argmin(np.abs(waiting_times - waiting_time))


def get_last_filled_buffer(fills_btw_assemblies):
    return (len(fills_btw_assemblies) - 
            np.argmax(np.flip(fills_btw_assemblies)))


def get_filled_buffers(fills_assembly_switch, fills_btw_assemblies):
    filled_positions = np.nonzero(fills_btw_assemblies)[0]
    if filled_positions.shape == (0,):
        filled_positions = np.array([0])
    return np.argmin(fills_assembly_switch[filled_positions])


def get_fill_factor(fills_assembly_switch, fills_btw_assemblies):
    return (0.9 * (np.sum(fills_assembly_switch) / len(fills_assembly_switch)) +
            0.1 * (np.sum(fills_btw_assemblies) / len(fills_btw_assemblies)))


class ClAgent():
    def __init__(self, source_waiting_time, processing_time_diff, complex_line):
        self.source_waiting_time = source_waiting_time
        self.processing_time_diff = processing_time_diff

        self.n_workers = complex_line.n_workers
        self.n_assemblies = complex_line.n_assemblies

        self.part_count = -1 # set to -1 so that shuffle is called at the beginning

    def shuffle_if_needed(self, state, actions):
        df = state.df()
        processing_times = [df[f"A{i}_processing_time"].iloc[-1] for i in range(self.n_assemblies)]

        worker_assignments = [worker.value for worker in state.get_actions()["Pool"]]
        worker_names = [worker.name for worker in state.get_actions()["Pool"]]

        # get the fastest process that has workers assigned to it
        fastest_stations = np.argsort(processing_times)
        for i in fastest_stations:
            if i in worker_assignments:
                fastest_station = i
                break

        slowest_station = np.argmax(processing_times)

        if processing_times[slowest_station] - processing_times[fastest_station] > self.processing_time_diff:
            # assign worker from fastest to slowest station
            worker_of_fast_station = np.where(worker_assignments == fastest_station)[0][0]
            worker_assignments[worker_of_fast_station] = slowest_station
        actions['Pool'] = dict(zip(worker_names, worker_assignments))

    def actions_for_switch(self, actions, state):
        # Fetch from buffer where fill is largest
        fills = np.array(
            [state[f'Buffer_Switch_to_A{i}']['fill'].value for i in range(self.n_assemblies)]
        )
        min = np.min(fills)
        index = np.where(fills == min)[0][-1]  # prioritize last buffer on line
        actions['Switch'] = {
            'index_buffer_out': index
        }

    def __call__(self, state, env):
        actions = {}

        self.actions_for_switch(actions, state)

        # set waiting time
        actions['Source'] = {'waiting_time': self.source_waiting_time}
        # shuffel only after new part is produced
        if state['EOL']['n_parts_produced'].value > self.part_count:
            self.part_count = state['EOL']['n_parts_produced'].value
            self.shuffle_if_needed(state, actions)
        return actions


class ComplexLine(Line):
    '''
    Assembly line with a configurable number of assembly stations served by a component source
    '''
    def __init__(
            self,
            n_workers,
            n_assemblies=8,
            n_carriers=20,
            alternate=True,
            assembly_condition=30,
            random_state=0,
            *args,
            **kwargs,
    ):
        self.n_carriers = n_carriers
        self.alternate = alternate
        self.n_assemblies = n_assemblies
        self.n_workers = n_workers
        self.assembly_condition = assembly_condition
        self.random_state = random_state
        self.processing_times = [10+30*i for i in range(self.n_assemblies)]
        super().__init__(random_state=random_state, *args, **kwargs)
        self.reset(random_state)

    def reset(self, random_state=None):
        super().reset(random_state=random_state)
        random.shuffle(self.processing_times)

    def build(self):
        magazine = Magazine(
            'Setup',
            unlimited_carriers=False,
            carriers_in_magazine=self.n_carriers,
            position=(50, 100),
            carrier_capacity=self.n_assemblies,
            actionable_magazine=False,
        )

        pool = WorkerPool(name='Pool', n_workers=self.n_workers, transition_time=2)

        sink = Sink(
            'EOL',
            position=(self.n_assemblies*200-150, 100),
            processing_time=2
        )

        sink.connect_to_output(magazine, capacity=6, transition_time=6)

        source = Source(
            'Source',
            position=((self.n_assemblies/2)*200+100, 150),
            processing_time=1,
            waiting_time_step=1,
            unlimited_carriers=True,
            carrier_capacity=1,
            actionable_waiting_time=True,
            part_specs=[{
                "assembly_condition": self.assembly_condition,
            }],
        )

        switch = Switch(
            'Switch',
            position=((self.n_assemblies/2)*200-50, 150),
            alternate=self.alternate,
            processing_time=0,
        )

        source.connect_to_output(switch, capacity=2, transition_time=2)

        # Create assemblies
        assemblies = []

        for i in range(self.n_assemblies):
            a = Assembly(
                f'A{i}',
                position=((i+1)*200-150, 300),
                processing_time=self.processing_times[i],
                worker_pool=pool,
                NOK_part_error_time=2,
            )

            a.connect_to_component_input(switch, capacity=4, transition_time=4)
            assemblies.append(a)
        # connect assemblies
        magazine.connect_to_output(assemblies[0], capacity=4, transition_time=4)
        for a_prior, a_after in zip(assemblies[:-1], assemblies[1:]):
            a_prior.connect_to_output(a_after, capacity=2, transition_time=10)

        assemblies[-1].connect_to_output(sink, capacity=4, transition_time=4)


if __name__ == '__main__':
    ramp_up_waiting_time = 6
    waiting_time = 2
    n_assemblies = 3
    n_workers = 3*n_assemblies
    scrap_factor = 1/n_assemblies

    line = ComplexLine(
        realtime=False,
        alternate=False,
        n_assemblies=n_assemblies,
        n_workers=n_workers,
        step_size=1,
        scrap_factor=scrap_factor,
        random_state=0,
        assembly_condition=30
    )

    agent = ClAgent(
        source_waiting_time=4,
        processing_time_diff=0.9,
        complex_line=line,
    )

    line.run(
        simulation_end=4000,
        agent=agent,
        capture_screen=False,
        show_status=True,
        visualize=True,
        )
    print("Produced: ", line.get_n_parts_produced())
    print("Scrap: ", line.get_n_scrap_parts())
    print("Reward: ", line.get_n_parts_produced() - line.get_n_scrap_parts()*scrap_factor)
