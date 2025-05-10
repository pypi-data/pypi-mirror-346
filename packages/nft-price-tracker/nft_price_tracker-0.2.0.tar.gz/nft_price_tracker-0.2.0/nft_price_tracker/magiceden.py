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

class Chain(Enum):
    SOLANA = "solana"
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    BASE = "base"
    ARBITRUM = "arbitrum"
    ABSTRACT = "abstract"

class MagicEdenNFTFetcher:
    def __init__(self, chain: Chain = Chain.ABSTRACT):
        self.chain = chain
        self.base_url = "https://api-mainnet.magiceden.dev"
        self.headers = {
            "accept": "*/*",
            "Authorization": f"Bearer {os.getenv('MAGICEDEN_API_KEY')}"
        }

    def get_collection_by_name_or_address(self, collection_identifier: str) -> Dict:
        """
        Get collection information by name or address and return the contract address
        Returns a tuple of (collection_info, contract_address)
        """
        endpoint = f"/v3/rtp/{self.chain.value}/collections/v7"
        params = {
            "id": collection_identifier,
            "includeMintStages": "false",
            "includeSecurityConfigs": "false",
            "normalizeRoyalties": "false",
            "useNonFlaggedFloorAsk": "false",
            "sortBy": "allTimeVolume",
            "limit": 1
        }
        
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            collection_info = response.json()
            collections = collection_info.get("collections", [])
            if not collections:
                raise Exception("No collection found")
            
            # Get the contract address from the collection info
            contract_address = collections[0].get("id")
            if not contract_address:
                raise Exception("Contract address not found in collection info")
                
            return collection_info, contract_address
        else:
            raise Exception(f"Failed to fetch collection info: {response.status_code}")

    def get_collection_nfts(self, collection_address: str, batch_size: int = 100) -> List[Dict]:
        """Get listed NFTs in a collection with their prices"""
        endpoint = f"/v3/rtp/{self.chain.value}/tokens/v6"
        continuation = None
        listed_nfts = []
        
        # First, get the total number of listed NFTs for the progress bar
        collection_info, _ = self.get_collection_by_name_or_address(collection_address)
        total_listed = int(collection_info.get("collections", [{}])[0].get("onSaleCount", 0))
        
        # Initialize progress bar with proper type conversion
        progress_bar = tqdm(
            total=total_listed,
            desc=f"{Fore.YELLOW}Fetching NFTs{Style.RESET_ALL}",
            bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} NFTs [{elapsed}<{remaining}, {rate_fmt}]",
            colour="yellow"
        )
        
        try:
            while True:
                params = {
                    "collection": collection_address,
                    "sortBy": "floorAskPrice",
                    "limit": batch_size,
                    "includeTopBid": "false",
                    "excludeEOA": "false",
                    "includeAttributes": "false",
                    "includeQuantity": "false",
                    "includeDynamicPricing": "false",
                    "includeLastSale": "false",
                    "includeRawData": "false"
                }
                
                if continuation:
                    params["continuation"] = continuation
                    
                url = f"{self.base_url}{endpoint}"
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code != 200:
                    print(f"\n{Fore.RED}Error fetching NFTs: {response.status_code}{Style.RESET_ALL}")
                    break
                    
                data = response.json()
                tokens = data.get("tokens", [])
                
                # Process each token and check for valid price
                for token in tokens:
                    market_data = token.get("market", {})
                    floor_ask = market_data.get("floorAsk", {})
                    
                    if not floor_ask:
                        return listed_nfts
                        
                    price_info = floor_ask.get("price", {})
                    if not price_info:
                        return listed_nfts
                        
                    amount = price_info.get("amount", {})
                    if not amount or amount.get("decimal", 0) == 0:
                        return listed_nfts
                    
                    # This NFT has a valid price, add it to our list
                    listed_nfts.append(token)
                    progress_bar.update(1)
                
                # Check if we have more pages
                continuation = data.get("continuation")
                if not continuation:
                    break
                
            return listed_nfts
        finally:
            # Ensure progress bar is closed even if an error occurs
            progress_bar.close()

    def get_price_currency(self) -> str:
        """Get the price currency symbol based on the selected chain"""
        currency_map = {
            Chain.SOLANA: "SOL",
            Chain.ETHEREUM: "ETH",
            Chain.POLYGON: "MATIC",
            Chain.BASE: "ETH",
            Chain.ARBITRUM: "ETH",
            Chain.ABSTRACT: "ETH"
        }
        return currency_map.get(self.chain, "UNKNOWN")

    def get_nft_metadata(self, token_uri: str) -> Dict:
        """Fetch NFT metadata from tokenURI"""
        try:
            # Handle IPFS URLs
            if token_uri.startswith('ipfs://'):
                token_uri = f'https://ipfs.io/ipfs/{token_uri[7:]}'
            
            response = requests.get(token_uri)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"{Fore.RED}Failed to fetch metadata: {response.status_code}{Style.RESET_ALL}")
                return {}
        except Exception as e:
            print(f"{Fore.RED}Error fetching metadata: {str(e)}{Style.RESET_ALL}")
            return {}

