from rath.links.auth import AuthTokenLink
from rath.links.compose import TypedComposedLink
from rath.links.dictinglink import DictingLink
from rath.links.file import FileExtraction
from rath.links.split import SplitLink
from rekuest_next.contrib.rath.set_assignation_link import SetAssignationLink
from pydantic import Field
from mikro_next.links.upload import UploadLink


class ArkitektMikroNextLinkComposition(TypedComposedLink):
    fileextraction: FileExtraction = Field(default_factory=FileExtraction)
    dicting: DictingLink = Field(default_factory=DictingLink)
    assignation_link: SetAssignationLink = Field(default_factory=SetAssignationLink)
    upload: UploadLink = Field(default_factory=UploadLink)
    auth: AuthTokenLink
    split: SplitLink
