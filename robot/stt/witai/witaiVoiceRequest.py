from request import Request

class WitaiVoiceRequest(Request):
    def __init__(self, client_access_token, base_url, path, data):
        super(WitaiVoiceRequest, self).__init__(client_access_token,
                                           base_url,
                                           path,
                                           data)

    def _prepare_headers(self):
        return {
            'Content-Type': 'audio/wav',
            'Transfer-Encoding': 'chunked'
        }

    def _prepage_begin_request_data(self):
        return None

    def _prepage_end_request_data(self):
        return None
