
class Expenses:

    def __init__(self, user_id, date, description, spending_type, category, amount):
        self.user_id = user_id
        self.date = date
        self.description = description
        self.spending_type = spending_type
        self.category = category
        self.amount = amount

    def export_as_dict(self):
        resp = {
            "user_id": self.user_id,
            "date": self.date,
            "description": self.description,
            "spending_type": self.spending_type,
            "category": self.category,
            "amount": self.amount
        }
        return resp

    def export_as_sheet_list(self):
        resp = [self.date,
                self.description,
                self.spending_type,
                self.category,
                self.amount,
                self.user_id]
        return resp