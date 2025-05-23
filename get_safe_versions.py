#!/usr/bin/env python3

import requests
import json
import sys
import re
from urllib.parse import quote
from datetime import datetime
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC


def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)


def get_app_guid(app_name):
    url = f"https://api.veracode.com/appsec/v1/applications?name={quote(app_name)}"
    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    response.raise_for_status()
    apps = response.json().get("_embedded", {}).get("applications", [])
    if not apps:
        raise ValueError(f"Application with name '{app_name}' not found.")
    return apps[0]["guid"]


def get_sbom(app_guid):
    url = f"https://api.veracode.com/srcclr/sbom/v1/targets/{app_guid}/cyclonedx?type=application"
    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    response.raise_for_status()
    return response.json()


def get_safe_versions(component_ref):
    url = f"https://api.veracode.com/srcclr/v3/component-activity/{quote(component_ref, safe='')}"
    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    if response.status_code == 200:
        data = response.json()
        return data.get("safe_versions", [])
    return []


def main(app_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = sanitize_filename(app_name)
    sbom_filename = f"sbom_{safe_name}_{timestamp}.json"
    safe_versions_filename = f"safe_versions_{safe_name}_{timestamp}.json"

    print(f"Getting application GUID for '{app_name}'...")
    app_guid = get_app_guid(app_name)

    print(f"Generating SBOM for app GUID {app_guid}...")
    sbom = get_sbom(app_guid)

    print(f"Saving SBOM to '{sbom_filename}'...")
    with open(sbom_filename, "w") as sbom_file:
        json.dump(sbom, sbom_file, indent=2)

    print("Processing components...")
    components = sbom.get("components", [])
    results = []

    for comp in components:
        ref = comp.get("bom-ref", "")
        name = comp.get("name", "")
        print(f"Fetching safe versions for {ref}...")
        safe_versions = get_safe_versions(ref)
        results.append({
            "component": name,
            "ref": ref,
            "safe_versions": safe_versions
        })

    print("\n=== Safe Versions Summary ===")
    for result in results:
        print(f"{result['component']} ({result['ref']}):")
        print("  Safe versions:", ", ".join(result["safe_versions"]) or "None")
        print()

    print(f"Saving safe version summary to '{safe_versions_filename}'...")
    with open(safe_versions_filename, "w") as out_file:
        json.dump(results, out_file, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 get_safe_versions.py <AppProfileName>")
        sys.exit(1)
    app_name = sys.argv[1]
    main(app_name)
#!/usr/bin/env python3

import requests
import json
import sys
import re
from urllib.parse import quote
from datetime import datetime
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC


def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)


def get_app_guid(app_name):
    url = f"https://api.veracode.com/appsec/v1/applications?name={quote(app_name)}"
    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    response.raise_for_status()
    apps = response.json().get("_embedded", {}).get("applications", [])
    if not apps:
        raise ValueError(f"Application with name '{app_name}' not found.")
    return apps[0]["guid"]


def get_sbom(app_guid):
    url = f"https://api.veracode.com/srcclr/sbom/v1/targets/{app_guid}/cyclonedx?type=application"
    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    response.raise_for_status()
    return response.json()


def get_safe_versions(component_ref):
    url = f"https://api.veracode.com/srcclr/v3/component-activity/{quote(component_ref, safe='')}"
    response = requests.get(url, auth=RequestsAuthPluginVeracodeHMAC())
    if response.status_code == 200:
        data = response.json()
        return data.get("safe_versions", [])
    return []


def main(app_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = sanitize_filename(app_name)
    sbom_filename = f"sbom_{safe_name}_{timestamp}.json"
    safe_versions_filename = f"safe_versions_{safe_name}_{timestamp}.json"

    print(f"Getting application GUID for '{app_name}'...")
    app_guid = get_app_guid(app_name)

    print(f"Generating SBOM for app GUID {app_guid}...")
    sbom = get_sbom(app_guid)

    print(f"Saving SBOM to '{sbom_filename}'...")
    with open(sbom_filename, "w") as sbom_file:
        json.dump(sbom, sbom_file, indent=2)

    print("Processing components...")
    components = sbom.get("components", [])
    results = []

    for comp in components:
        ref = comp.get("bom-ref", "")
        name = comp.get("name", "")
        print(f"Fetching safe versions for {ref}...")
        safe_versions = get_safe_versions(ref)
        results.append({
            "component": name,
            "ref": ref,
            "safe_versions": safe_versions
        })

    print("\n=== Safe Versions Summary ===")
    for result in results:
        print(f"{result['component']} ({result['ref']}):")
        print("  Safe versions:", ", ".join(result["safe_versions"]) or "None")
        print()

    print(f"Saving safe version summary to '{safe_versions_filename}'...")
    with open(safe_versions_filename, "w") as out_file:
        json.dump(results, out_file, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 get_safe_versions.py <AppProfileName>")
        sys.exit(1)
    app_name = sys.argv[1]
    main(app_name)
