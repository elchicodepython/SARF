# CLI

## Installation

`pip install sarf`

## Configuration

### Docker

SARF requires some infrastructure in order to work properly.
The bare minimum is a pubsub like rabbit where notifications will be sent
after each tool execution and a data storage that could be either an ftp
or an s3.

For a quickstart we can use the following docker compose.

```yaml
version: '3'

services:
  minio:
    image: minio/minio
    ports:
      - "9000:9000"
    environment:
      MINIO_ACCESS_KEY: minioaccesskey
      MINIO_SECRET_KEY: miniosecretkey
    volumes:
      - ./s3_data:/data
    command: server /data

  rabbitmq:
    image: rabbitmq:latest
    ports:
      - 5672:5672
      - 15672:15672
    volumes:
      - ./rabbitmq_data:/var/lib/rabbitmq
    environment:
      - RABBITMQ_DEFAULT_USER=sarf_queue_admin
      - RABBITMQ_DEFAULT_PASS=sarf_queue_password

```

Once all the components are running we can write SARF configuration file.

The configuration file can be either in:

- /etc/sarf/config.yml
- ~/.config/sarf_config.ymk
- sarf_config.yml

If this file does not exist, create it with the
following content.

```yaml
defaults:
  rabbitmq_queue_conf: &default_rabbitmq_conf
    type: "rabbitmq"
    connection_string: amqp://sarf_queue_admin:sarf_queue_password@localhost:5672/

messages:
  # Name to be sent in messages as the emitter
  # of the actions made with this instance
  emitter: "ethical hacker email or identifier"

  tools:
    __baseconf: &__baseconf_tools_messages
      <<: *default_rabbitmq_conf
      queue: "tools"
    pub: *__baseconf_tools_messages
    sub: *__baseconf_tools_messages

  reports:
    __baseconf: &__baseconf_reports_messages
      <<: *default_rabbitmq_conf
      queue: "reports"
    pub: *__baseconf_reports_messages
    sub: *__baseconf_reports_messages

storage_backend:
  tools:
    upload:
      type: "s3"
      conf:
        access_key: minioaccesskey
        secret_key: miniosecretkey
        endpoint_url: http://127.0.0.1:9000
        bucket: tools

  reports:
    upload:
      type: "s3"
      conf:
        access_key: minioaccesskey
        secret_key: miniosecretkey
        endpoint_url: http://127.0.0.1:9000
        bucket: reports
```

## Add the output of a tool to SARF

The output of any console tool can be redirected to sarf. It doesn't matter if
these are plain text or binary.

This version of `SARF` works with a `FTP` or an `S3` Server as a storage backend
and a `rabbitmq` as a pubsub.

In order for sarf to prepare to receive the output of a tool, the `ingest`
flag must be added to it.

`nmap 192.168.1.0/24 | sarf ingest --tool nmap --tags network:192.168.1.0 --report KNB-21`

`--tags` flag is optional. It adds tags to the received data that can be
    very useful to interconnect with other tools.

The received data must be associated with a report.
The chosen report will be obtained from the environment variable SARF_REPORT.
The chosen report can also be provided explicitly with the `--report` flag.

### TIPS

- If you are using a ticketing system like JIRA can be handy to define the report
  as a ticket and use the ticket id as a report id.

- The infrastructure needs to be deployed one single time. You can deploy it in
  a local network and work together with all your coworkers.
