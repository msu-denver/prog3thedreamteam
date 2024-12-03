import pandas as pd
from app import create_app
from app.extensions import db
from app.models import MysticBurger

app = create_app()

def load_data():
    # Read the CSV file
    df = pd.read_csv('C:\School\MSU\Fall2024\CS3250_SWDevMethodsAndTools\github\projects\project-3-final-project-thedreamteam2\Database\mysticburgers.csv')
    
    # Clean up column names
    df.columns = df.columns.str.strip()

    # Convert 'Magic' column to boolean
    df['Magic'] = df['Magic'].astype(bool)

    # Print the columns to verify
    print(df.columns)

    # Clear existing data
    with app.app_context():
        db.session.query(MysticBurger).delete()
        db.session.commit()

        # Insert new data
        for index, row in df.iterrows():
            burger = MysticBurger(
                store=row['Store'],
                category=row['Category'],
                item=row['Item'],
                description=row['Description'],
                price=row['Price'],
                qty=row['Qty'],
                magic=row['Magic']
            )
            db.session.add(burger)
        db.session.commit()
        print("Database populated with CSV data!")

if __name__ == '__main__':
    load_data()