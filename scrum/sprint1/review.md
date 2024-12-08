# Sprint Review

Date/Time: 11/22/24

Participants: Full group



User story 1 is completed.
All of the documentation stuff was completed.
The database was created, and is viewable through user story 1.


We used the following code to test the database:
###Testing function:
###@app.route('/populate-db')
###def populate_db():
    sample_burgers = [
        MysticBurger(store='Mystic Store 1', category='Burgers', item='Mystic Burger', description='A magical burger', price=9.99, qty=10, magic=True),
        MysticBurger(store='Mystic Store 2', category='Drinks', item='Mystic Shake', description='A magical shake', price=4.99, qty=20, magic=True),
        MysticBurger(store='Mystic Store 3', category='Sides', item='Mystic Fries', description='Magical fries', price=2.99, qty=30, magic=False)
    ]
    db.session.bulk_save_objects(sample_burgers)
    db.session.commit()
    return "Database populated with sample data!"
 