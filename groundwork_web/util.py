import re
import copy


def get_routes(flask_app, url, context):
    """
    Filters all existing route rules of a flask app by a given pattern.
    Returns a dictionary of rules, which match the pattern

    If several rules exist for the same url, the rules are merged into a single rule.

    :param context: context for which the routes git registered
    :param flask_app: flask application object
    :param url: regular expression pattern of route (without pattern part!)
    :return: dictionary of found rules
    """
    url_prefix = context.url_prefix

    rules = flask_app.url_map.iter_rules()

    found_rules = []

    pattern = re.compile('/'.join([url_prefix, url]).replace('/', r'\/'))

    # Find needed route rules
    for rule in rules:
        rule_url = rule.rule
        result = pattern.search(rule_url)

        if result is not None:
            found_rules.append(rule)

    # Rules can exist multiple time for the same url inside flask
    # Therefore we need to combine at least the methods of identical rules
    merged_rules = {}
    for found_rule in found_rules:
        found_rule_name = found_rule.rule
        if found_rule_name not in merged_rules.keys():
            # We need to create a coy of the rule, as we manipulate it later
            # for our needs (e.g. merging methods).
            # And this must not be done on the original routes/rules, which would affect
            # the flask app behavior.
            merged_rules[found_rule_name] = copy.copy(found_rule)
        else:
            current_methods = list(found_rule.methods)
            existing_methods = list(merged_rules[found_rule_name].methods)
            new_methods = [i for i in current_methods if i not in existing_methods]
            merged_rules[found_rule_name].methods = existing_methods + new_methods

    # Create needed list and element structure
    routes = []
    for key, rule in merged_rules.items():
        route = {
            'url': rule.rule.replace(url_prefix, '', 1),
            'methods': rule.methods,
            'name': rule.rule.replace('/', '', 1).replace('/', '_').rstrip('_'),
            'context': context.name
        }

        parameters = re.findall('<([a-zA-Z0-9_]*)>', rule.rule)
        route_params = {}
        for param in parameters:
            route_params[param] = {
                'name': param,
                'type': None,
                'description': None
            }

        route['parameters'] = route_params

        routes.append(route)

    return routes
