import pandas as pd
from app import create_app
from app.extensions import db
from app.models import MysticBurger, User
import bcrypt

app = create_app()


def load_data():
    df = pd.read_csv('/app/Database/mysticburgers.csv')
    df.columns = df.columns.str.strip()
    df['Magic'] = df['Magic'].astype(bool)
    print(df.columns)
    with app.app_context():
        db.create_all()
        db.session.query(MysticBurger).delete()
        db.session.commit()

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

        print("Deleting all users...")
        db.session.query(User).delete()
        db.session.commit()
        print("All users deleted.")

        print("Creating admin user...")
        admin_user = User(
            id='admin',
            name='Admin User',
            admin=True,
            passwd=bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())
        )
        db.session.add(admin_user)

        db.session.commit()
        print("Admin user created.")


if __name__ == '__main__':
    load_data()
