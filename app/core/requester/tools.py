
def iterate_responses(verbose_responses):

    for verbose_response in verbose_responses:
        response = verbose_response[0]
        identifies = verbose_response[1].identifiers
        id_index = 0
        for data in response:
            yield data, identifies[id_index]
            id_index += 1
