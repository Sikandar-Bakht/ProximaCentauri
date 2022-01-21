 #!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core
from sprint_four_proj.sikandar_pipeline_stack import SikandarPipelineStack
from sprint_five_proj.sprint_five_proj_stack import SprintFiveProjStack

app = core.App()
print("triggers5")
#SikandarPipelineStack(app, "sikandarpipeline", env=core.Environment(account = '315997497220', region = 'us-east-2'))
SprintFiveProjStack(app, "sprintfiveprojstack")
app.synth()
