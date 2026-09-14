---
title: Management System
permalink: /docs/management-system/
---

## Management System

The management system is the central component of CSLE and manages the overall execution of the framework. 
It is a distributed system that consists of N >= 1 physical servers connected through an IP network. 
One of the servers is designated to be the "leader" and the other servers are "workers". 
Workers can perform local management actions but not actions that affect the overall system state. 
These actions are routed to the leader, which applies them sequentially to ensure consistent 
updates to the system state.

The leader is elected using a leader election protocol that uses the metastore for coordination (see Fig. 3). 
A new leader is elected by a quorum whenever the current leader fails or becomes unresponsive. 
This means that the management system tolerates up to N/2-1 failing servers.

<p align="center">
<img src="./../../img/mgmt_system.png" width="40%">
<p class="captionFig">
Figure 3: Architecture diagram of the management system; 
it is a distributed system with a designated leader, 
which is elected using a leader election algorithm that uses the metastore for coordination.
</p>
</p>

Each server of the management system executes the following services: 
(1) an instance of the emulation system; (2) a replica of the metastore; 
(3) an instance of the simulation system; (4) an HTTP server; and (5), 
a set of monitoring services, namely Prometheus, Grafana, cAdvisor, and Node exporter (see Fig. 4).

<p align="center">
<img src="./../../img/grafana_screenshot.png" width="60%">
<p class="captionFig">
Figure 4: A Grafana dashboard for monitoring a physical server of the management system; 
cAdvisor and Node exporter are used to push system metrics to Prometheus, 
which stores the metrics in a time-series database, whose data is visualized with Grafana dashboards.
</p>
</p>

Management actions on a server (e.g., starting containers, stopping emulations, or reading log files) are executed by a *cluster manager*, a gRPC server that runs on each server of the management system. The cluster manager is only reachable with a shared secret: every request from the REST API or the CLI must carry the `cluster_manager_token` defined in the configuration (`config.json`) as gRPC metadata, and requests without a valid token are rejected. Users authenticate towards the REST API with session tokens, so the cluster manager token is a service-to-service credential that is never exposed to end users. See the installation guide for how to configure the token.
