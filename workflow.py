import asyncio
from temporalio import workflow
from temporalio.common import RetryPolicy
from activities import extract_data, load_data, transform_data
from datetime import timedelta

@workflow.defn
class ETLWorkflow:
    def __init__(self):
        self.signal_data = None
        self.signal_received = False
        self.state = "initialized"

    #ALLOW WORKFLOW TO RECEIVE A SIGNAL AT ANY TIME
    @workflow.signal
    async def update_data(self, new_data: str):
        self.signal_data = new_data
        self.signal_received = True
        print(f"Received signal with data: {self.signal_data}")
    
    @workflow.run
    async def run(self) -> str:
        load_attempt_counter = 0
        
        #EXTRACT
        self.state = "extract started"
        extract_result = await workflow.execute_activity(
            extract_data, schedule_to_close_timeout=timedelta(seconds=10)
        )
        await asyncio.sleep(5)
        
        # Check if a signal was received before transforming
        if self.signal_received:
            print(f"Signal received: {self.signal_data}")
        
        #TRANSFORM
        self.state = "transform step started"
        transform_result = await workflow.execute_activity(
            transform_data, schedule_to_close_timeout=timedelta(seconds=10)
        )
        await asyncio.sleep(5)
        
        #LOAD
        self.state = "load step started"
        
        # Specify max num. of attempts
        max_failures = 3

        #Retry policy is max_failures + 1 attempt

        #Track current attempt
        current_attempt = 0

        #Execute load activity
        while True:            
            current_attempt += 1
            try:                
                load_result = await workflow.execute_activity(
                    load_data, 
                    args = [max_failures, current_attempt],
                    schedule_to_close_timeout=timedelta(seconds=10),
                    retry_policy = RetryPolicy(maximum_attempts=max_failures + 1),
                )
                break
            except Exception as e:
                print(f"Attempt {current_attempt} failed: {e}")

        return f"{extract_result} -> {transform_result} -> {load_result}"
    
    @workflow.query
    def get_state(self) -> str:
        return self.state