from aws_cdk import (
    core as cdk
)
from sprint_four_proj.sprint_four_proj_stack import SprintFourProjStack

class SprintFourProjStage(cdk.Stage):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        s4_stack = SprintFourProjStack(self, 'SikandarS4Instance')
