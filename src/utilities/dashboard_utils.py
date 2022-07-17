def detected_test_call(call_object):
    """
        Discovers whether or not a call should be classified as a "test".
        Returns a boolean for the discovered state.
    """
    phone_number = call_object.get("payload").get("object").get("callee").get("phone_number")
    if phone_number == "933" or phone_number == 311:
        return True
    return False

def get_calls(received_calls):
    """
        Pulls calls out of the received_calls list.
        Returns a generator object.
    """
    for call in received_calls:
        yield dict(data=call)
    received_calls.clear()  