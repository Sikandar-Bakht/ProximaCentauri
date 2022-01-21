from aws_cdk import (
    core as cdk
)
from sprint_five_proj.sprint_five_proj_stack import SprintFiveProjStack

class SprintFiveProjStage(cdk.Stage):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        s5_stack = SprintFiveProjStack(self, 'SikandarS5Instance')
