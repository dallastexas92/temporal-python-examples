from temporalio import activity

#EXTRACT ACTIVITY
@activity.defn
async def extract_data() -> str:
    return "I'm the extract step!"

#TRANSFORM ACTIVITY
@activity.defn
async def transform_data() -> str:
    return "I'm the transform step!"

#LOAD ACTIVITY
@activity.defn
async def load_data(max_failures: int, current_attempt: int) -> str:
    if current_attempt <= max_failures:
        raise Exception(f"Load step failed on attempt {current_attempt}!")
    return f"I'm the load step! I completed after {current_attempt} attempt(s)"