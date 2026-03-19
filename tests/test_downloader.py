import unittest
from unittest import mock 
from click.testing import CliRunner
from app.cli import run_cli
from app.objects.date import Date
from app.objects.image_downloader import ImageDownloader


class MissingInputTests(unittest.TestCase):
    runner = CliRunner()

    def test_only_resolution_input(self):
        test_cases = [' -r 64x64', '-r 1280x1024', '--resolution 1920x1080']
        for x in test_cases:
            with self.subTest(x=x):
                result = self.runner.invoke(run_cli, x.split(), input ='1')
                print(result)
                self.assertIn('Error', result.output)
                self.assertIn("Missing option '-m' ", result.output)
                self.assertEqual(2, result.exit_code)


if __name__ == '__main__':
    unittest.main()

