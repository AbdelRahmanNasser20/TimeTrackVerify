import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Employee

config_name = os.getenv('FLASK_ENV',)
print("THIS IS ", config_name)
# print("DATABASE_URL ", os.getenv('DATABASE_URL'))
# print("HEROKU_DATABASE_URL, ", os.getenv('HEROKU_DATABASE_URL'))

# print("SQLALCHEMY_DATABASE_URI" , os.getenv('SQLALCHEMY_DATABASE_URI'))
# SQLALCHEMY_DATABASE_URI = "postgres://u7rjm4v00r7o80:p29318c85fd890024aabb5af0d2eee671f3b489fceb0846bc261184455c66a610@cb5ajfjosdpmil.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dcbccjj9ki7jbl"

app = create_app(config_name)



teachers = [
    {"FirstName": "Abdel-Rahman", "LastName": "Nasser", "Email": "abdel.nasser045@gmail.com", "PhoneNumber": "2404766903", "Location": "Silver Spring"},
    {"FirstName": "Will", "LastName": "Corbin", "Email": "info@pandaprogrammer.com", "PhoneNumber": "2029073400", "Location": "Gaithersburg"},
    {"FirstName": "Erika", "LastName": "Loc", "Email": "billing@pandaprogrammer.com", "PhoneNumber": "2406721633", "Location": "Gaithersburg"},
    {"FirstName": "Natan", "LastName": "Corbin", "Email": "natan21dog@gmail.com", "PhoneNumber": "", "Location": "Gaithersburg"},
    {"FirstName": "Aline", "LastName": "Hirsch", "Email": "alinehirsch@outlook.com", "PhoneNumber": "2408603663", "Location": "Gaithersburg"},
    {"FirstName": "Omar", "LastName": "Mahmud", "Email": "omar.zawad2000@gmail.com", "PhoneNumber": "2406599711", "Location": "Gaithersburg"},
    {"FirstName": "Angelina", "LastName": "Roman", "Email": "angelinaihr@gmail.com", "PhoneNumber": "(301) 524 - 3393", "Location": "Gaithersburg"},
    {"FirstName": "Shreyas", "LastName": "Bachu", "Email": "shreyasbachu1355@gmail.com", "PhoneNumber": "(240) 756 - 0856", "Location": "Gaithersburg"},
    {"FirstName": "Omar", "LastName": "Nabeel", "Email": "omarfrommd@gmail.com", "PhoneNumber": "(301) 275 - 8165", "Location": "Gaithersburg"},
    {"FirstName": "Milan", "LastName": "Valderrama", "Email": "milanvalderrama56@gmail.com", "PhoneNumber": "(240) - 855 - 2789", "Location": "Gaithersburg"},
    {"FirstName": "Dashawna", "LastName": "Lara", "Email": "Dashawnaandamy@gmail.com", "PhoneNumber": "(240) 477 - 9430", "Location": "Gaithersburg"},
    {"FirstName": "Kyle", "LastName": "Gacuma", "Email": "kylelhedaria@gmail.com", "PhoneNumber": "(240) 595 - 9098", "Location": "Gaithersburg"},
    {"FirstName": "Zafir", "LastName": "Kazi", "Email": "zafir.kazi@gmail.com", "PhoneNumber": "(301) 605 - 5131", "Location": "Gaithersburg"},
    {"FirstName": "Justin", "LastName": "Johnson", "Email": "justinsapone@gmail.com", "PhoneNumber": "(301) 919 - 9328", "Location": "Gaithersburg"},
    {"FirstName": "Robert", "LastName": "Klebs", "Email": "robertklebs@gmail.com", "PhoneNumber": "(240) 743 - 9037", "Location": "Gaithersburg"},
    {"FirstName": "Alyssa", "LastName": "Corbin", "Email": "alyssa21dog@gmail.com", "PhoneNumber": "240-796-4295", "Location": "Gaithersburg"},
    {"FirstName": "Shayaan", "LastName": "Paracha", "Email": "shayaan.paracha@gmail.com", "PhoneNumber": "(240) 755 - 1122", "Location": "Gaithersburg"},
    {"FirstName": "Rhea", "LastName": "Chelar", "Email": "rhea.chelar@gmail.com", "PhoneNumber": "(240) 651 - 9067", "Location": "Gaithersburg"},
    {"FirstName": "Ian", "LastName": "Wang", "Email": "ianjwang16@gmail.com", "PhoneNumber": "(303) 475 - 5421", "Location": "Gaithersburg"},
    {"FirstName": "Sebastian", "LastName": "Tejerina", "Email": "sebastiantju5@gmail.com", "PhoneNumber": "(240) 870 - 0409", "Location": "Gaithersburg"},
    {"FirstName": "Radewa", "LastName": "Tan", "Email": "tanpradewa@gmail.com", "PhoneNumber": "(240) 328 - 2979", "Location": "Gaithersburg"},
    {"FirstName": "Sean", "LastName": "Karasik", "Email": "skarasik26@gmail.com", "PhoneNumber": "(202) 568 - 4756", "Location": "Gaithersburg"},
    {"FirstName": "Abdur", "LastName": "Shakir", "Email": "arshakir999@gmail.com", "PhoneNumber": "(301) 278 - 2624", "Location": "Gaithersburg"},
    {"FirstName": "Jonathan", "LastName": "Rodriguez", "Email": "jonathanherrera2002@gmail.com", "PhoneNumber": "(240) 688-5618", "Location": "Gaithersburg"},
    {"FirstName": "Ian", "LastName": "Huang", "Email": "ian0205huang@gmail.com", "PhoneNumber": "(626) 725 - 6506", "Location": "Gaithersburg"},
    {"FirstName": "Shreya", "LastName": "Ezhava", "Email": "shreyaezhava02@gmail.com", "PhoneNumber": "(202) 550 - 8454", "Location": "Gaithersburg"},
    {"FirstName": "Brandon", "LastName": "Sobremisana", "Email": "brandonsobre301@gmail.com", "PhoneNumber": "(240) 888 - 7792", "Location": "Gaithersburg"},
    {"FirstName": "Ethan", "LastName": "Phan", "Email": "ethan9phan@gmail.com", "PhoneNumber": "(301) 919-4789", "Location": "Gaithersburg"},
    {"FirstName": "Yoni", "LastName": "Zaslavsky", "Email": "yoni.m.zaslavsky@gmail.com", "PhoneNumber": "(240) 474 - 8113", "Location": "Gaithersburg"},
    {"FirstName": "Femi", "LastName": "Elias", "Email": "nifemielias1@gmail.com", "PhoneNumber": "(301) 339 - 3345", "Location": "Gaithersburg"},
    {"FirstName": "Josephine", "LastName": "Rakow", "Email": "josephinerakow@gmail.com", "PhoneNumber": "(301) 655-7425", "Location": "Gaithersburg"},
    {"FirstName": "Selina", "LastName": "Li", "Email": "selinali168888@gmail.com", "PhoneNumber": "(240) 805 - 8518", "Location": "Gaithersburg"},
    {"FirstName": "Aleeza", "LastName": "Sadiq", "Email": "aleezasa8@gmail.com", "PhoneNumber": "", "Location": "Gaithersburg"},
    {"FirstName": "Drew", "LastName": "Li", "Email": "drewli0145@gmail.com", "PhoneNumber": "240 - 506 - 0329", "Location": "Gaithersburg"},
    {"FirstName": "Kian", "LastName": "Saedi", "Email": "ksaedi2006@gmail.com", "PhoneNumber": "(240) 328 - 0927", "Location": "Gaithersburg"},
    {"FirstName": "Ava", "LastName": "Bull", "Email": "avacbull@icloud.com", "PhoneNumber": "(301) 310 - 3489", "Location": "Gaithersburg"},
    {"FirstName": "Matthew", "LastName": "Deleon", "Email": "hew.h.deleon@gmail.com", "PhoneNumber": "(240) 705 - 0780", "Location": "Gaithersburg"},
    {"FirstName": "Serin", "LastName": "Palathingal", "Email": "serinp15@gmail.com", "PhoneNumber": "(301) 667 - 9228", "Location": "Gaithersburg"},
    {"FirstName": "Jaylynne", "LastName": "Yang", "Email": "jaylynneyang@gmail.com", "PhoneNumber": "(240) 756 - 0101", "Location": "Gaithersburg"},
    {"FirstName": "Allison", "LastName": "Andreyev", "Email": "allisonmandreyev@gmail.com", "PhoneNumber": "TBD", "Location": "Gaithersburg"},
    {"FirstName": "Christina", "LastName": "Martirosova", "Email": "cmartirosova@gmail.com", "PhoneNumber": "TBD", "Location": "Gaithersburg"},
    {"FirstName": "Jason", "LastName": "Lee", "Email": "jasonlee131045@gmail.com", "PhoneNumber": "TBD", "Location": "Gaithersburg"},
    {"FirstName": "Shreya", "LastName": "Kar", "Email": "k9trufflelove@gmail.com", "PhoneNumber": "(240) 805 - 8543", "Location": "Gaithersburg"},
    {"FirstName": "Somesh", "LastName": "Kar", "Email": "lambo3668@gmail.com", "PhoneNumber": "(240) 597-6034", "Location": "Gaithersburg"},
    {"FirstName": "Danna", "LastName": "Park", "Email": "dannapark15@gmail.com", "PhoneNumber": "(240) 688 - 1264", "Location": "Gaithersburg"},
    {"FirstName": "Adrian", "LastName": "Sinfuego", "Email": "ansinfuego1@gmail.com", "PhoneNumber": "TBD", "Location": "Gaithersburg"},
    {"FirstName": "Meymuna", "LastName": "Oweis", "Email": "meymuna.oweis@gmail.com", "PhoneNumber": "TBD", "Location": "Gaithersburg"},
    {"FirstName": "Mohamad", "LastName": "Fouladi", "Email": "mohamad@pandaprogrammer.com", "PhoneNumber": "2405521003", "Location": "Silver Spring"},
    {"FirstName": "Bisrat", "LastName": "Tadesse", "Email": "dev.bizzy@gmail.com", "PhoneNumber": "2406452843", "Location": "Silver Spring"},
    {"FirstName": "Eric", "LastName": "Sierra", "Email": "ericgabbialon@gmail.com", "PhoneNumber": "2408480814", "Location": "Silver Spring"},
    {"FirstName": "Hamid", "LastName": "Nassehi", "Email": "hnassehi@terpmail.umd.edu", "PhoneNumber": "2406713391", "Location": "Silver Spring"},
    {"FirstName": "Alieu", "LastName": "Cole", "Email": "alieucole6@gmail.com", "PhoneNumber": "(240)-476-9135", "Location": "Silver Spring"},
    {"FirstName": "Jainam", "LastName": "Patel", "Email": "jainamp14@gmail.com", "PhoneNumber": "(240) 360-9968", "Location": "Silver Spring"},
    {"FirstName": "Neel", "LastName": "Joshi", "Email": "neel.joshi301@gmail.com", "PhoneNumber": "202-981-2645", "Location": "Silver Spring"},
    {"FirstName": "Erick", "LastName": "Chacon", "Email": "chacon.erick23@gmail.com", "PhoneNumber": "(240)308-9463", "Location": "Silver Spring"},
    {"FirstName": "Vihan", "LastName": "PERERA", "Email": "vihanperera334@gmail.com", "PhoneNumber": "240 817 8139", "Location": "Silver Spring"},
    {"FirstName": "William", "LastName": "Yen", "Email": "WilliamYen98@gmail.com", "PhoneNumber": "240-274-7729", "Location": "Silver Spring"},
    {"FirstName": "Colin", "LastName": "Nguyen", "Email": "cnguyen4995@gmail.com", "PhoneNumber": "240-461-4995", "Location": "Silver Spring"},
    {"FirstName": "Hans", "LastName": "Banag", "Email": "hansbanag@gmail.com", "PhoneNumber": "(240) 681 - 8892", "Location": "Silver Spring"},
    {"FirstName": "Antonio", "LastName": "Lopez", "Email": "ant.lopez1942@gmail.com", "PhoneNumber": "(240) 425-8564", "Location": "Silver Spring"},
    {"FirstName": "Brando", "LastName": "Morley", "Email": "morley0566@gmail.com", "PhoneNumber": "(201)-927-8586", "Location": "Silver Spring"},
    {"FirstName": "Daniel", "LastName": "Lobsenz", "Email": "dlobsenz@gmail.com", "PhoneNumber": "", "Location": "Silver Spring"},
    {"FirstName": "Emran", "LastName": "Shirzoi", "Email": "emranshirzoi@gmail.com", "PhoneNumber": "(202) 754 - 6883", "Location": "Silver Spring"},
    {"FirstName": "Mamadou", "LastName": "Pethe Diallo", "Email": "pethediallo1@gmail.com", "PhoneNumber": "240-883-2137", "Location": "Silver Spring"},
    {"FirstName": "Getnet", "LastName": "Workalemahu", "Email": "getehour@gmail.com", "PhoneNumber": "240-505-3208", "Location": "Silver Spring"},
    {"FirstName": "Cheikh", "LastName": "Dia", "Email": "diacheikhlax@gmail.com", "PhoneNumber": "+1 301 775 5819", "Location": "Silver Spring"},
    {"FirstName": "David", "LastName": "Arrazola", "Email": "darrazol@terpmail.umd.edu", "PhoneNumber": "240-264-9075", "Location": "Silver Spring"},
    {"FirstName": "Valery", "LastName": "Lara Gomez", "Email": "vlgn10124@gmail.com", "PhoneNumber": "+1 (240) 630-9013", "Location": "Silver Spring"},
    {"FirstName": "Shakib", "LastName": "Chowdhury", "Email": "chowdhuryshakib901@gmail.com", "PhoneNumber": "301-675-7009", "Location": "Silver Spring"},
    {"FirstName": "Thejitha", "LastName": "Rajapakshe", "Email": "thejitha.rajapakshe@gmail.com", "PhoneNumber": "(301) 676-3460", "Location": "Silver Spring"},
    {"FirstName": "Jeremiah", "LastName": "Akalu", "Email": "jeremiahteklu@gmail.com", "PhoneNumber": "301-968-5205", "Location": "Silver Spring"},
    {"FirstName": "George", "LastName": "Baldwin", "Email": "Gbaldwin306@gmail.com", "PhoneNumber": "301-281-7640", "Location": "Silver Spring"},
    {"FirstName": "Daniel", "LastName": "Acevedo-Ruz", "Email": "dacevedo@terpmail.umd.edu", "PhoneNumber": "301-300-4105", "Location": "Silver Spring"},
    {"FirstName": "Amy", "LastName": "Tran", "Email": "", "PhoneNumber": "", "Location": "Silver Spring"},
    {"FirstName": "Ryan", "LastName": "Parks", "Email": "ryan@pandaprogrammer.com", "PhoneNumber": "3016339540", "Location": "Northern Moco"}
]


def add_teachers_to_db():
    with app.app_context():
        for teacher in teachers:
            name = f"{teacher['FirstName']} {teacher['LastName']}"
            email = teacher['Email']
            phone_number = teacher['PhoneNumber']
            location = teacher['Location']

            # Check if the employee already exists in the database
            existing_employee = Employee.query.filter_by(email=email).first()
            if existing_employee:
                print(f"Employee with email {email} already exists.")
                continue

            # Create a new employee record
            new_employee = Employee(
                name=name,
                email=email,
                phone_number=phone_number
            )
            db.session.add(new_employee)
        
        # Commit the changes to the database
        db.session.commit()

if __name__ == '__main__':
    add_teachers_to_db()
    print("Teachers added to the database.")