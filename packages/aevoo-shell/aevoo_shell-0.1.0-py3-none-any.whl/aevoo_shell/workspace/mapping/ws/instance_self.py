from dataclasses import dataclass

from .instance import Instances, Instance


@dataclass(eq=False, repr=False)
class InstancesSelf(Instances):

    @property
    def domain_dn(self):
        return self.ctx.user_ctx.domain_dn

    def ui_command_create(
        self,
        cid: str,
        model_name: str,
        inputs: str | None = None,
        model_ns: str = "default",
        version: str = None,
    ):
        return super().ui_command_create(
            cid, model_name, self.domain_dn, self.mapping_id, inputs, model_ns, version
        )


@dataclass(eq=False, repr=False)
class InstanceSelf(Instance):
    pass
