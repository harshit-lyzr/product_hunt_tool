import os

from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv

# Initialize the FastAPI app
app = FastAPI()

# Define your API token
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Set the headers, including authorization with your token
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json"
}

# Endpoint to fetch trending products from Product Hunt
url = "https://api.producthunt.com/v2/api/graphql"

# GraphQL query to get trending products
query = """
{
  posts(order: RANKING, first: 10) {
    edges {
      node {
        name
        description
        votesCount
        website
        tagline
      }
    }
  }
}
"""


@app.get("/trending-products")
def get_trending_products():
    # Send the request to Product Hunt API
    response = requests.post(url, json={'query': query}, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        products = []

        # Extract and format the products data
        for product in data['data']['posts']['edges']:
            product_data = product['node']
            products.append({
                "name": product_data['name'],
                "description": product_data['description'],
                "votes": product_data['votesCount'],
                "website": product_data['website'],
                "tagline": product_data['tagline']
            })

        return {"products": products}
    else:
        # If the request failed, raise an HTTPException with the status code
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve data")

