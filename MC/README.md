# Private MC production

Full chain runs Gauss + Boole + Moore (L0 + HLT) + Brunel + DaVinci.
For local tests, one needs to run manually each step. For grid usage, 
the file `ganga-fullChain.py` configures a task with all the steps.


## Gauss Job configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc48-opt
~/cmtuser/GaussDev_v49r10/run bash
gaudirun.py Gauss-Job.py Gauss-evts.py
```
where the `GaussDev_v49r10` project should have the new decfile options `13102601.py` created with `make install`.

This creates the following files: `Gauss-13102601-5ev-20190605-histos.root`, `Gauss-13102601-5ev-20190605.sim`, 
`GeneratorLog.xml`, `NewCatalog.xml`, that are needed to test the rest of the steps locally.


## Boole Job configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc49-opt
lb-run Boole/v30r3 bash
gaudirun.py Boole-Job.py Boole-input.py
```

This needs the `Gauss-13102601-5ev-20190605.sim` and `NewCatalog.xml` files produced by the Gauss job and 
produces `Boole.digi` and `Boole-histos.root`.


## L0 Job configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc48-opt
lb-run Moore/v25r4 bash
gaudirun.py L0-Job.py L0-input.py
```

This needs the `Boole.digi` file produced by the Boole job and the `NewCatalog.xml` file produced by the Gauss job.
It produces `13102601-L0App.digi`.


## HLT Job configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc48-opt
lb-run Moore/v25r4 bash
gaudirun.py HLT1-Job.py HLT1-input.py
gaudirun.py HLT2-Job.py HLT2-input.py
```

This needs the `13102601-L0App.digi` file produced by the L0 job.
The HLT1 job produces `13102601-HLT1.digi` and `test_catalog.xml`.
The HLT2 one prdocues `13102601-HLT2.digi`.


## Brunel Job configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc49-opt
lb-run Brunel/v50r5 bash
gaudirun.py Brunel-Job.py
```

This needs the `13102601-HLT2.digi` file produced by the HLT2 job 
and the `NewCatalog.xml` file with the link to the `.sim` file to copy the MC 
information to the output `DST`.
It produces `Brunel.dst` and `Brunel-histos.root`.

### Note on the Brunel version
In the production request 48724 `Brunel/v50r4` was used with `x86_64-slc6-gcc62-opt`. 
However this version is not available under this platform. Moreover, this version 
is marked as obsolete in the [Brunel project page](http://lhcbdoc.web.cern.ch/lhcbdoc/brunel/releases/). So we move to `Brunel/v50r5` and use it with `x86_64-slc6-gcc49-opt`, 
which is the only platform for which this version is available in `cvmfs`.


## Stripping step configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc49-opt
lb-run DaVinci/v41r4p5 bash
gaudirun.py Strip-Job.py
```

This needs the `Brunel.dst` file produced by the Brunel job and produces the files
`000000.AllStreams.dst` and `DVHistos.root`. 