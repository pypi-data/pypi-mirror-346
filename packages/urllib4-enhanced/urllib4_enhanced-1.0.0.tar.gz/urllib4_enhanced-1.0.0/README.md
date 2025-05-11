<h1 align="center">

# urllib4: A Modern HTTP Client for Python

</h1>

<p align="center">
  <a href="https://pypi.org/project/urllib4-enhanced"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/urllib4-enhanced.svg?maxAge=86400" /></a>
  <a href="https://pypi.org/project/urllib4-enhanced"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/urllib4-enhanced.svg?maxAge=86400" /></a>
  <a href="https://github.com/zinzied/urllib4/actions?query=workflow%3ACI"><img alt="Coverage Status" src="https://img.shields.io/badge/coverage-100%25-success" /></a>
</p>

urllib4 is a powerful, *user-friendly* HTTP client for Python. It builds on the solid foundation of urllib3 while adding significant new capabilities for modern web applications.

urllib4 includes all the critical features from urllib3:

- Thread safety
- Connection pooling
- Client-side SSL/TLS verification
- File uploads with multipart encoding
- Helpers for retrying requests and dealing with HTTP redirects
- Support for gzip, deflate, brotli, and zstd encoding
- Proxy support for HTTP and SOCKS

Plus these powerful new features:

- **Enhanced HTTP/2 Support** with server push and adaptive flow control
- **WebSocket Support** with RFC 6455 compliance
- **Improved Security Features** including Certificate Transparency and SPKI pinning
- **Groundwork for HTTP/3 (QUIC)** support

urllib4 is powerful and easy to use:

```python3
>>> import urllib4
>>> resp = urllib4.request("GET", "http://httpbin.org/robots.txt")
>>> resp.status
200
>>> resp.data
b"User-agent: *\nDisallow: /deny\n"
```

## Installing

urllib4 can be installed with [pip](https://pip.pypa.io):

```bash
$ python -m pip install urllib4-enhanced
```

Alternatively, you can grab the latest source code from GitHub:

```bash
$ git clone https://github.com/zinzied/urllib4.git
$ cd urllib4
$ pip install .
```


## Documentation

Documentation for urllib4 is available in the code and examples below. Full documentation will be available soon.

## Enhanced Features

### HTTP/2 Support

```python
import urllib4
from urllib4.http2 import inject_into_urllib4, ConnectionProfile

# Enable HTTP/2 support
inject_into_urllib4()

# Create a pool manager with a specific connection profile
http = urllib4.PoolManager(http2_profile=ConnectionProfile.HIGH_PERFORMANCE)

# Make a request (automatically uses HTTP/2 if the server supports it)
response = http.request("GET", "https://nghttp2.org")
print(f"HTTP version: {response.version_string}")
```

### WebSocket Support

```python
from urllib4.websocket import connect

# Connect to a WebSocket server
ws = connect("wss://echo.websocket.org")

# Send a message
ws.send("Hello, WebSocket!")

# Receive a message
message = ws.receive()
print(f"Received: {message.text}")

# Close the connection
ws.close()
```

### Enhanced Security Features

```python
import urllib4
from urllib4.util.cert_verification import SPKIPinningVerifier, CertificateTransparencyPolicy
from urllib4.util.hsts import HSTSCache, HSTSHandler

# Create a pool manager with SPKI pinning
pins = {
    "example.com": {"pin-sha256:YLh1dUR9y6Kja30RrAn7JKnbQG/uEtLMkBgFF2Fuihg="}
}
http = urllib4.PoolManager(
    spki_pins=pins,
    cert_transparency_policy=CertificateTransparencyPolicy.BEST_EFFORT
)

# Create an HSTS handler
hsts_cache = HSTSCache()
hsts_handler = HSTSHandler(hsts_cache)

# Secure a URL if needed
url = "http://example.com/api"
secured_url = hsts_handler.secure_url(url)  # Returns https://example.com/api if in HSTS cache
```

## Community

Join the urllib4 community for asking questions and collaborating with other contributors. We welcome feedback and contributions!


## Contributing

urllib4 happily accepts contributions. Please feel free to submit a Pull Request or open an issue on GitHub.

## Migration from urllib3

urllib4 is designed to be a drop-in replacement for urllib3 in most cases:

```python
# Before
import urllib3
http = urllib3.PoolManager()

# After
import urllib4
http = urllib4.PoolManager()
```

Additional features are available through new modules and parameters.

## Security Disclosures

To report a security vulnerability, please use responsible disclosure practices and contact the maintainers directly.

## Acknowledgements

urllib4 builds on the excellent work of the urllib3 project and its contributors. We extend our gratitude to the original authors and maintainers of urllib3 for their foundational work.
