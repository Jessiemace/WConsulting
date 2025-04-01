#mongodb queries
import pymongo
from datetime import datetime

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client['WConsulting']
employee_feedback_col = mongo_db['employee_feedback']
offboarding_review_col = mongo_db['offboarding_review']
employee_development_col = mongo_db['employee_personal_development']
reprimands_col = mongo_db['reprimands']

try:
    
    # Queries

    # Query for terminated employees and convert to a list
    terminated_employees = list(offboarding_review_col.find({
        "OFFBOARDING_DECISION_CATEGORY": "Terminated"
    }))

    print(terminated_employees)

    # Find feedback for terminated employees 
    for x in employee_feedback_col.find({"EMPLOYEE_ID": {"$in": [12, 22]}}):
        print(x)
    under_review_employees = list(offboarding_review_col.find({
        "OFFBOARDING_DECISION_CATEGORY": "Under Review"
    }))
    print(under_review_employees)


    #Sorting employees by most recent reprimands
    mydoc = reprimands_col.find().sort("REPRIMAND_DATE", -1)
    for x in mydoc:
        print(x)

    # Create a new feedback entry

    # Define the new feedback
    new_feedback = {
        "FEEDBACK_DATE": datetime.now().strftime("%Y-%m-%d"),  # Current date in YYYY-MM-DD format
     "FEEDBACK_TEXT": "Employee has shown great progress in decision-making and has taken on more responsibility in managing projects."
    }

    # Update the feedback list for Employee 3
    employee_feedback_col.update_one(
        {"EMPLOYEE_ID": 3},  
        {"$push": {"FEEDBACK": new_feedback}}      )

    print("New feedback entry added for Employee 3.")


    # Identifying employees with more serious remprimands where HR had to be involved 
    for reprimand_HR in reprimands_col.find({"HR_INVOLVEMENT": True}):
      print(reprimand_HR)

    # Find key areas for improvement within the firm
    for x in employee_development_col.find({},{ "EMPLOYEE_ID":1, "AREAS_FOR_IMPROVEMENT":1}):
     print(x)


    # Updating
    # Update the employee 20 offboarding decision to terminated
    myquery = { "EMPLOYEE_ID": 20 }
    newvalues = { "$set": { "OFFBOARDING_DECISION_CATEGORY": "Terminated" } }

    result = offboarding_review_col.update_one(myquery, newvalues)

    # Print the result of the update
    print(f"Documents matched: {result.matched_count}")
    print(f"Documents modified: {result.modified_count}")

    # Print documents in the collection after the update
    for x in offboarding_review_col.find({"EMPLOYEE_ID": 20}):
     print(x)

    # Deleting
    # Removing employee 10 from offboarding review as deemd valuable
    offboarding_review_col.delete_one({"EMPLOYEE_ID": 10})


except Exception as e:
    # Handle general exceptions
    print(f"An error occurred: {e}")

finally:
# Ensure MongoDB connection is closed
    if 'mongo_client' in locals():
        mongo_client.close()  # Close the MongoDB connection
        print("MongoDB connection closed.")
