from temporalio import activity

#EXTRACT ACTIVITY
@activity.defn
async def extract_data() -> str:
    return "I'm the extract step!"

#TRANSFORM ACTIVITY
@activity.defn
async def transform_data(fail_first_attempt: bool) -> str:
    if fail_first_attempt:
        raise Exception("Transform step failed on 1st attempt!")
    return "I'm the transform step!"

#LOAD ACTIVITY
@activity.defn
async def load_data() -> str:
    return "I'm the load step!"