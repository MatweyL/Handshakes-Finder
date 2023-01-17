import dataclasses
from typing import List, Iterable


def _required_list_format(params):
    return [params] if isinstance(params, (int, str, float, bool)) else params


def _build_api_call_template(qp):
    api_call_template = f"API.friends.get({{0}})"
    call_body_template = "'user_id': {}"
    if qp.fields:
        fields = f"'fields':[{','.join(repr(field) for field in qp.fields)}]"
        call_body_template = f"{call_body_template},{fields}"
    return api_call_template.format(f"{{LEFT_BRACKET}}{call_body_template}{{RIGHT_BRACKET}}")


@dataclasses.dataclass
class GetFriendsQuery:
    identifiers: Iterable[int]
    fields: List[str] | str = None
    batch_size: int = 25
    timeout_step: float = 0.35
    access_token: str = None
    api_call_template: str = None

    def __post_init__(self):
        if not isinstance(self.identifiers, list):
            self.identifiers = list(self.identifiers)
        if self.fields:
            self.fields = _required_list_format(self.fields)
        if not self.api_call_template:
            self.api_call_template = _build_api_call_template(self)

    def copy(self, identifiers):
        return GetFriendsQuery(
            identifiers=identifiers,
            fields=self.fields,
            batch_size=self.batch_size,
            timeout_step=self.timeout_step,
            access_token=self.access_token,
            api_call_template=self.api_call_template
        )

    def get_queries_params_batch(self):
        current_index = 0
        while current_index < len(self.identifiers):
            batch_size = self.batch_size if len(self.identifiers) - current_index >= self.batch_size else len(self.identifiers) - current_index
            next_index = batch_size + current_index
            yield self.copy(self.identifiers[current_index:next_index])
            current_index = next_index

    def get_query(self) -> str:
        return f"https://api.vk.com/method/execute?v=5.131&" \
               f"access_token={self.access_token}&" \
               f"code=return [{','.join(self.api_call_template.format(identifier, LEFT_BRACKET='{', RIGHT_BRACKET='}') for identifier in self.identifiers)}];"


if __name__ == "__main__":
    gfq = GetFriendsQuery(
        identifiers=[1, 2, 3]
    )
    print(gfq.get_query())
