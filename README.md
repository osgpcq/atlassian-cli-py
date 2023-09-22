# atlassian-cli-py
Atlassian Python command-line interface.

Extract informations from Atlassian.


# Usage
```
./atlassian-cli.py --help
options:
  -h, --help       show this help message and exit
  --client CLIENT  Choose the credential (default: exo)
  --users          List users (default: False)
  --debug          Debug information (default: False)
  --verbose        Verbose (default: False)

./atlassian-cli.py
╭────┬─────────────────────────────────────────────┬─────────────┬──────────────┬──────────┬─────────┬──────────────────┬──────────╮
│    │ accountId                                   │ accountType │ displayName  │ active   │ locale  │ emailAddress     │ timeZone │
├────┼─────────────────────────────────────────────┼─────────────┼──────────────┼──────────┼─────────┼──────────────────┼──────────┤
│  0 │ 000000:ffffffff-ffff-ffff-ffff-ffffffffffff │ atlassian   │ User1 User01 │ False    │ es_ES   │ email@domain.ext │          │

```


# History
Still in quick & dirty dev phase!
