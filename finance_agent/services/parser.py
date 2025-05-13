import csv
from io import TextIOWrapper
import pdfplumber
import re
from datetime import datetime
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

def parse_transactions(file, file_type='csv'):
    if file_type == 'pdf':
        return parse_pdf(file)
    return parse_csv(file)

def parse_csv(file):
    transactions = []
    reader = csv.DictReader(TextIOWrapper(file, encoding='utf-8'))

    for row in reader:
        transactions.append({
            'date': row.get('Date'),
            'amount': float(row.get('Amount', 0)),
            'merchant': row.get('Merchant'),
            'card': row.get('Card'),
            'category': row.get('Category', ''),  # optional
        })
    return transactions

def extract_date_from_text(text):
    """Extract date from text using various formats."""
    date_patterns = [
        r'\d{1,2}/\d{1,2}/\d{2,4}',  # MM/DD/YY or MM/DD/YYYY
        r'\d{4}-\d{2}-\d{2}',        # YYYY-MM-DD
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group()
            for date_format in ['%m/%d/%y', '%m/%d/%Y', '%Y-%m-%d']:
                try:
                    return datetime.strptime(date_str, date_format).strftime('%Y-%m-%d')
                except ValueError:
                    continue
    return None

def extract_amount_from_text(text):
    """Extract amount from text."""
    match = re.search(r'\$?([0-9,.]+)', text)
    if match:
        try:
            amount = float(match.group(1).replace(',', ''))
            # Basic validation
            if amount <= 0 or amount > 10000:
                logger.warning(f"Skipping suspicious amount: {amount}")
                return None
            return amount
        except (ValueError, TypeError):
            return None
    return None

def parse_pdf(file):
    transactions = []
    try:
        with pdfplumber.open(file) as pdf:
            logger.info(f"Processing PDF with {len(pdf.pages)} pages")
            
            # First, extract all text from the PDF
            all_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
            
            logger.info("Extracted text from all pages")
            
            # Use the more accurate regex pattern for Amex statements
            transaction_pattern = re.compile(
                r'(\d{2}/\d{2}/\d{2}) (.+?)\s+\$([0-9,.]+)',
                re.DOTALL
            )
            
            matches = transaction_pattern.findall(all_text)
            logger.info(f"Found {len(matches)} potential transactions")
            
            # Process each match
            for date_str, merchant_raw, amount_str in matches:
                try:
                    # Parse date
                    date = datetime.strptime(date_str, "%m/%d/%y").strftime("%Y-%m-%d")
                    
                    # Clean merchant name
                    merchant = re.sub(r'\s+', ' ', merchant_raw).strip()
                    
                    # Parse amount
                    amount = float(amount_str.replace(",", ""))
                    
                    # Skip zero amounts and suspiciously large amounts
                    if amount <= 0 or amount > 10000:
                        logger.warning(f"Skipping suspicious amount: {amount} for merchant: {merchant}")
                        continue
                    
                    # Skip if merchant name is too short or contains suspicious patterns
                    if len(merchant) < 3 or "TTY:" in merchant or "Account Ending" in merchant:
                        logger.warning(f"Skipping suspicious merchant: {merchant}")
                        continue
                    
                    # Check for duplicates
                    is_duplicate = any(
                        t['date'] == date and 
                        t['amount'] == amount and 
                        t['merchant'] == merchant
                        for t in transactions
                    )
                    
                    if not is_duplicate:
                        transactions.append({
                            'date': date,
                            'amount': amount,
                            'merchant': merchant,
                            'card': 'PDF Import',
                            'category': 'PDF Import'
                        })
                        logger.info(f"Added transaction: {date} - {merchant} - ${amount}")
                
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error parsing transaction: {str(e)}")
                    continue
    
    except Exception as e:
        logger.error(f"Error parsing PDF: {str(e)}")
        raise Exception(f"Error parsing PDF: {str(e)}")
    
    logger.info(f"Total valid transactions found: {len(transactions)}")
    return transactions
