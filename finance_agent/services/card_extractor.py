import re
from typing import List, Dict
import PyPDF2
import os
import json
from openai import OpenAI

# Regex-based card extraction
def extract_card_info(text: str) -> List[Dict]:
    card_patterns = [
        r'((?:American\s+Express|Amex)\s+(?:Platinum|Gold|Green|Blue|EveryDay|Hilton|Delta|Marriott|Business\s+(?:Platinum|Gold|Green|Blue)|Cash\s+Magnet|Surpass|Bonvoy|Card))',
        r'((?:American\s+Express|Amex)\s+Card(?:®)?)',
        r'(Platinum\s+Card(?:®)?)',
        r'(Chase\s+(?:Freedom|Sapphire|Slate|Ink|Amazon|Disney|United|Southwest|Marriott|Hyatt|IHG|Aeroplan|Freedom\s+Unlimited|Freedom\s+Flex|Slate\s+Edge|Ink\s+Business\s+(?:Preferred|Unlimited|Cash|Plus)))',
        r'(Citi\s+(?:Premier|Rewards\+|Double\s+Cash|Custom\s+Cash|Simplicity|Diamond\s+Preferred|Costco))',
        r'(Capital\s+One\s+(?:Savor|SavorOne|Venture|VentureOne|Quicksilver|Spark))',
        r'(Discover\s+(?:it|Miles|More|Student|Business))',
        r'(Bank\s+of\s+America\s+(?:Customized\s+Cash|Travel\s+Rewards|Premium\s+Rewards|Business\s+Advantage))',
        r'(Wells\s+Fargo\s+(?:Active\s+Cash|Reflect|Autograph|Business\s+Elite|Propel))',
        r'(US\s+Bank\s+(?:Altitude\s+Reserve|Cash\s+Plus|Visa\s+Platinum))',
        r'(HDFC\s+(?:Regalia|Infinia|Millennia|MoneyBack|IndianOil|Freedom|Diners\s+Club))',
        r'(ICICI\s+(?:Coral|Rubyx|Sapphiro|Amazon|Expressions|Emeralde|Manchester\s+United|Ferrari))',
        r'(Axis\s+(?:Magnus|Select|Ace|Neo|Freecharge|Vistara|Flipkart|MYZONE|Buzz|Signature|Reserve))',
        r'(SBI\s+(?:Card|SimplySAVE|Elite|Prime|IRCTC|BPCL|Air\s+India|Shaurya))',
        r'(Kotak\s+(?:811|Essentia|League|Royale|Fortune))',
        r'(IndusInd\s+(?:Pinnacle|Legend|Nexxt|Platinum|Aura))',
        r'(RBL\s+(?:Platinum|Play|Shoprite|Popcorn|Icon|Zerocard))',
        r'(YES\s+Bank\s+(?:Prosperity|Exclusive|PREMIUM|First))',
        r'(IDFC\s+FIRST\s+(?:Select|Wealth|Millennia))',
        r'((?:Mastercard|Visa|American\s+Express|RuPay|Diners\s+Club)\s+(?:Platinum|Gold|Signature|Infinite|Select|World\s+Elite))',
        r'(Platinum\s+Card)',
        r'(Credit\s+Card\s+Ending\s+\d{4})',
        r'(Card\s+Ending\s+\d{4})'
    ]
    combined_pattern = '|'.join(f'({p})' for p in card_patterns)
    matches = re.finditer(combined_pattern, text, re.IGNORECASE)

    cards = []
    for match in matches:
        card_name = match.group(0).strip()
        if card_name and card_name.lower() not in [c['name'].lower() for c in cards]:
            cards.append({
                'name': card_name,
                'type': 'credit',
                'confidence': 'high' if any(b in card_name.lower() for b in ['chase', 'amex', 'citi', 'capital one']) else 'medium'
            })
    return cards

# Extract text from PDF
def extract_text_from_pdf(pdf_file) -> str:
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return ""

# Chunk large text for GPT
def chunk_text(text: str, max_chunk_size: int = 4000) -> List[str]:
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    current_chunk = ""
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

# Fallback GPT-based extractor
def extract_card_info_from_gpt(text: str) -> List[str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    chunks = chunk_text(text)
    all_cards = set()

    for chunk in chunks:
        prompt = f"""Extract all credit card names from this statement text. Return ONLY a JSON array of card names, nothing else.
Example response format: ["American Express Platinum Card", "Chase Sapphire Preferred"]

Statement text:
{chunk}"""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a credit card statement analyzer. Extract credit card names and return them as a JSON array. Only return the JSON array, no other text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=150
            )
            card_names = json.loads(response.choices[0].message.content.strip())
            all_cards.update(card_names)
        except Exception as e:
            print(f"Error getting card names from GPT: {str(e)}")
            continue

    return list(all_cards)

# Unified function
def get_current_cards(transactions: List[Dict], pdf_files: List = None) -> List[str]:
    card_names = set()

    if pdf_files:
        for pdf_file in pdf_files:
            text = extract_text_from_pdf(pdf_file)
            if text:
                # 1. Try regex first
                regex_cards = extract_card_info(text)
                if regex_cards:
                    print("✅ Regex Match:", [c['name'] for c in regex_cards])
                    card_names.update([c['name'] for c in regex_cards if c['confidence'] == 'high'])
                else:
                    # 2. Fallback to GPT
                    gpt_cards = extract_card_info_from_gpt(text)
                    print("🔄 GPT Fallback:", gpt_cards)
                    card_names.update(gpt_cards)

    # Clean names
    cleaned_cards = []
    for card in card_names:
        card = re.sub(r'^(?:Card|Credit\s+Card|Debit\s+Card)\s+', '', card, flags=re.IGNORECASE)
        card = re.sub(r'\s+(?:Card|Credit\s+Card|Debit\s+Card)$', '', card, flags=re.IGNORECASE)
        card = re.sub(r'\s+\*\*\*\*\d{4}$', '', card)
        cleaned_cards.append(card.strip())

    return list(set(cleaned_cards))
