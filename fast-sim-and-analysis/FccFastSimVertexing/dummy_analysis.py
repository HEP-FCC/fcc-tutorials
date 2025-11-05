'''
Dummy analysis, part of the Tracking and vertexing example using specific
flavour decays tutorial.

To run it use:
```bash
fccanalysis run dummy_analysis.py --test --nevents 10 --output dummy_result.root
```
'''

testFile = "/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/" \
           "p8_ee_Zuds_ecm91/events_125841058.root"

# includePaths = ["analyzers.h"]


class RDFanalysis():
    '''
    Mandatory class, where the analysis is defined.
    '''
    def analysers(df):
        '''
        Mandatory method, where the operations on the dataframe are registered.
        '''
        df2 = (df
            # Dummy define:
            .Define("dummy_momentum_collection",
                    "VtxAna::dummy_analyzer(ReconstructedParticles)")
        )

        return df2

    def output():
        '''
        Mandatory method, defining output columns.
        '''
        branchList = [
            "dummy_momentum_collection",
        ]

        return branchList
