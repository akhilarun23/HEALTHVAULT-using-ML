import numpy as np
import pandas as pd
from scipy.stats import mode
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import random
import mysql.connector as my
import warnings



con = my.connect(user = 'root',password = '1234', host = 'localhost', database = 'security' )
cursor = con.cursor()

def booking():
    print('\n')
    cursor.execute('select * from doctor')
    result = cursor.fetchall()
    print("--------------------")

    count = 0
        
    for i in result:
        for j in i:
            print(j," ", end = "")
            count +=1
            if count <4:
                continue
            else:
                print("\n")
                count = 0
                continue
    print("--------------------\n")

        
    #inserting data into database
    specialist = input("Enter the specialist that you want to consult: ")
    dept = input("Enter the deparment: ")
    cursor.execute("Insert into booking (p_id, doctor, department) values(%s,%s,%s)",(usern,specialist,dept))
    con.commit()    
    print("Appointment successfully booked.")
    random_no = random.randint(1,100)
    print("Your Token number is : ", random_no)
    print("\nThank you for using HealthVault!\n")

def ml():
        DATA_PATH = "testing.csv"
        data = pd.read_csv(DATA_PATH)
 
        # Checking whether the dataset is balanced or not
        disease_counts = data["prognosis"].value_counts()
        temp_df = pd.DataFrame({
            "Disease": disease_counts.index,
            "Counts": disease_counts.values
        })
        encoder = LabelEncoder()
        data["prognosis"] = encoder.fit_transform(data["prognosis"])
        X = data.iloc[:,:-1]
        y = data.iloc[:, -1]
        X_train, X_test, y_train, y_test =train_test_split(X, y, test_size = 0.2, random_state = 24)
        def cv_scoring(estimator, X, y):
            return accuracy_score(y, estimator.predict(X))
 
        # Initializing Models
        models = {"SVC":SVC(), "Gaussian NB":GaussianNB(), "Random Forest":RandomForestClassifier(random_state=18)}
        svm_model = SVC()
        svm_model.fit(X_train, y_train)
        preds = svm_model.predict(X_test)

        # Training and testing Naive Bayes Classifier
        nb_model = GaussianNB()
        nb_model.fit(X_train, y_train)
        preds = nb_model.predict(X_test)
 
        # Training and testing Random Forest Classifier
        rf_model = RandomForestClassifier(random_state=18)
        rf_model.fit(X_train, y_train)
        preds = rf_model.predict(X_test)

        # Training and testing SVM Classifier
        svm_model = SVC()
        svm_model.fit(X_train, y_train)
        preds = svm_model.predict(X_test)
 
        # Training and testing Naive Bayes Classifier
        nb_model = GaussianNB()
        nb_model.fit(X_train, y_train)
        preds = nb_model.predict(X_test)
        final_svm_model = SVC()
        final_nb_model = GaussianNB()
        final_rf_model = RandomForestClassifier(random_state=18)
        final_svm_model.fit(X, y)
        final_nb_model.fit(X, y)
        final_rf_model.fit(X, y)

        # suppress warning messages
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)


        test_data = pd.read_csv("testing.csv").dropna(axis=1)
 
        test_X = test_data.iloc[:, :-1]
        test_Y = encoder.transform(test_data.iloc[:, -1])
 
        # Making prediction by take mode of predictions
        # made by all the classifiers
        svm_preds = final_svm_model.predict(test_X)
        nb_preds = final_nb_model.predict(test_X)
        rf_preds = final_rf_model.predict(test_X)
        final_preds = [mode([i,j,k])[0][0] for i,j,k in zip(svm_preds, nb_preds, rf_preds)]
        symptoms = X.columns.values
 
        # Creating a symptom index dictionary to encode the
        # input symptoms into numerical form
        symptom_index = {}
        for index, value in enumerate(symptoms):
            symptom = " ".join([i.capitalize() for i in value.split("_")])
            symptom_index[symptom] = index
 
        data_dict = {
            "symptom_index":symptom_index,
            "predictions_classes":encoder.classes_
        }
 
        # Defining the Function
        # Input: string containing symptoms separated by commas
        # Output: Generated predictions by models
        ade =["itching","skin rash","nodal skin eruptions","continuous_sneezing","shivering","chills","joint pain","stomach pain","acidity","ulcers on tongue","muscle_wasting","vomiting","burning micturition","spotting urination","fatigue","weight gain","anxiety","cold hands and feets","mood swings","weight loss","restlessness","lethargy","patches in throat","irregular sugar level","cough","high fever","sunken eyes","breathlessness","sweating","dehydration","indigestion","headache","yellowish skin","dark urine","nausea","loss of appetite","pain behind the eyes","back pain","constipation","abdominal pain","diarrhoea","mild fever","yellow urine","yellowing of eyes","acute liver failure","fluid overload","swelling of stomach","swelled lymph nodes","malaise","blurred and distorted vision","phlegm","throat irritation","redness of eyes","sinus pressure","runny nose","congestion","chest pain","weakness in limbs","fast heart rate","pain during bowel movements","pain in anal region","bloody stool","irritation in anus","neck pain","dizziness","cramps","bruising","obesity","swollen legs","swollen blood vessels","puffy face and eyes","enlarged thyroid","brittle nails","swollen extremeties","excessive hunger","extramarital contacts","drying and tingling lips","slurred speech","knee pain","hip joint pain","muscle weakness","stiff neck","swelling joints","movement stiffness","spinning movements","loss of balance","unsteadiness","weakness of one body side","loss of smell","bladder discomfort","foul smell of urine","continuous feel of urine","passage of gases","internal itching","toxic look (typhos)","depression","irritability","muscle pain","altered sensorium","red spots over body","belly pain","abnormal menstruation","dischromic patches","watering from eyes","increased appetite","polyuria","family history","mucoid sputum","rusty_ putum","lack of concentration","visual disturbances","receiving blood transfusion","receiving unsterile injections","coma","stomach bleeding","distention of abdomen","history of alcohol consumption","fluid overload","blood in sputum","prominent veins on calf","palpitations","painful walking","pus filled pimples","blackheads","scurring","skin peeling","silver like dusting","small dents in nails","inflammatory nails","blister","red sore around nose","yellow crust ooze"]
        def predictDisease():
            print("\n\n\n")
            print("------------------")
            for i in ade:
                print(i)
            print("------------------")
            print("\n\n\n")
            print("choose the symptom from the above symptoms that you suffer from:")
            symptoms = input("State your symptoms : ")
            symptoms = symptoms.title()
            symptoms = symptoms.split(",")
     
            # creating input data for the models
            input_data = [0] * len(data_dict["symptom_index"])
            for symptom in symptoms:
                index = data_dict["symptom_index"][symptom]
                input_data[index] = 1
         
            # reshaping the input data and converting it
            # into suitable format for model predictions
            input_data = np.array(input_data).reshape(1,-1)
     
            # generating individual outputs
            rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
            nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
            svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]
     
            # making final prediction by taking mode of all predictions
            final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])[0][0]
            predictions = {
                "rf_model_prediction": rf_prediction,
                "naive_bayes_prediction": nb_prediction,
                "svm_model_prediction": svm_prediction,
                "final_prediction":final_prediction
            }
            return predictions
 
        # Testing the function
        cut = predictDisease()
        mylst = list(cut.values())
        wordfreq = {}

        for word in mylst:
            if word in wordfreq:
                wordfreq[word] += 1
        else:
            wordfreq[word] = 1

        mostcmnword = max(wordfreq, key=wordfreq.get)
        print("\n\n\n")
        print("---------------------------")
        print("The most probable disease for the mentioned syptoms is: ",mostcmnword)
        
        


        ad ={"Fungal infection": "Fluconazole, Terbinafine, Clotrimazole" , "Allergy": "Loratadine, Cetirizine, Fexofenadine, Diphenhydramine" , "GERD": "Omeprazole, Esomeprazole, Lansoprazole, Ranitidine" , "Chronic cholestasis": "Ursodeoxycholic acid, Cholestyramine" , "Drug Reaction": "Antihistamines, Corticosteroids", "Peptic ulcer diseae": "Omeprazole, Ranitidine, Sucralfate", "AIDS": "Antiretroviral therapy (ART)","Diabetes": "Metformin, Insulin, Sitagliptin, Glipizide", "Gastroenteritis": "Loperamide, Ciprofloxacin, Azithromycin" , "Bronchial Asthma": "Albuterol, Fluticasone, Montelukast, Theophylline"  ,"Hypertension": "Lisinopril, Amlodipine, Hydrochlorothiazide, Losartan" ,"Migraine": "Sumatriptan, Propranolol, Topiramate","Cervical spondylosis Paralysis": "Ibuprofen, Naproxen, Cyclobenzaprine" ,"paralysis(brain hemorrhage)": "Rehabilitation therapy, Blood thinners"  ,"Jaundice": "Ursodeoxycholic acid, Vitamin K, Liver transplant","Malaria": "Chloroquine, Quinine, Artemisinin-based combination therapy","Chicken pox": "Acyclovir, Valacyclovir, Antihistamines","Dengue": "Acetaminophen, Intravenous fluids","Typhoid": "Ciprofloxacin, Azithromycin","hepatitis A": "Rest, Intravenous fluids","Hepatitis B": "Antiviral medications, Interferon","Hepatitis C": "Antiviral medications", "Hepatitis D": "No specific treatment" ,"Hepatitis E": "Rest, Intravenous fluids","Alcoholic hepatitis": "Corticosteroids, Abstinence from alcohol" ,"Tuberculosis": "Isoniazid, Rifampin, Ethambutol, Pyrazinamide","Common Cold": "Acetaminophen, Ibuprofen, Decongestants" ,"Pneumonia": "Antibiotics, Oxygen therapy" ,"Dimorphic hemmorhoids(piles)": "Topical creams, Suppositories, Surgery" ,"Heart attack": "Aspirin, Nitroglycerin, Beta blockers","Varicose veins":  "Compression stockings, Sclerotherapy, Laser treatment","Hypothyroidism": "Levothyroxine","Hyperthyroidism": "Methimazole, Propylthiouracil","Hypoglycemia": "Glucose tablets, Sugary foods","Osteoarthristis":"Acetaminophen, NSAIDs, Topical creams"  ,"Arthritis": "NSAIDs, DMARDs, Biologic agents","(vertigo) Paroymsal  Positional Vertigo":"Meclizine, Dimenhydrinate, Epley maneuver" , "Acne": "Benzoyl peroxide, Salicylic acid, Retinoids", "Urinary tract infection": "Antibiotics, Phenazopyridine" ,"Psoriasis": "Topical corticosteroids, Methotrexate, Biologic agents","Impetigo":"Topical antibiotics, Oral antibiotics"}
        adlist = list(ad.keys())
        adval = list(ad.values())


        diet = {
            "Fungal infection":"Avoid high sugar and refined carbohydrate foods, and increase intake of probiotics such as yogurt and kefir.",
            "Allergy":"Identify and avoid trigger foods, increase intake of anti-inflammatory foods such as fatty fish, leafy greens, and berries.",
            "GERD":"Avoid spicy, acidic, and fatty foods, and limit caffeine and alcohol. Eat smaller, more frequent meals and avoid lying down for at least 2-3 hours after eating.",
            "Chronic cholestasis":"Eat a low-fat, high-fiber diet and avoid fried and processed foods. Increase intake of antioxidant-rich fruits and vegetables.",
            "Drug Reaction":"Identify and avoid trigger foods, and consume a nutrient-dense, balanced diet to support overall health and healing.",
            "Peptic ulcer disease":"Avoid spicy and acidic foods, and limit caffeine and alcohol. Eat smaller, more frequent meals and avoid lying down for at least 2-3 hours after eating.",
            "AIDS":"Eat a nutrient-dense, balanced diet with adequate protein and calories to support immune function. Avoid raw or undercooked foods and practice good food safety.",
            "Diabetes":"Eat a well-balanced diet with controlled portions and consistent carbohydrate intake. Choose whole grains, lean proteins, and plenty of fruits and vegetables.",
            "Gastroenteritis":"Consume bland, easily digestible foods such as crackers, rice, and bananas. Avoid high-fat and spicy foods, caffeine, and alcohol. Stay hydrated with water and electrolyte-rich fluids.",
            "Bronchial Asthma":"Increase intake of antioxidant-rich fruits and vegetables, and consume omega-3 fatty acids found in fatty fish and flaxseeds. Avoid trigger foods such as dairy, gluten, and processed foods.",
            "Hypertension":"Limit sodium intake and increase consumption of potassium-rich foods such as leafy greens, bananas, and sweet potatoes. Choose lean proteins and whole grains, and limit alcohol intake.",
            "Migraine":"Identify and avoid trigger foods, and consume a well-balanced diet with adequate hydration. Increase intake of magnesium-rich foods such as almonds, spinach, and avocado.",
            "Cervical spondylosis":"Eat a nutrient-dense, balanced diet to support overall health and healing. Consume foods rich in calcium, magnesium, and vitamin D for bone health.",
            "Paralysis (brain hemorrhage)":"Eat a nutrient-dense, balanced diet to support overall health and healing. Adequate protein and calorie intake are important for healing and tissue repair.",
            "Jaundice":"Avoid fatty and fried foods, and consume a low-fat, high-fiber diet with plenty of fruits and vegetables. Drink plenty of fluids to stay hydrated.",
            "Malaria":"Consume a well-balanced diet with adequate protein and calories to support immune function and healing. Stay hydrated with water and electrolyte-rich fluids.",
            "Chicken pox":"Consume a nutrient-dense, balanced diet to support overall health and healing. Stay hydrated with water and electrolyte-rich fluids.",
            "Dengue":"Consume a nutrient-dense, balanced diet to support overall health and healing. Stay hydrated with water and electrolyte-rich fluids.",
            "Typhoid":"Consume a nutrient-dense, balanced diet with plenty of fluids to support overall health and healing. Avoid high-fiber and high-fat foods.",
            "Hepatitis A":"Avoid fatty and fried foods, and consume a low-fat, high-fiber diet with plenty of fruits and vegetables. Drink plenty of fluids to stay hydrated.",
            "Hepatitis B":"Avoid fatty and fried foods, and consume a low-fat, high-fiber",
            "Hepatitis C":"Avoid fatty and fried foods, and consume a low-fat, high-fiber diet with plenty of fruits and vegetables. Drink plenty of fluids to stay hydrated.",
            "Hepatitis D":"Avoid fatty and fried foods, and consume a low-fat, high-fiber diet with plenty of fruits and vegetables. Drink plenty of fluids to stay hydrated.",
            "Hepatitis E":"Avoid fatty and fried foods, and consume a low-fat, high-fiber diet with plenty of fruits and vegetables. Drink plenty of fluids to stay hydrated.",
            "Alcoholic hepatitis":"Avoid alcohol and consume a low-fat, high-fiber diet with plenty of fruits and vegetables. Drink plenty of fluids to stay hydrated.",
            "Tuberculosis":"Consume a well-balanced diet with adequate protein and calories to support immune function and healing. Increase intake of vitamin D and calcium for bone health.",
            "Common cold":"Increase intake of vitamin C-rich foods such as citrus fruits and bell peppers, and consume warm, soothing foods such as soup and herbal tea. Stay hydrated with water and electrolyte-rich fluids.",
            "Pneumonia":"Consume a well-balanced diet with adequate protein and calories to support immune function and healing. Increase intake of vitamin C and zinc-rich foods such as citrus fruits, bell peppers, and lean meats.",
            "Dimorphic hemorrhoids (piles)":"Increase intake of fiber-rich foods such as whole grains, fruits, and vegetables to promote regular bowel movements. Stay hydrated with water and electrolyte-rich fluids.",
            "Heart attack":"Eat a heart-healthy diet low in saturated and trans fats, and high in fiber-rich whole grains, fruits, and vegetables. Limit sodium intake and choose lean proteins.",
            "Varicose veins":"Increase intake of fiber-rich foods such as whole grains, fruits, and vegetables to promote regular bowel movements and reduce pressure on veins. Consume flavonoid-rich foods such as berries and citrus fruits to improve vein function",
            "Hypothyroidism":"Consume a well-balanced diet with adequate intake of iodine and selenium, which are important for thyroid function. Increase intake of nutrient-dense foods such as lean proteins, fruits, and vegetables.",
            "Hyperthyroidism":"Consume a well-balanced diet with adequate intake of calcium and vitamin D to support bone health. Limit intake of iodine-rich foods and avoid caffeine and alcohol.",
            "Hypoglycemia":"Eat frequent, balanced meals and snacks with controlled portions to maintain blood sugar levels. Choose complex carbohydrates and high-fiber foods to promote steady glucose release.",
            "Osteoarthritis":"Consume a well-balanced diet with adequate intake of calcium and vitamin D for bone health. Increase intake of antioxidant-rich foods such as berries and leafy greens to reduce inflammation.",
            "Arthritis":"Increase intake of anti-inflammatory foods such as fatty fish, nuts, and leafy greens. Avoid trigger foods such as dairy, gluten, and processed foods.",
            "(vertigo) Paroxysmal Positional Vertigo":"Avoid trigger foods such as caffeine and alcohol. Consume a well-balanced diet with adequate intake of magnesium and vitamin D to support nerve function.",
            "Acne":"Avoid high glycemic index foods and dairy products, and increase intake of antioxidant-rich foods such as berries and leafy greens. Stay hydrated with water and electrolyte-rich fluids.",
            "Urinary tract infection":"Increase intake of water and other fluids to promote urine flow and flush out bacteria. Consume cranberry products or supplements to prevent bacterial adherence to the urinary tract.",
            "Psoriasis":"Eating a diet rich in fruits, vegetables, whole grains, and lean proteins can help to support overall health and reduce inflammation, which may help to improve psoriasis symptoms",
            "Impetigo":"maintain a well-balanced diet with adequate intake of nutrients such as vitamin C and zinc to support immune function and promote healing. Drinking plenty of fluids, especially water, can also help to keep the skin hydrated and healthy"
        }
        dietlist = list(diet.keys())


        print("The Medication for", mostcmnword ,"is: ",end="")
        print(ad[mostcmnword])
        print("Please consider consulting a physician for the dosage of the medicines")
        print("---------------------------")
        print("\n\n")
        print("---------------------------")
        print("The Diet plan for",mostcmnword,"is:")
        print(diet[mostcmnword])
        print("---------------------------")
        print("\n\n\n")


        dis = mostcmnword
        med = ad[mostcmnword]
        cursor.execute("insert into diagnosis(p_id,disease_diagnosed,meds_prescribed) values(%s,%s,%s)",(usern,dis,med))
        con.commit()


