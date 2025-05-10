import requests
import json
from typing import Dict, List, Optional, Union, Any
import time
from enum import Enum
from colorama import init, Fore, Style
import os
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Initialize colorama
init()

class OpenSeaNFTFetcher:
    def __init__(self):
        self.base_url = "https://api.opensea.io/api/v2"
        self.headers = {
            "accept": "application/json",
            "x-api-key": os.getenv('OPENSEA_API_KEY')
        }

    def get_account_info(self, address_or_username: str) -> Dict:
        """Get account information from OpenSea"""
        endpoint = f"/accounts/{address_or_username}"
        url = f"{self.base_url}{endpoint}"
        
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch account info: {response.status_code}")

    def get_collection_by_slug(self, collection_slug: str) -> Dict:
        """Get collection information by slug"""
        # Get collection info
        endpoint = f"/collections/{collection_slug}"
        url = f"{self.base_url}{endpoint}"
        
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            collection_data = response.json()
            
            # Get collection stats with the correct endpoint
            stats_endpoint = f"/collections/{collection_slug}/stats"
            stats_url = f"{self.base_url}{stats_endpoint}"
            stats_response = requests.get(stats_url, headers=self.headers)
            
            if stats_response.status_code == 200:
                stats_data = stats_response.json()
                # Update stats with the new format
                collection_data['stats'] = {
                    'total_volume': stats_data.get('total', {}).get('volume', 0),
                    'total_sales': stats_data.get('total', {}).get('sales', 0),
                    'average_price': stats_data.get('total', {}).get('average_price', 0),
                    'num_owners': stats_data.get('total', {}).get('num_owners', 0),
                    'market_cap': stats_data.get('total', {}).get('market_cap', 0),
                    'floor_price': stats_data.get('total', {}).get('floor_price', 0),
                    'floor_price_symbol': stats_data.get('total', {}).get('floor_price_symbol', 'ETH'),
                    # Add 24h stats
                    '24h_volume': stats_data.get('intervals', [{}])[0].get('volume', 0),
                    '24h_volume_change': stats_data.get('intervals', [{}])[0].get('volume_change', 0),
                    '24h_sales': stats_data.get('intervals', [{}])[0].get('sales', 0),
                    '24h_average_price': stats_data.get('intervals', [{}])[0].get('average_price', 0)
                }
            
            return collection_data
        else:
            raise Exception(f"Failed to fetch collection info: {response.status_code}")

    def get_collection_nfts(self, collection_slug: str, limit: int = 50) -> List[Dict]:
        """Get listed NFTs in a collection"""
        endpoint = f"/listings/collection/{collection_slug}/all"
        next_cursor = None
        listed_nfts = []
        
        try:
            while True:
                params = {
                    "limit": limit
                }
                
                if next_cursor:
                    params["next"] = next_cursor
                    
                url = f"{self.base_url}{endpoint}"
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code != 200:
                    print(f"{Fore.RED}Error fetching NFTs: {response.status_code}{Style.RESET_ALL}")
                    break
                    
                data = response.json()
                listings = data.get("listings", [])
                
                # Process each listing and extract NFT information
                for listing in listings:
                    try:
                        # Get price in ETH
                        price_wei = listing.get('price', {}).get('current', {}).get('value', '0')
                        price_eth = float(price_wei) / (10 ** 18)  # Convert from wei to ETH
                        
                        # Get NFT details from protocol data
                        protocol_data = listing.get('protocol_data', {}).get('parameters', {})
                        offer = protocol_data.get('offer', [{}])[0]
                        
                        nft_data = {
                            'identifier': offer.get('identifierOrCriteria', ''),
                            'token_address': offer.get('token', ''),
                            'price': {
                                'current': {
                                    'value': price_eth,
                                    'currency': listing.get('price', {}).get('current', {}).get('currency', 'ETH')
                                }
                            },
                            'order_hash': listing.get('order_hash', ''),
                            'chain': listing.get('chain', 'ethereum'),
                            'start_time': protocol_data.get('startTime', ''),
                            'end_time': protocol_data.get('endTime', ''),
                            'seller': protocol_data.get('offerer', '')
                        }
                        
                        listed_nfts.append(nft_data)
                    except Exception as e:
                        print(f"{Fore.RED}Error processing listing: {str(e)}{Style.RESET_ALL}")
                        continue
                
                # Check if we have more pages
                next_cursor = data.get("next")
                if not next_cursor or not listings:  # Stop if no more listings or empty response
                    break
                
            return listed_nfts
        except Exception as e:
            print(f"{Fore.RED}Error in get_collection_nfts: {str(e)}{Style.RESET_ALL}")
            return []

