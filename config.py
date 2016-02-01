def validate_config(document, filename):
    if 'parameters' not in document or not isinstance(document['parameters'], dict):
        raise RuntimeError('{0}: parameters node is required and must be a dictionary'.format(filename))

    parameters_dict = document['parameters']

    if 'complete_downloads_path' not in parameters_dict or not len(parameters_dict['complete_downloads_path']) > 0:
        raise RuntimeError('{0}: parameters.complete_downloads_path node is required'.format(filename))

    if 'library_path' not in parameters_dict or not len(parameters_dict['library_path']) > 0:
        raise RuntimeError('{0}: parameters.library_path node is required'.format(filename))

    if 'tvdb_api_key' not in parameters_dict or not len(parameters_dict['tvdb_api_key']) > 0:
        raise RuntimeError('{0}: parameters.tvdb_api_key node is required'.format(filename))

    if 'md5_check' in parameters_dict:
        if parameters_dict['md5_check'] is not None and not isinstance(parameters_dict['md5_check'], bool):
            raise RuntimeError('{0}: parameters.md5_check node is must be true or false')
    else:
        parameters_dict['md5_check'] = False

    if 'pushover' in parameters_dict:
        if parameters_dict['pushover'] is not None:
            if not isinstance(parameters_dict['pushover'], dict):
                raise RuntimeError('{0}: parameters.pushover node must be a dictionary'.format(filename))

            pushover_dict = parameters_dict['pushover']

            if 'token' not in pushover_dict or not len(pushover_dict['token']) > 0:
                raise RuntimeError('{0}: parameters.pushover.token node is required'.format(filename))

            if 'user_key' not in pushover_dict or not len(pushover_dict['user_key']) > 0:
                raise RuntimeError('{0}: parameters.pushover.user_key node is required'.format(filename))

            if 'device' not in pushover_dict:
                parameters_dict['pushover']['device'] = None

            if 'ignore_hd' in pushover_dict:
                if pushover_dict['ignore_hd'] is not None \
                        and not isinstance(pushover_dict['ignore_hd'], bool):
                    raise RuntimeError('{0}: parameters.pushover.ignore_hd must be true or false'.format(filename))
            else:
                parameters_dict['pushover']['ignore_hd'] = False
    else:
        parameters_dict['pushover'] = None

    if 'series_title_overrides' in parameters_dict:
        if parameters_dict['series_title_overrides'] is not None:
            if not isinstance(parameters_dict['series_title_overrides'], list):
                raise RuntimeError('{0}: parameters.series_title_overrides node must be a list'.format(filename))

            for override in parameters_dict['series_title_overrides']:
                if not isinstance(override, dict):
                    raise RuntimeError('{0}: elements of parameters.series_title_overrides node must be '
                                       'dictionaries'.format(filename))

                if 'match' not in override or 'replacement' not in override:
                    raise RuntimeError('{0}: elements of parameters.series_title_overrides node must contain both a '
                                       '"match" and "replacement" key'.format(filename))
    else:
        parameters_dict['series_title_overrides'] = None

    if 'series_season_offsets' in parameters_dict:
        if parameters_dict['series_season_offsets'] is not None:
            if not isinstance(parameters_dict['series_season_offsets'], list):
                raise RuntimeError('{0}: parameters.series_season_offsets node must be a list'.format(filename))

            for override in parameters_dict['series_season_offsets']:
                if not isinstance(override, dict):
                    raise RuntimeError('{0}: elements of parameters.series_season_offsets node must be '
                                       'dictionaries'.format(filename))

                if 'series_id' not in override \
                        or 'since_season_index' not in override \
                        or 'since_episode_index' not in override:
                    raise RuntimeError('{0}: elements of parameters.series_season_offsets node must contain '
                                       '"series_id", "since_season_index" and "since_episode_index" '
                                       'keys'.format(filename))
    else:
        parameters_dict['series_season_offsets'] = None

    return parameters_dict
