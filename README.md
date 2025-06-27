# Surf Data Forecast PoC (API fetching and displaying Rough Proof of Concept)
- A rough proof-of-concept (PoC) of Flask application that:
    - Fetches real-time (live) data from CDIP's public NetCDF server (THREDDS)
          - Pending access to CDIPpy python library beta access
    - Parses, filters using "xarray"
    - Displays signficant wave heights and respective timestamps on basic frontend via local Flask
    
- Basic PoC --> plan to use a python library in the future if possible, feasible (when available - CDIPpy)
    - relies on and uses "xarray", "flask", and "datetime"
    - React implemented as well. Previously was simple html, etc. 
