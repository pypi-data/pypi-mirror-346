"""
Alfalfa weevil

- Does not yet include diapause stage
- Interactions with plant are ignored
- Iranian biotype
"""

"weevil" = {
    "type": "functional_population",
    "stages": {
        "ova": {
            "type": "functional_population",
            "k": 25,
            "age_structure": True,           # Idea of age structure needs to be formalised
            "bdfs": {
                "functions": {
                    "day_degrees": {
                        "function": "Del*a*(T-T_min)/(1+b**(T-T_max))",
                        "inputs": {"a": 0.0105, "b": 2.5, "T_min": 10.75, "T_max": 33.5},
                    },
                }
            },
            "processes": {
                "objects": {
                    "mortality": {          # Any biodemographic function can also be captured when it's used, like this
                        "functions": {"rate": "zerone(a*temp**4 + b*temp**3 + c*temp**2 + d*temp + e)"},
                        "inputs": {"a": 0.0948760, "b": -0.0199293, "c": 0.0016311, "d": -0.0000584, "e": 0.0000008},
                        "var_name": "x",
                    }
                }
            },
            "dynamics": {
                "objects": {
                    "mass": {
                        "Del": 100.7,
                        "inputs": {
                            "flow_in": 0,
                            "day_degrees": "ova.bdfs.day_degrees",
                        }
                    },
                },
                "var_name": "M",
            },
            "variable_ports": ["mass_flow_out"],
            "variable_connections": {"mass_flow_out": {"dynamics.mass.M_10"}}          # "Hidden" variables can still be connected to   

        },

        "larvae": {
            "type": "functional_population",
            "var_name": "M",         # This var_name is inherited to all dynamics and processes objects. See ova for alternative.
            "k": 25,
            "Del": 164.5,            # Del is specified here instead
            "age_structure": True,
            "bdfs": {
                "functions": {
                    "day_degrees": {
                        "function": "Del*a*(T-T_min)/(1+b**(T-T_max))",
                        "inputs": {"a": 0.0065, "b": 2.5, "T_min": 10.75, "T_max": 33.5},
                    },
                }
            },
            "processes": {
                "objects": {
                    "mortality": {
                        "functions": {"rate": "zerone(a*temp**4 + b*temp**3 + c*temp**2 + d*temp + e)"},
                        "inputs": {"a": 0.0220431, "b": -0.0019589, "c": -0.0000168, "d": 0.0000060, "e": -0.0000001},
                    }
                }
            },
            "dynamics": {
                "objects": {
                    "mass": {               # Del is not specified here, but it is inherited from parameters above
                        "inputs": {
                            "flow_in": "weevil.ova.mass_flow_out",          # This draws the flow input from the ova output
                            "day_degrees": "larvae.bdfs.day_degrees",
                        },          
                    }
                }
            }
        },

        "pupae": {
            "type": "functional_population",
            "var_name": "M",        
            "k": 25,
            "Del": 108.36,          
            "age_structure": True,
            "bdfs": {
                "functions": {
                    "day_degrees": {
                        "function": "Del*a*(T-T_min)/(1+b**(T-T_max))",
                        "inputs": {"a": 0.00975, "b": 2.5, "T_min": 10.75, "T_max": 33.75},
                    },
                }
            },
            "processes": {
                "objects": {
                    "mortality": {
                        "functions": {"rate": "zerone(a*temp**4 + b*temp**3 + c*temp**2 + d*temp + e)"},
                        "inputs": {"a": 0.0000003, "b": -0.0000177, "c": 0.0003327, "d": -0.0029581, "e": 0.0151908},
                    }
                }
            },
            "dynamics": {
                "objects": {
                    "mass": {               # Del is not specified here, but it is inherited from parameters above
                        "inputs": {
                            "flow_in": "weevil.larvae.mass_flow_out",          # This draws the flow input from the ova output
                            "day_degrees": "pupae.bdfs.day_degrees",
                        },          
                    }
                }
            }
        },

        "pre_ovip": {
            "type": "functional_population",
            "var_name": "M",        
            "k": 25,
            "Del": 459.17,          
            "age_structure": True,
            "processes": {
                "objects": {
                    "mortality": {
                        "functions": {"rate": "zerone(a*temp**4 + b*temp**3 + c*temp**2 + d*temp + e)"},
                        "inputs": {"a": 0.0000001, "b": -0.0000041, "c": 0.0000321, "d": 0.0002382, "e": 0.0042006},
                    }
                }
            },
            "dynamics": {
                "objects": {
                    "mass": {               # Del is not specified here, but it is inherited from parameters above
                        "inputs": {
                            "flow_in": "weevil.larvae.mass_flow_out",          # This draws the flow input from the ova output
                            "day_degrees": "weevil.adults.bdfs.day_degrees",    # Points to the same DD function as weevil adults
                        },          
                    }
                }
            }
        },

        "adults": {
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
    } 
}