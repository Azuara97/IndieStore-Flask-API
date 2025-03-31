from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@localhost/IndieStore?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Users Table
class Users(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(200), nullable=False)
    PasswordHash = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(1), nullable=False)
    ConcurrencyStamp = db.Column(db.String(max), nullable=True)
    EmailConfirmed = db.Column(db.Boolean, nullable=True)
    NormalizedUserName = db.Column(db.String(100), nullable=True)
    NormalizedEmail = db.Column(db.String(200), nullable=True)
    SecurityStamp = db.Column(db.String(max), nullable=True)
    AccessFailedCount = db.Column(db.Integer, nullable=True)
    LockoutEnabled = db.Column(db.Boolean, nullable=True)
    LockoutEnd = db.Column(db.DateTime, nullable=True)
    TwoFactorEnabled = db.Column(db.Boolean, nullable=True)
    PhoneNumber = db.Column(db.String(20), nullable=True)
    PhoneNumberConfirmed = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return f'<User {self.UserName}>'

#Store Table
class Store(db.Model):
    gameID = db.Column(db.Integer, primary_key=True, nullable=False)
    gameName = db.Column(db.String(100), nullable=False)
    gameDesc = db.Column(db.String(max), nullable=False)
    genre = db.Column(db.String(25), nullable=False)
    gameVer = db.Column(db.Float, nullable=False)
    datePublish = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Store {self.Name}>'

#Initialize tables
@app.before_request
def create_tables():
    db.create_all()

#Register user
@app.route('/Users/Register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = Users(UserName=data['UserName'],
                     Email=data['Email'],
                     PasswordHash=data['PasswordHash'],
                     type=data['type'],
                     ConcurrencyStamp=data['ConcurrencyStamp'],
                     EmailConfirmed=data['EmailConfirmed'],
                     NormalizedUserName=data['NormalizedUserName'],
                     NormalizedEmail=data['NormalizedEmail'],
                     SecurityStamp=data['SecurityStamp'],
                     AccessFailedCount=data['AccessFailedCount'],
                     LockoutEnabled=data['LockoutEnabled'],
                     LockoutEnd=data['LockoutEnd'],
                     TwoFactorEnabled=data['TwoFactorEnabled'],
                     PhoneNumber=data['PhoneNumber'],
                     PhoneNumberConfirmed=data['PhoneNumberConfirmed'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

#Login user
@app.route('/Users/Login', methods=['POST'])
def login():
    data = request.get_json()

    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = Users.query.filter_by(UserName = username).first()
    if user and password == user.PasswordHash:
        return jsonify({ 'message': 'Login Succesfully' }), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

#Get all users
@app.route('/Users/GetAllUsers', methods=['GET'])
def getAllUsers():
    print(Users.query.all())
    users = Users.query.all()
    user_list = []
    for user in users:
        user_list.append({'Id': user.Id,
                          'UserName': user.UserName,
                          'Email': user.Email,
                          'PasswordHash': user.PasswordHash,
                          'type': user.type,
                          'ConcurrencyStamp': user.ConcurrencyStamp,
                          'EmailConfirmed': user.EmailConfirmed,
                          'NormalizedUserName': user.NormalizedUserName,
                          'NormalizedEmail': user.NormalizedEmail,
                          'SecurityStamp': user.SecurityStamp,
                          'AccessFailedCount': user.AccessFailedCount,
                          'LockoutEnabled': user.LockoutEnabled,
                          'LockoutEnd': user.LockoutEnd,
                          'TwoFactorEnabled': user.TwoFactorEnabled,
                          'PhoneNumber': user.PhoneNumber,
                          'PhoneNumberConfirmed': user.PhoneNumberConfirmed})
    return jsonify(user_list)

#Get user
@app.route('/Users/GetUser/<int:id>', methods=['GET'])
def getUser(id):
    user = Users.query.get_or_404(id)
    return jsonify({'Id': user.Id,
                    'UserName': user.UserName,
                    'Email': user.Email,
                    'PasswordHash': user.PasswordHash,
                    'type': user.type,
                    'ConcurrencyStamp': user.ConcurrencyStamp,
                    'EmailConfirmed': user.EmailConfirmed,
                    'NormalizedUserName': user.NormalizedUserName,
                    'NormalizedEmail': user.NormalizedEmail,
                    'SecurityStamp': user.SecurityStamp,
                    'AccessFailedCount': user.AccessFailedCount,
                    'LockoutEnabled': user.LockoutEnabled,
                    'LockoutEnd': user.LockoutEnd,
                    'TwoFactorEnabled': user.TwoFactorEnabled,
                    'PhoneNumber': user.PhoneNumber,
                    'PhoneNumberConfirmed': user.PhoneNumberConfirmed})

#Update
@app.route('/Users/UpdateUser/<int:id>', methods=['PUT'])
def updateUser(id):
    user = Users.query.get_or_404(id)
    data = request.get_json()
    user.UserName = data['UserName']
    user.Email = data['Email']
    user.PasswordHash = data['PasswordHash']
    user.type = data['type']
    user.ConcurrencyStamp = data['ConcurrencyStamp']
    user.EmailConfirmed = data['EmailConfirmed']
    user.NormalizedUserName = data['NormalizedUserName']
    user.NormalizedEmail = data['NormalizedEmail']
    user.SecurityStamp = data['SecurityStamp']
    user.AccessFailedCount = data['AccessFailedCount']
    user.LockoutEnabled = data['LockoutEnabled']
    user.LockoutEnd = data['LockoutEnd']
    user.TwoFactorEnabled = data['TwoFactorEnabled']
    user.PhoneNumber = data['PhoneNumber']
    user.PhoneNumberConfirmed = data['PhoneNumberConfirmed']
    db.session.commit()
    return jsonify({'Message': 'User updated'})

#Delete
@app.route('/Users/DeleteUser/<int:id>', methods=['DELETE'])
def deleteUser(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'Message': 'User deleted'})

#Get all store games
@app.route('/Store/GetAllStoreGames', methods=['GET'])
def getStoreGames():
    store_games = Store.query.all()
    store_list = []
    for game in store_games:
        store_list.append({'gameID': game.gameID,
                           'gameName': game.gameName,
                           'gameDesc': game.gameDesc,
                           'genre': game.genre,
                           'gameVer': game.gameVer,
                           'datePublish': game.datePublish,
                           'price': game.price})
    return jsonify(store_list)

#Run app
if __name__ == '__main__':
    app.run(debug=True)