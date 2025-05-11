[![CICD](https://github.com/aschulte201/logctx/actions/workflows/cicd.yml/badge.svg?branch=main)](https://github.com/aschulte201/logctx/actions/workflows/cicd.yml)

## Enabling

The core module provides a `logging.Filter` subclass designed to inject the current active context into any log messages.

Below is a demo usage on how to enable context injection:

```python
import logging
import logctx

root_logger = logging.getLogger()
console_handler = logging.StreamHandler()

formatter = jsonlogger.JsonFormatter("%(logctx)s")
context_filter = ContextInjectingLoggingFilter(output_field="logctx")

console_handler.setFormatter(formatter)
console_handler.addFilter(context_filter)

root_logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)
```

# Generators
* During execution
* Between yields

## Log Arguments
* Raises during initializtaion
* Value Error
* Able to rename args
* Unable to extract from kwargs
* Unable to work on generators
* Unable to work on async functions

# update
* can change root context