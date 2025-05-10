import asyncio
import os
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from colorama import init, Fore, Style
from dotenv import load_dotenv
from .opensea import OpenSeaNFTFetcher, format_price as format_opensea_price
from .magiceden import MagicEdenNFTFetcher, Chain, format_price as format_magiceden_price

# Load environment variables
load_dotenv()

# Initialize colorama
init()

class NFTPriceTracker:
    def __init__(self):
        self.opensea = OpenSeaNFTFetcher()
        self.magiceden = MagicEdenNFTFetcher(Chain.ETHEREUM)  # Default to Ethereum for comparison

    async def get_opensea_data(self, collection_slug: str) -> Dict:
        """Fetch OpenSea collection data"""
        try:
            collection_info = self.opensea.get_collection_by_slug(collection_slug)
            nfts = self.opensea.get_collection_nfts(collection_slug)
            return {
                "collection_info": collection_info,
                "nfts": nfts,
                "success": True
            }
        except Exception as e:
            print(f"{Fore.RED}Error fetching OpenSea data: {str(e)}{Style.RESET_ALL}")
            return {"success": False, "error": str(e)}

    async def get_magiceden_data(self, collection_identifier: str) -> Dict:
        """Fetch Magic Eden collection data"""
        try:
            collection_info, contract_address = self.magiceden.get_collection_by_name_or_address(collection_identifier)
            nfts = self.magiceden.get_collection_nfts(contract_address)
            return {
                "collection_info": collection_info,
                "nfts": nfts,
                "success": True
            }
        except Exception as e:
            print(f"{Fore.RED}Error fetching Magic Eden data: {str(e)}{Style.RESET_ALL}")
            return {"success": False, "error": str(e)}

    def display_comparison(self, opensea_data: Dict, magiceden_data: Dict):
        """Display comparison between OpenSea and Magic Eden data"""
        print(f"\n{Fore.CYAN}=== NFT Collection Comparison ==={Style.RESET_ALL}")
        
        # OpenSea Data
        if opensea_data.get("success"):
            os_collection = opensea_data["collection_info"]
            os_stats = os_collection.get("stats", {})
            os_nfts = opensea_data["nfts"]
            
            print(f"\n{Fore.BLUE}OpenSea Statistics:{Style.RESET_ALL}")
            print(f"Floor Price: {format_opensea_price(os_stats.get('floor_price'))} ETH")
            print(f"24h Volume: {format_opensea_price(os_stats.get('24h_volume'))} ETH")
            print(f"Total Volume: {format_opensea_price(os_stats.get('total_volume'))} ETH")
            print(f"Listed NFTs: {len(os_nfts)}")
        else:
            print(f"\n{Fore.RED}OpenSea data unavailable: {opensea_data.get('error')}{Style.RESET_ALL}")

        # Magic Eden Data
        if magiceden_data.get("success"):
            me_collections = magiceden_data["collection_info"].get("collections", [])
            if me_collections:
                me_collection = me_collections[0]
                me_nfts = magiceden_data["nfts"]
                
                print(f"\n{Fore.GREEN}Magic Eden Statistics:{Style.RESET_ALL}")
                print(f"Floor Price: {format_magiceden_price(me_collection.get('floorPrice'), 'ETH')} ETH")
                print(f"24h Volume: {format_magiceden_price(me_collection.get('volume24h'), 'ETH')} ETH")
                print(f"Total Volume: {format_magiceden_price(me_collection.get('volumeAll'), 'ETH')} ETH")
                print(f"Listed NFTs: {len(me_nfts)}")
        else:
            print(f"\n{Fore.RED}Magic Eden data unavailable: {magiceden_data.get('error')}{Style.RESET_ALL}")

        # Price Comparison
        if opensea_data.get("success") and magiceden_data.get("success"):
            print(f"\n{Fore.YELLOW}Price Comparison Analysis:{Style.RESET_ALL}")
            
            os_floor = float(os_stats.get('floor_price', 0))
            me_floor = float(me_collection.get('floorPrice', 0))
            
            if os_floor and me_floor:
                diff_percentage = ((os_floor - me_floor) / me_floor) * 100
                better_marketplace = "OpenSea" if os_floor < me_floor else "Magic Eden"
                
                print(f"Floor Price Difference: {abs(diff_percentage):.2f}%")
                print(f"Better Floor Price on: {better_marketplace}")
            
            # Lowest Listings Comparison
            print(f"\n{Fore.YELLOW}Lowest 5 Listings Comparison:{Style.RESET_ALL}")
            
            if os_nfts:
                print("\nOpenSea Lowest Listings:")
                sorted_os = sorted(os_nfts, key=lambda x: float(x.get('price', {}).get('current', {}).get('value', 0)))
                for nft in sorted_os[:5]:
                    price = float(nft.get('price', {}).get('current', {}).get('value', 0))
                    token_id = nft.get('identifier')
                    print(f"Token ID: {token_id} - Price: {format_opensea_price(price)} ETH")
            
            if me_nfts:
                print("\nMagic Eden Lowest Listings:")
                sorted_me = sorted(me_nfts, key=lambda x: float(x.get('market', {}).get('floorAsk', {}).get('price', {}).get('amount', {}).get('decimal', 0)))
                for nft in sorted_me[:5]:
                    price = float(nft.get('market', {}).get('floorAsk', {}).get('price', {}).get('amount', {}).get('decimal', 0))
                    token_id = nft.get('token', {}).get('tokenId')
                    print(f"Token ID: {token_id} - Price: {format_magiceden_price(price, 'ETH')} ETH")

    def save_report(self, opensea_data: Dict, magiceden_data: Dict, filename: str = None):
        """Save comparison data to a report file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nft_report_{timestamp}.txt"

        try:
            with open(filename, "w") as f:
                f.write("NFT Collection Comparison Report\n")
                f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                # OpenSea Data
                if opensea_data.get("success"):
                    os_collection = opensea_data["collection_info"]
                    os_stats = os_collection.get("stats", {})
                    f.write("OpenSea Statistics:\n")
                    f.write(f"Collection Name: {os_collection.get('name', 'N/A')}\n")
                    f.write(f"Floor Price: {format_opensea_price(os_stats.get('floor_price'))} ETH\n")
                    f.write(f"24h Volume: {format_opensea_price(os_stats.get('24h_volume'))} ETH\n")
                    f.write(f"Total Volume: {format_opensea_price(os_stats.get('total_volume'))} ETH\n\n")

                # Magic Eden Data
                if magiceden_data.get("success"):
                    me_collections = magiceden_data["collection_info"].get("collections", [])
                    if me_collections:
                        me_collection = me_collections[0]
                        f.write("Magic Eden Statistics:\n")
                        f.write(f"Collection Name: {me_collection.get('name', 'N/A')}\n")
                        f.write(f"Floor Price: {format_magiceden_price(me_collection.get('floorPrice'), 'ETH')} ETH\n")
                        f.write(f"24h Volume: {format_magiceden_price(me_collection.get('volume24h'), 'ETH')} ETH\n")
                        f.write(f"Total Volume: {format_magiceden_price(me_collection.get('volumeAll'), 'ETH')} ETH\n")

            print(f"\n{Fore.GREEN}Report saved to: {filename}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error saving report: {str(e)}{Style.RESET_ALL}")

async def main():
    tracker = NFTPriceTracker()
    
    # Get collection identifiers from user
    print(f"\n{Fore.CYAN}Enter collection information:{Style.RESET_ALL}")
    opensea_slug = input("OpenSea collection slug (e.g., 'doodles-official'): ").strip()
    magiceden_id = input("Magic Eden collection ID or name: ").strip()
    
    if not opensea_slug or not magiceden_id:
        print(f"{Fore.RED}Both collection identifiers are required{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.YELLOW}Fetching data from both marketplaces...{Style.RESET_ALL}")
    
    # Fetch data from both marketplaces
    opensea_data = await tracker.get_opensea_data(opensea_slug)
    magiceden_data = await tracker.get_magiceden_data(magiceden_id)
    
    # Display comparison
    tracker.display_comparison(opensea_data, magiceden_data)
    
    # Ask if user wants to save report
    save = input("\nWould you like to save this report? (y/n): ").strip().lower()
    if save == 'y':
        tracker.save_report(opensea_data, magiceden_data)

if __name__ == "__main__":
    asyncio.run(main()) 