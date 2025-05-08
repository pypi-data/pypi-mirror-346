from yta_validation.parameter import ParameterValidator
from datetime import datetime


class Date:
    """
    Class to encapsulate and simplify the way we handle dates
    and datetimes.
    """

    @staticmethod
    def get_rfc_datetime(
        year: int = 1900,
        month: int = 1,
        day: int = 1,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0
    ) -> str:
        """
        Receives a date based on provided parameters and turns it into
        a RFC datetime, returning it like '2025-05-08T06:09:00Z'.

        If you don't provide the 'microsecond' parameter, the string 
        will be like this '2025-05-08T06:09:00Z', but if you provide it,
        the string will be like this '2025-05-08T06:09:00.123456Z'.
        """
        return f'{datetime(year, month, day, hour, minute, second, microsecond).isoformat()}Z'

    @staticmethod
    def seconds_to_hh_mm_ss(
        seconds: int
    ) -> str:
        """
        Turn the provided amount of 'seconds' to a time
        in the format HH:MM:SS.
        """
        ParameterValidator.validate_positive_number('seconds', seconds, do_include_zero = True)
        
        hh = seconds // 3600
        mm = (seconds % 3600) // 60 
        ss = seconds % 60

        return f'{hh:02}:{mm:02}:{ss:02}'

    # TODO: Make this more configurable
    @staticmethod
    def current_datetime(
    ) -> str:
        """
        Return the current time moment, as a string, in
        the 'DD/MM/YYYY HH:MM:SS' format.
        """
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# TODO: Build more methods to simplify our work