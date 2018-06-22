from main import Bot


def register(site_name: str):
    """
    Registers decorated functions in the Bot.site_functions dictionary.
    Therefore, store site functions decorated with @register can be easily
    'disabled' by commenting the decorator, and new stores can be added simply
    by including the decorator without modification to other files.
    :param site_name: str, site domain, ex. 'microcenter.com'
    :return: function register_site_func
    """
    def register_site_func(site_function):
        """
        Adds site_name: site_function to Bot's dictionary
        :param site_function: function, decorated function that is to be registered
        :return: function, unchanged original function
        """
        Bot.site_functions[site_name] = site_function
        return site_function
    return register_site_func

