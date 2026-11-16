from pathlib import Path

PROJECT_ROOT=Path(__file__).resolve().parent
DWSIM_PATH=Path.home() / "AppData" / "Local" / "DWSIM"
SIMULATION_PATH=PROJECT_ROOT / "models" / "bacalhau_v2.dwxmz"
OUTPUT_PATH=PROJECT_ROOT / "outputs"

OPERATING_VARIABLES=[
    ("bacalhau3", "PROP_MS_3"),
    ("atm_cdu", "Reflux ratio"),
    ("atm_cdu", "Bottoms flowrate"),
    ("atm_cdu", "Sidestream1 liquid flow"),
    ("atm_cdu", "Sidestream2 liquid flow"),
    ("atm_cdu", "Sidestream3 liquid flow"),
    ("atm_cdu", "Sidestream4 liquid flow"),
    ("atm_cdu", "Sidestream5 liquid flow"),
]

STREAM_NAMES=(
        "bacalhau3",
        "top",
        "hnaphtha",
        "kerosene",
        "ldiesel",
        "hdiesel",
        "ago",
        "bottom",
    )

CHRACTERIZATION_PROP={
    "Reid Vapor Pressure",
    "Density @ 15 C",
    "Freezing Point",
    "Kinematic Viscosity @ 15 C",
    "Kinematic Viscosity @ 40 C",
    "Kinematic Viscosity @ 100 C",
    "D86 95%",
    "D86 90%",
    "D86 50%",
    "D86 5%",
    "TBP 95%",
    "TBP 50%",
    "TBP 5%",
    "Flash Point (Closed Cup)",
    "Cetane Index (D4737)",
    "Pour Point",
    "D1160 5%",
    "D1160 50%",
    "D1160 95%"
}

SEPARATION_PROP={
    "top": ["D86 50%", "D86 95%", "Reid Vapor Pressure"],
    "hnaphtha": ["D86 5%", "D86 50%", "D86 95%", "Kinematic Viscosity @ 15 C"],
    "kerosene": ["D86 5%", "D86 50%", "D86 95%", "Freezing Point", "Kinematic Viscosity @ 15 C", "Flash Point (Closed Cup)"],
    "ldiesel": ["D86 5%", "D86 50%", "D86 90%", "D86 95%", "Kinematic Viscosity @ 40 C", "Flash Point (Closed Cup)", "Cetane Index (D4737)"],
    "hdiesel": ["D86 5%", "D86 50%", "D86 90%", "D86 95%", "Kinematic Viscosity @ 40 C", "Flash Point (Closed Cup)"],
    "ago": ["TBP 5%", "TBP 50%", "TBP 95%", "D1160 5%", "D1160 50%", "D1160 95%", "Flash Point (Closed Cup)"],
    "bottom": ["TBP 5%", "TBP 50%", "Flash Point (Closed Cup)"],
}

MAX_FEED_MOLAR_FLOW=1000.0
N_OBJECTIVES=2
N_PRE_CONSTRAINTS=2
N_SIMULATION_CONSTRAINTS=1
PENALTY=1e12

ALGORITHM="NSGA2"
N_OBJECTIVES=2
POPULATION_SIZE=10