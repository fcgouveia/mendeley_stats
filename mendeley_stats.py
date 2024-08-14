import requests
import csv
import webbrowser

# Constants
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = ''  # Should match the one registered in Mendeley API settings
AUTH_URL = 'https://api.mendeley.com/oauth/authorize'
TOKEN_URL = 'https://api.mendeley.com/oauth/token'
DOI_FILE = 'DOIs.csv'  # The file containing the list of DOIs

# Base URL for Mendeley API
BASE_URL = 'https://api.mendeley.com'

def get_access_token():
    """Step through OAuth2 flow to obtain an access token."""
    
    # Step 1: Redirect user to Mendeley for authorization
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'all',
    }
    
    auth_url = requests.Request('GET', AUTH_URL, params=params).prepare().url
    print(f"Please go to the following URL to authorize access: {auth_url}")
    
    # Automatically open the browser for the user
    webbrowser.open(auth_url)
    
    # Step 2: Get the authorization code from the redirect URI
    auth_code = input('Enter the authorization code you received: ')
    
    # Step 3: Exchange authorization code for an access token
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    
    response = requests.post(TOKEN_URL, data=data)
    response_data = response.json()
    
    if response.status_code == 200:
        access_token = response_data.get('access_token')
        print("Access token retrieved successfully.")
        return access_token
    else:
        print(f"Failed to retrieve access token: {response.status_code} - {response.text}")
        return None

def get_document_id(doi, access_token):
    """Get the Mendeley document ID using the DOI."""
    
    url = f'{BASE_URL}/catalog'
    params = {'doi': doi}
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data and isinstance(data, list):
            return data[0].get('id')
    else:
        print(f"Failed to retrieve document ID for DOI {doi}: {response.status_code} - {response.text}")
    
    return None

def get_document_readers(document_id, access_token):
    """Get the number of readers for a document."""
    
    url = f'{BASE_URL}/catalog/{document_id}?view=stats'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.mendeley-document.1+json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant information if available
        readers_count = data.get('reader_count', 'N/A')
        
        return {
            'readers_count': readers_count,
        }
    else:
        print(f"Failed to retrieve data for document ID {document_id}: {response.status_code} - {response.text}")
        return None
        
def process_dois(file_path, access_token):
    """Process a list of DOIs from a file and print all content obtained."""
    
    results = []
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            doi = row[0].strip()
            
            if doi:
                print(f"Processing DOI: {doi}")
                
                # Get Mendeley document ID from DOI
                document_id = get_document_id(doi, access_token)
                
                if document_id:
                    # Get document stats
                    document_stats = get_document_readers(document_id, access_token)
                    
                    if document_stats:
                        results.append({
                            'DOI': doi,
                            'Document ID': document_id,
                            'Number of Readers': document_stats['readers_count']
                        })
                else:
                    results.append({
                        'DOI': doi,
                        'Error': 'Could not find document ID'
                    })
                    
    # Print all results
    print("\nAll Results:")
    for result in results:
        print(result)

def main():
    # Obtain the access token
    access_token = get_access_token()
    
    if access_token:
        # Process DOIs from the file
        process_dois(DOI_FILE, access_token)

if __name__ == '__main__':
    main()
