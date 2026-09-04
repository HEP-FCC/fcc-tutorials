# Distributed computing: basic concepts

<!-- contributors:start -->
:::{admonition} Page contributors
:class: callout dropdown

Michel Villanueva
:::
<!-- contributors:end -->

:::{admonition} Learning Objectives
:class: objectives

- Understand why FCC simulation and analysis need computing resources distributed over many sites
- Know the difference between a local batch system and the grid
- Learn the vocabulary used in the rest of this chapter: Virtual Organization, certificate,
  proxy, job, sandbox, Storage Element, logical file name, replica, production
- Get a mental picture of what DIRAC does when you submit a job or register a file
:::

This page is written for readers who have never used grid computing in High Energy Physics (HEP). Its purpose is to explain the concepts that the
following pages take for granted. Experienced users of DIRAC, Rucio or familiar with the [WLCG](https://wlcg.web.cern.ch/) can skip straight to [Getting started with FCC distributed computing](RegisteringToFccVO.md).



## Why distributed computing?

A full detector simulation of a single FCC-ee event takes seconds of CPU time. Physics studies need billions of events 
for every process and every detector concept, and the resulting files [add up to tens of petabytes](https://doi.org/10.1140/epjp/s13360-021-02189-y). 
As FCC consolidates its physics case and detector designs, the computing needs will grow even further.
No single computing center is expected to provide that alone.

The High Energy Physics community solved this problem with the Worldwide LHC Computing Grid (WLCG): a
federation of computing centres, from CERN itself to national laboratories and university clusters, which agree to run 
each other's jobs and store each other's data using common interfaces and a common mechanism to identify users. 
"The grid" is the common name for this distributed computing system. 

At this moment, FCC does not have its own grid. It uses a share of the existing WLCG.

The grid is different from your local resources in different ways:

- **Nothing is local.** Your program runs on a machine you have never logged into. Everything it needs (software, input data, configuration) 
  has to be brought there, and everything it produces has to be stored somewhere.
- **Authentication is centrally handled.** A remote site has no account for you. Instead, sites trust the FCC Virtual Organization (VO).
  To use the grid, you need to become a member of the VO. All the certificate and proxy machinery described below exists to make this trust chain work.

### The grid and local batch systems 

A **batch system** is a scheduler that queues jobs and runs them on a farm of machines inside one computing center. 
For example, CERN runs [HTCondor](https://batchdocs.web.cern.ch/) on its farm, reachable from `lxplus`. Many universities run HTCondor or Slurm. In batch system 
you already have an account, the shared filesystem (AFS, EOS) is mounted on the worker nodes, and you can `ssh` in to look at things.

The grid glues many batch systems together behind a single interface. In exchange for scale, there is no shared filesystem across sites,
you cannot log in, and you need a grid identity rather than a local account.


## Design principles

### Compute vs Storage

A core design principle for distributed computing in HEP is the separation of **compute** vs **storage**.

* **Jobs are transient entities** that simply consume and produce data. They run on worker nodes, and once done they disappear. No information is preserved in the long term.
* In contrast, **data has persistence**, replication policies, and provenance — it “lives” long after a job finishes.

Following this logic, elements on the grid are divided into two categories:

| Building block | What it is |
|---|---|
| **Computing Element (CE)** | The site's front door for jobs. DIRAC talks to the CE; the CE hands work to the site's local batch system. | 
| **Storage Element (SE)** | A disk or tape service where files live. Each SE has a name inside DIRAC and speaks one or more transfer protocols. |


### Networking

Another core component of the grid is the network. Without networking, there is no distributed computing.

Sites are connected to each other through a combination of public internet and dedicated regional 
research networks (e.g. GÉANT, ESnet, Internet2).

CERN (as the Tier-0 center) is connected to the Tier-1 data centers around the world on a dedicated, private network called the 
LHC Optical Private Network (LHCOPN). It relies on dedicated long-distance optical-fiber links (10 to 100 gigabits per second), 
spanning oceans and continents.

Multiple federations across the Europe, Asia Pacific and the Americas are interconnected with LHC Open Network Environment (LHCONE). 
Unlike LHCOPN, LHCONE is not a set of dedicated physical links, but a virtual network that provides high-bandwidth, 
low-latency connectivity between sites, while also ensuring security and reliability without requiring new dedicated infrastructure.

Without going deep into the details, the idea is to illustrate the importance of networking in distributed computing.

:::{admonition} Note
:class: note
At the time of writing, FCC does not have its own dedicated network. It uses the WLCG infrastructure, sharing it the with the LHC and other HEP experiments.
::: 

### Software distribution

The [CERN VM File System](https://cernvm.cern.ch/fs/) (CVMFS) is a read-only filesystem that distributes software to worker nodes. 
It is mounted on every WLCG site, and it is a very efficient way to make software available to jobs that run on remote sites.

CVMFS is what makes it possible for a job to `source /cvmfs/sw.hsf.org/key4hep/setup.sh` on any worker node in the world and find exactly 
the same software you tested on a local resource like `lxplus`. 

Read more about CVMFS in the [documentation](https://cvmfs.readthedocs.io/en/stable/cpt-overview/).

## Identity and authorization

The grid needs to answer two questions for every request: *who are you* (authentication) and *what are you allowed to do* (authorization).

### Grid certificates

A **grid certificate** is an X.509 certificate, issued to you personally by a **Certification Authority (CA)**. CERN users obtain
theirs from the [CERN CA](https://ca.cern.ch/ca/). The certificate contains your  **Distinguished Name (DN)**, a string such as:
```
/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=feynman/CN=137137/CN=Richard Feynman
```

This DN is your identity on the grid, independent of any site or storage element.

- To register with a Virtual Organization you must present the certificate from a **web browser**, which means importing it into the browser first, 
  together with the CA certificates so that the browser trusts the registration site. 
- On interactive sessions (like in `lxplus`, the certificate is expected as two files, `~/.globus/usercert.pem` and `~/.globus/userkey.pem`, 
  which the DIRAC client reads when creating a proxy.

