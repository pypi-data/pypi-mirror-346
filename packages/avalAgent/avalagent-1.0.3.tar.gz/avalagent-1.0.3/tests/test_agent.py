import unittest

from pydantic import SecretStr

from avalAgent.agent import AvalAgent

API_KEY = "aa-H6C4tHm3MmLKsiHPzMdbrBUlYMHLXORMS3hRVYoNVSDbayYe"


class TestAvalAgent(unittest.TestCase):

    def setUp(self):
        self.api_key =  (API_KEY)
        self.base_url = "https://api.avalai.ir/v1"
        self.agent = AvalAgent(api_key=self.api_key, base_url=self.base_url)
        self.assertEqual(type(  self.agent.api_key), SecretStr)
    def test_get_response_success(self, ):
        response = self.agent.get_response("answer back with only a number , no string", "say 2")


if __name__ == "__main__":
    unittest.main()