def select_chain() -> Chain:
    """Select blockchain network"""
    print("\nAvailable chains:")
    chains = [chain.value for chain in Chain]
    for i, chain in enumerate(chains, 1):
        print(f"{i}. {chain}")
        
    while True:
        choice = input(f"\nSelect chain (1-{len(chains)}, press Enter for Abstract): ").strip()
        
        # If no input, use Abstract as default
        if not choice:
            print("Using default chain: Abstract")
            return Chain.ABSTRACT
            
        try:
            index = int(choice) - 1
            if 0 <= index < len(chains):
                return Chain(chains[index])
        except ValueError:
            pass
            
        print(f"Please enter a number between 1 and {len(chains)}")

def get_nested_value(data: Dict, *keys: str, default: Any = 0) -> Any:
    """Safely get nested value from dictionary"""
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
    return current

def format_price(price: Union[float, int, str, None], currency: str) -> str:
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
    # Default collection address for Abstract chain
    DEFAULT_COLLECTION = "0x5fedb9a131f798e986109dd89942c17c25c81de3"
    
    try:
        # Get chain selection from user or use default
        chain = select_chain()
        
        # Get collection address or name from user or use default
        collection_identifier = input(f"\nEnter collection address or name (press Enter for {DEFAULT_COLLECTION}): ").strip()
        if not collection_identifier:
            collection_identifier = DEFAULT_COLLECTION
            print(f"{Fore.CYAN}Using default collection: {DEFAULT_COLLECTION}{Style.RESET_ALL}")
        
        fetcher = MagicEdenNFTFetcher(chain)
        
        # Get collection info and resolve contract address
        print(f"\n{Fore.YELLOW}Fetching collection information...{Style.RESET_ALL}")
        try:
            collection_info, contract_address = fetcher.get_collection_by_name_or_address(collection_identifier)
            print(f"{Fore.CYAN}Resolved contract address: {contract_address}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error fetching collection info: {str(e)}{Style.RESET_ALL}")
            return
        
        # Debug: Print raw response
        #print(f"\n{Fore.BLUE}API Response:{Style.RESET_ALL}")
        #print(json.dumps(collection_info, indent=2))
        
        currency = fetcher.get_price_currency()
        
        # Get collection data
        collections = collection_info.get("collections", [])
        if not collections:
            print(f"{Fore.RED}No collection data found. Available keys in response: {list(collection_info.keys())}{Style.RESET_ALL}")
            return
            
        collection = collections[0]  # Get the first collection
        
        # Display collection info
        print(f"\n{Fore.GREEN}Collection Statistics:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Name:{Style.RESET_ALL} {collection.get('name', 'N/A')}")
        
        # Get prices from the structure
        floor_price = 0
        floor_ask = collection.get('floorAsk', {})
        if floor_ask:
            price_info = floor_ask.get('price', {})
            if price_info:
                amount = price_info.get('amount', {})
                if amount:
                    floor_price = amount.get('decimal', 0)

        # Get volume from the structure
        volume_24h = collection.get('volume', {}).get('1day', 0)
        
        print(f"{Fore.CYAN}Floor Price:{Style.RESET_ALL} {format_price(floor_price, currency)}")
        print(f"{Fore.CYAN}Total Supply:{Style.RESET_ALL} {collection.get('tokenCount', 'N/A')}")
        print(f"{Fore.CYAN}Listed Count:{Style.RESET_ALL} {collection.get('onSaleCount', 'N/A')}")
        print(f"{Fore.CYAN}24h Volume:{Style.RESET_ALL} {format_price(volume_24h, currency)}")
            
        # Get NFT listings using the resolved contract address
        print(f"\n{Fore.YELLOW}Fetching NFT listings...{Style.RESET_ALL}")
        nfts = fetcher.get_collection_nfts(contract_address)
        
        if not nfts:
            print(f"{Fore.RED}No listed NFTs found{Style.RESET_ALL}")
            return
            
        # Display results
        print(f"\n{Fore.GREEN}Found {len(nfts)} listed NFTs{Style.RESET_ALL}")
        
        # Sort NFTs by price
        def get_nft_price(nft):
            market_data = nft.get("market", {})
            floor_ask = market_data.get("floorAsk", {})
            price_info = floor_ask.get("price", {})
            amount = price_info.get("amount", {})
            return amount.get("decimal", 0)
        
        sorted_nfts = sorted(nfts, key=get_nft_price)
        
        # Display lowest 10 and highest 10 NFTs
        print(f"\n{Fore.YELLOW}Lowest 10 prices:{Style.RESET_ALL}")
        for nft in sorted_nfts[:10]:
            token_data = nft.get("token", {})
            token_id = token_data.get("tokenId")
            price = get_nft_price(nft)
            
            # Get metadata
            metadata = token_data.get("metadata", {})
            token_uri = metadata.get("tokenURI")
            if token_uri:
                nft_metadata = fetcher.get_nft_metadata(token_uri)
                attributes = nft_metadata.get("attributes", [])
                attr_str = format_attributes(attributes)
            else:
                attr_str = "No metadata"
            
            print(f"{Fore.CYAN}Token ID:{Style.RESET_ALL} {token_id} - "
                  f"{Fore.GREEN}Price:{Style.RESET_ALL} {format_price(price, currency)} - "
                  f"{Fore.MAGENTA}Attributes:{Style.RESET_ALL} {attr_str}")
            
        print(f"\n{Fore.YELLOW}Highest 10 prices:{Style.RESET_ALL}")
        for nft in sorted_nfts[-10:]:
            token_data = nft.get("token", {})
            token_id = token_data.get("tokenId")
            price = get_nft_price(nft)
            
            # Get metadata
            metadata = token_data.get("metadata", {})
            token_uri = metadata.get("tokenURI")
            if token_uri:
                nft_metadata = fetcher.get_nft_metadata(token_uri)
                attributes = nft_metadata.get("attributes", [])
                attr_str = format_attributes(attributes)
            else:
                attr_str = "No metadata"
            
            print(f"{Fore.CYAN}Token ID:{Style.RESET_ALL} {token_id} - "
                  f"{Fore.GREEN}Price:{Style.RESET_ALL} {format_price(price, currency)} - "
                  f"{Fore.MAGENTA}Attributes:{Style.RESET_ALL} {attr_str}")
            
        # Calculate average price
        prices = [get_nft_price(nft) for nft in nfts]
        valid_prices = [p for p in prices if p > 0]
        
        if valid_prices:
            avg_price = sum(valid_prices) / len(valid_prices)
            print(f"\n{Fore.YELLOW}Average price:{Style.RESET_ALL} {format_price(avg_price, currency)}")
        else:
            print(f"\n{Fore.RED}No valid prices found{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        print("\nFull error details:")
        import traceback
        print(traceback.format_exc())
        print(Style.RESET_ALL)

if __name__ == "__main__":
    main() 