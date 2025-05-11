# LineFlow

`LineFLow` is a python framework to simulate assembly lines. It allows to model
arbitrary discrete part assembly lines and provides an `gymnasium` environment to
optimize them with reinforcement learning.

![til](docs/imgs/lineflow.gif)

# Examples


## Visualization 
This is how an assembly line can be implemented and visualized:


```python
from lineflow.simulation import Line, Source, Sink, Process

class SimpleLine(Line):

    def build(self):

        # Set up stationary objects
        source = Source(
            name='Source',
            processing_time=5,
            position=(100, 500),
            unlimited_carriers=True,
        )

        process = Process('Process', processing_time=6, position=(350, 500))
        sink = Sink('Sink', processing_time=3, position=(600, 500))
        
        # Wire them with buffers
        source.connect_to_output(station=process, capacity=3)
        process.connect_to_output(station=process, capacity=2)


line = SimpleLine()
line.run(simulation_end=500, visualize=True)

df = line.get_observations()
```

## Training RL agents

This is how an RL agent can be trained using `LineFlow`:

```python

from stable_baselines3 import PPO
from lineflow.simulation import LineSimulation

line = SimpleLine()
env = LineSimulation(line, simulation_end=100)
model = PPO("MlpPolicy", env)
model.learn(total_timesteps=100)
```

# Docs

Serve the docs with

```bash
mkdocs serve
```


# Paper

If you use our work in your research, please consider citing us with

```
@article{lineflow,
  author = {Kai M{\"u}ller and Martin Wenzel and Tobias Windisch},
  title = {LineFlow: A framework to learn active control of production lines},
  year = {2025},
}
```

See [this README](./scripts/README.md) for more details how to run the benchmarks.


# Funding

The research behind LineFlow is funded by the Bavarian state ministry of research. Learn more
[here](https://kefis.fza.hs-kempten.de/de/forschungsprojekt/599-lineflow).
