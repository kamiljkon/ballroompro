from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from helperfunctions import getinput
import hashlib
Base = declarative_base()
engine = create_engine("sqlite:///data.db", echo=False)
Session = sessionmaker(bind=engine)

class User(Base):
    """
    Class using the SQLAlchemy library to create a database of users.
    
    """

    __tablename__ = "users"
    email = Column("email", String, primary_key=True)
    name = Column("name", String)
    account_type = Column("account_type", CHAR)
    password = Column("password", String)
    leading = relationship("Partnership", foreign_keys="[Partnership.leader_email]",
                           back_populates="leader")
    following = relationship("Partnership", foreign_keys="[Partnership.follower_email]",
                             back_populates="follower")

    def __init__(self, email, name, account_type, password):
        self.email = email
        self.name = name
        self.account_type = account_type
        self.password = password

    def __repr__(self):
        return f"{self.email}, {self.name}, {self.account_type}"
    
    def signup(interface):
        """
        Function to register a profile.

        Args:
            interface (str) -> type of account to be created (e.g. organizer, competitor)
        
        Returns:
            competitionsdata.json
        """
        email = input("Enter email adress: ")
        name = input("Enter name and surname: ").lower()
        password = input("Enter password: ")
        conf_password = input("Confirm password: ")
        if conf_password == password:
            encoded = conf_password.encode()
            password = hashlib.md5(encoded).hexdigest()
        else:
            print("Passwords do not match.")
            return None
        
        session = Session()

        existing_user_check = session.query(User).filter(User.email == email).first()
        if existing_user_check is not None:
            print("E-mail already registered, try again.")
            return None

        new_user = User(email, name, interface, password)
        session.add(new_user)
        session.commit()
        return new_user
        
    def login():
        """
        Function to login and verify a user.

        Returns:
            user_email (str) -> email of the loggedin user
            True (bool) -> confirmation of succesful log-in
        """
        user_email = input("Enter email: ")
        password = input("Enter password: ")

        auth = password.encode()
        auth_hash = hashlib.md5(auth).hexdigest()

        session = Session()
        user = session.query(User).filter_by(email=user_email).one_or_none()
        if user is not None:
            if user.password == auth_hash:
                return user_email, True
            else:
                print("Incorrect password.")
                return False
        else:
            print("User not found.")
            return False
        
    Base.metadata.create_all(bind=engine)

class Partnership(Base):
    """
    Class using the SQLAlchemy library to create a database of partnerships..
    
    """

    __tablename__ = "partnerships"
    partnershipid = Column(Integer, primary_key=True, autoincrement=True)
    leader_email = Column(String, ForeignKey("users.email"))
    follower_email = Column(String, ForeignKey("users.email"))
    leader = relationship("User", foreign_keys=[leader_email], back_populates="leading")
    follower = relationship("User", foreign_keys=[follower_email], back_populates="following")


    def new_partnership(useremail):
        """
        Function to create new partnerships.

        Args:
            useremail (str) -> email of the operating user

        Returns:
            Creates a new partnership object and appends the database.
            
        """

        print("\n#######\nTo create a new partnership, input your partner's and the partnerships details.")
        print("BEWARE! If you plan switching between leading/following in various styles, you have to create two partnerships.\n")
        partnername = input("Please input your partner's last name: ").lower()

        session = Session()
        potentialpartners = session.query(User).filter(
            User.name.like(f"%{partnername}%"),
            User.account_type == "C").all()
        if len (potentialpartners) == 0:
            print(f"Found no partner with lastname {partnername}.")
            return None      
        if len(potentialpartners) == 1:
            print("Found your partner!")
            for partner in potentialpartners:
                partneremail = partner.email
        else:
            i = 1
            for partner in potentialpartners:
                print(f"Partner {i}:\n Name: {partner}\n Email: {partner.email}\n")
                i += 1
            partnerchoice = getinput("xchoices", "Found multiple partners, please select the correct one from the list: ", i)
            partneremail = potentialpartners[partnerchoice-1].email
        
        leadfollow = getinput("Y/N", "Will you be leading [Y] or following [N]?: ")
        if leadfollow == "Y":
            leader_email = useremail
            follower_email = partneremail
        else:
            leader_email = partneremail
            follower_email = useremail
        
        existing_partnership = session.query(Partnership).filter(
            Partnership.leader_email == leader_email,
            Partnership.follower_email == follower_email)
        if existing_partnership:
            print("This partnership already exists.")
            return None
        
        new_partnership = Partnership(
            leader_email=leader_email,
            follower_email=follower_email)
        session.add(new_partnership)
        session.commit()
        print("Partnership succesfully added.")

    Base.metadata.create_all(bind=engine)