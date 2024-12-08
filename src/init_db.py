def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized!")
