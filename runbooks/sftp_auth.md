# SFTP Public Key Authentication Failure

System: SFTP

## Symptoms
The client reaches the SFTP server, but login fails with
`Permission denied (publickey)`.

## Diagnostic checks
1. Confirm the hostname, port, and service account.
2. Check that the client is offering the intended SSH key.
3. Ask the endpoint owner to compare the public key fingerprint
   with the key registered for that service account.

## Recovery steps
If the registered key is wrong, have the authorized endpoint owner
update it through the approved process. Run one controlled test
transfer and confirm the expected file reaches the destination.

## Escalation
If authentication still fails, contact the endpoint owner with the
UTC timestamp, service account alias, public key fingerprint, and
sanitized error. Never include the private key.