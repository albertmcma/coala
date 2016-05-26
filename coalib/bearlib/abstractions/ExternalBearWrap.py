from functools import partial
import json
import inspect

from coalib.bears.LocalBear import LocalBear
from coala_decorators.decorators import enforce_signature
from coalib.misc.Shell import run_shell_command
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.settings.FunctionMetadata import FunctionMetadata


def _create_wrapper(klass, options):
    class ExternalBearWrapBase(LocalBear):

        @staticmethod
        def get_executable():
            """
            Returns the executable of this class.

            :return:
                The executable name.
            """
            return options["executable"]

        @classmethod
        def _get_optional_metadata(cls):
            if hasattr(cls, 'optional_args'):
                return FunctionMetadata.from_function(
                    cls.optional_args,
                    omit={"self"})
            return None

        @classmethod
        def get_metadata(cls):
            metadata = cls._get_optional_metadata()
            metadata.desc = (
                    "{}\n\nThis bear uses the {!r} executable.".format(
                        inspect.getdoc(cls), cls.get_executable()))
            return metadata

        def run(self, filename, file, **kwargs):
            print(kwargs)
            json_string = json.dumps({
                                    'filename': filename,
                                    'file': file
                                    })
            out, err = run_shell_command(self.get_executable(), json_string)
            output = json.loads(out)

            for result in output:
                yield Result.from_values(
                    origin=self,
                    message=result['message'],
                    file=filename,
                    line=result['line'])

    result_klass = type(klass.__name__, (klass, ExternalBearWrapBase), {})
    result_klass.__doc__ = klass.__doc__ if klass.__doc__ else ""
    return result_klass


@enforce_signature
def external_bear_wrap(executable: str,
                       **options):

    options["executable"] = executable

    return partial(_create_wrapper, options=options)
