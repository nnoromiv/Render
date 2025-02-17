from happy_again import db
from sqlalchemy import Column, String, Float, Integer, Boolean

class CompletedTasks (db.Model):
    INDEX = 'index'
    USER_ID = 'user_id'
    TASK_COMPLETED = 'task_completed'
    TIMESTAMP="timestamp"

    index = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    task_completed = Column(String(32), nullable=False)
    timestamp = Column(String(32), nullable=False)
    
    __table_name = 'completed_tasks'
    __bind_key__ = 'happyagaindb'

    def __init__(self, user_id, task_completed, timestamp):
        self.user_id = user_id
        self.task_completed = task_completed
        self.timestamp = timestamp
    
    def to_json(self):
        return{
            self.USER_ID: self.user_id,
            self.TASK_COMPLETED: self.task_completed,
            self.TIMESTAMP: self.timestamp
        }

class FactorAnalysisData (db.Model):
    USER_ID = 'user_id'
    AGE ='age'
    COVIDQ1='covidq1'
    COVIDQ2='covidq2'
    COVIDQ3='covidq3'
    COVIDQ4_DRY_COUNTINUOUS_COUGH='covidq4_dry_continuous_cough'
    COVIDQ4_SORE_THROAT='covidq4_sore_throat'
    COVIDQ4_RUNNY_NOSE_NASAL_CONGESTION='covidq4_runny_nose_nasal_congestion'
    COVIDQ4_LOSS_OF_TASTE_SMELL='covidq4_loss_of_taste_smell'
    COVIDQ4_LOSS_OF_APPETITE='covidq4_loss_of_appetite'
    COVIDQ4_FEVER='covidq4_fever'
    COVIDQ4_CHILLS='covidq4_chills'
    COVIDQ4_HEADACHE='covidq4_headache'
    COVIDQ4_BODYHACHES='covidq4_body_aches'
    COVIDQ4_FATIGUE='covidq4_fatigue' 
    COVIDQ4_SHORTNESS_BREATH = 'covidq4_shortness_breath'
    COVIDQ4_NAUSEA_VOMITING = 'covidq4_nausea_and_or_vomiting'
    COVIDQ4_DIARRHEA = 'covidq4_diarrhea'
    COVIDQ4_OTHER = 'covidq4_other'
    COVIDQ4_TOTAL = 'covidq4_total'
    COVIDQ6 = 'covidq6'
    COVIDQ7 = 'covidq7'
    COVIDQ8 = 'covidq8'
    COVIDQ9 = 'covidq9'
    COVIDQ10 = 'covidq10'
    COVIDQ11_EXTREME_TIREDNESS_FATIGUE = 'covidq11_extreme_tiredness_fatigue'
    COVIDQ11_SHORTNESS_BREATH = 'covidq11_shortness_of_breath'
    COVIDQ11_CHEST_PAIN_TIGHTNESS = 'covidq11_chest_pain_or_tightness'
    COVIDQ11_PROBLEMS_MEMORY = 'covidq11_problems_with_memory'
    COVIDQ11_PROBLEMS_CONCENTRATION = 'covidq11_problems_with_concentration'
    COVIDQ11_DIFFICULTIES_SLEEPING_INSOMNIA = 'covidq11_difficulties_sleeping_insomnia'
    COVIDQ11_DIFFICULTIES_HEART_PALPITATIONS = 'covidq11_difficulties_heart_palpitations'
    COVIDQ11_DIZZINESS = 'covidq11_dizziness'
    COVIDQ11_PINS_NEEDLES = 'covidq11_pins_and_needles'
    COVIDQ11_JOINT_PAIN = 'covidq11_joint_pain'
    COVIDQ11_DEPRESSION = 'covidq11_depression'
    COVIDQ11_ANXIETY = 'covidq11_anxiety'
    COVIDQ11_TINNITUS = 'covidq11_tinnitus'
    COVIDQ11_EARACHE = 'covidq11_earache'
    
    # TODO: START
    COVIDQ11_FEELING_SICK = 'covidq11_feeling_sick'
    COVIDQ11_DIARRHEA = 'covidq11_diarrhea'
    COVIDQ11_STOMACH_ACHES = 'covidq11_stomach_aches'
    COVIDQ11_LOSS_OF_APPETITE = 'covidq11_loss_of_appetite'
    # TODO: CHANGE
    COVIDQ11_HIGH_TEMPERATURE = 'covidq11_high_temperature'
    COVIDQ11_COUGH = 'covidq11_cough'
    COVIDQ11_HEADACHES = 'covidq11_headaches'
    COVIDQ11_SORE_THROAT = 'covidq11_sore_throat'
    COVIDQ11_CHANGES_TO_SENSE_OF_SMELL_OR_TASTE = 'covidq11_changes_to_sense_of_smell_or_taste'
    # TODO: END
    
    COVIDQ11_RASHES = 'covidq11_rashes'
    COVIDQ11_OTHER = 'covidq11_other'
    COVIDQ11_TOTAL = 'covidq11_total'
    COVIDQ13_EXTREME_TIREDNESS_FATIGUE = 'covidq13_extreme_tiredness_fatigue'
    COVIDQ13_SHORTNESS_BREATH = 'covidq13_shortness_of_breath'
    COVIDQ13_CHEST_PAIN_TIGHTNESS = 'covidq13_chest_pain_or_tightness'
    COVIDQ13_PROBLEMS_MEMORY = 'covidq13_problems_with_memory'
    COVIDQ13_PROBLEMS_CONCENTRATION = 'covidq13_problems_with_concentration'
    COVIDQ13_DIFFICULTIES_SLEEPING_INSOMNIA = 'covidq13_difficulties_sleeping_insomnia'
    COVIDQ13_DIFFICULTIES_HEART_PALPITATIONS = 'covidq13_difficulties_heart_palpitations'
    COVIDQ13_DIZZINESS = 'covidq13_dizziness'
    COVIDQ13_PINS_NEEDLES = 'covidq13_pins_and_needles'
    COVIDQ13_JOINT_PAIN = 'covidq13_joint_pain'
    COVIDQ13_DEPRESSION = 'covidq13_depression'
    COVIDQ13_ANXIETY = 'covidq13_anxiety'
    COVIDQ13_TINNITUS = 'covidq13_tinnitus'
    COVIDQ13_EARACHE = 'covidq13_earache'
    COVIDQ13_FEELING_SICK = 'covidq13_feeling_sick'
    COVIDQ13_DIARRHEA = 'covidq13_diarrhea'
    COVIDQ13_STOMACH_ACHES = 'covidq13_stomach_aches'
    COVIDQ13_LOSS_OF_APPETITE = 'covidq13_loss_of_appetite'
    COVIDQ13_HIGH_TEMPERATURE = 'covidq13_high_temperature'
    COVIDQ13_COUGH = 'covidq13_cough'
    COVIDQ13_HEADACHES = 'covidq13_headaches'
    COVIDQ13_SORE_THROAT = 'covidq13_sore_throat'
    COVIDQ13_CHANGES_TO_SENSE_OF_SMELL_OR_TASTE = 'covidq13_changes_to_sense_of_smell_or_taste'
    COVIDQ13_RASHES = 'covidq13_rashes'
    COVIDQ13_OTHER = 'covidq13_other'
    COVIDQ13_TOTAL = 'covidq13_total'
    COVIDQ15 = 'covidq15'
    QOL_TOTAL_SCORE = 'qol_total_score'
    QOL11 = 'qol11'
    QOL16 = 'qol16'
    FATIGUE_TOTAL_SCORE = 'fatigue_total_score'
    FATIGUE8 = 'fatigue8'
    FATIGUE11 = 'fatigue11'

    user_id = Column(String(64),primary_key=True)
    age = Column(Integer, nullable=True)
    covidq1 = Column(Integer, nullable=True)
    covidq2 = Column(Integer, nullable=True)
    covidq3 = Column(Integer, nullable=True)
    covidq4_dry_continuous_cough = Column(Integer,nullable=True)
    covidq4_sore_throat = Column(Integer, nullable=True)
    covidq4_runny_nose_nasal_congestion = Column(Integer, nullable=True)
    covidq4_loss_of_taste_smell = Column(Integer, nullable=True)
    covidq4_loss_of_appetite = Column(Integer, nullable=True)
    covidq4_fever = Column(Integer, nullable=True)
    covidq4_chills = Column(Integer, nullable=True)
    covidq4_headache = Column(Integer, nullable=True)
    covidq4_body_aches = Column(Integer, nullable=True)
    covidq4_fatigue=Column(Integer, nullable=True)
    covidq4_shortness_breath = Column(Integer, nullable=True)
    covidq4_nausea_and_or_vomiting = Column(Integer, nullable=True)
    covidq4_diarrhea = Column(Integer, nullable=True)
    covidq4_other = Column(Integer, nullable=True)
    covidq4_total = Column(Integer, nullable=True)
    covidq6 = Column(Integer, nullable=True)
    covidq7 = Column(Integer, nullable=True)
    covidq8 = Column(Integer, nullable=True)
    covidq9 = Column(Integer, nullable=True)
    covidq10 = Column(Integer, nullable=True)
    covidq11_extreme_tiredness_fatigue = Column(Integer, nullable=True)
    covidq11_shortness_of_breath = Column(Integer, nullable=True)
    covidq11_chest_pain_or_tightness = Column(Integer, nullable=True)
    covidq11_problems_with_memory = Column(Integer, nullable=True)
    covidq11_problems_with_concentration = Column(Integer, nullable=True)
    covidq11_difficulties_sleeping_insomnia = Column(Integer, nullable=True)
    covidq11_difficulties_heart_palpitations = Column(Integer, nullable=True)
    covidq11_dizziness = Column(Integer, nullable=True)
    covidq11_pins_and_needles = Column(Integer, nullable=True)
    covidq11_joint_pain = Column(Integer, nullable=True)
    covidq11_depression = Column(Integer, nullable=True)
    covidq11_anxiety = Column(Integer, nullable=True)
    covidq11_tinnitus = Column(Integer, nullable=True)
    covidq11_earache = Column(Integer, nullable=True)
    # TODO: Start
    covidq11_feeling_sick = Column(Integer, nullable=True)
    covidq11_diarrhea = Column(Integer, nullable=True)
    covidq11_stomach_aches = Column(Integer, nullable=True)
    covidq11_loss_of_appetite = Column(Integer, nullable=True)
    # TODO: Change
    covidq11_high_temperature = Column(Integer, nullable=True)
    covidq11_cough = Column(Integer, nullable=True)
    covidq11_headaches = Column(Integer, nullable=True)
    covidq11_sore_throat = Column(Integer, nullable=True)
    covidq11_changes_to_sense_of_smell_or_taste = Column(Integer, nullable=True)
    # TODO: End
    covidq11_rashes = Column(Integer, nullable=True)
    covidq11_other = Column(Integer, nullable=True)
    covidq11_total = Column(Integer, nullable=True)
    covidq13_extreme_tiredness_fatigue = Column(Integer, nullable=True)
    covidq13_shortness_of_breath = Column(Integer, nullable=True)
    covidq13_chest_pain_or_tightness = Column(Integer, nullable=True)
    covidq13_problems_with_memory = Column(Integer, nullable=True)
    covidq13_problems_with_concentration = Column(Integer, nullable=True)
    covidq13_difficulties_sleeping_insomnia = Column(Integer, nullable=True)
    covidq13_difficulties_heart_palpitations = Column(Integer, nullable=True)
    covidq13_dizziness = Column(Integer, nullable=True)
    covidq13_pins_and_needles = Column(Integer, nullable=True)
    covidq13_joint_pain = Column(Integer, nullable=True)
    covidq13_depression = Column(Integer, nullable=True)
    covidq13_anxiety = Column(Integer, nullable=True)
    covidq13_tinnitus = Column(Integer, nullable=True)
    covidq13_earache = Column(Integer, nullable=True)
    
    covidq13_feeling_sick = Column(Integer, nullable=True)
    covidq13_diarrhea = Column(Integer, nullable=True)
    covidq13_stomach_aches = Column(Integer, nullable=True)
    covidq13_loss_of_appetite = Column(Integer, nullable=True)
    
    covidq13_high_temperature = Column(Integer, nullable=True)
    covidq13_cough = Column(Integer, nullable=True)
    covidq13_headaches = Column(Integer, nullable=True)
    covidq13_sore_throat = Column(Integer, nullable=True)
    covidq13_changes_to_sense_of_smell_or_taste = Column(Integer, nullable=True)
    
    covidq13_rashes = Column(Integer, nullable=True)
    covidq13_other = Column(Integer, nullable=True)
    covidq13_total = Column(Integer, nullable=True)
    covidq15 = Column(Integer, nullable=True)
    qol_total_score = Column(Integer, nullable=True)
    qol11 = Column(Integer, nullable=True)
    qol16 = Column(Integer, nullable=True)
    fatigue_total_score = Column(Integer, nullable=True)
    fatigue8 = Column(Integer, nullable=True)
    fatigue11 = Column(Integer, nullable=True)

    __table_name = 'factor_analisys_data'
    __bind_key__ = 'happyagaindb'

    def __init__(self, user_id, age, cq1,cq2,cq3,cq4dry,cq4sore,cq4nasal,cq4taste, cq4appetite,cq4fever,cq4chills,cq4head,cq4body,cq4fatigue,covidq4_shortness_of_breath_difficulty_breathing,
                covidq4_nausea_and_or_vomiting, covidq4_diarrhea, covidq4_other,
                covidq4_total, covidq6, covidq7, covidq8, covidq9, covidq10,
                covidq11_extreme_tiredness_fatigue, covidq11_shortness_of_breath,
                covidq11_chest_pain_or_tightness, covidq11_problems_with_memory,
                covidq11_problems_with_concentration, covidq11_difficulties_sleeping_insomnia,
                covidq11_difficulties_heart_palpitations, covidq11_dizziness,
                covidq11_pins_and_needles, covidq11_joint_pain, covidq11_depression,
                covidq11_anxiety, covidq11_tinnitus, covidq11_earache,
                
                # TODO: Start
                covidq11_feeling_sick,
                covidq11_diarrhea, 
                covidq11_stomach_aches, 
                covidq11_loss_of_appetite,
                # TODO: Change
                covidq11_high_temperature, 
                covidq11_cough, 
                covidq11_headaches,
                covidq11_sore_throat, 
                covidq11_changes_to_sense_of_smell_or_taste,
                # TODO: End
                
                covidq11_rashes, 
                covidq11_other, 
                covidq11_total,
                covidq13_extreme_tiredness_fatigue, 
                covidq13_shortness_of_breath,
                covidq13_chest_pain_or_tightness, covidq13_problems_with_memory,
                covidq13_problems_with_concentration, covidq13_difficulties_sleeping_insomnia,
                covidq13_difficulties_heart_palpitations, covidq13_dizziness,
                covidq13_pins_and_needles, covidq13_joint_pain, covidq13_depression,
                covidq13_anxiety, covidq13_tinnitus, covidq13_earache, 
                
                covidq13_feeling_sick,
                covidq13_diarrhea, 
                covidq13_stomach_aches, 
                covidq13_loss_of_appetite,
                
                covidq13_high_temperature, 
                covidq13_cough, 
                covidq13_headaches,
                covidq13_sore_throat, 
                covidq13_changes_to_sense_of_smell_or_taste,
                
                covidq13_rashes, covidq13_other, covidq13_total,
                covidq15, qol_total_score, qol11, qol16,
                fatigue_total_score, fatigue8, fatigue11):
        self.user_id = user_id
        self.age=age
        self.covidq1=cq1
        self.covidq2=cq2
        self.covidq3=cq3
        self.covidq4_dry_continuous_cough=cq4dry
        self.covidq4_sore_throat=cq4sore
        self.covidq4_runny_nose_nasal_congestion=cq4nasal
        self.covidq4_loss_of_taste_smell=cq4taste
        self.covidq4_loss_of_appetite=cq4appetite
        self.covidq4_fever=cq4fever
        self.covidq4_chills=cq4chills
        self.covidq4_headache=cq4head
        self.covidq4_body_aches=cq4body
        self.covidq4_fatigue=cq4fatigue
        self.covidq4_shortness_breath = covidq4_shortness_of_breath_difficulty_breathing
        self.covidq4_nausea_and_or_vomiting = covidq4_nausea_and_or_vomiting
        self.covidq4_diarrhea = covidq4_diarrhea
        self.covidq4_other = covidq4_other
        self.covidq4_total = covidq4_total
        self.covidq6 = covidq6
        self.covidq7 = covidq7
        self.covidq8 = covidq8
        self.covidq9 = covidq9
        self.covidq10 = covidq10
        self.covidq11_extreme_tiredness_fatigue = covidq11_extreme_tiredness_fatigue
        self.covidq11_shortness_of_breath = covidq11_shortness_of_breath
        self.covidq11_chest_pain_or_tightness = covidq11_chest_pain_or_tightness
        self.covidq11_problems_with_memory = covidq11_problems_with_memory
        self.covidq11_problems_with_concentration = covidq11_problems_with_concentration
        self.covidq11_difficulties_sleeping_insomnia = covidq11_difficulties_sleeping_insomnia
        self.covidq11_difficulties_heart_palpitations = covidq11_difficulties_heart_palpitations
        self.covidq11_dizziness = covidq11_dizziness
        self.covidq11_pins_and_needles = covidq11_pins_and_needles
        self.covidq11_joint_pain = covidq11_joint_pain
        self.covidq11_depression = covidq11_depression
        self.covidq11_anxiety = covidq11_anxiety
        self.covidq11_tinnitus = covidq11_tinnitus
        self.covidq11_earache = covidq11_earache
        
        # TODO: Start
        self.covidq11_feeling_sick = covidq11_feeling_sick
        self.covidq11_diarrhea = covidq11_diarrhea
        self.covidq11_stomach_aches = covidq11_stomach_aches
        self.covidq11_loss_of_appetite = covidq11_loss_of_appetite
        # TODO: Change
        self.covidq11_high_temperature = covidq11_high_temperature
        self.covidq11_cough = covidq11_cough
        self.covidq11_headaches = covidq11_headaches
        self.covidq11_sore_throat = covidq11_sore_throat
        self.covidq11_changes_to_sense_of_smell_or_taste = covidq11_changes_to_sense_of_smell_or_taste
        # TODO: End
        
        self.covidq11_rashes = covidq11_rashes
        self.covidq11_other = covidq11_other
        self.covidq11_total = covidq11_total
        self.covidq13_extreme_tiredness_fatigue = covidq13_extreme_tiredness_fatigue
        self.covidq13_shortness_of_breath = covidq13_shortness_of_breath
        self.covidq13_chest_pain_or_tightness = covidq13_chest_pain_or_tightness
        self.covidq13_problems_with_memory = covidq13_problems_with_memory
        self.covidq13_problems_with_concentration = covidq13_problems_with_concentration
        self.covidq13_difficulties_sleeping_insomnia = covidq13_difficulties_sleeping_insomnia
        self.covidq13_difficulties_heart_palpitations = covidq13_difficulties_heart_palpitations
        self.covidq13_dizziness = covidq13_dizziness
        self.covidq13_pins_and_needles = covidq13_pins_and_needles
        self.covidq13_joint_pain = covidq13_joint_pain
        self.covidq13_depression = covidq13_depression
        self.covidq13_anxiety = covidq13_anxiety
        self.covidq13_tinnitus = covidq13_tinnitus
        self.covidq13_earache = covidq13_earache
        
        self.covidq13_feeling_sick = covidq13_feeling_sick
        self.covidq13_diarrhea = covidq13_diarrhea
        self.covidq13_stomach_aches = covidq13_stomach_aches
        self.covidq13_loss_of_appetite = covidq13_loss_of_appetite
        
        self.covidq13_high_temperature = covidq13_high_temperature
        self.covidq13_cough = covidq13_cough
        self.covidq13_headaches = covidq13_headaches
        self.covidq13_sore_throat = covidq13_sore_throat
        self.covidq13_changes_to_sense_of_smell_or_taste = covidq13_changes_to_sense_of_smell_or_taste
        
        self.covidq13_rashes = covidq13_rashes
        self.covidq13_other = covidq13_other
        self.covidq13_total = covidq13_total
        self.covidq15 = covidq15
        self.qol_total_score = qol_total_score
        self.qol11 = qol11
        self.qol16 = qol16
        self.fatigue_total_score = fatigue_total_score
        self.fatigue8 = fatigue8
        self.fatigue11 = fatigue11
        
        
        
    
    def to_json(self):
        return{
            self.USER_ID: self.user_id,
            self.AGE: self.age,
            self.COVIDQ1: self.covidq1,
            self.COVIDQ2:self.covidq2,
            self.COVIDQ3:self.covidq3,
            self.COVIDQ4_DRY_COUNTINUOUS_COUGH:self.covidq4_dry_continuous_cough,
            self.COVIDQ4_SORE_THROAT:self.covidq4_sore_throat,
            self.COVIDQ4_RUNNY_NOSE_NASAL_CONGESTION:self.covidq4_runny_nose_nasal_congestion,
            self.COVIDQ4_LOSS_OF_TASTE_SMELL:self.covidq4_loss_of_taste_smell,
            self.COVIDQ4_LOSS_OF_APPETITE:self.covidq4_loss_of_appetite,
            self.COVIDQ4_FEVER:self.covidq4_fever,
            self.COVIDQ4_CHILLS:self.covidq4_chills,
            self.COVIDQ4_HEADACHE:self.covidq4_headache,
            self.COVIDQ4_BODYHACHES:self.covidq4_body_aches,
            self.COVIDQ4_FATIGUE:self.covidq4_fatigue,
            self.COVIDQ4_SHORTNESS_BREATH: self.covidq4_shortness_breath,
            self.COVIDQ4_NAUSEA_VOMITING: self.covidq4_nausea_and_or_vomiting,
            self.COVIDQ4_DIARRHEA: self.covidq4_diarrhea,
            self.COVIDQ4_OTHER: self.covidq4_other,
            self.COVIDQ4_TOTAL: self.covidq4_total,
            self.COVIDQ6: self.covidq6,
            self.COVIDQ7: self.covidq7,
            self.COVIDQ8: self.covidq8,
            self.COVIDQ9: self.covidq9,
            self.COVIDQ10: self.covidq10,
            self.COVIDQ11_EXTREME_TIREDNESS_FATIGUE: self.covidq11_extreme_tiredness_fatigue,
            self.COVIDQ11_SHORTNESS_BREATH: self.covidq11_shortness_of_breath,
            self.COVIDQ11_CHEST_PAIN_TIGHTNESS: self.covidq11_chest_pain_or_tightness,
            self.COVIDQ11_PROBLEMS_MEMORY: self.covidq11_problems_with_memory,
            self.COVIDQ11_PROBLEMS_CONCENTRATION: self.covidq11_problems_with_concentration,
            self.COVIDQ11_DIFFICULTIES_SLEEPING_INSOMNIA: self.covidq11_difficulties_sleeping_insomnia,
            self.COVIDQ11_DIFFICULTIES_HEART_PALPITATIONS: self.covidq11_difficulties_heart_palpitations,
            self.COVIDQ11_DIZZINESS: self.covidq11_dizziness,
            self.COVIDQ11_PINS_NEEDLES: self.covidq11_pins_and_needles,
            self.COVIDQ11_JOINT_PAIN: self.covidq11_joint_pain,
            self.COVIDQ11_DEPRESSION: self.covidq11_depression,
            self.COVIDQ11_ANXIETY: self.covidq11_anxiety,
            self.COVIDQ11_TINNITUS: self.covidq11_tinnitus,
            self.COVIDQ11_EARACHE: self.covidq11_earache,
            
            self.COVIDQ11_FEELING_SICK: self.covidq11_feeling_sick,
            self.COVIDQ11_DIARRHEA: self.covidq11_diarrhea,
            self.COVIDQ11_STOMACH_ACHES: self.covidq11_stomach_aches,
            self.COVIDQ11_LOSS_OF_APPETITE: self.covidq11_loss_of_appetite,
            
            self.COVIDQ11_HIGH_TEMPERATURE: self.covidq11_high_temperature,
            self.COVIDQ11_COUGH: self.covidq11_cough,
            self.COVIDQ11_HEADACHES: self.covidq11_headaches,
            self.COVIDQ11_SORE_THROAT: self.covidq11_sore_throat,
            self.COVIDQ11_CHANGES_TO_SENSE_OF_SMELL_OR_TASTE: self.covidq11_changes_to_sense_of_smell_or_taste,
            
            self.COVIDQ11_RASHES: self.covidq11_rashes,
            self.COVIDQ11_OTHER: self.covidq11_other,
            self.COVIDQ11_TOTAL: self.covidq11_total,
            self.COVIDQ13_EXTREME_TIREDNESS_FATIGUE: self.covidq13_extreme_tiredness_fatigue,
            self.COVIDQ13_SHORTNESS_BREATH: self.covidq13_shortness_of_breath,
            self.COVIDQ13_CHEST_PAIN_TIGHTNESS: self.covidq13_chest_pain_or_tightness,
            self.COVIDQ13_PROBLEMS_MEMORY: self.covidq13_problems_with_memory,
            self.COVIDQ13_PROBLEMS_CONCENTRATION: self.covidq13_problems_with_concentration,
            self.COVIDQ13_DIFFICULTIES_SLEEPING_INSOMNIA: self.covidq13_difficulties_sleeping_insomnia,
            self.COVIDQ13_DIFFICULTIES_HEART_PALPITATIONS: self.covidq13_difficulties_heart_palpitations,
            self.COVIDQ13_DIZZINESS: self.covidq13_dizziness,
            self.COVIDQ13_PINS_NEEDLES: self.covidq13_pins_and_needles,
            self.COVIDQ13_JOINT_PAIN: self.covidq13_joint_pain,
            self.COVIDQ13_DEPRESSION: self.covidq13_depression,
            self.COVIDQ13_ANXIETY: self.covidq13_anxiety,
            self.COVIDQ13_TINNITUS: self.covidq13_tinnitus,
            self.COVIDQ13_EARACHE: self.covidq13_earache,
            
            # TODO: Start
            self.COVIDQ13_FEELING_SICK: self.covidq13_feeling_sick,
            self.COVIDQ13_DIARRHEA: self.covidq13_diarrhea,
            self.COVIDQ13_STOMACH_ACHES: self.covidq13_stomach_aches,
            self.COVIDQ13_LOSS_OF_APPETITE: self.covidq13_loss_of_appetite,
            # TODO: Change
            self.COVIDQ13_HIGH_TEMPERATURE: self.covidq13_high_temperature,
            self.COVIDQ13_COUGH: self.covidq13_cough,
            self.COVIDQ13_HEADACHES: self.covidq13_headaches,
            self.COVIDQ13_SORE_THROAT: self.covidq13_sore_throat,
            self.COVIDQ13_CHANGES_TO_SENSE_OF_SMELL_OR_TASTE: self.covidq13_changes_to_sense_of_smell_or_taste,
            # TODO: End
            
            self.COVIDQ13_RASHES: self.covidq13_rashes,
            self.COVIDQ13_OTHER: self.covidq13_other,
            self.COVIDQ13_TOTAL: self.covidq13_total,
            self.COVIDQ15: self.covidq15,
            self.QOL_TOTAL_SCORE: self.qol_total_score,
            self.QOL11: self.qol11,
            self.QOL16: self.qol16,
            self.FATIGUE_TOTAL_SCORE: self.fatigue_total_score,
            self.FATIGUE8: self.fatigue8,
            self.FATIGUE11: self.fatigue11
        }
