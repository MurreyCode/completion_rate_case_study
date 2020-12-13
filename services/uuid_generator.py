import uuid


class UuidGenerator(object):

    def __init__(self):
        pass

    @staticmethod
    def build_uuid(form_id, predictor_name):
        """
        Method that builds the uuid for the table `labels_master`. The key is composed by
        [<file_key>+<lang>+(clf_versions)]. A file_key + all classifier names used in the prediction uniquely
        identify a prediction in the `labels_master` table. We sort all classifier names to avoid ordering ambiguity.
        """
        name = f"{form_id}{predictor_name}"
        uuid_key = uuid.uuid5(uuid.NAMESPACE_X500, name)
        return uuid_key
