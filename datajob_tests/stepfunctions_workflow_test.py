import unittest
from mock import Mock
from mock import patch
from tech_skills_parser.deployment.glue_job import GlueJob
from tech_skills_parser.deployment import stepfunctions_workflow
from moto import mock_stepfunctions
from stepfunctions.steps.states import Parallel
from stepfunctions.steps.compute import GlueStartJobRunStep

from tech_skills_parser.deployment.stepfunctions_workflow import StepfunctionsWorkflow


@stepfunctions_workflow.task
class SomeMockedClass(object):
    def __init__(self, unique_glue_job_name):
        self.unique_glue_job_name = unique_glue_job_name


class StepfunctionsWorkflowTestTest(unittest.TestCase):
    @mock_stepfunctions
    def test_create_tasks_for_orchestration_simple_flow_successfully(self):
        task1 = stepfunctions_workflow.task(SomeMockedClass("task1"))
        task2 = stepfunctions_workflow.task(SomeMockedClass("task2"))
        task3 = stepfunctions_workflow.task(SomeMockedClass("task3"))
        task4 = stepfunctions_workflow.task(SomeMockedClass("task4"))

        with StepfunctionsWorkflow(
            "some-name", "arn:aws:iam::303915887687:role/some-role"
        ) as a_step_functions_workflow:
            task1 >> [task2, task3] >> task4

        self.assertTrue(
            isinstance(a_step_functions_workflow.chain_of_tasks[0], GlueStartJobRunStep)
        )
        self.assertTrue(
            isinstance(a_step_functions_workflow.chain_of_tasks[1], Parallel)
        )
        self.assertTrue(
            isinstance(a_step_functions_workflow.chain_of_tasks[2], GlueStartJobRunStep)
        )

    @mock_stepfunctions
    def test_create_tasks_for_orchestration_starts_with_parallel_flow_successfully(
        self,
    ):
        task1 = stepfunctions_workflow.task(SomeMockedClass("task1"))
        task2 = stepfunctions_workflow.task(SomeMockedClass("task2"))
        task3 = stepfunctions_workflow.task(SomeMockedClass("task2"))

        with StepfunctionsWorkflow(
            "some-name", "arn:aws:iam::303915887687:role/some-role"
        ) as a_step_functions_workflow:
            [task1, task2] >> task3

        self.assertTrue(
            isinstance(a_step_functions_workflow.chain_of_tasks[0], Parallel)
        )
        self.assertTrue(
            isinstance(a_step_functions_workflow.chain_of_tasks[1], GlueStartJobRunStep)
        )