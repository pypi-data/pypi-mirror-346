from pydantic import BaseModel, AnyUrl, field_validator, model_validator, Field


class BaseID(BaseModel):

    @field_validator("id", mode="before")
    @classmethod
    def slugify(cls, s):
        if isinstance(s, str):
            return s.replace(" ", "%20")
        return s

    id: AnyUrl


class LanguageString(BaseModel):
    """A language string is a dictionary with language codes as keys and
    strings as values. The language codes are ISO 2-character codes.
    Add additional languages as needed, but once more than one exists,
    logic is needed to enable all to be optional, but one must be declared."""

    @model_validator(mode="before")
    @classmethod
    def check_language_string(cls, values):
        if isinstance(values, dict) and len(values) == 0:
            raise ValueError("At least one language string must be provided.")
        return values

    en: list[str] | None = None
    fr: list[str] | None = None
    de: list[str] | None = None
    it: list[str] | None = None
    es: list[str] | None = None


class LabelValue(BaseModel):
    """Used as the value of the requiredStatement and metadata items."""

    label: LanguageString
    value: LanguageString


class Image(BaseID):
    type: str = "Image"
    width: int | None
    height: int | None


class Thumbnail(Image):
    format: str = "image/jpeg"


class Logo(Image):
    format: str = "image/png"


class Homepage(BaseID):
    type: str = "Text"
    label: LanguageString
    format: str = "text/html"
    language: list[str]


class PartOf(BaseID):
    type: str = "Collection"


class Provider(BaseID):
    type: str = "Agent"
    label: LanguageString
    homepage: list[Homepage] | None
    logo: list[Logo] | None


class Choice(BaseModel):
    type: str = "Choice"
    items: list = []


class ImageService(BaseID):
    type: str = "ImageService3"
    profile: str = "level0"


class ExternalAuthService(BaseModel):
    context: str = Field(
        default="http://iiif.io/api/auth/1/context.json", validation_alias="@context"
    )
    profile: str = "http://iiif.io/api/auth/1/external"
    label: LanguageString
    failureHeader: LanguageString
    failureDescription: LanguageString
