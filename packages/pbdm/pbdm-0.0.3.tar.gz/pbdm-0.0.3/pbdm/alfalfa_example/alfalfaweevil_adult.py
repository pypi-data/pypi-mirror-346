"adults" = {
    "type": "functional_population",
    "var_name": "M", 
    "k": 100,
    "Del": 3500,            # Del is specified here instead
    "age_structure": True,
    "bdfs": {
        "functions": {
            "day_degrees": {
                "function": "Del*a*(T-T_min)/(1+b**(T-T_max))",
                "inputs": {"a": 0.00155, "b": 3.5, "T_min": 4.37, "T_max": 33.5},
            },
            "ovip_rate": {
                "age_var_name": "A",
                "function": "a*b*(A-A_min)/(1 + c**A)*M(A)",
                "inputs": {"a": 1.07, "b": 0.0127, "c": 1.001385, "A_min": 75, "M": "adults.dynamics.mass"},
            },
            "ovip_scalar": {
                "function": "zerone(a*(temp-temp_min)/(1 + b**(temp-temp_max))))",
                "inputs": {"a": 0.065, "b": 2.5, "temp_min": 9.85, "temp_max": 29}
            },
        },
    },
    "processes": {
        "objects": {
            "mortality": {
                "functions": {"rate": "zerone(a*temp**4 + b*temp**3 + c*temp**2 + d*temp + e)"},
                "inputs": {"a": 0.0000001, "b": -0.0000041, "c": 0.0000321, "d": 0.0002382, "e": 0.0042006},
            },
            "oviposition": {
                "var_name": "M_ova",
                "functions": {"rate": "ovip_rate * ovip_scalar * fec_mult * sex_ratio * day_degrees"},         #### syntax may be changed in the future
                "inputs": {
                    "fec_mult": 1, 
                    "sex_ratio": 0.5,
                    "day_degrees": "adult.bdfs.day_degrees",
                    "ovip_rate": "adult.bdfs.ovip_rate",
                    "ovip_scalar": "adult.bdfs.ovip_scalar",
                },
                "outputs": {"M_ova": {"weevil.ova.dynamics.mass.flow_in"}},
            }
        }
    },
    "dynamics": {
        "objects": {
            "mass": {              
                "inputs": {
                    "flow_in": "weevil.preovip.mass_flow_out",
                    "day_degrees": "adult.bdfs.day_degrees",
                },        
            }
        }
    }
}