class ComponentScoreCoefficient (db.Model):
    INDEX='index'
    QUESTION = 'question'
    ONE = 'one'
    TWO = 'two'
    THREE='three'
    FOUR='four'
    FIVE='five'
    SIX='six'
    SEVEN='seven'
    EIGHT='eight'
    NINE='nine'
    TEN='ten'
    ELEVEN='elevn'
    TWELVE='twelve'
    THIRTEEN ='thirteen'
    FOURTEEN='fourteen'
    FIFTEEN='fifteen'
    SIXTEEN='sixteen'
    SEVENTEEN='seventeen'
    EIGHTEEN='eighteen'
    NINETEEN='nineteen'
    TWENTY='twenty'
    TWENTYONE='twentyone'

    index=Column(Integer,primary_key=True)
    question = Column(String(300), nullable=False )
    one = Column(Float(32), nullable=False)
    two = Column(Float(32), nullable=False)
    three= Column(Float(32), nullable=False)
    four = Column(Float(32), nullable=False)
    five = Column(Float(32), nullable=False)
    six = Column(Float(32), nullable=False)
    seven = Column(Float(32), nullable=False)
    eight = Column(Float(32), nullable=False)
    nine = Column(Float(32), nullable=False)
    ten = Column(Float(32), nullable=False)
    eleven = Column(Float(32), nullable=False)
    twelve = Column(Float(32), nullable=False)
    thirteen= Column(Float(32), nullable=False)
    fourteen= Column(Float(32), nullable=False)
    fifteen=Column(Float(32), nullable=False)
    sixteen= Column(Float(32), nullable=False)
    seventeen= Column(Float(32), nullable=False)
    eighteen= Column(Float(32), nullable=False)
    nineteen= Column(Float(32), nullable=False)
    twenty= Column(Float(32), nullable=False)
    twentyone= Column(Float(32), nullable=False)
    
    
    
    __table_name = 'component_score_coefficient'
    __bind_key__ = 'happyagaindb'

    def __init__(self, index,question, one, two, three, four, five, six, seven, eight,
                 nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen,
                 seventeen, eighteen, nineteen, twenty, twentyone):
        self.index=index
        self.question = question
        self.one = one
        self.two = two
        self.three=three
        self.four=four
        self.five=five
        self.six=six
        self.seven=seven
        self.eight=eight
        self.nine=nine
        self.ten=ten
        self.eleven=eleven
        self.twelve=twelve
        self.thirteen=thirteen
        self.fourteen=fourteen
        self.fifteen=fifteen
        self.sixteen=sixteen
        self.seventeen=seventeen
        self.eighteen=eighteen
        self.nineteen=nineteen
        self.twenty=twenty
        self.twentyone=twentyone
    
    def to_json(self):
        return{
            self.INDEX:self.index,
            self.QUESTION: self.question,
            self.ONE: self.one,
            self.TWO: self.two,
            self.THREE: self.three,
            self.FOUR: self.four,
            self.FIVE: self.five,
            self.SIX: self.six,
            self.SEVEN: self.seven,
            self.EIGHT: self.eight,
            self.NINE: self.nine,
            self.TEN: self.ten,
            self.ELEVEN: self.eleven,
            self.TWELVE: self.twelve,
            self.THIRTEEN: self.thirteen,
            self.FOURTEEN: self.fourteen,
            self.FIFTEEN: self.fifteen,
            self.SIXTEEN: self.sixteen,
            self.SEVENTEEN: self.seventeen,
            self.EIGHTEEN: self.eighteen,
            self.NINETEEN: self.nineteen,
            self.TWENTY: self.twenty,
            self.TWENTYONE: self.twentyone

        }

