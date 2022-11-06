import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from blog import app, mail
 
 #Add profile picture to the user profile and save
def save_profile_pics(form_picture):
     random_hex = secrets.token_hex(8)
     _, f_ext = os.path.splitext(form_picture.filename)
     picture_filename = random_hex + f_ext
     picture_path = os.path.join(app.root_path, 'static/profile_images', picture_filename)
     
     #Resizing the users profile pictures 
     
     resize_output = (125, 125)
     new_image = Image.open(form_picture)
     new_image.thumbnail(resize_output)
     new_image.save(picture_path)
     return picture_filename
 
 
#funtion to send emails users for authentications
def reset_email(user):
    token = user.get_reset_token()
    send_message = Message('Password Reset Request', sender='noreply@demo.com', 
                           recipients=[user.email])
    send_message.body = f''' To reset your password, visit the link below:
{url_for('reset_token', token=token, _external=True )}

If you did not make this request, please ignore with no changes
''' 
    mail.send(send_message)