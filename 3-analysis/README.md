# Analysis

The preceding chapters introduced event generation and detector simulation. The next step is to use reconstructed events to answer for example the following physics questions: which events resemble our signal, which observables distinguish them from backgrounds, and how many events do we expect to observe?

[FCCAnalyses](https://hep-fcc.github.io/FCCAnalyses/) provides tools for this step. It combines access to EDM4hep objects, reusable physics algorithms, and ROOT's event-processing tools. In this chapter, you will use it to build particle candidates, select events, and produce distribution plots for signal and background samples.

```{rubric} Where FCCAnalyses fits
```

Several packages work together in an FCC analysis:

| Component | Role in the analysis |
|---|---|
| Key4hep | Provides a compatible software environment containing the packages used along the event-processing chain. |
| EDM4hep | Defines particles, tracks, vertices, detector hits, and their relations. The tutorial starts from reconstructed events stored in this format. |
| ROOT RDataFrame | Describes and executes operations on event data, including new observables, selections, and histograms. |
| FCCAnalyses | Provides analysis steering and reusable algorithms for working with these objects. |
| Your analysis | Specifies the input samples, physics calculations, selections, and outputs needed for your study. |

The analysis is configured in Python, while many calculations are performed in C++. For example, a Python script can ask RDataFrame to create a column using a C++ function from FCCAnalyses. You can also provide your own helper functions in a header that ROOT compiles just in time.

```{rubric} Thinking in columns and selections
```

An RDataFrame analysis describes a computation graph. Each event supplies input collections, and operations define how those inputs are used:

- `Alias()` gives an existing column another name, useful for accessing relation fields.
- `Define()` creates a column, such as the selected muons or a candidate's mass.
- `Filter()` keeps events that satisfy a condition.
- Histogram actions accumulate distributions, while an output operation such as `Snapshot()` writes selected columns to a new file.

A column may contain one value per event or a collection of values. Selecting muons within an event therefore differs from selecting the event itself: an event can remain in the dataframe even when its selected-muon collection is empty.

RDataFrame evaluates work lazily. Defining columns, adding filters, and booking histograms builds the graph; requesting the results triggers processing. Booking the required histograms before evaluating them allows several distributions to be filled in the same event loop.

```{rubric} Two ways to organise the work
```

For a compact analysis, we can calculate observables, apply selections, and fill histograms all in one step:

```text
reconstructed events → observables and selections → histograms → plots
```

For a computationally more expensive analysis, we can first save a reduced ntuple containing only the observables needed for later processing:

```text
reconstructed events → observables and pre-selections → reduced ntuple

```
then
```
reduced ntuple → selections and histograms → plots
```

The second workflow lets us change cuts without repeating candidate reconstruction and processings like flavour tagging. Its tradeoff is that later steps can use only the information saved in the ntuple; a change to the reconstruction or a missing observable requires rerunning the first stage.

Section 3.1 introduces both workflows through the same Higgs signal and background samples. Part I uses a `build_graph` method to perform a recoil analysis in one step. Part II adds jet reconstruction and flavour tagging, then separates ntuple production, final selections, and plotting into individual stages.

```{rubric} Working through this chapter
```

- [Higgs analysis](3-1-higgs-analysis/README.md): follow reconstructed events through candidate building, event selection, normalisation, and plotting.
- [Tracking and vertexing](3-2-tracking-vertexing/README.md): explore more involved tracking and vertexing examples.
- [Further information](3-3-useful-info/README.md): consult the reference material on EDM4hep collections and C++ analyzers when you need more detail.

If you have problems or questions, [open an issue](https://github.com/HEP-FCC/fcc-tutorials/issues) on the [tutorial repository](https://github.com/HEP-FCC/fcc-tutorials).

```{eval-rst}
.. toctree::
    :caption: Contents:

    3-1-higgs-analysis/README.md
    3-2-tracking-vertexing/README.md
    3-3-useful-info/README.md

```
