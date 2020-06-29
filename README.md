eNMS
An enterprise-grade vendor-agnostic network automation platform.
Branch	Status	Coverage	Documentation	Python Style	JavaScript Style	License
master	Build Status (master branch)	Coverage (master branch)	Documentation (master branch)	PEP8
Code style: black	Code style: google
Code style: prettier	License
develop	Build Status (develop branch)	Coverage (develop branch)	Documentation (develop branch)
Introduction
eNMS is a vendor-agnostic NMS designed for building workflow-based network automation solutions.

eNMS

It encompasses the following aspects of network automation:

Configuration Management Service: Backup with Git, change and rollback of configurations.
Validation Services: Validate data about the state of a device with Netmiko and NAPALM.
Ansible Service: Store and run Ansible playbooks.
REST Service: Send REST calls with variable URL and payload.
Python Script Service: Any python script can be integrated into the web UI. eNMS will automatically generate a form in the UI for the script input parameters.
Workflows: Services can be combined together graphically in a workflow.
Scheduling: Services and workflows can be scheduled to start at a later time, or run periodically with CRON.
Event-driven automation: Services and workflows can be triggered by an external event (REST call, Syslog message, etc).
Main features
1. Network creation
Your network topology can be created manually or imported from an external Source of Truth (OpenNMS, LibreNMS, or Netbox). Once created, it is displayed in a sortable and searchable table. A dashboard provides a graphical overview of your network with dynamic charts.
