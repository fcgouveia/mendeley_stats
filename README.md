# mendeley_stats

A Script to Grap Mendeley Document Reader Counter via API based on a list of DOIs 

This Python script interacts with the Mendeley API to retrieve reader counts for academic documents based on their DOIs (Digital Object Identifiers).

## Features

- OAuth2 authentication with Mendeley API
- Retrieves document IDs from DOIs
- Fetches reader counts for documents
- Processes multiple DOIs from a CSV file
- Prints results for each DOI

## Prerequisites

- Python 3.x
- `requests` library
- Mendeley API credentials (Client ID and Client Secret)

## Setup

1. Clone this repository or download the script.
2. Install the required library:

```
pip install requests
```

3. Create a Mendeley API application to obtain your Client ID and Client Secret.
4. Update the following constants in the script:
- `CLIENT_ID`
- `CLIENT_SECRET`
- `REDIRECT_URI`

## Usage

1. Prepare a CSV file named `DOIs.csv` with a list of DOIs, one per line.
2. Run the script:

```
python mendeley_stats.py
```

3. The script will open a web browser for Mendeley authentication. Log in and authorize the application.
4. Copy the authorization code from the redirect URL and paste it into the console when prompted.
5. The script will process each DOI and print the results.

## Output

The script will print information for each DOI, including:
- DOI
- Mendeley Document ID
- Number of Readers

If a document ID cannot be found for a DOI, an error message will be displayed.

## Note

This script uses the Mendeley API, which may have rate limits or usage restrictions. Please review Mendeley's API documentation and terms of service before use.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions, issues, and feature requests are welcome.

## Author

Fábio Castro Gouveia

## Acknowledgments

- Mendeley for providing the API
- The `requests` library maintainers
- My Junior Programmers ChatGPT and Claude
