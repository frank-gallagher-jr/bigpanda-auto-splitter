## AUTO-SPLITTER

**BigPanda Incident Auto-Splitter**

Frank Gallagher | BigPanda Solution Architect | May 2024 - https://github.com/frank-gallagher-jr

PURPOSE: This script will take a highly correlated event in BigPanda and split ALL correlated alerts into individual BigPanda incidents.

USE CASE: You made a mistake or you were not strict enough with correlation and you accidentally correlated alerts which shouldn't be correlated together (generally due to poor source data quality and generic use of tag values)

For example: Let's say you have a correlation pattern of "Service" which looks for opportunities to group alerts together over 2 hours. If alerts come in from an observability host with a generic Service tag value such as "Monitoring" due to a generic payload issue, you may find out that the correlation pattern needs to be updated far too late to prevent this unwanted behavior.

Auto-Splitter takes your environment ID (found in the URL of BigPanda) and the incident ID (found in the URL of BigPanda) and automatically splits all of the alerts out into their own new BigPanda Incidents.  This saves manual operations in the BigPanda UI which would be tedious.

	USAGE: python3 auto-splitter.py <Insert Environment ID> <Insert Incident ID to be fully split>


**USE WITH CAUTION AND USE WISELY!** 

**MAKE NOTE: The Split function is asynchronous.**

Read more about the API here: https://docs.bigpanda.io/reference/split-incident
