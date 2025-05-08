# sopel-managerbot

"Manager-like" approval/denial responses for Sopel IRC bots.

(Note: Does not manage other Sopel instances. That plugin would have to be
called `sopel-botmanager`. 😉)

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-managerbot
```

## Using

This plugin provides two command sets:

* `.approve`/`.yes`: Fetches a "yes" reason from [yes-as-a-service][]
* `.deny`/`.no`: Fetches a "no" reason from [no-as-a-service][]

These commands do not take any arguments.


[yes-as-a-service]: https://github.com/misterdim/yes-as-a-service
[no-as-a-service]: https://github.com/hotheadhacker/no-as-a-service
