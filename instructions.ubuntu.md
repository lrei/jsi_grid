## Get Certificate

Using Firefox:

go to  https://signet-ca.ijs.si
-> User -> Request a Certificate -> Request a certificate with automatic browser detection

PIN needs to be N numbers long e.g.: 91546546316

This will require approval from Jan Jona Javoršek (jona.javorsek@ijs.si).
so you will probably need to e-mail him before or after. 

Note: I had to give him an ID document (passport).

Now in Firefox go to:
Preferences -> Advanced -> Certificates -> View Certificates -> Select the SIGNET certificate -> Backup -> PKCS12

Use a serious password!


```bash
openssl pkcs12 -in usercert.p12 -clcerts -nokeys -out usercert.pem
openssl pkcs12 -in usercert.p12 -nocerts -nodes -out userkey.pem
chmod 400 userkey.pem
chmod 644 usercert.pem
mkdir ~/.arc
mv userkey.pem usercert.pem ~/.arc/
```

Note: the permissions are important - otherwise you get a cryptic error down the
line.

go to https://voms.sling.si:8443/voms/nsc.ijs.si
and request membership to the VO


## Intall Nordugrid/ARC Software

On Ubuntu 17.04:


```
sudo apt-get install nordugrid-arc-client nordugrid-arc-plugins-globus nordugrid-arc-plugins-needed
```


on Ubuntu 14.04 (taken from 
the [original instructions](http://www.sling.si/sling/uporabniki/uporabniski-vmesniki/nordugrid-arc-client-ubuntu-trusty-14-04/)):


```bash
wget http://download.nordugrid.org/repos/latest/ubuntu/dists/trusty/main/binary-amd64/nordugrid-release_13.11~trusty1_all.deb
sudo dpkg -i nordugrid-release_13.11~trusty1_all.deb
wget -q -O - http://download.nordugrid.org/DEB-GPG-KEY-nordugrid.asc | sudo apt-key add -
sudo apt-get install nordugrid-arc-client nordugrid-arc-plugins-globus
```


For both 14.04 and 17.04, edit `/etc/apt/sources.list` e.g.:


```bash
sudo vi /etc/apt/sources.list 
```


And append these lines:

```
#### EGI Trust Anchor Distribution ####
deb http://repository.egi.eu/sw/production/cas/1/current egi-igtf core
```


Run:


```bash
wget -q -O - https://dist.eugridpma.info/distribution/igtf/current/GPG-KEY-EUGridPMA-RPM-3 | sudo apt-key add -
sudo apt-get update
sudo apt-get install ca-policy-egi-core
mkdir -p ~/.arc/vomsdir
```


Create a file (e.g. vi) `~/.arc/vomsdir/voms.sling.si.lsc` and add the lines


```
/C=SI/O=SiGNET/O=SLING/CN=voms.sling.si
/C=SI/O=SiGNET/CN=SiGNET CA
```


Create a file `~/.arc/vomses` and add the line:


```
"nsc.ijs.si" "voms.sling.si" "15004" "/C=SI/O=SiGNET/O=SLING/CN=voms.sling.si" "nsc.ijs.si"
```


Then run


```bash
sudo apt-get install fetch-crl
```


Add `fetch-crl` to your crontab via `crontab -e` e.g.:\

```
0 0 * * * fetch-crl
```


Finally edit  `~/.arc/client.conf` amd add the lines:


```
[computing/nsc]
#url=ldap://nsc.ijs.si:2135
#infointerface=org.nordugrid.ldapng
#jobinterface=org.nordugrid.gridftpjob
url=https://arc.ijs.si:6000/arex
infointerface=org.ogf.glue.emies.resourceinfo
submissioninterface=org.ogf.glue.emies.activitycreation
default=yes
```


## Executing Jobs

I think the following has to be done often because of the validaty of the proxy:


```bash
arcproxy -S nsc.ijs.si
```


Then to submit a job. I have uploaded an example script and job description file.
The example is a simple test and its job description file should be modified for
real workloads: [full-test.tar](https://drive.google.com/file/d/0B3CDC49Z2hjxcnA1N29tZ3Byd28/view?usp=sharing)


```bash
tar -xf full-test.tar
arcsub -c nsc.ijs.si -S org.nordugrid.gridftpjob -o joblist.xml test-tf.xrsl -d DEBUG
```


Should return


```
...
Job submitted with jobid: gsiftp://nsc.ijs.si:2811/jobs/4qkMDmzm9kqnOeFSGmVnjcgoABFKDmABFKDmFsGKDmABFKDm6kGqvm
...
```


Submitting job files with data up to ~1GB is OK.
For larger files, contact Barbara, the admin: barbara.krasovec@ijs.si


To check the status of jobs (a few minutes after submitting):


```bash
arcstat -c nsc.ijs.si
```


And then to get the results:


```bash
arcget gsiftp://nsc.ijs.si:2811/jobs/4qkMDmzm9kqnOeFSGmVnjcgoABFKDmABFKDmFsGKDmABFKDm6kGqvm
```

## Listing the available RTE's
The available runTimeEnvironments are listed in the [status page](http://www.sling.si/gridmonitor/clusdes.php?host=nsc.ijs.si&port=2135&lang=en) or can be listed using `ldapsearch` that can be installed by:


```bash
 sudo apt install ldap-utils
```


```bash
ldapsearch -x -h nsc.ijs.si -p 2135 -b ' Mds-Vo-name=local,o=grid'| grep 'nordugrid-cluster-runtimeenvironment'
```

## Select XRSL Options
Extracted from [Nordugrid: Extended Resource Specification Language](http://www.nordugrid.org/documents/xrsl.pdf)

* **count** - Specifies amount of sub-jobs to be submitted for parallel tasks.
* **countpernode** - Specifies amount of sub-jobs per node to be submitted for parallel tasks. Note: The count attribute
must be specified when this attribute is specified.
* **cputime** - Maximal CPU time request for the job. For a multi-processor job, this is a sum over all requested
processors. This attribute should be used to direct the job to a system with sufficient CPU resources, typically,
a batch queue with the sufficient upper time limit. Jobs exceeding this maximum most likely will be
terminated by remote systems! E.g.: "2 day, 12 hours", "1 week", "1 hour, 30 minutes".
* **wallTime** - Maximal wall clock time request for the job. This attribute should be used to direct the job to a system with sufficient CPU resources, typically, a batch queue with the sufficient upper time limit. Jobs exceeding this maximum most likely will be
terminated by remote systems!
* **memory** - Memory required for the job, per count for parallel jobs. Similarly to cpuTime, this attribute should be used to direct a job to a resource with a sufficient capacity. Jobs exceeding this memory limit will most likely be terminated by the remote system.
* **notify** - Request e-mail notifications on job status change. E.g. (notify="be your.name@your.domain.com") notifications will be sent
at the job’s beginning (b) and at its end (e).
* **(environment=("OMP_NUM_THREADS" "8"))** Maximum is 64.


