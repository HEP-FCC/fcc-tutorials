# Structure for /eos/experiment/fcc/prod

## Overview
FCC Monte Carlo productions will be handled by the DIRAC system and stored at CERN under

```
 /eos/experiment/fcc/prod/fcc
```

where `/eos/experiment/fcc/prod` is the mapped endpoint and `/fcc` is required to honour DIRAC request to start with `/<VO>`.
The directory `/eos/experiment/fcc/prod` is divided in two grand zones:
`/fcc/user/[u]/[username]` and `/fcc/[ee,hh,eh]`.

The purpose of the user area is to provide some temporary space for user private jobs.

The other areas are meant for production files. A hierarchical structure for the output files is being defined for an efficient use of this area.
The purpose of these pages is to describe such a structure.

Complete metadata will be available from DIRAC through the unique identifier `DiracProdID` discussed above.