def old_user():
    global usern
    usern = input('Enter patient ID: ')
    pwdu = input('Enter patients password: ')
    cursor.execute('select password from passwords where p_id like (%s)',(usern,))
    result = cursor.fetchall()
    for i in result:
        for j in i:
            if j == pwdu:
                print('Login successfully completed')
                print("\n\n--/Control panel\-- \n\n1.Display patient details \n2.Book an appointment \n3.AI consultation")
                pri = int(input())


    
                if pri == 1:
                    print("\n")
                    cursor.execute('select * from patients where p_id = (%s)',(usern,))
                    result = cursor.fetchall()
                    cu = 0
                    su = 0
                    print("--------------------")
                    for i in result:
                        for j in i:
                            print(j," ", end = "")
                            cu +=1
                            if cu <5:
                                continue
                            else:
                                print("\n")
                                cu = 0
                                continue
                    
                    print("--------------------")

                    print("\n\n")
                    print("--------------------")
                    print("Previously diagnosed diseases: ")
                    cursor.execute("select * from diagnosis where p_id = (%s)",(usern,))
                    resu = cursor.fetchall()
                    for i in resu:
                        for j in i:
                            print(j," ", end = "")
                            su +=1
                            if su <4:
                                continue
                            else:
                                print("\n")
                                su = 0
                                continue
                    print("\n")
                    print("--------------------")

                    asku = input("would you like to continue using the program(Y/N): ")
                    if asku.lower() == 'y':
                        print("\n\n--/Control panel\-- \n\n1.Book an appointment \n2.AI consultation")
                        prin = int(input())
                        if prin == 1:
                            booking()
                        elif prin == 2:
                            ml()
                            asker = input("would you like to continue to book an appointment with a doctor(Y/N)")
                            if asker.lower() == 'y':
                                booking()
                    else:
                        print("Thank you for using Health vault!")




                if pri == 2:
                    booking()

                if pri == 3:
                    ml()
                    asker = input("would you like to continue to book an appointment with a doctor(Y/N)")
                    if asker.lower() == 'y':
                        booking()
                    else:
                        print("Thank you for using HealthVault!")
            else:
                print('Incorrect password! \nCheck your password and username ')
                break
            break
        break


