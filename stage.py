
import numpy as np
from typing import List
from typing import Iterator

class Engine: 

    def __init__(self, mass_gross: float, mass_propellant: float, specific_impulse: float, name = None, group = None, count = 1) -> None:
        self.mass_gross = mass_gross
        self.mass_propellant = mass_propellant
        self.mass_structure = mass_gross - mass_propellant
        if(mass_gross == 0):
            self.structural_mass_fraction = 1
        else:
            self.structural_mass_fraction = self.mass_structure / self.mass_gross
        self.specific_impulse = specific_impulse
        self.v_exhaust = 9.8 * specific_impulse
        self.name = name
        self.group = group
        self.count = count
    
    def payload(payload_mass): # -> Self:
        return Engine(payload_mass, np.nan, np.nan, name= "Payload", group="Payload")
        
    def from_row(row): # -> Self:
        name = row[0]
        mass_gross = float(row[6])
        mass_propellant = float(row[7])
        specific_impulse = float(row[10])
        group = row[15]


        return Engine(mass_gross, mass_propellant, specific_impulse, name, group)

    def delta_v(self, payload_mass: float) -> float:
        return self.v_exhaust * np.log((payload_mass + self.mass_gross) / (payload_mass + self.mass_structure))

    def __mul__(self, other):
        return Engine(self.mass_gross * other, self.mass_propellant * other, self.specific_impulse, name = self.name, group = self.group, count=self.count * other)
    __rmul__ = __mul__
    
    def __str__(self) -> str:
        return self.name + " x" + str(self.count)


class Stage:
    def __init__(self, engines: Engine, delta_v: float) -> None:
        self.engines = engines
        self.delta_v = delta_v
        if self.engines.mass_propellant == 0:
            self.mass_fraction = 1
        else:
            self.mass_fraction = ( np.exp(-1 * self.delta_v / self.engines.v_exhaust) - self.engines.structural_mass_fraction) / \
            (1 - self.engines.structural_mass_fraction)


class STS:

    def __init__(self, engines: List[Engine], counts: List[int]) -> None:
        engines_total = [engine * count for engine, count in zip(engines, list(counts))]
        cumulative_masses = np.cumsum([engine.mass_gross for engine in engines_total])
        delta_vs = [0] + [engines_total[i].delta_v(cumulative_masses[i-1]) for i in range(1,len(engines_total))]
        stages = [Stage(e, dv) for e, dv in zip(engines_total, delta_vs)]
        self.engine_counts = counts
        self.payload_mass = stages[0].engines.mass_gross
        self.stages = stages
        self.engines = [s.engines for s in self.stages]

    def mass_fraction(self) -> float:
        return np.prod([s.mass_fraction for s in self.stages[1:]])
    
    def delta_V(self) -> float:
        return np.sum([s.delta_v for s in self.stages[1:]])
    
    def engine_count(self) -> int:
        engine_groups = [e.group for e in self.engines]
        return sum([ (g != "None" and g != "Payload") * n for g, n, in zip(engine_groups, self.engine_counts)])
    
    def __str__(self) -> str:
        return ", ".join([f"E: {s.engines} DV: {int(s.delta_v)} m/s" for s in self.stages])
