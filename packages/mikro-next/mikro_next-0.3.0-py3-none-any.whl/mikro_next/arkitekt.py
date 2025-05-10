import json
import os
from pydantic import Field
from rath.links.file import FileExtraction
from rath.links.dictinglink import DictingLink
from rath.links.auth import AuthTokenLink
from rath.links.split import SplitLink
from fakts_next import Fakts
from herre_next import Herre
from arkitekt_next.service_registry import BaseArkitektService, Params
from arkitekt_next.base_models import Requirement

from mikro_next.mikro_next import MikroNext
from mikro_next.rath import MikroNextLinkComposition, MikroNextRath
from rath.links.split import SplitLink
from fakts_next.contrib.rath.aiohttp import FaktsAIOHttpLink
from fakts_next.contrib.rath.graphql_ws import FaktsGraphQLWSLink
from herre_next.contrib.rath.auth_link import HerreAuthLink
from mikro_next.contrib.fakts.datalayer import FaktsDataLayer
from mikro_next.links.upload import UploadLink
from mikro_next.datalayer import DataLayer
from graphql import OperationType
from herre_next import Herre
from fakts_next import Fakts
from arkitekt_next.service_registry import (
    BaseArkitektService,
    Params,
    get_default_service_registry,
)

from arkitekt_next.base_models import Manifest

try:
    from rekuest_next.links.context import ContextLink
    from rath.links.compose import TypedComposedLink

    class ArkitektMikroNextLinkComposition(TypedComposedLink):
        fileextraction: FileExtraction = Field(default_factory=FileExtraction)
        """ A link that extracts files from the request and follows the graphql multipart request spec"""
        dicting: DictingLink = Field(default_factory=DictingLink)
        """ A link that converts basemodels to dicts"""
        upload: UploadLink
        """ A link that uploads supported data types like numpy arrays and parquet files to the datalayer"""
        auth: AuthTokenLink
        """ A link that adds the auth token to the request"""
        """ A link that splits the request into a http and a websocket request"""
        assignation: ContextLink = Field(default_factory=ContextLink)
        split: SplitLink

except ImportError:
    ArkitektMikroNextLinkComposition = MikroNextLinkComposition


class ArkitektMikroNextRath(MikroNextRath):
    link: ArkitektMikroNextLinkComposition


class ArkitektNextMikroNext(MikroNext):
    rath: ArkitektMikroNextRath
    datalayer: DataLayer


def build_relative_path(*path: str) -> str:
    return os.path.join(os.path.dirname(__file__), *path)


class MikroService(BaseArkitektService):

    def get_service_name(self):
        return "mikro"

    def build_service(
        self, fakts: Fakts, herre: Herre, params: Params, manifest: Manifest
    ):
        datalayer = FaktsDataLayer(fakts_group="datalayer", fakts=fakts)

        return ArkitektNextMikroNext(
            rath=ArkitektMikroNextRath(
                link=ArkitektMikroNextLinkComposition(
                    auth=HerreAuthLink(herre=herre),
                    upload=UploadLink(
                        datalayer=datalayer,
                    ),
                    split=SplitLink(
                        left=FaktsAIOHttpLink(
                            fakts_group="mikro", fakts=fakts, endpoint_url="FAKE_URL"
                        ),
                        right=FaktsGraphQLWSLink(
                            fakts_group="mikro", fakts=fakts, ws_endpoint_url="FAKE_URL"
                        ),
                        split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                    ),
                )
            ),
            datalayer=datalayer,
        )

    def get_requirements(self):
        return [
            Requirement(
                key="mikro",
                service="live.arkitekt.mikro",
                description="An instance of ArkitektNext Mikro to make requests to the user's data",
                optional=True,
            ),
            Requirement(
                key="datalayer",
                service="live.arkitekt.s3",
                description="An instance of ArkitektNext Datalayer to make requests to the user's data",
                optional=True,
            ),
        ]

    def get_graphql_schema(self):
        schema_graphql_path = build_relative_path("api", "schema.graphql")
        with open(schema_graphql_path) as f:
            return f.read()

    def get_turms_project(self):
        turms_prject = build_relative_path("api", "project.json")
        with open(turms_prject) as f:
            return json.loads(f.read())




get_default_service_registry().register(MikroService())