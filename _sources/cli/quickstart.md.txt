# CLI

## Installation

`pip install sarf`

This version of `SARF` works with a `FTP` Server as a storage backend
and a `rabbitmq` as a pubsub.

### Running a custom FTP Server as a tools storage backend

```bash
docker run -d \
    -p 21:21 \
    -p 21000-21010:21000-21010 \
    -e USERS="sarf|sarf" \
    --name "sarf_ftp" \
    delfer/alpine-ftp-server
```

## Configuration

Before continuing check you can access to the rabbitmq and the FTP.

Once all the components are installed we can write SARF configuration file
in /etc/sarf/config.yml. If this file does not exist, create it.

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

storage_backend:
  tools:
    upload:
      type: "ftp"
      conf:
        user: "sarf"
        password: "sarf"
        host: "127.0.0.1"
        basedir: "/ftp/sarf"
```

## Usage

### Add the output of a tool to SARF

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
