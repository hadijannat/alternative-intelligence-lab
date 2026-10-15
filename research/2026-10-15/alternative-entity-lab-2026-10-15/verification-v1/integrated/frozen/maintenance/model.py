"""Material tokens and arbitrary work units; no identified molecular reaction."""

from dataclasses import dataclass, fields, replace
import math


def quantity(name, value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a finite nonnegative number")
    return float(value)


@dataclass(frozen=True)
class Params:
    conversion_rate: float = 0.8
    structure_yield: float = 0.5
    energy_yield: float = 2.0
    renewal_energy_cost: float = 0.5
    decay_rate: float = 0.04
    energy_leak_rate: float = 0.03
    renewal: bool = True

    def __post_init__(self):
        for field in fields(self):
            if field.name != "renewal":
                quantity(field.name, getattr(self, field.name))
        if self.structure_yield > 1:
            raise ValueError("structure_yield cannot exceed one")
        if not isinstance(self.renewal, bool):
            raise ValueError("renewal must be Boolean")


@dataclass(frozen=True)
class State:
    fuel: float
    waste: float
    structure: float
    energy: float
    spent: float
    dissipated: float
    energy_generated: float
    fed_total: float
    initial_material: float
    initial_energy: float
    founder_structure: float
    new_structure: float


@dataclass(frozen=True)
class StepResult:
    state: State
    accepted_influx: float
    actual_work: float
    renewed: float
    decayed: float
    converted: float


def validate(state):
    for field in fields(state):
        quantity(field.name, getattr(state, field.name))
    for actual, expected, name in (
        (state.fuel + state.waste + state.structure, state.initial_material + state.fed_total, "material"),
        (state.energy + state.spent + state.dissipated, state.initial_energy + state.energy_generated, "energy"),
        (state.founder_structure + state.new_structure, state.structure, "structure labels"),
    ):
        if not math.isclose(actual, expected, abs_tol=1e-10, rel_tol=1e-10):
            raise ValueError(f"Unbalanced {name}: {actual} != {expected}")


def initialise(fuel=0.5, structure=1.0, energy=0.25):
    fuel, structure, energy = (quantity(k, v) for k, v in (("fuel", fuel), ("structure", structure), ("energy", energy)))
    state = State(fuel, 0.0, structure, energy, 0.0, 0.0, 0.0, 0.0, fuel + structure, energy, structure, 0.0)
    validate(state)
    return state


def debit_work(state, work):
    """Pay an instantaneous caller-owned task; caller gates its effect on actual work."""
    validate(state)
    paid = min(quantity("work", work), state.energy)
    result = replace(state, energy=state.energy - paid, spent=state.spent + paid)
    validate(result)
    return result, paid


def step(state, influx, work, dt, params=Params()):
    """Advance once; the caller must debit accepted_influx from a finite reservoir."""
    validate(state)
    influx, work, dt = (quantity(k, v) for k, v in (("influx", influx), ("work", work), ("dt", dt)))
    if dt <= 0:
        raise ValueError("dt must be positive; use debit_work for instantaneous tasks")
    if not isinstance(params, Params):
        raise ValueError("params must be Params")
    retention = math.exp(-params.decay_rate * dt)
    founder = state.founder_structure * retention
    renewed_structure = state.new_structure * retention
    surviving = founder + renewed_structure
    decayed = state.structure - surviving
    energy = state.energy * math.exp(-params.energy_leak_rate * dt)
    dissipated = state.dissipated + state.energy - energy
    fuel = state.fuel + influx
    converted = min(fuel, params.conversion_rate * surviving * dt)
    generated = params.energy_yield * converted
    energy += generated
    renewed = params.structure_yield * converted if params.renewal else 0.0
    if params.renewal_energy_cost:
        renewed = min(renewed, energy / params.renewal_energy_cost)
    renewal_work = min(energy, renewed * params.renewal_energy_cost)
    energy -= renewal_work
    dissipated += renewal_work
    result = State(
        fuel=fuel - converted,
        waste=state.waste + decayed + converted - renewed,
        structure=surviving + renewed,
        energy=energy,
        spent=state.spent,
        dissipated=dissipated,
        energy_generated=state.energy_generated + generated,
        fed_total=state.fed_total + influx,
        initial_material=state.initial_material,
        initial_energy=state.initial_energy,
        founder_structure=founder,
        new_structure=renewed_structure + renewed,
    )
    result, paid = debit_work(result, work)
    return StepResult(result, influx, paid, renewed, decayed, converted)
