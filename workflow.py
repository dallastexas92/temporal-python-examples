import asyncio
from temporalio import workflow
from activities import extract_data, load_data, transform_data
from datetime import timedelta

@workflow.defn
class ETLWorkflow:
    @workflow.run
    async def run(self) -> str:
        transform_attempt_counter = 0
        
        #EXTRACT
        extract_result = await workflow.execute_activity(
            extract_data, schedule_to_close_timeout=timedelta(seconds=10)
        )
        await asyncio.sleep(5)
        
        #TRANSFORM
        while True:
            try:
                transform_attempt_counter += 1
                transform_result = await workflow.execute_activity(
                    transform_data, transform_attempt_counter == 1, schedule_to_close_timeout=timedelta(seconds=10)
                )
                break
            except Exception as e:
                print(f"Attempt {transform_attempt_counter} failed: {e}")
                await asyncio.sleep(2)

        await asyncio.sleep(5)
        #LOAD
        load_result = await workflow.execute_activity(
            load_data, schedule_to_close_timeout=timedelta(seconds=10)
        )
        return f"{extract_result} -> {transform_result} -> {load_result}"