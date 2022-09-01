# CLI

## Installation

`pip install sarf`

## Configuration

Before continuing check you can access to the rabbitmq and the FTP.

Once all the components are installed we can write SARF configuration file
in /etc/sarf/config.yml. If this file does not exist, create it with the
following content.

```yaml
messages:
  # Name to be sent in messages as the emitter
  # of the actions made with this instance
  emitter: "ethical hacker email or identifier"

  tools:
    pub:
      type: "rabbitmq"
      connection_string: ""
      queue: "tools"

  reports:
    pub:
      type: "rabbitmq"
      connection_string: ""
      queue: "tools"

storage_backend:
  tools:
    upload:
      type: "ftp"
      conf:
        user: "sarf"
        password: "sarf"
        host: "127.0.0.1"
        basedir: "/ftp/sarf/tools"

  reports:
    upload:
      type: "ftp"
      conf:
        user: "sarf"
        password: "sarf"
        host: "127.0.0.1"
        basedir: "/ftp/sarf/reports"

crud:
  companies:
    type: json
    conf:
      filename: ~/.sarf/data/companies.json

  projects:
    type: json
    conf:
      filename: ~/.sarf/data/projects.json

  reports:
    type: json
    conf:
      filename: ~/.sarf/data/reports.json

  vulnerabilities:
    type: json
    conf:
      filename: ~/.sarf/data/vulnerabilities.json

  vuln_templates:
    type: json
    conf:
      filename: ~/.sarf/data/vuln_templates.json
```

The folder `~/.sarf` should be created also. This is the folder
where SARF will store the data files defined in the previous
configuration.


You are doing great! Lets achieve the next level together.

```
SARF~$ sarf

   ____    _    ____  _____
  / ___|  / \  |  _ \|  ___|
  \___ \ / _ \ | |_) | |_
   ___) / ___ \|  _ <|  _|
  |____/_/   \_\_| \_\_|

  Welcome to SARF - XXXXXX edition
  The Security Assesment and Reporting Framework.

Usage: sarf --help
```

## Work with SARF Projects

Projects are the main unit of a security assesment in SARF.

An app could have multiple penetration tests.
Each penetration test must be associated with a report.
All the related reports for the same asset should belong to the same project.

```bash
SARF~$ sarf --projects --addi
[+] name: Web elchicodepython.github.io
[+] Saved with uuid 77d78b25-56ef-480f-8745-88e9a66b937c
```

## Start a SARF Report

```bash
SARF~$ sarf --reports --addi
In the next step you are going to search for a Project
name to search:
Found 1 items. Continue? [Y]:
? Project  elchicodepython.github.io
? Report name  11/22 Periodic security assesment to elchicodepython.github.io
[+] Saved with uuid dc1687ce-65ab-4946-ad59-9c27d427a4b5
```

After creating a `Report` you can list all the existing reports
with the flag `--get-all`. This flag also works with all the sarf `CRUD objects`, more on this later.

```bash
SARF~$ sarf --reports --get-all
[+] dc1687ce-65ab-4946-ad59-9c27d427a4b5: 11/22 Periodic security assesment to elchicodepython.github.io
[+] 22d5c89f-4e98-4847-844e-9c40a61c5dfe: 10/22 Periodic security assesment to elchicodepython.github.io
```

## Add a vulnerability to a Report

```bash
SARF~$ sarf --vulns --addi
? Use template?  No
? Title
...
```

## Creating vulnerability templates

SARF can use `Vulnerability templates` to speed up the security assesment reporting
process. `Vulnerability templates` can be created manually with the following command:
`sarf --vuln-templates addi`. After creating a Vulnerability template they can be selected
to fill some defaults for the vulnerability fields like the title, description and references.

Vulnerability templates can also be imported with a script from a third party.

**Importing Vulnerability templates from vuln_repo**
```
cd /tmp
git clone https://github.com/elchicodepython/SARF-Security-Assesment-and-Reporting-Framework
cd SARF-Security-Assesment-and-Reporting-Framework/vendors/templates/vuln_repo/
./download_templates.sh
python import_templates.py
```

You may see the following output after importing the templates.
```
SARF~$ python import_templates.py
Importing [XSS] Stored cross-site scripting
Importing [XSS] Reflected cross-site scripting
...
```

After importing the templates you will have the capability to select a
template when writting a vulnerability. **This will speed-up your reporting
workflow.**

> Take into account that SARF reporting engine is not ready yet.
  It will be available in 0.4.

## SARF CRUD objects

SARF `crud objects` are:
- projects `--projects`
- reports  `--reports`
- vulnerabilities `--vulns`
- vulnerability templates `--vuln-templates`

SARF CRUD objects can perform CRUD operations using the following flags:
- `--get <UUID>`
- `--get-all`
- `--addi`
- `--add <UUID> field1:value1;field2:value2` Only recommended for scripting.
- `--delete <UUID>`


## Add the output of a tool to SARF

The output of any console tool can be redirected to sarf. It doesn't matter if
these are plain text or binary.

This version of `SARF` works with a `FTP` Server as a storage backend
and a `rabbitmq` as a pubsub.

You can run a custom FTP tools backend on docker using the following command:

```bash
docker run -d \
    -p 21:21 \
    -p 21000-21010:21000-21010 \
    -e USERS="sarf|sarf" \
    --name "sarf_ftp" \
    delfer/alpine-ftp-server
```

In order for sarf to prepare to receive the output of a tool, the `--ingest`
flag must be added to it.

`nmap 192.168.1.0/24 | sarf --ingest --tags nmap,network:192.168.1.0 --report 98aa3c7e-5e15-4b6a-a009-83be6d2597ff`

`--tags` flag is optional. It adds tags to the received data that can be
    very useful to interconnect with other tools.

The received data must be associated with a report.
The chosen report will be obtained from the environment variable SARF_REPORT.
The chosen report can also be provided explicitly with the `--report` flag.
