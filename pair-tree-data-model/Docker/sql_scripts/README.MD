<h1>READ ME</h1>
<p>
These scripts are used to enable notification on the Postgres database whenever an operation is performed on the SAMPLES
table. You can apply these using psql (CLI), via pgAdmin, or via a Python program (e.g. the main.py under 
the ORM directory).
</p>

<h2>Sample_changed.sql:</h2>
<p>
This enables Triggers on the SAMPLES Table whenever an INSERT or UPDATE operation is done on it.
</p>

<h2>Samples_notify.sql:</h2>
<p>
This script is invoked by the Trigger setup by the previous script. This creates an
 asynchronous NOTIFY message which contains the same record written onto the SAMPLES table.
</p>
 
<h2>TODO:</h2>
 The listener.py app (placed under the app folder) is designed receive these NOTIFY messages and extract the payload as
 JSON string. The Key-Value pairs it contains should be written to the Observation Table of the STA model inside the 
 FROST server.  As this is already in JSON format, perhaps we can just replace the "keys" with those of the STA models 
 and simply POST the string to the FROST-Server instead of going via SQL statements.