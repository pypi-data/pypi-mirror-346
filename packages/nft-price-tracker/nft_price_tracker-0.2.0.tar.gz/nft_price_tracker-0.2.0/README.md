# NFT Price Tracker

A Python tool for tracking NFT prices across different marketplaces (OpenSea and Magic Eden).

## Features

- Track NFT prices across multiple marketplaces simultaneously
- Compare floor prices between OpenSea and Magic Eden
- View lowest and highest priced NFTs in collections
- Generate detailed price comparison reports
- Support for both Ethereum and Solana NFTs

## Installation

```bash
pip install nft-price-tracker
```

## Usage

```python
from nft_price_tracker import NFTPriceTracker

# Initialize tracker
tracker = NFTPriceTracker()

# Track a collection
tracker.track_collection(
    opensea_slug="doodles-official",
    magiceden_id="your_collection_id"
)
```

Or use the command line interface:

```bash
nft-tracker
```

## Requirements

- Python 3.8+
- OpenSea API Key
- Magic Eden API Key (optional)

## Configuration

Create a `.env` file in your project root:

```env
OPENSEA_API_KEY=your_opensea_api_key_here
MAGICEDEN_API_KEY=your_magiceden_api_key_here
```

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. 