import re
from typing import List, Dict

def extract_card_info(text: str) -> List[Dict]:
    """
    Extract credit card information from statement text.
    Returns a list of dictionaries containing card details.
    """
    cards = []
    
    # Common card patterns
    card_patterns = [
        # Chase patterns
        r'(Chase\s+(?:Freedom|Sapphire|Slate|Ink|Amazon|Disney|United|Southwest|Marriott|Hyatt|IHG|British\s+Airways|Aeroplan|World\s+of\s+Hilton|IHG\s+One|World\s+Elite\s+Mastercard|Freedom\s+Unlimited|Freedom\s+Flex|Slate\s+Edge|Ink\s+Business\s+(?:Preferred|Unlimited|Cash|Plus)))',
        # Amex patterns
        r'(American\s+Express\s+(?:Gold|Platinum|Green|Blue|EveryDay|Hilton|Delta|Marriott|Business\s+(?:Gold|Platinum|Green|Blue|EveryDay)))',
        # Citi patterns
        r'(Citi\s+(?:Double\s+Cash|Custom\s+Cash|Premier|Rewards\+|Diamond\s+Preferred|Simplicity|Costco))',
        # Capital One patterns
        r'(Capital\s+One\s+(?:Savor|SavorOne|Venture|VentureOne|Quicksilver|Spark))',
        # Discover patterns
        r'(Discover\s+(?:it|Miles|More|Student|Business))',
        # Bank of America patterns
        r'(Bank\s+of\s+America\s+(?:Customized\s+Cash|Travel\s+Rewards|Premium\s+Rewards|Business\s+Advantage))',
        # Generic patterns for other cards
        r'((?:Mastercard|Visa|American\s+Express)\s+(?:Platinum|Gold|Signature|Infinite|World\s+Elite))'
    ]
    
    # Combine all patterns
    combined_pattern = '|'.join(f'({pattern})' for pattern in card_patterns)
    
    # Find all matches
    matches = re.finditer(combined_pattern, text, re.IGNORECASE)
    
    # Process matches
    for match in matches:
        card_name = match.group(0).strip()
        if card_name and card_name not in [card['name'] for card in cards]:
            cards.append({
                'name': card_name,
                'type': 'credit',  # Default to credit card
                'confidence': 'high' if any(brand in card_name.lower() for brand in ['chase', 'amex', 'citi', 'capital one']) else 'medium'
            })
    
    return cards

def get_current_cards(transactions: List[Dict]) -> List[str]:
    """
    Extract current credit cards from transaction data and statement text.
    Returns a list of unique card names.
    """
    # Get unique card names from transactions
    card_names = set()
    
    # First, get cards from transaction data
    for txn in transactions:
        card = txn.get('card', '')
        if card and card != 'PDF Import':  # Skip generic PDF import entries
            card_names.add(card)
    
    # Then, try to extract cards from statement text if available
    for txn in transactions:
        # Look for card info in description/merchant fields
        description = txn.get('description', '') or txn.get('merchant', '')
        if description:
            extracted_cards = extract_card_info(description)
            for card in extracted_cards:
                if card['confidence'] == 'high':  # Only add high confidence matches
                    card_names.add(card['name'])
    
    # Clean up card names
    cleaned_cards = []
    for card in card_names:
        # Remove common prefixes/suffixes
        card = re.sub(r'^(?:Card|Credit\s+Card|Debit\s+Card)\s+', '', card, flags=re.IGNORECASE)
        card = re.sub(r'\s+(?:Card|Credit\s+Card|Debit\s+Card)$', '', card, flags=re.IGNORECASE)
        # Remove last 4 digits if present
        card = re.sub(r'\s+\*\*\*\*\d{4}$', '', card)
        cleaned_cards.append(card.strip())
    
    return list(set(cleaned_cards))  # Remove any duplicates after cleaning 