# Datalift

> The tool that help you store and retrieve tools outputs.

`pip install datalift`

Datalift it is a command-line tool designed to tools outputs to a storage service.
Users can input data either by passing a filename or through stdout from another tool.

The application is designed to streamline the process of uploading and
organizing data, making it easy for users to securely store and access their
data.

This project comes from splitting SARF into multiple modules.

## Using this package as a standalone app

```bash
datalift -h
usage: datalift [-h] [--download] [--stdout] [--path PATH] [filename]

Upload data and send notifications.

positional arguments:
  filename     name of file

optional arguments:
  -h, --help   show this help message and exit
  --download   download file from storage
  --stdout     print content to stdout
  --path PATH  file uploaded file. uuid generated if not provided

# Example
echo "Tool output" | datalift
Dummy Storage in use! Change it in configuration.
Uploaded in e3bca2eb-496b-447d-b2b8-e0ebce6f5351
```


### Configuration

If you plan to use datalift as a CLI app you should create a configuration file in
`/etc/datalift/config.yml`.

In the configuration file you should configure your storage backend:

Example with a dummy backend

```yaml
storage_backend:
  type: dummy
```

Example with a ftp backend
```yaml
storage_backend:
  type: ftp
  conf:
    user: admin
    password: admin
    host: localhost
    basedir: /
```
