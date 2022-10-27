# microSWIFT_io
Python modules for microSWIFT onboard and telemetry input/output. Forked from `edwinrainville/microSWIFT-io`. 

See `examples/` for usage. 

## Structure:

```
microSWIFT_io
│  
└───examples
│  
└───onboard
│  
└───telemetry
    │   
    └───requirements.txt
    │  
    └───pull_telemetry.py
    │       create_request()
    │       pull_telemetry_as_var()
    │       pull_telemetry_as_zip()
    │       pull_telemetry_as_json()
    │       pull_telemetry_as_kml()
    │
    └───read_SBD.py
    │       read_SBD()
    │       get_sensor_type()
    │       unpack_SBD()
    │
    └───compile_SBD.py
    │       compile_SBD()
    │       to_pandas_datetime_index()
    │        
    └───definitions.py
    │       get_sensor_type_definition()
    │       get_variable_definitions()
    │   
    └───telemetry_analytics.py
```