class BclearerLoadConfigurations:
    def __init__(
        self,
        identity_hash_configuration_list: list,
        alternative_identity_hash_configuration_list: list,
        core_content_hash_configuration_list: list,
        content_hash_configuration_list: list,
        columns_in_scope_configuration_list: list,
    ) -> None:
        self.identity_hash_configuration_list = identity_hash_configuration_list

        self.alternative_identity_hash_configuration_list = alternative_identity_hash_configuration_list

        self.core_content_hash_configuration_list = core_content_hash_configuration_list

        self.content_hash_configuration_list = content_hash_configuration_list

        self.columns_in_scope_configuration_list = columns_in_scope_configuration_list
