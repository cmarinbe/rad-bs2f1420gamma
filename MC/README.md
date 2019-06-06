# Private MC production

Full chain runs Gauss + Boole + Moore (L0 + HLT) + Brunel + DaVinci.
For local tests, one needs to run manually each step. For grid usage, 
the file `ganga-fullChain.py` configures a task with all the steps.


## Grid usage

The file `ganga-fullChain.py` configures a task where all the steps are chained 
together. The final output are the output files of the stripping step, called 
`000000.AllStreams.dst`, which are stored on the grid. Also the `.sim` files 
created by Gauss, which are the most costly to produce, are stored on the grid. 
The rest of the intermediate files are removed to save space, since they are 
fast to reproduce if needed.

To run the ganga task, one first needs a local version of the different software 
projects, that will be used as input to the various `GaudiExec` jobs. You can 
get this by simply doing:
```bash
lb-dev Project/version
cd ProjectDev_version
make
```
inside your `cmtuser` folder. This folder needs to be specified in the variable 
`cmtpath` in `ganga-fullChain.py`. The versions of the projects should match the 
ones defined at the beginning of `ganga-fullChain.py`.

No modifications of the default projects are needed. But the new decfile should 
be included in the Gauss project. This can be done by:
```bash
lb-dev Gauss/version
cd GaussDev_version
git lb-clone-pkg Gen/DecFiles
cp Bs_f1420gamma=HighPtGamma,DecProdCut Gen/DecFiles/dkfiles
make install
```
This will create the file `Gen/DecFiles/options/13102601.py` to be used in 
the ganga job.

After this we are ready to launch `ganga` and create our task:
```bash
ganga
%ganga ganga-fullChain.py
```
This creates a task inside `ganga` called `Bs2f1420Gamma_fullMC`. You can see 
the list of tasks by typing `tasks`. It will automatically generate the necessary 
jobs for the first step, submit them, monitor them and retrieve the output. When 
the first step is completed, it will automatically create the job to run the 
second step on the output of the first. `Ganga` can be off while a given step 
is running but needs to be running for it to retrieve the output and create 
the jobs to run the following step. 

Setting the `test` variable to `True` will create only 2 subjobs generating 
10 events each as a test but still run the full chain. In this case, the task 
has to be run manually using `task.run()`. This allows to check the configuration 
and modify it if needed before launching the test task. It is recommended to 
do this the first time you run to check all the steps are properly configured 
and linked together. After this, one can set the `test` variable to `False`. 
This will run 4 units (ie separate jobs for the same step) with 500 subjobs 
generating 200 events each, ie a total of 1M events. Notice that it might 
take a while for `Ganga` to create and submit the jobs once a task is running 
and it is not very verbose while doing so. So please be patient.


## Local tests

### Gauss Job configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc48-opt
~/cmtuser/GaussDev_v49r10/run bash
gaudirun.py Gauss-Job.py Gauss-evts.py
```
where the `GaussDev_v49r10` project should have the new decfile options `13102601.py` created with `make install`.

This creates the following files: `Gauss-13102601-5ev-20190605-histos.root`, `Gauss-13102601-5ev-20190605.sim`, 
`GeneratorLog.xml`, `NewCatalog.xml`, that are needed to test the rest of the steps locally.


### Boole Job configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc49-opt
lb-run Boole/v30r3 bash
gaudirun.py Boole-Job.py Boole-input.py
```

This needs the `Gauss-13102601-5ev-20190605.sim` and `NewCatalog.xml` files produced by the Gauss job and 
produces `Boole.digi` and `Boole-histos.root`.


### L0 Job configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc48-opt
lb-run Moore/v25r4 bash
gaudirun.py L0-Job.py L0-input.py
```

This needs the `Boole.digi` file produced by the Boole job and the `NewCatalog.xml` file produced by the Gauss job.
It produces `13102601-L0App.digi`.


### HLT Job configuration

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


### Brunel Job configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc49-opt
lb-run Brunel/v50r5 bash
gaudirun.py Brunel-Job.py Brunel-input.py
```

This needs the `13102601-HLT2.digi` file produced by the HLT2 job 
and the `NewCatalog.xml` file with the link to the `.sim` file to copy the MC 
information to the output `DST`.
It produces `Brunel.dst` and `Brunel-histos.root`.

#### Note on the Brunel version
In the production request 48724 `Brunel/v50r4` was used with `x86_64-slc6-gcc62-opt`. 
However this version is not available under this platform. Moreover, this version 
is marked as obsolete in the [Brunel project page](http://lhcbdoc.web.cern.ch/lhcbdoc/brunel/releases/). So we move to `Brunel/v50r5` and use it with `x86_64-slc6-gcc49-opt`, 
which is the only platform for which this version is available in `cvmfs`.


### Stripping step configuration

This can be run for local tests like:
```bash
LbLogin -c x86_64-slc6-gcc49-opt
lb-run DaVinci/v41r4p5 bash
gaudirun.py Strip-Job.py Strip-input.py
```

This needs the `Brunel.dst` file produced by the Brunel job and produces the files
`000000.AllStreams.dst` and `DVHistos.root`. 