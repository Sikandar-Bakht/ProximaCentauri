from aws_cdk import (
    core as cdk,
    pipelines as pipelines,
    aws_codepipeline_actions as cp_actions
)

from aws_cdk import core
from sprint_four_proj.sprint_four_proj_stage import SprintFourProjStage

class SikandarPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        source = pipelines.CodePipelineSource.git_hub(repo_string = "Sikandar-Bakht/ProximaCentauri",
                                             branch="main",
                                             authentication=cdk.SecretValue.secrets_manager("Sikandar/github/token"),
                                             trigger = cp_actions.GitHubTrigger.POLL
                                             )
        
        synth = pipelines.ShellStep("Synth", input=source,
                                            commands=["cd ./Sikandar_Bakht/sprint4/SprintFourProj",
                                                      "pip install -r requirements.txt",
                                                      "npm install -g aws-cdk",
                                                      "cdk synth"],
                                            primary_output_directory = "./Sikandar_Bakht/sprint4/SprintFourProj/cdk.out"
                                            )
        pipeline = pipelines.CodePipeline(self,
                                          'SikandarPipeline',
                                          synth = synth
                                            )
        Beta = SprintFourProjStage(self, "beta", env = {
                                            'account':'315997497220',
                                            'region' : 'us-east-2'
                                            })
                                            
        Prod = SprintFourProjStage(self, "Prod", env = {
                                            'account':'315997497220',
                                            'region' : 'us-east-2'
                                            })

        unit_test = pipelines.ShellStep("unit_test", commands=["cd ./Sikandar_Bakht/sprint4/SprintFourProj",  
                                                               "pip install -r requirements.txt",
                                                               "pytest unit_test",
                                                               "pytest integtest"])
     
        pipeline.add_stage(Beta, post=[unit_test])
        

        pipeline.add_stage(Prod, pre=[pipelines.ManualApprovalStep("PromoteToProd")])
        