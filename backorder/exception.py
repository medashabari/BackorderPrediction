import sys, os

def error_message_details(error, error_detail:sys):
    """
    This Function returns the Error Mesage in details

    Parameters:
    -------------
    error = Error
    error = Error message
    """

    _, _, exc_tb = error_detail.exc_info()

    # Get the Filename that causes the Error 

    file_name = exc_tb.tb_frame.f_code.co_filename 

    # prepare the Error Message 

    error_message = error_message ="Error occured python script name [{0}] line number [{1}] error message [{2}]".format(file_name,exc_tb.tb_lineno,str(error))

    return error_message

class BackOrderException(Exception):
    """
    Returns : Error and Exception Details.
    """
    def __init__(self,error,error_detail:sys):
        self.error_message = error_message_details(error=error, error_detail=error_detail)

    def __str__(self):
        return self.error_message