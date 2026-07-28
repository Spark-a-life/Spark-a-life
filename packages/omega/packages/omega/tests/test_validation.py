from wisegen_omega.validation import validate_mission

def test_schema_valid():
 assert validate_mission({"objective":"A valid objective","success_criteria":["pass"],"captain":{"decision":"APPROVE"}})==[]
def test_schema_invalid(): assert validate_mission({})
