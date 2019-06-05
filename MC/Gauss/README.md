# Gauss Job configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc48-opt
~/cmtuser/GaussDev_v49r10/run gaudirun.py Gauss-Job.py
```
where the `GaussDev_v49r10` project should have the new decfile options `13102601.py` created with `make install`.

This creates the following files: `Gauss-13102601-5ev-20190605-histos.root`, `Gauss-13102601-5ev-20190605.sim`, 
`GeneratorLog.xml`, `NewCatalog.xml`, that are needed to test the rest of the steps locally.