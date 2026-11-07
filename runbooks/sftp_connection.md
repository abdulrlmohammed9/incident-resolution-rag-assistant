# SFTP Connection Timeout

System: SFTP

## Symptoms
The client cannot establish a TCP connection to the SFTP endpoint.
The connection times out before SSH authentication starts.

## Diagnostic checks

1. Confirm the destination hostname and port in the SFTP client configuration.
2. From the Windows machine that runs the transfer, open PowerShell and test
   the configured TCP port. Replace `sftp.example.com` and `22` with the
   hostname and port from the client configuration.

   ```powershell
   Test-NetConnection -ComputerName "sftp.example.com" -Port 22
   ```

   - `TcpTestSucceeded : True` means a TCP connection was established.
     SSH authentication and file transfer still need to be verified separately.
   - `TcpTestSucceeded : False` means the TCP connection could not be
     established from that machine. Check the hostname, port, network route,
     firewall, and outbound IP allowlist.
3. If the test fails, ask the endpoint owner to confirm that the service is
   listening on the configured port and that the transfer machine's outbound
   IP is on the allowlist.

## Recovery steps
Have the network or endpoint owner correct the connectivity issue.
Once the port is reachable, run one controlled test transfer and confirm
the file arrived at the destination.

## Escalation
If the port remains unreachable, escalate to the network team or endpoint
owner. Include the UTC timestamp, destination hostname and port, source
environment, and sanitized timeout message.