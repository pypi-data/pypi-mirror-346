from copy import deepcopy


decorated_behavior_template = """
config => {
    if (config.request.path == '%s') {
        %s
    }
}"""

patched_template = """
        config.response.body = {response_body}
"""


def patch_some_service(imposters, expected_url, response_body):
    """
    Adds decorated behavior to mock and returns modified imposters
    """
    patched_imposters = deepcopy(imposters)
    if imposters.get('some_service'):
        patched_response = patched_template.format(response_body=response_body)
        decorated_behavior = decorated_behavior_template % (
            expected_url,
            patched_response,
        )
        patched_imposters['some_service']['stubs'][0]['responses'][0]['behaviors'] = [
            {'decorate': decorated_behavior}
        ]
    return patched_imposters