class ComponentScoreCoefficientDemo (db.Model):
    INDEX='index'
    QUESTION = 'question'
    ONE = 'one'
    TWO = 'two'
    THREE='three'
    FOUR='four'
    FIVE='five'
    SIX='six'
    SEVEN='seven'
    EIGHT='eight'
    NINE='nine'
    TEN='ten'
    ELEVEN='elevn'
    TWELVE='twelve'
    THIRTEEN ='thirteen'
    FOURTEEN='fourteen'
    FIFTEEN='fifteen'
    SIXTEEN='sixteen'
    SEVENTEEN='seventeen'
    EIGHTEEN='eighteen'
    NINETEEN='nineteen'
    TWENTY='twenty'
    TWENTYONE='twentyone'

    index=Column(Integer,primary_key=True)
    question = Column(String(300), nullable=False )
    one = Column(Float(32), nullable=False)
    two = Column(Float(32), nullable=False)
    three= Column(Float(32), nullable=False)
    four = Column(Float(32), nullable=False)
    five = Column(Float(32), nullable=False)
    six = Column(Float(32), nullable=False)
    seven = Column(Float(32), nullable=False)
    eight = Column(Float(32), nullable=False)
    nine = Column(Float(32), nullable=False)
    ten = Column(Float(32), nullable=False)
    eleven = Column(Float(32), nullable=False)
    twelve = Column(Float(32), nullable=False)
    thirteen= Column(Float(32), nullable=False)
    fourteen= Column(Float(32), nullable=False)
    fifteen=Column(Float(32), nullable=False)
    sixteen= Column(Float(32), nullable=False)
    seventeen= Column(Float(32), nullable=False)
    eighteen= Column(Float(32), nullable=False)
    nineteen= Column(Float(32), nullable=False)
    twenty= Column(Float(32), nullable=False)
    twentyone= Column(Float(32), nullable=False)
    
    
    
    __table_name = 'component_score_coefficient_demo'
    __bind_key__ = 'happyagaindb'

    def __init__(self, index,question, one, two, three, four, five, six, seven, eight,
                 nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen,
                 seventeen, eighteen, nineteen, twenty, twentyone):
        self.index=index
        self.question = question
        self.one = one
        self.two = two
        self.three=three
        self.four=four
        self.five=five
        self.six=six
        self.seven=seven
        self.eight=eight
        self.nine=nine
        self.ten=ten
        self.eleven=eleven
        self.twelve=twelve
        self.thirteen=thirteen
        self.fourteen=fourteen
        self.fifteen=fifteen
        self.sixteen=sixteen
        self.seventeen=seventeen
        self.eighteen=eighteen
        self.nineteen=nineteen
        self.twenty=twenty
        self.twentyone=twentyone
    
    def to_json(self):
        return{
            self.INDEX:self.index,
            self.QUESTION: self.question,
            self.ONE: self.one,
            self.TWO: self.two,
            self.THREE: self.three,
            self.FOUR: self.four,
            self.FIVE: self.five,
            self.SIX: self.six,
            self.SEVEN: self.seven,
            self.EIGHT: self.eight,
            self.NINE: self.nine,
            self.TEN: self.ten,
            self.ELEVEN: self.eleven,
            self.TWELVE: self.twelve,
            self.THIRTEEN: self.thirteen,
            self.FOURTEEN: self.fourteen,
            self.FIFTEEN: self.fifteen,
            self.SIXTEEN: self.sixteen,
            self.SEVENTEEN: self.seventeen,
            self.EIGHTEEN: self.eighteen,
            self.NINETEEN: self.nineteen,
            self.TWENTY: self.twenty,
            self.TWENTYONE: self.twentyone

        }