def new_user():
    d = input('Enter Patient ID: ')
    b = input('Enter your password: ') 
    c = input('Confirm your password: ')
    
    if b == c :
        print('Password Confirmed!')
        ab = 'insert into passwords (p_id,password) values(%s,%s)'
        ac = (d,b,)
        cursor.execute(ab,ac)
        con.commit()
    
    else:
        print('Password does not match...')
        tr = input("Would you like to try again?(Y/N) : ")
        count = 1
       
        if tr.lower() == 'y':
            2
            while count < 2:
                d = input('Enter Patient ID: ')
                b = input('Enter your password: ')
                c = input('Confirm your password: ')
                
                if b == c :
                    print('Password Confirmed!')
                    ab = 'insert into passwords (platform,password) values(%s,%s)'
                    ac = (d,b,)
                    cursor.execute(ab,ac)
                    con.commit()
                    break
               
                elif b!=c:
                    print("Password does not match, Exceeded number of chances!!")
                    count +=1

       


    #Inserting patient data 
    print('\n')
    de = input("Renter patient ID: ")
    be = input("Enter patient name: ")
    ce = int(input("Enter the age: "))
    ge = input("Enter the gender: ")
    fe = int(input("Enter the phone: "))

    ab = 'insert into patients (p_id,patient_name,age,Gender,phone_no) values(%s,%s,%s,%s,%s)'
    ac = (de,be,ce,ge,fe,)
    cursor.execute(ab,ac)
    con.commit() 



    



print("\n")
print("-----Welcome to Health vault-----")
print('\n')

a = input('Are you a new user?(Y/N) : ')
if a.lower() == 'y':
    new_user()

    eq = input("would you like to continue to the remaining functions?(Y/N)")
    if eq.lower() == 'y':
        print("\n\n\n")
        old_user()
    else:
        print("Thank you for creating an account!") 
    
elif a.lower() == 'n':
    old_user()
