# Guide to interfacing a Monte Carlo generator

The way a Monte Carlo generator program is interfaced to the FCC software is twofold:
   1. Through a Gaudi algorithm acfing as interface (see for exple, PythiaInterface).
      This is possible when the generator provides a library with well defined calls for initialization, generartion of an event, finalization;
   1. Through a event data frmat understood by FCCSW: `stdhep`, `LHEf`.

Using common data format is is the most common way, less demanding for the generator. There are however generators not providign events in the common
data, or even not providing the evets at all. These generators need either to be modified to make them able to write out the events in one of the
formats understood by FCCSW, or, if teh format they provide is potentially of common interest, a Gaudi algorithm needs to be writen not read the format.

## From `Pythia6` to `LHEf`
For generators written at the time of `Pythia6`, a typical case was that the events were internally stored in the `PYTHIA COMMON BLOCK`.
Converters from such a common block to `LHEf` exist thogh not in modular form.

### The `LHEf` format

### The conversion code

### Example of interface

## Reading `LHEf` data files


