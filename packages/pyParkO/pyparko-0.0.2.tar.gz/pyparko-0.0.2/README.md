# pyParkO

### Abstract
`pyParkO` is a Python-based algorithm implementation of the Parker-Oldenburg method for: 
1. **Forward modeling**: Calculating gravity anomalies from the density interface.  
2. **Inverse modeling**: Recovering the density interface from gravity anomalies.  

### Key Features  
- A Parker-Oldenburg toolkit containing:  
  - Forward program (`density interface → gravity anomalies`).  
  - Inversion program (`gravity anomalies → density interface`), optimized for reconstructing **seafloor topography** from gridded gravity data.  
- Extended capability to handle **variable density-contrast scenarios** (implemented in this package).  
- **Critical note**: When `mu=0`, the variable density-contrast formula simplifies to the original Parker-Oldenburg method.  

### Functionality  
✅ Parameter tuning for constant/variable density-contrast models.  
✅ Regional adaptability for seafloor topography inversion.  
✅ Built-in visualization tools for forward/inverse results.  

### More Information
For more information, please visit the GitHub website: https://github.com/Eurrreka/pyParkO
