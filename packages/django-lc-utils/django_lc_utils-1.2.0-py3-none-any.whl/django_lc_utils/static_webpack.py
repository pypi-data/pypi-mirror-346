from whitenoise.storage import CompressedManifestStaticFilesStorage


class OriginalWebpackOutput(CompressedManifestStaticFilesStorage):
    """
    Customized whitenoise storage system that ignores hashing of webpack output.

    To integrate add the following to your configuration:
    STATICFILES_STORAGE = "los.utils.static_webpack.OriginalWebpackOutput"
    """

    def hashed_name(self, name, content=None, filename=None):
        """
        Do not hash webpack output.
        """
        if name.startswith("final/"):
            if self._new_files is not None:
                self._new_files.add(self.clean_name(name))
            return name
        else:
            return super().hashed_name(name, content, filename)
