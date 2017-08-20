# python_buildovpn
Build client OpenVPN configs automatically with Python

## How-to
* Edit '\configs\config.template' to suit your general needs
* Edit 'OVPN_DIR' path in 'build-config.py'
* Ensure keys have been built already for the client
* Run 'build-config.py', when prompted enter the client name (used to find key files)

## Notes
* This was written specifically for my configuration, but it should be fairly general for simple networks.
* It includes a fix to have Windows clients treat the OVPN network as a private network, by setting a low-metric default gateway.
* It also creates two config files per client: One does not affect the server-pushed routes, and the other ignores all pushed routes and only sets up routing for the VPN subnet. I found this useful as my VPN server is set to route all traffic, but sometimes for the sake of speed I want routing between VPN clients/server but not routing of all online traffic.
