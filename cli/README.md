# SARF CLI

## Add the output of a tool to SARF

The output of any console tool can be redirected to sarf. It doesn't matter if
these are in plain text or binary.
In order for sarf to prepare to receive the output of a tool, the `--ingest`
flag must be added to it.

`nmap 192.168.1.0/24 | sarf --ingest --tags nmap,network:192.168.1.0 --report lbk`

`--tags` flag is optional. It adds tags to the received data that can be
    very useful to interconnect with other tools.

The received data must be associated with a report.
The chosen report will be obtained from the environment variable SARF_REPORT.
The chosen report can also be provided explicitly with the `--report` flag.

> This is all for now. SARF is at a very early stage of its development.
  Give it a star on [github](https://github.com/elchicodepython/SARF-Security-Assesment-and-Reporting-Framework) to find out all its progress.
