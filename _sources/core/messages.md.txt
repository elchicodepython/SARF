# CORE | Messages
Messages are one of the most important parts of `SARF`.
All tools that use `SARF` communicate through them.

In this section of the SARF we will see how this communication occurs.

## Generic information

### Required infrastructure

SARF messages are not tied to a specific technology. These can be sent through any piece of software that
allows messages communication.
Messages from one part of SARF may be sent over one technology and messages from another part over another.

Instead of referring to a specific piece of infrastructure such as rabbitmq we will refer to the Messages abstraction with the keyword [app]Messages. Being [app] the part of SARF that we are working with.

## App Messages


```{mermaid}
sequenceDiagram
    sarf->>[app]Messages: Send message
```

### Tools Messages

When a tool send his output to SARF this data is stored in a `Storage backend`, then a message with metadata is published using `[app]Messages`. In this way other tools could listen to this message in order
to perform custom actions.


```{mermaid}
sequenceDiagram
    app->>sarf: Pipe output
    sarf->>Storage: Upload file
    sarf->>[app]Messages: Notify Tool execution
```

### Tools Messages structure

Message metadata for tools contains the following fields:

- emitter: str
- tags: list[str]
- storage_type: str
- project_id: str
- path: str


## Listeners

```{mermaid}
sequenceDiagram
    sarf-listener-1->>[app]Messages: Listen messages
    sarf-listener-2->>[app]Messages: Listen messages
    sarf-listener-1->>MessageHandler-1: Process message
    sarf-listener-2->>MessageHandler-2: Process message
```
