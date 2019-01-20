# ProxiesPool
This pool serve for crawler.

In the web crawler mission, the target website always restrict the access of data through IP address. For example, when the server found that lots of requests were from the same IP address in a very short time, the server will block the access from this IP.

To solve this problem, we need a pool which contains many proxy IPs. The crawler can get the new IP continually from this pool. And this pool can also update itself.
