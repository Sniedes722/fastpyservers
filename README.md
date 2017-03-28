# fastwebserver
Async Python 3.5+ Web Server built with UVLoop

## First Benchmark Test
Even without any sort of HTTP Parser or router implementation, the results were as followed:
```
Running 20s test @ http://sneedserver.herokuapp.com
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   184.23ms   53.95ms   1.16s    90.81%
    Req/Sec   109.04     39.19   202.00     67.99%
  21739 requests in 20.05s, 5.14MB read
Requests/sec:   1084.22
Transfer/sec:    262.54KB
```
A 20 second test was run using 10 workers and 200 open connections. The server was running on Heroku's basic deployment.

## TODO
- Add httptools as parser
- Enable routing
- More detail request/responses
- Implement gunicorn pattern
