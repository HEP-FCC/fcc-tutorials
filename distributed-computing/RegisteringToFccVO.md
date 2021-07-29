# Getting started with FCC distributed computing

## Registering to the FCC VO

The [standard Grid VO registration procedure][signup]
should be followed to be enable to use the resources connected with the FCC VO.

> **NOTE**<br> 
> You need to use a browser where you have installed your certificate and the CERN CA certificates.
> Firefox usually works fine, Google Chrome usually does not work. Safari might also work.

[signup]: https://voms2.cern.ch:8443/voms/fcc/aup/sign.action

## Enabling DIRAC

DIRAC available on CernVM-FS. To enable the relevant applications and scripts, the
following setup script needs first to be sourced

```
source /cvmfs/clicdp.cern.ch/DIRAC/bashrc
```

To submit jobs through DIRAC a proxy needs to be created and uploaded:

```
dirac-proxy-init -g fcc_user
```
A successful creation looks like this:
```
Generating proxy...
Enter Certificate password:
Added VOMS attribute /fcc
Uploading proxy..
Proxy generated:
subject      : /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis/CN=2178341058/CN=3000266373
issuer       : /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis/CN=2178341058
identity     : /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis
timeleft     : 23:53:58
DIRAC group  : fcc_user
path         : /tmp/x509up_u2759
username     : ganis
properties   : NormalUser
VOMS         : True
VOMS fqan    : ['/fcc']

Proxies uploaded:
 DN                                                                           | Group | Until (GMT)
 /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis |  | 2022/05/13 12:12
```
The last section shows the valid proxies upload to the DIRAC system. It can also be checked with
```
$ dirac-proxy-info -m
subject      : /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis/CN=2178341058/CN=3000266373
issuer       : /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis/CN=2178341058
identity     : /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis
timeleft     : 23:50:40
DIRAC group  : fcc_user
path         : /tmp/x509up_u2759
username     : ganis
properties   : NormalUser
VOMS         : True
VOMS fqan    : ['/fcc']
== Proxies uploaded ==
DN                                                                           | Group | Until (GMT)
/DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis |  | 2022/05/13 12:12
```

If everything worked fine, your proxy should be mapped to the `fcc001` user. This can be checked this way:

```
$ export EOS_MGM_URL=root://eospublic.cern.ch
$ XrdSecPROTOCOL=gsi,unix eos whoami
Virtual Identity: uid=140035 (99,140035) gid=2855 (99,2855) [authz:gsi] host=lxplus743.cern.ch domain=cern.ch geo-location=0513
```

At CERN the uid of `fcc001` is 140035.

## The web portal

The [DIRAC web portal][diracweb] is available to check the status of things. It shows all the jobs submmited and the
files registered. Some example screenshot is shown below.

> **NOTE**<br>
> As for the VO registration, you need to use a browser where you have installed your certificate and the CERN CA certificates.
> Firefox usually works fine, Google Chrome usually does not work. Safari might also work.

[diracweb]: https://voilcdiracwebapp2.cern.ch/DIRAC/?view=tabs&theme=Crisp&url_state=1|*DIRAC.JobMonitor.classes.JobMonitor




