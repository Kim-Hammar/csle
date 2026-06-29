# Level 8

An emulation environment with a set of nodes that run common networked services such as SSH, FTP, Telnet, IRC, Kafka, 
etc. Some of the services are vulnerable to different network attacks 
such as the SambaCry exploit, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1,and SQL injection. 
Moreover, some nodes are vulnerable to privilege escalation attacks (e.g. CVE-2010-0426 and CVE-2015-5602) 
which can be used by the attacker to extend his privileges after compromising the host.    
The task of an attacker agent is to identify the vulnerabilities and 
exploit them and discover hidden flags
on the nodes. Conversely, the task of the defender is to harden the defense of the nodes and to detect the 
attacker. 

- Number of nodes: 27
- IDS: Yes (Snort)
- Traffic generation: Yes
- Number of flags: 22
- Vulnerabilities: SambaCry, Shellshock, CVE-2015-1427, CVE-2015-3306, CVE-2016-100033_1,and SQL injection., 
- as well as SSH, FTP, Telnet servers that can be compromised using dictionary attacks

## Architecture

<p align="center">
<img src="env.png" width="600">
</p>

## Useful commands

```bash
make install # Install the emulation in the metastore
make uninstall # Uninstall the emulation from the metastore   
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../../../../LICENSE.md)

Creative Commons

(C) 2020-2026, Kim Hammar