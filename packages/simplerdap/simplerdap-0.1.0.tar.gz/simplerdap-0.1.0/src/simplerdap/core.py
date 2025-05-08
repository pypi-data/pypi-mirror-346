import json
import urllib.request
import urllib.error
import urllib.parse
import ipaddress
import os
import logging
import time
from .exceptions import SimpleRDAPError, BootstrapError

IANA_BASE_URL = "https://data.iana.org/rdap/"
DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "simplerdap")
CACHE_EXPIRY_SECONDS = 24 * 60 * 60

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

def _fetch_url(url, timeout=10):
    try:
        req = urllib.request.Request(url, headers={'Accept': 'application/rdap+json'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        log.error(f"HTTPError fetching {url}: Status {e.code} - {e.reason}")
        raise
    except Exception as e:
        log.error(f"Generic error fetching {url}: {e}")
        raise SimpleRDAPError(f"Failed to fetch or parse {url}: {e}")

def _get_bootstrap_sources(custom_bootstrap_paths=None):
    resolved_sources = {}
    all_types = ['dns', 'ipv4', 'ipv6', 'asn']
    default_iana_sources = {
        "dns": IANA_BASE_URL + "dns.json",
        "ipv4": IANA_BASE_URL + "ipv4.json",
        "ipv6": IANA_BASE_URL + "ipv6.json",
        "asn": IANA_BASE_URL + "asn.json",
    }

    if custom_bootstrap_paths and not isinstance(custom_bootstrap_paths, dict):
        log.warning("custom_bootstrap_paths was provided but not as a dictionary. Using IANA defaults for all types.")
        custom_bootstrap_paths = None

    for type_key in all_types:
        if custom_bootstrap_paths and type_key in custom_bootstrap_paths:
            resolved_sources[type_key] = custom_bootstrap_paths[type_key]
            log.info(f"Using custom bootstrap source for {type_key}: {custom_bootstrap_paths[type_key]}")
        else:
            resolved_sources[type_key] = default_iana_sources[type_key]
            if custom_bootstrap_paths:
                 log.warning(f"Custom bootstrap source for {type_key} not provided. Using IANA default: {resolved_sources[type_key]}")
            else:
                 log.info(f"Using IANA default bootstrap source for {type_key}: {resolved_sources[type_key]}")
                 
    return resolved_sources

def _load_bootstrap_data(source_location, type_key, cache_dir=DEFAULT_CACHE_DIR):
    os.makedirs(cache_dir, exist_ok=True)
    
    # Generate a cache file name. If it's a URL, base it on the type_key for simplicity, 
    # assuming one primary URL (IANA or custom) per type for caching.
    # If it's a local file, we don't cache it, we read it directly.
    cache_file_name = f"{type_key}_bootstrap.json"
    cache_file_path = os.path.join(cache_dir, cache_file_name)

    if source_location.startswith("http://") or source_location.startswith("https://"):
        if os.path.exists(cache_file_path) and \
           (time.time() - os.path.getmtime(cache_file_path)) < CACHE_EXPIRY_SECONDS:
            log.info(f"Loading cached bootstrap data for {type_key} from: {cache_file_path}")
            try:
                with open(cache_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if "services" in data: # Basic validation
                    return data
                else:
                    log.warning(f"Cached bootstrap data in {cache_file_path} for {type_key} is invalid. Refetching.")
            except (json.JSONDecodeError, IOError) as e:
                log.warning(f"Failed to load cached bootstrap data from {cache_file_path} for {type_key}: {e}. Refetching.")
        
        log.info(f"Fetching bootstrap data for {type_key} from URL: {source_location}")
        try:
            data = _fetch_url(source_location)
            with open(cache_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f)
            if "services" not in data:
                 raise BootstrapError(f"Fetched bootstrap data from {source_location} for {type_key} is missing 'services' key.")
            return data
        except Exception as e:
            raise BootstrapError(f"Failed to fetch or cache bootstrap data for {type_key} from {source_location}: {e}")

    elif os.path.exists(source_location):
        log.info(f"Loading bootstrap data for {type_key} from local file: {source_location}")
        try:
            with open(source_location, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if "services" in data: # Basic validation
                return data
            else:
                log.warning(f"Custom bootstrap file {source_location} for {type_key} is invalid (missing 'services'). Attempting IANA fallback.")
                iana_fallback_url = IANA_BASE_URL + f"{type_key}.json"
                log.info(f"Fetching IANA fallback for {type_key} from {iana_fallback_url}")
                # Call _load_bootstrap_data for the IANA URL, it will handle fetching & caching
                return _load_bootstrap_data(iana_fallback_url, type_key, cache_dir) 
        except (json.JSONDecodeError, IOError) as e:
            log.warning(f"Failed to load custom bootstrap file {source_location} for {type_key}: {e}. Attempting IANA fallback.")
            iana_fallback_url = IANA_BASE_URL + f"{type_key}.json"
            log.info(f"Fetching IANA fallback for {type_key} from {iana_fallback_url}")
            return _load_bootstrap_data(iana_fallback_url, type_key, cache_dir)
    else:
        log.warning(f"Custom bootstrap file {source_location} for {type_key} not found. Attempting IANA fallback.")
        iana_fallback_url = IANA_BASE_URL + f"{type_key}.json"
        log.info(f"Fetching IANA fallback for {type_key} from {iana_fallback_url}")
        return _load_bootstrap_data(iana_fallback_url, type_key, cache_dir)

def _find_rdap_server_from_bootstrap(item_to_lookup, query_type, bootstrap_data):
    if not bootstrap_data or "services" not in bootstrap_data:
        raise BootstrapError("Invalid or empty bootstrap data provided for server lookup.")
    
    services = bootstrap_data["services"]
    
    for service_entry in services:
        if len(service_entry) < 2:
            continue
        
        keys = service_entry[0]
        rdap_urls = service_entry[1]
        
        if not rdap_urls: continue

        if query_type == "domain":
            tld = item_to_lookup.lower()
            if tld in keys:
                return rdap_urls[0]
        elif query_type == "asn":
            try:
                asn_val = int(item_to_lookup)
                for key_pattern in keys:
                    if '-' in key_pattern:
                        low, high = map(int, key_pattern.split('-'))
                        if low <= asn_val <= high:
                            return rdap_urls[0]
                    elif str(asn_val) == key_pattern:
                         return rdap_urls[0]
            except ValueError:
                continue
        elif query_type == "ipv4" or query_type == "ipv6":
            try:
                ip_addr_to_lookup = ipaddress.ip_address(item_to_lookup)
                for key_pattern in keys:
                    if ip_addr_to_lookup in ipaddress.ip_network(key_pattern, strict=False):
                        return rdap_urls[0]
            except ValueError:
                continue
    return None

def _determine_query_type(query):
    try:
        ip_addr = ipaddress.ip_address(query)
        return "ipv4" if ip_addr.version == 4 else "ipv6"
    except ValueError:
        pass
    
    if query.lower().startswith("as") and query[2:].isdigit():
        return "asn"
    
    # Check for TLD-like structure; simple check, might need refinement for complex cases
    parts = query.split('.')
    if len(parts) > 1 and parts[-1].isalpha(): 
        return "domain"
        
    return "unknown"

def lookup(query, custom_bootstrap_paths=None, output_format="json", timeout=10):
    log.info(f"Performing lookup for: '{query}'")
    original_query = query
    query_type = _determine_query_type(original_query)

    if query_type == "unknown":
        raise SimpleRDAPError(f"Could not determine query type for: '{original_query}'")

    bootstrap_sources = _get_bootstrap_sources(custom_bootstrap_paths)
    
    item_for_bootstrap_lookup = original_query
    bootstrap_type_key = query_type

    if query_type == "domain":
        bootstrap_type_key = "dns"
        item_for_bootstrap_lookup = original_query.split('.')[-1].lower() # Use TLD for DNS bootstrap
    elif query_type == "asn":
        item_for_bootstrap_lookup = original_query[2:] if original_query.lower().startswith("as") else original_query
        try:
            int(item_for_bootstrap_lookup) # Validate it's a number
        except ValueError:
            raise SimpleRDAPError(f"Invalid ASN format: {original_query}")
    
    source_location = bootstrap_sources[bootstrap_type_key]
    
    try:
        bootstrap_data = _load_bootstrap_data(source_location, bootstrap_type_key)
        rdap_server_base_url = _find_rdap_server_from_bootstrap(item_for_bootstrap_lookup, query_type, bootstrap_data)
    except Exception as e:
        # Catching generic Exception here because _load_bootstrap_data can raise various things
        # including recursive calls leading to BootstrapError or SimpleRDAPError from _fetch_url
        log.error(f"Error processing bootstrap data for {query_type} from {source_location}: {e}")
        raise BootstrapError(f"Failed to get RDAP server due to bootstrap error with {source_location}: {e}")

    if not rdap_server_base_url:
        raise BootstrapError(f"Could not find RDAP server for '{original_query}' (type: {query_type}, item: '{item_for_bootstrap_lookup}') using {source_location}")

    if not rdap_server_base_url.endswith('/'):
        rdap_server_base_url += '/'

    encoded_query_item = urllib.parse.quote(original_query)
    if query_type == "asn":
        # Use the numeric part for the RDAP path
        encoded_query_item = urllib.parse.quote(item_for_bootstrap_lookup) 

    rdap_url_path_segment = {
        "domain": "domain/",
        "ipv4": "ip/",
        "ipv6": "ip/",
        "asn": "autnum/"
    }
    rdap_url = f"{rdap_server_base_url}{rdap_url_path_segment[query_type]}{encoded_query_item}"

    log.info(f"Querying RDAP URL: {rdap_url}")
    result_data = _fetch_url(rdap_url, timeout=timeout)

    if output_format == "string":
        return json.dumps(result_data, indent=2, ensure_ascii=False)
    elif output_format == "json":
        return result_data
    else:
        raise ValueError("Invalid output_format. Choose 'json' or 'string'.")

