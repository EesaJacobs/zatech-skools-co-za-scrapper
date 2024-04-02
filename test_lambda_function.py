from unittest import main, TestCase

from lambda_function import LambdaFunction

class LambdaFunctionTestCase(TestCase):

    lambda_function: LambdaFunction = None

    def setUp(self):
        self.lambda_function = LambdaFunction()

    def test_scrapping(self):
        self.lambda_function.handle_event(event=None, context=None)


if __name__ == '__main__':
    main()
