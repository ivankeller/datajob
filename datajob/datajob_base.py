from abc import abstractmethod

from aws_cdk import aws_iam as iam
from aws_cdk import core

from datajob import logger
from datajob.datajob_stack import DataJobStack


class DataJobBase(core.Construct):
    def __init__(self, datajob_stack, name, **kwargs):
        super().__init__(datajob_stack, name, **kwargs)
        assert isinstance(
            datajob_stack, DataJobStack
        ), f"we expect the scope argument to be of type {DataJobStack}"
        self.name = name
        self.project_root = datajob_stack.project_root
        self.stage = datajob_stack.stage
        self.unique_name = f"{self.name}-{self.stage}"
        self.datajob_context = datajob_stack.datajob_context
        logger.info(f"adding job {self} to stack workflow resources")
        datajob_stack.resources.append(self)

    @abstractmethod
    def create(self):
        """create datajob"""

    def get_role(self, unique_name, service_principal):
        """get the role for the datajob"""
        role_name = unique_name + "-role"
        logger.debug(f"creating role {role_name}")
        glue_job_role = iam.Role(
            self,
            role_name,
            assumed_by=iam.ServicePrincipal(service_principal),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
            ],
        )
        return glue_job_role
