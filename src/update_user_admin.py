from app import app, db
from app.models import User

def update_user_admin(user_id, is_admin):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.admin = is_admin
        try:
            db.session.commit()
            print(f"User {user_id} admin status updated to {is_admin}.")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
    else:
        print("User not found.")

if __name__ == '__main__':
    user_id_to_update = input("Enter the user ID you want to update: ")
    is_admin_input = input("Set admin status (True/False): ")
    is_admin = is_admin_input.lower() == 'true'  # Convert input to boolean

    with app.app_context():
        update_user_admin(user_id_to_update, is_admin)