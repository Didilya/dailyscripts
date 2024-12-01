# need access to https://learn.microsoft.com/ru-ru/linkedin/talent/easy-apply
import requests

# 1. Authentication: Get an access token
def get_access_token(client_id, client_secret, redirect_uri, auth_code):
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Error getting access token: {response.json()}")

# 2. Fetch job postings
def fetch_jobs(access_token, keyword, location):
    headers = {'Authorization': f'Bearer {access_token}'}
    search_url = "https://api.linkedin.com/v2/jobSearch"
    params = {
        'keywords': keyword,
        'location': location,
        'count': 10  # Adjust based on your needs
    }
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching jobs: {response.json()}")

# 3. Automate applications (if available via API)
def apply_to_job(access_token, job_id, profile_id):
    headers = {'Authorization': f'Bearer {access_token}'}
    apply_url = f"https://api.linkedin.com/v2/jobApplications"
    payload = {
        'job': f'urn:li:job:{job_id}',
        'profile': f'urn:li:person:{profile_id}'
    }
    response = requests.post(apply_url, headers=headers, json=payload)
    if response.status_code == 201:
        print(f"Successfully applied for job ID {job_id}")
    else:
        raise Exception(f"Error applying to job: {response.json()}")

# 4. Main workflow
if __name__ == "__main__":
    CLIENT_ID = "your_client_id"
    CLIENT_SECRET = "your_client_secret"
    REDIRECT_URI = "your_redirect_uri"
    AUTH_CODE = "your_auth_code"

    try:
        # Get OAuth access token
        token = get_access_token(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_CODE)
        print("Access Token Obtained:", token)

        # Fetch jobs based on keyword and location
        jobs = fetch_jobs(token, "Python Developer", "Remote")
        for job in jobs.get('elements', []):
            print(f"Job Title: {job['title']}, Job ID: {job['id']}")
            # Apply for job if applicable (requires LinkedIn API access to applications)
            # apply_to_job(token, job['id'], "your_profile_id")
    except Exception as e:
        print("Error:", e)