def format_price(price: Union[float, int, str, None], currency: str = "ETH") -> str:
    """Format price with appropriate decimals"""
    try:
        if price is None:
            return f"0.0000 {currency}"
        price_float = float(price)
        return f"{price_float:.4f} {currency}"
    except (ValueError, TypeError):
        return f"0.0000 {currency}"

def format_attributes(attributes: List[Dict]) -> str:
    """Format NFT attributes into a string"""
    if not attributes:
        return "No attributes"
    
    attr_strings = []
    for attr in attributes:
        trait_type = attr.get('trait_type', '')
        value = attr.get('value', '')
        if trait_type and value:
            attr_strings.append(f"{trait_type}: {value}")
    
    return " | ".join(attr_strings) if attr_strings else "No attributes"

def main():
    try:
        # Get collection slug from user
        collection_slug = input("\nEnter collection slug (e.g., 'doodles-official'): ").strip()
        if not collection_slug:
            print(f"{Fore.RED}Collection slug is required{Style.RESET_ALL}")
            return
        
        fetcher = OpenSeaNFTFetcher()
        
        # Get collection info
        print(f"\n{Fore.YELLOW}Fetching collection information...{Style.RESET_ALL}")
        try:
            collection_info = fetcher.get_collection_by_slug(collection_slug)
            
            print(f"\n{Fore.CYAN}Collection Information:{Style.RESET_ALL}")
            print(f"Name: {collection_info.get('name', 'N/A')}")
            print(f"Description: {collection_info.get('description', 'N/A')}")
            print(f"Total Supply: {collection_info.get('total_supply', 'N/A')}")
            
            # Get floor price and other stats with the new format
            stats = collection_info.get('stats', {})
            
            print(f"\n{Fore.CYAN}Collection Statistics:{Style.RESET_ALL}")
            print(f"Floor Price: {format_price(stats.get('floor_price'))} {stats.get('floor_price_symbol', 'ETH')}")
            print(f"Total Volume: {format_price(stats.get('total_volume'))}")
            print(f"Total Sales: {stats.get('total_sales', 0)}")
            print(f"Number of Owners: {stats.get('num_owners', 0)}")
            print(f"Market Cap: {format_price(stats.get('market_cap'))}")
            print(f"Average Price: {format_price(stats.get('average_price'))}")
            
            print(f"\n{Fore.CYAN}24h Statistics:{Style.RESET_ALL}")
            print(f"Volume: {format_price(stats.get('24h_volume'))}")
            print(f"Volume Change: {stats.get('24h_volume_change', 0):.2f}%")
            print(f"Sales: {stats.get('24h_sales', 0)}")
            print(f"Average Price: {format_price(stats.get('24h_average_price'))}")
            
        except Exception as e:
            print(f"{Fore.RED}Error fetching collection info: {str(e)}{Style.RESET_ALL}")
            return
            
        # Get NFT listings
        print(f"\n{Fore.YELLOW}Fetching all listed NFTs...{Style.RESET_ALL}")
        nfts = fetcher.get_collection_nfts(collection_slug)
        
        if not nfts:
            print(f"{Fore.RED}No listed NFTs found{Style.RESET_ALL}")
            return
            
        # Display results
        print(f"\n{Fore.GREEN}Found {len(nfts)} listed NFTs{Style.RESET_ALL}")
        
        # Sort NFTs by price
        def get_nft_price(nft):
            return float(nft.get('price', {}).get('current', {}).get('value', 0))
        
        sorted_nfts = sorted(nfts, key=get_nft_price)
        
        # Display lowest 10 NFTs
        print(f"\n{Fore.YELLOW}Lowest 10 prices:{Style.RESET_ALL}")
        for nft in sorted_nfts[:10]:
            token_id = nft.get('identifier')
            price = get_nft_price(nft)
            seller = nft.get('seller', '')[:8] + '...'  # Show first 8 chars of seller address
            
            print(f"Token ID: {token_id} - Price: {format_price(price)} - Seller: {seller}")
            
        # Display highest 10 NFTs
        print(f"\n{Fore.YELLOW}Highest 10 prices:{Style.RESET_ALL}")
        for nft in sorted_nfts[-10:]:
            token_id = nft.get('identifier')
            price = get_nft_price(nft)
            seller = nft.get('seller', '')[:8] + '...'  # Show first 8 chars of seller address
            
            print(f"Token ID: {token_id} - Price: {format_price(price)} - Seller: {seller}")
            
        # Calculate average price
        prices = [get_nft_price(nft) for nft in nfts]
        valid_prices = [p for p in prices if p > 0]
        
        if valid_prices:
            avg_price = sum(valid_prices) / len(valid_prices)
            print(f"\n{Fore.YELLOW}Average price: {format_price(avg_price)}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}No valid prices found{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 