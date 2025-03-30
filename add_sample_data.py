from datetime import datetime, timedelta
import random
from app import app, db
from models import Doctor, Medicine

def add_sample_doctors():
    # Check if doctors already exist
    if db.session.query(Doctor).count() > 0:
        print("Doctors already exist in the database. Skipping...")
        return
    
    doctors = [
        {
            "first_name": "Sarah",
            "last_name": "Johnson",
            "email": "sarah.johnson@healthcare.com",
            "phone": "555-123-4567",
            "specialty": "Cardiology",
            "qualification": "MD, FACC - Harvard Medical School",
            "experience_years": 15,
            "bio": "Dr. Sarah Johnson is a board-certified cardiologist with over 15 years of experience in treating heart conditions. She specializes in preventive cardiology and heart failure management. Dr. Johnson has published numerous research papers on cardiovascular health and is committed to providing personalized care to her patients.",
            "consultation_fee": 150.00,
            "available_days": "Monday,Tuesday,Thursday,Friday",
            "available_times": '{"morning": ["09:00 AM", "10:00 AM", "11:00 AM"], "afternoon": ["02:00 PM", "03:00 PM", "04:00 PM"]}'
        },
        {
            "first_name": "Michael",
            "last_name": "Chen",
            "email": "michael.chen@healthcare.com",
            "phone": "555-234-5678",
            "specialty": "Neurology",
            "qualification": "MD, PhD - Johns Hopkins University",
            "experience_years": 12,
            "bio": "Dr. Michael Chen is a neurologist specializing in the diagnosis and treatment of neurological disorders including stroke, epilepsy, and multiple sclerosis. He completed his neurology residency at Johns Hopkins Hospital and a fellowship in stroke and cerebrovascular diseases. Dr. Chen combines clinical expertise with compassionate care to help patients manage complex neurological conditions.",
            "consultation_fee": 175.00,
            "available_days": "Monday,Wednesday,Friday",
            "available_times": '{"morning": ["08:00 AM", "09:00 AM", "10:00 AM"], "afternoon": ["01:00 PM", "02:00 PM", "03:00 PM"]}'
        },
        {
            "first_name": "Emily",
            "last_name": "Patel",
            "email": "emily.patel@healthcare.com",
            "phone": "555-345-6789",
            "specialty": "Pediatrics",
            "qualification": "MD, FAAP - University of Pennsylvania",
            "experience_years": 8,
            "bio": "Dr. Emily Patel is a board-certified pediatrician who provides comprehensive care for children from birth through adolescence. Her areas of interest include early childhood development, asthma management, and preventive healthcare. Dr. Patel is known for her gentle approach and ability to connect with young patients and their families.",
            "consultation_fee": 120.00,
            "available_days": "Tuesday,Wednesday,Thursday,Saturday",
            "available_times": '{"morning": ["09:00 AM", "10:00 AM", "11:00 AM"], "afternoon": ["03:00 PM", "04:00 PM", "05:00 PM"]}'
        }
    ]
    
    for doctor_data in doctors:
        doctor = Doctor(**doctor_data)
        db.session.add(doctor)
    
    db.session.commit()
    print(f"Added {len(doctors)} sample doctors to the database.")

def add_sample_medicines():
    # Check if medicines already exist
    if db.session.query(Medicine).count() > 0:
        print("Medicines already exist in the database. Skipping...")
        return
    
    medicines = [
        {
            "name": "CardioGuard",
            "generic_name": "Amlodipine",
            "category": "Cardiovascular",
            "description": "CardioGuard (Amlodipine) is a calcium channel blocker that dilates (widens) blood vessels and improves blood flow. It's used to treat high blood pressure and chest pain (angina) and may also be prescribed for coronary artery disease.",
            "dosage": "5mg, 10mg tablets",
            "price": 24.99,
            "stock_quantity": 120,
            "manufacturer": "HealthPharm Inc.",
            "requires_prescription": True,
            "side_effects": "Common side effects may include headache, dizziness, swelling of ankles or feet, tiredness, and flushing. Serious side effects are rare but may include irregular heartbeat or allergic reactions."
        },
        {
            "name": "NeuroClear",
            "generic_name": "Topiramate",
            "category": "Neurology",
            "description": "NeuroClear (Topiramate) is an anticonvulsant medication used to treat seizure disorders, migraines, and certain types of nerve pain. It works by reducing abnormal excitement in the brain.",
            "dosage": "25mg, 50mg, 100mg tablets",
            "price": 32.50,
            "stock_quantity": 85,
            "manufacturer": "NeuroPharma Labs",
            "requires_prescription": True,
            "side_effects": "Common side effects include drowsiness, dizziness, coordination problems, speech problems, and changes in taste. More serious effects may include vision problems, decreased sweating, and metabolic acidosis."
        },
        {
            "name": "KidRelief",
            "generic_name": "Ibuprofen (Pediatric Formula)",
            "category": "Pediatrics",
            "description": "KidRelief is a pediatric formulation of ibuprofen designed specifically for children. It provides effective relief from fever, pain, and inflammation with a pleasant fruit flavor that children find easy to take.",
            "dosage": "100mg/5ml oral suspension",
            "price": 12.99,
            "stock_quantity": 200,
            "manufacturer": "PediatriCare Pharmaceuticals",
            "requires_prescription": False,
            "side_effects": "Generally well-tolerated when used as directed. May cause upset stomach, mild heartburn, or nausea. Long-term use or higher doses may increase risk of gastrointestinal or kidney issues."
        },
        {
            "name": "AllerFree",
            "generic_name": "Cetirizine",
            "category": "Allergy",
            "description": "AllerFree is a 24-hour antihistamine that provides relief from allergy symptoms such as sneezing, runny nose, watery eyes, and itching. It's non-drowsy for most users and can be taken once daily.",
            "dosage": "10mg tablets",
            "price": 18.75,
            "stock_quantity": 150,
            "manufacturer": "AllerCare Therapeutics",
            "requires_prescription": False,
            "side_effects": "May cause mild drowsiness, dry mouth, or fatigue in some individuals. Serious side effects are very rare."
        },
        {
            "name": "VitaHealth Daily Multivitamin",
            "generic_name": "Multivitamin and Mineral Complex",
            "category": "Supplements",
            "description": "A complete daily multivitamin formula containing essential vitamins and minerals to support overall health and wellbeing. Includes vitamins A, C, D, E, B-complex, and key minerals like zinc, magnesium, and selenium.",
            "dosage": "One tablet daily with food",
            "price": 15.49,
            "stock_quantity": 300,
            "manufacturer": "VitaHealth Nutrition",
            "requires_prescription": False,
            "side_effects": "Generally well-tolerated. May cause mild stomach discomfort if taken without food."
        }
    ]
    
    for medicine_data in medicines:
        medicine = Medicine(**medicine_data)
        db.session.add(medicine)
    
    db.session.commit()
    print(f"Added {len(medicines)} sample medicines to the database.")

if __name__ == "__main__":
    with app.app_context():
        add_sample_doctors()
        add_sample_medicines()
        print("Sample data added successfully!")