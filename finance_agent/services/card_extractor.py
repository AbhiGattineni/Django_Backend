import re
from typing import List, Dict
import PyPDF2
import io
import os
from openai import OpenAI

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from a PDF file.
    """
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

def chunk_text(text: str, max_chunk_size: int = 4000) -> List[str]:
    """
    Split text into chunks of approximately max_chunk_size characters,
    trying to break at sentence boundaries.
    """
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Split into sentences
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

def extract_card_info_from_gpt(text: str) -> List[str]:
    """
    Use ChatGPT to extract credit card names from text.
    Returns a list of card names.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Split text into chunks if it's too long
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
            
            # Parse the response as JSON
            import json
            card_names = json.loads(response.choices[0].message.content.strip())
            all_cards.update(card_names)
            
        except Exception as e:
            print(f"Error getting card names from GPT for chunk: {str(e)}")
            continue
    
    return list(all_cards)

def get_current_cards(transactions: List[Dict], pdf_files: List = None) -> List[str]:
    """
    Extract current credit cards from PDF statements using GPT.
    Returns a list of unique card names.
    """
    card_names = set()
    
    if pdf_files:
        for pdf_file in pdf_files:
            text = extract_text_from_pdf(pdf_file)

            if text:
                # Use GPT to extract card names
                extracted_cards = extract_card_info_from_gpt(text)
                card_names.update(extracted_cards)
                print(extracted_cards)
    
    # Clean up card names
    cleaned_cards = []
    for card in card_names:
        # Remove common prefixes/suffixes
        card = re.sub(r'^(?:Card|Credit\s+Card|Debit\s+Card)\s+', '', card, flags=re.IGNORECASE)
        card = re.sub(r'\s+(?:Card|Credit\s+Card|Debit\s+Card)$', '', card, flags=re.IGNORECASE)
        # Remove last 4 digits if present
        card = re.sub(r'\s+\*\*\*\*\d{4}$', '', card)
        cleaned_cards.append(card.strip())
    
    return list(set(cleaned_cards))
