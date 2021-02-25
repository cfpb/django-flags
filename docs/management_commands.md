# Management Commands

Django-Flags provides two management commands that allow for enabling and disabling of feature flags from the command line.

## `enable_flag FLAG_NAME`

Enable a flag by adding or setting an existing database boolean condition to `True`. If the flag has other required conditions, those will take precedence. 

This command calls the [`flags.state.enable_flag` function](../api/state#enable_flagflag_name-create_boolean_conditiontrue-requestnone) function.

```
./manage.py enable_flag MY_FLAG
```

## `disable_flag FLAG_NAME`

Disable a flag by adding or setting an existing database boolean condition to `False`. If the flag has other required conditions, those will take precedence. 

This command calls the [`flags.state.enable_flag` function](../api/state#disable_flagflag_name-create_boolean_conditiontrue-requestnone) function.

```
./manage.py disable_flag MY_FLAG
```
