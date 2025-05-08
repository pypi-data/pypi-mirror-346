# SimpleRDAP

`SimpleRDAP` is a simple, lightweight Python library for performing RDAP (Registration Data Access Protocol) lookups. It can use the standard IANA bootstrap data or allow users to specify custom local or remote bootstrap files.

The library is designed to be easy to use, with minimal dependencies (only Python's built-in libraries), and provides clear error handling, directly re-raising `urllib.error.HTTPError` for HTTP-related issues.

## Features

*   Performs RDAP lookups for domains, IPv4/IPv6 addresses, and ASNs.
*   Uses IANA RDAP bootstrap services by default.
*   Supports custom bootstrap files (local paths or URLs) for DNS, IPv4, IPv6, and ASN lookups.
*   Automatically caches downloaded bootstrap files from URLs to reduce redundant requests (default cache in `~/.cache/simplerdap/`, expires after 24 hours).
*   If a custom local bootstrap file is invalid or not found, it attempts to fall back to the corresponding IANA bootstrap URL.
*   Returns results as a Python dictionary (`dict`) or a formatted JSON string.
*   Directly re-raises `urllib.error.HTTPError` for HTTP errors, allowing standard error handling.
*   Custom exceptions `SimpleRDAPError` and `BootstrapError` for other library-specific issues.
*   Clean, comment-free codebase for easy reading and modification.

## Installation

```bash
python -m pip install /path/to/SimpleRDAP
# Or after building a wheel:
# python -m pip install simplerdap-0.1.0-py3-none-any.whl
```

## Usage Example

```python
import json
import urllib.error
from simplerdap import lookup, SimpleRDAPError, BootstrapError
import logging

# Optional: Configure logging to see library activity
logging.basicConfig(level=logging.INFO)
# To see detailed bootstrap loading/caching messages:
# logging.getLogger("simplerdap.core").setLevel(logging.INFO)


# --- Basic Lookups (using default IANA bootstrap) ---
print("--- Basic Lookups ---")
try:
    # Domain lookup
    domain_info = lookup("example.com")
    print(f"Domain 'example.com' Handle: {domain_info.get('handle')}")

    # IPv4 lookup (output as string)
    ipv4_info_str = lookup("1.1.1.1", output_format="string")
    print(f"\nIPv4 '1.1.1.1' Info (first 100 chars):\n{ipv4_info_str[:100]}...")

    # ASN lookup
    asn_info = lookup("AS15169")
    print(f"\nASN 'AS15169' Name: {asn_info.get('name')}")

except urllib.error.HTTPError as e:
    print(f"\nHTTP Error: {e.code} - {e.reason}")
    # You can access e.headers, e.fp (response body file-like object) if needed
except BootstrapError as e:
    print(f"\nBootstrap Error: {e}")
except SimpleRDAPError as e:
    print(f"\nSimpleRDAP Error: {e}")
except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")


# --- Lookup with Custom Bootstrap Files/URLs ---
print("\n\n--- Lookup with Custom Bootstrap ---")

# Example: Using a custom local file for DNS and a custom URL for IPv4,
# falling back to IANA for IPv6 and ASN.

# Create dummy bootstrap files for demonstration
# In a real scenario, these would be valid RDAP bootstrap JSON files.
dummy_dns_bootstrap = {
    "description": "Dummy DNS Bootstrap File",
    "publication": "2023-01-01T00:00:00Z",
    "version": "1.0",
    "services": [
        [
            ["com", "net"],
            ["https://custom.rdap.example.com/dns/"]
        ]
    ]
}
try:
    with open("/tmp/custom_dns.json", "w") as f:
        json.dump(dummy_dns_bootstrap, f)
except IOError:
    print("Could not write dummy custom_dns.json, custom DNS test might fail partially.")

custom_paths = {
    "dns": "/tmp/custom_dns.json",  # Path to a local file
    "ipv4": "https://data.iana.org/rdap/ipv4.json" # Can also be a URL (here, same as IANA for demo)
    # 'ipv6' and 'asn' will use IANA defaults as they are not specified here
}

try:
    # Domain lookup using custom DNS bootstrap
    # This will likely fail to find 'example.org' if not in dummy_dns_bootstrap
    # or if custom.rdap.example.com is not real.
    print("\nLooking up 'example.com' with custom DNS bootstrap...")
    custom_domain_info = lookup("example.com", custom_bootstrap_paths=custom_paths)
    print(f"Custom Domain 'example.com' RDAP URL (from custom bootstrap): {custom_domain_info.get('links', [{}])[0].get('href')}")

    print("\nLooking up '192.0.2.1' with custom IPv4 bootstrap (IANA URL in this case)...")
    custom_ipv4_info = lookup("192.0.2.1", custom_bootstrap_paths=custom_paths)
    print(f"Custom IPv4 '192.0.2.1' Name: {custom_ipv4_info.get('name')}")

except urllib.error.HTTPError as e:
    print(f"HTTP Error during custom lookup: {e.code} - {e.reason}")
except BootstrapError as e:
    print(f"Bootstrap Error during custom lookup: {e}")
except SimpleRDAPError as e:
    print(f"SimpleRDAP Error during custom lookup: {e}")
except Exception as e:
    print(f"An unexpected error occurred during custom lookup: {e}")

```

## Error Handling

*   **`urllib.error.HTTPError`**: Raised for any HTTP errors encountered when fetching RDAP data or bootstrap files from URLs (e.g., 404 Not Found, 500 Server Error). You can catch this directly and inspect `e.code`, `e.reason`, etc.
*   **`simplerdap.BootstrapError`**: Raised for issues related to loading, parsing, or using bootstrap files (e.g., file not found, invalid format, RDAP server not found for a query).
*   **`simplerdap.SimpleRDAPError`**: Base error for other library-specific issues, such as inability to determine query type or general fetching/parsing failures not covered by `HTTPError`.

## How Custom Bootstrap and Fallback Works

When you provide `custom_bootstrap_paths` as a dictionary (e.g., `{"dns": "/path/to/dns.json", "ipv4": "url/for/ipv4.json"}`):

1.  **Specified Custom File/URL**: For each type (`dns`, `ipv4`, `ipv6`, `asn`), if a path/URL is provided in `custom_bootstrap_paths`, the library will attempt to use it.
    *   **Local Files**: If it's a local path, the library reads it directly. If the file is not found or is invalid (e.g., not JSON, missing "services" key), a warning is logged, and the library **falls back to the default IANA URL** for that specific type and attempts to fetch and cache it.
    *   **URLs**: If it's a URL, the library fetches it. The content is cached locally (default: `~/.cache/simplerdap/TYPE_bootstrap.json`) for 24 hours. If fetching fails (e.g., HTTP error) or the fetched data is invalid, a `BootstrapError` is raised (it does not automatically fall back to IANA if a custom *URL* fails, as the intent was to use that specific custom URL).
2.  **IANA Default**: If a type is *not* specified in `custom_bootstrap_paths`, the library defaults to the corresponding IANA bootstrap URL (e.g., `https://data.iana.org/rdap/dns.json`). This is also fetched and cached.

This provides flexibility to use your own bootstrap sources while having a reliable fallback for missing or invalid local custom files.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

