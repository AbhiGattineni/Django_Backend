class TransactionCategorizer:
    def __init__(self):
        self.category_rules = {
            'DINING': [
                'CHIPOTLE', 'MCDONALD', 'WENDY', 'CARL', 'IN-N-OUT', 'BIRYANI',
                'PARADISE BIRYANI', 'ULAVACHARU', 'MASALA REPUBLIC', 'ZAREEN',
                'THE HALAL GUYS', 'ALEXANDER\'S PATISSERIE'
            ],
            'TRAVEL': [
                'HERTZ', 'NATIONAL CAR', 'FRONTIER AIRLINES', 'RENTALTOLL',
                'HERTZTOLL', 'Residence Inn', 'MARRIOTT'
            ],
            'TRANSPORTATION': [
                'LYFT', 'Uber', 'UNION 76', 'CHEVRON', 'VALERO', 'SHELL',
                'SUNOCO', 'BP', 'EXXON'
            ],
            'SHOPPING': [
                'WALMART', 'TARGET', 'SAFEWAY', '7-ELEVEN', 'INDIA CASH AND CARRY'
            ],
            'ENTERTAINMENT': [
                'YOUTUBE', 'HULU', 'NETFLIX', 'SPOTIFY', 'TOP GOLF'
            ],
            'SERVICES': [
                'GOOGLE', 'TMOBILE', 'DMV', 'SMOG CHECK', 'CAR WASH'
            ],
            'OTHER': []  # Default category
        }

    def get_category(self, merchant):
        merchant = merchant.upper()
        for category, keywords in self.category_rules.items():
            if any(keyword.upper() in merchant for keyword in keywords):
                return category
        return 'OTHER'

    def categorize_transactions(self, transactions):
        categorized = []
        for txn in transactions:
            category = self.get_category(txn['merchant'])
            categorized.append({
                **txn,
                'category': category
            })
        return categorized 