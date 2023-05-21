# Using SARF from Docker

⚠️ This is currently under development. See detected problems.

Deploy the infra of SARF with docker could be a great idea.
As you should know SARF its not coupled to an specific backend
so this is just an example of how we could configure SARF.

To do this you can use the docker-compose provided in this folder.

Take into account that the default infrastructure configuration
is insecure so please don't expose it.

## Detected problems

The FTP image in use is crashing after some seconds.
We need to found other that keeps running.
