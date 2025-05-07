# Ideas

## Separate env loading from .env reading

Statements:

**The `application` should not read any `environment` configuration file.**

- The execution will be the same for any run environment, local app, docker, kubernetes - no local files


**The `environment` should be `delivered` to the `application`.**

- Loading and delivering `environment` should be done by separate process.

**The `application` needs to map `environment variables` into `Config` object.

- The applications could do it easily


## Runenv

Features which runenv should deliver:

**The CLI:**

- manages different environments / env files for dev, pre, and prd - use .runenv/ directory; allow export  current as .env (target file) to use with f.e. docker --load-env
- loads defined environment file and run target application
- decrypts / encrypts whole .env or single variables - how to deliver/split keys? sops? age? pluggable?

**The API:**

- loads environment variables into Config object
- cast types using defined fields and types
- optionally decrypt variables using some RUNENV_SECRET (test or path to key file) - delivered separately from runenv variables


**Language?:**

- CLI could be written in any language, f.e. golang - installed separately or during f.e. pip install
- The SDK to load variables can be written in different languages:
    - python
    - javascript
    - golang
    - java
    - lua
    - ruby


## Similar project

- pydantic settings - loads env, check and compare
- sops + direnv - decrypts and loads environment for local env
