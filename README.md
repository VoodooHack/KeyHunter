# Ethereum Private Key Scanner with Modular Pattern Filtering

A flexible tool for generating Ethereum private keys with customizable pattern filters and balance checking capabilities.

## Features

- 🔑 **Secure random private key generation**
- 🎯 **Modular pattern filtering system** - easily add custom filters
- 💰 **Balance checking** via Etherscan API
- 📊 **Statistics tracking**
- 🧩 **Extensible architecture** - create your own filter modules

## Default Filters Included

1. **NoRepeatingFilter**: Excludes keys with the same character repeating more than N times (default: 6)
   - Example excluded: `aaaaaaabc123...`

2. **NoTripleTripleFilter**: Excludes keys with patterns like AAA BBB CCC
   - Example excluded: `111222333abc...`

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Dependencies

- `eth-account` - For Ethereum key and address generation
- `web3` - Ethereum Web3 library
- `requests` - For API calls to check balances

## Quick Start

### Basic Usage

```python
from eth_key_scanner import ETHKeyScanner, NoRepeatingFilter, NoTripleTripleFilter

# Create scanner with default filters
scanner = ETHKeyScanner(filters=[
    NoRepeatingFilter(max_repeats=6),
    NoTripleTripleFilter()
])

# Generate 10 keys and check balances
results = scanner.generate_and_check_batch(
    batch_size=10,
    check_balances=True,
    api_key="YOUR_ETHERSCAN_API_KEY",  # Optional but recommended
    delay=0.2  # Delay between API calls
)

# Print statistics
scanner.print_stats()
```

### Run the Example

```bash
python eth_key_scanner.py
```

## Creating Custom Filters

Creating your own filter is easy! Just inherit from `PatternFilter`:

```python
from eth_key_scanner import PatternFilter

class MyCustomFilter(PatternFilter):
    def __init__(self, my_param):
        self.my_param = my_param
    
    def is_valid(self, hex_key: str) -> bool:
        # Your filtering logic here
        # Return True if key passes, False if it should be filtered out
        return True  # or False
    
    def get_name(self) -> str:
        return f"MyCustomFilter(param={self.my_param})"
```

### Example Custom Filters

See `custom_filters_example.py` for more examples:

- **NoSequentialFilter**: Filters out sequential patterns (123456, ABCDEF)
- **NoPalindromeFilter**: Filters out palindromes (ABCCBA)
- **NoCommonPatternFilter**: Filters out common weak patterns
- **MinEntropyFilter**: Ensures minimum character diversity
- **NoAlternatingFilter**: Filters out alternating patterns (ABABAB)

Run the custom filters demo:

```bash
python custom_filters_example.py
```

## API Reference

### ETHKeyScanner Class

#### Methods

- `__init__(filters: List[PatternFilter])` - Initialize scanner with filters
- `add_filter(filter: PatternFilter)` - Add a new filter
- `remove_filter(filter_name: str)` - Remove a filter by name
- `list_filters()` - Get list of active filter names
- `generate_private_key()` - Generate a random private key
- `apply_filters(hex_key: str)` - Test if a key passes all filters
- `private_key_to_address(private_key: str)` - Convert key to ETH address
- `check_balance(address: str, api_key: str)` - Check address balance
- `generate_and_check_batch(batch_size, check_balances, api_key, delay)` - Main batch generation method
- `print_stats()` - Display scanning statistics

### PatternFilter Base Class

All custom filters must implement:

- `is_valid(hex_key: str) -> bool` - Returns True if key passes filter
- `get_name() -> str` - Returns the name of the filter

## Balance Checking

The tool uses the Etherscan API to check balances. 

### Rate Limits

- **Without API key**: 5 calls/second, 100,000 calls/day
- **With free API key**: Higher limits

Get a free API key at: https://etherscan.io/apis

### Usage

```python
scanner.generate_and_check_batch(
    batch_size=100,
    check_balances=True,
    api_key="YOUR_API_KEY_HERE",
    delay=0.2  # Adjust delay to respect rate limits
)
```

## Statistics Tracking

The scanner tracks:
- Total keys generated
- Keys filtered out
- Keys that passed filters
- Addresses checked for balance
- Addresses with balance found

Access stats with `scanner.print_stats()` or `scanner.stats` dictionary.

## Configuration Examples

### High Security Filters

```python
from custom_filters_example import *

scanner = ETHKeyScanner(filters=[
    NoRepeatingFilter(max_repeats=4),
    NoTripleTripleFilter(),
    NoSequentialFilter(max_sequential=4),
    NoPalindromeFilter(min_palindrome_length=5),
    NoCommonPatternFilter(),
    MinEntropyFilter(min_unique_chars=14),
    NoAlternatingFilter(max_alternating=6)
])
```

### Minimal Filtering

```python
scanner = ETHKeyScanner(filters=[
    NoRepeatingFilter(max_repeats=10),
])
```

### No Filtering (Pure Random)

```python
scanner = ETHKeyScanner(filters=[])
```

## Performance Considerations

- **Filter Rate**: More restrictive filters = more keys generated per valid key
- **Balance Checking**: API rate limits are the main bottleneck
- **Batch Size**: Larger batches are more efficient but take longer

## Important Notes

### Probability of Finding Funds

The probability of randomly generating a private key that controls funds is astronomically low (approximately 1 in 2^256). This tool is primarily for:

- **Educational purposes**: Understanding Ethereum key generation
- **Wallet recovery**: Testing potential private keys you may have partial information about
- **Security research**: Analyzing weak key patterns
- **Pattern analysis**: Understanding key space and entropy

### Security Warnings

- **Never share private keys** that control real funds
- **Store private keys securely** if you generate any for actual use
- Private keys with funds found randomly would be an unprecedented mathematical event

## License

This tool is provided for educational and research purposes.

## Contributing

To add your own filters:

1. Create a class inheriting from `PatternFilter`
2. Implement `is_valid()` and `get_name()`
3. Add it to your scanner with `scanner.add_filter(YourFilter())`

## Example Output

```
Ethereum Private Key Scanner
======================================================================
Active filters: ['NoRepeating(max=6)', 'NoTripleTriple']

Generating 5 valid keys with filters: ['NoRepeating(max=6)', 'NoTripleTriple']
----------------------------------------------------------------------
Generated 10/5 valid keys...

======================================================================
RESULTS
======================================================================

#1
Private Key: 3f2e8c9b4a1d5e7f8c2a9b3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f
Address:     0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
Balance:     0.0 ETH

...

======================================================================
SCANNING STATISTICS
======================================================================
Total keys generated:     8
Filtered out:             3
Passed filters:           5
Addresses checked:        5
Addresses with balance:   0
Filter rate:              37.50%
```
