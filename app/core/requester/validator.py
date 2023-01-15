from typing import List

from app.core.requester.data import GetFriendsQuery


def validate(responses: List[tuple]):
    errors = {}
    valid_data = []
    for verbose_response in responses:
        response = verbose_response[0]
        query_params: GetFriendsQuery = verbose_response[1]

        if not response.get('execute_errors') and not response.get('error'):  # if there is no errors - all response is valid
            valid_data.append((response['response'], query_params))

        elif response.get('response'):  # there is some errored api calls
            api_calls_i = 0
            identifiers_to_remove = []
            valid_api_calls = []

            execute_errors_i = 0

            for data in response['response']:
                if data:
                    valid_api_calls.append(data)
                else:

                    identifiers_to_remove.append(query_params.identifiers[api_calls_i])
                    error_code = response['execute_errors'][execute_errors_i]['error_code']
                    if not errors.get(error_code):
                        errors[error_code] = []
                    errors[error_code].append(query_params.identifiers[api_calls_i])
                    execute_errors_i += 1
                api_calls_i += 1
            for identifier_to_remove in identifiers_to_remove:
                query_params.identifiers.remove(identifier_to_remove)
            valid_data.append((valid_api_calls, query_params))

        else:  # got 'error' - all query failed
            # pprint.pprint(response)
            error_code = response['error']['error_code']
            if not errors.get(error_code):
                errors[error_code] = []
            errors[error_code].append(query_params)
    return valid_data, errors


