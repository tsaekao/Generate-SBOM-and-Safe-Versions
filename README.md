# Generate-SBOM-and-Safe-Versions
A Python script to grab a Veracode application profile's Upload &amp; Scan SCA results, create an SBOM, and return a list of all safe versions for each library.

## 🛠️ Prerequisites

- Python 3.7+
- Veracode API Credentials

---

## 🔐 Veracode API Credentials

The script uses the Python HMAC Signing Library. If you're running it locally, you can create a credentials file in ~/.veracode/credentials:

```bash
[default]
veracode_api_key_id = <YOUR_API_KEY_ID>
veracode_api_key_secret = <YOUR_API_KEY_SECRET>
```

OR make sure you have your API credentials set up in environment variables:

```bash
VERACODE_API_KEY_ID=your_api_key_id
VERACODE_API_KEY_SECRET=your_api_key_secret
```

---

## 📦 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-org/veracode-sbom-safe-versions.git
cd veracode-sbom-safe-versions
```

2. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

> 📄 `requirements.txt` contains:
> ```txt
> requests
> veracode-api-signing
> ```

---

## 🚀 Usage

Run the script by passing in your Veracode application profile name:

```bash
python3 get_safe_versions.py "My Application Name"
```

---

## 📁 Output

The script will:

1. Print the safe versions summary to the console
2. Save the generated SBOM to:
   ```
   sbom_<AppName>_<Timestamp>.json
   ```
3. Save the safe version list to:
   ```
   safe_versions_<AppName>_<Timestamp>.json
   ```

Example output:
```
system.data.sqlclient (nuget:system.data.sqlclient::4.8.3:)
  Safe versions: 4.9.0, 4.8.6
```
