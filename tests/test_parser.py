import pandas as pd
from transaction_parser import tag_business_expenses

def test_tag_business_expenses():
    df = pd.DataFrame({
        "description": ["Uber ride", "Cafe brunch", "Spotify"],
        "amount": [-20, -15, -10]
    })

    rules = {"uber": "Transport", "cafe": "Meals"}
    tagged = tag_business_expenses(df, rules)

    assert tagged["is_business"].sum() == 2
    assert tagged.loc[0, "category"] == "Transport"
