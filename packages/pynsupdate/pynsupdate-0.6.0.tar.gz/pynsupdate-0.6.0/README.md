# pynsupdate

A python wrapper to Dynamically update DNS using nsupdate. The reason is that 

* Why not use bash?
  I didn't really want to mess with parsing the output of `ip` figuring out how to remove
  what I don't want using `shell script`.

# Installation

You can either install with:

> [!CAUTION]
> Most distributions will frown at installing packages from pip. It might break things.

```sh
pip install pynsupdate
```

Or create a `virtual environment` and run the the same command within the venv.

## Requirements

If you really want to install by hand. See `pyproject.toml` for dependencies.

# Usage

The tool basically takes all the commands via command line. You will probably
run something like:

```sh
pynsupdate --zone <ZONE> --dns-server <IP or Name of DNS server> --key-file <location of the update key file>
```

> [!NOTE]
> Zone parameter must end with the '.'

For more details, use `-h` option. You w

# Features

* Support to multiple hostnames;
* Support for TSIG signatures (using `tsig-keygen`);
* Support for multiple IPs, both IPv4 and IPv6;
* Support for ignoring networks;

I haven't tested yet other keys (like the ones genereated by `ddnsec-keygen`). Maybe it works, maybe it doesn't.

# Automated updates

You can find on how to configure the service to run automatically
in this section.

This is a two part. A service and a timer.

## Service (SystemD)

Add the following to `/etc/systemd/system/pynsupdate.service`.

The examples below use a specific create user, `pynsupdate` and installation
path in `/opt/pynsupdate`. 

### Virtual environment

```
[Unit]
Description=Runs pynsupdate
After=network.target
Wants=pynsupdate.timer

[Service]
Type=oneshot
User=pynsupdate
WorkingDirectory={{ PYNSUPDATE_DIR }}
ExecStart=/opt/pynsupdate/.venv/bin/pynsupdate --zone {{ ZONE }} --dns-server {{ DNS_SERVER }} --key-file {{ KEY_PATH }} --ttl {{ TTL }}

[Install]
WantedBy=multi-user.target
```

### System install 

Basically the same, but change the `ExecStart`. Your distro might have a different installtion
path.

```
[Unit]
Description=Runs pynsupdate
After=network.target
Wants=pynsupdate.timer

[Service]
Type=oneshot
User=pynsupdate
WorkingDirectory={{ PYNSUPDATE_DIR }}
ExecStart=/usr/bin/pynsupdate --zone {{ ZONE }} --dns-server {{ DNS_SERVER }} --key-file {{ KEY_PATH }} --ttl {{ TTL }}

[Install]
WantedBy=multi-user.target
```

Once the file is there, you can test with `systemctl start pynsupdate.service`.

## Timer

You can use the timer at any point. From some very brief research, the upate time should be 
half the amount of the lease time.

Add the following to `/etc/systemd/system/pynsupdate.timer`.

```
[Unit]
Description=Enable pynsupdate timed updates
Requires=pynsupdate.service

[Timer]
Unit=pynsupdate.service
OnCalendar={{ CALENDAR SPECIFICATION }}

[Install]
WantedBy=timers.target
```

## Wrapping everything together

Once both files are in place and tested, run the following:

```
systemctl daemon-reload
systemctl enable --now $PYNSUPDATE_TIMER
```

This will make the timer run immediately and enable the timer. 

# Limitations

* Doesn't generate reverse zones

# References

* https://opensource.com/article/20/7/systemd-timers
* https://wiki.archlinux.org/title/Systemd/Timers


