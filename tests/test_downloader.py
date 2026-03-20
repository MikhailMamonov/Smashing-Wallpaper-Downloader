import unittest
from unittest import mock 
import requests
from click.testing import CliRunner
from app.cli import run_cli
from constants.api import *
from app.objects.date import Date
from app.objects.image_downloader import ImageDownloader


class MissingInputTests(unittest.TestCase):
    runner = CliRunner()

    def test_only_resolution_input(self):
        test_cases = [' -r 64x64', '-r 1280x1024', '--resolution 1920x1080']
        for x in test_cases:
            with self.subTest(x=x):
                result = self.runner.invoke(run_cli, x.split(), input ='1')
                self.assertIn('Error', result.output)
                self.assertIn("Missing option '-m' ", result.output)
                self.assertEqual(2, result.exit_code)

    def test_only_my_input(self):
        test_cases = ['-m 052018', '-m 52018', '--my 052018']
        for x in test_cases:
            with self.subTest(x=x):
                result = self.runner.invoke(run_cli, x.split(), input='1')
                self.assertIn('Error', result.output)
                self.assertIn("Missing option '-r' / '--resolution'", result.output)
                self.assertEqual(2, result.exit_code)

class InvalidInputTests(unittest.TestCase):
    runner = CliRunner()

    def test_invalid_resolution_input(self):
        test_cases = [
            '-r 64x64 -m 052019',
            '-r abcde -m  052019',
            '-r 1920x1080x -m 052019',
            '-r 19820x1080 -m 052019'
        ]
        for x in test_cases:
            with self.subTest(x=x):
                result = self.runner.invoke(run_cli, x.split(), input='2')
                self.assertIn('Resolution value is not valid', result.output)
                self.assertEqual(0, result.exit_code)
    
    def test_invalid_month_input(self):
        test_cases = [
            '-r 1280x1024 --my 002019',
            '-r 1280x1024 --my 132019',
            '-r 1280x1024 --my df2019',
        ]
        for x in test_cases:
            with self.subTest(x=x):
                result = self.runner.invoke(run_cli, x.split(), input='2')
                self.assertIn('Month value is not valid', result.output)
                self.assertEqual(0, result.exit_code)
        
    
    def test_invalid_year_input(self):
        test_cases = [
            '-r 1280x1024 --my 0512',
            '-r 1280x1024 --my 052056',
            '-r 1280x1024 --my 05abcde',
        ]
        for x in test_cases:
            with self.subTest(x=x):
                result = self.runner.invoke(run_cli, x.split(), input='2')
                self.assertIn('Year value is not valid', result.output)
                self.assertEqual(0, result.exit_code)
    
class ValidInputTests(unittest.TestCase):
    runner = CliRunner()

    @mock.patch.object(ImageDownloader, 'get_url')
    def test_get_url_valid_input(self, mock_get_url):
        test_cases = [
            '-r 1280x1024 -m 012015',
            '-r 1280x1024 -m 122019',
            '-r 1920x1080 -m 122019',
            '-r 1920x1080 -m 012015',
        ]
        for x in test_cases:
            with self.subTest(x=x):
                result = self.runner.invoke(run_cli, x.split(), input='2')
                _,res,_, my= x.split()
                date = Date(my)

                # ImageDownloader.get_url.called_with(
                mock_get_url.assert_called_with(
                    URL, 
                    date.year,
                    date.month_number,
                    date.month_name, 
                )
                
                self.assertIn('Trying to establish connection...', result.output)

    @mock.patch.object(ImageDownloader, 'fetch_content')
    def test_fetch_valid_input(self, mock_fetch):
        base_resolution = '640x480'
        test_cases = [
            '-r 1280x1024 -m 012015',
            '-r 1280x1024 -m 122019',
            '-r 1920x1080 -m 122019',
            '-r 1920x1080 -m 012015',
        ]    
        for x in test_cases:
            with self.subTest(x=x):
                result = self.runner.invoke(run_cli, x.split(), input='2')
                _,res,_, my= x.split()
                date = Date(my)

                new_url = ImageDownloader(base_resolution).get_url(
                     URL, 
                    date.year,
                    date.month_number,
                    date.month_name, 
                )
                # ImageDownloader.fetch_content.called_with(
                mock_fetch.assert_called_with(
                    new_url, 
                    timeout=5
                )
class DateClassTests(unittest.TestCase):
    def test_month_valid_value(self):
        test_cases = [
            ('052015', 5, 'May'),
            ('122000', 12, 'December'),
            ('012012', 1, 'January'),
        ]
        for value, exp_number, exp_name in test_cases:
            with self.subTest(x=value):
                date = Date(value)
                self.assertEqual(date.validate_month_input(value[:2]), value[:2])
                self.assertEqual(date.month_number, exp_number)
                self.assertEqual(date.month_name, exp_name)
    
    def test_year_valid_value(self):
        test_cases = [
            ('052015', 2015 ),
            ('122000', 2000),
            ('012012', 2012),
        ]
        for value, year in test_cases:
            with self.subTest(x=value):
                date = Date(value)
                self.assertEqual(date.validate_year_input(value[2:]), year)
                self.assertEqual(date.year, year)     

    def test_invalid_value(self):
        test_cases = ['  2015', '132015', 'ab2015', '121999', '01200g']
        for value in test_cases:
            with self.subTest(x=value):
                self.assertRaises(ValueError, Date, value) 

class ImageDownloaderClassTests(unittest.TestCase):
    base_resolution = '640x480'

    def test_resolution_valid_value(self):
        test_cases = ['640x480', '1280x1024', '1920x1080']
        for value in test_cases:
            with self.subTest(x=value):
                image_downloader = ImageDownloader(value)
                self.assertEqual(
                    image_downloader.validate_input(value), value)
                self.assertEqual(image_downloader.resolution, value)
    
    def test_resolution_invalid_value(self):
        test_cases = [
            '',
            '64x48', 
            '1280x1024-40', 
            '1920xx1080', 
            '1920x1080x1080'
        ]
        for value in test_cases:
            with self.subTest(x=value):
                self.assertRaises(ValueError, ImageDownloader, value)
    
    def test_getting_url(self):
        test_cases = [
           ( 
               ('abc.com', 2015, 5, 'May'), 
            'https://abc.com/2015/04/desktop-wallpaper-calendars-may-2015/'
            ),
           ( 
               ('abc.com', 2013, 11, 'November'), 
            'https://abc.com/2013/10/desktop-wallpaper-calendars-november-2013/'
            ),
           ( 
               ('abc.com', 2019, 1, 'January'), 
            'https://abc.com/2018/12/desktop-wallpaper-calendars-january-2019/'
            ),
        ]
        image_downloader = ImageDownloader(self.base_resolution)
        for x, exp_output in test_cases:
            with self.subTest(x=x):
                self.assertEqual(image_downloader.get_url(*x), exp_output)

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, content, status_code):
                self.content = content
                self.status_code = status_code
            
            def raise_for_status(self):
                if self.status_code != 200:
                    raise requests.HTTPError()
                return self.status_code
        if args[0] == 'http://someurl.com/test':
            return MockResponse('some_data', 200)
        if args[0] == 'http://someotherurl.com/test':
            return MockResponse('other_data', 200)
        if args[0] == 'http://nonexistenturl.com/test':
            return MockResponse(None, 404)
        if args[0] == 'http://unabletoconnecturl.com/test':
            raise requests.Timeout()
        raise requests.RequestException()
    
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_fetching_content(self, mock_get):
        image_downloader = ImageDownloader(self.base_resolution)

        resp = image_downloader.fetch_content('http://someurl.com/test')
        self.assertEqual(resp, 'some_data')

        resp = image_downloader.fetch_content('http://someotherurl.com/test')
        self.assertEqual(resp, 'other_data')

        with self.assertRaises(Exception) as err:
            image_downloader.fetch_content('http://nonexistenturl.com/test')
        self.assertIn('Error', err.exception.args[0])

        with self.assertRaises(Exception) as err:
            image_downloader.fetch_content('http://unabletoconnecturl.com/test')
        self.assertIn('Connection time out', err.exception.args[0])

        with self.assertRaises(Exception) as err:
            image_downloader.fetch_content('http://otherunknownurl.com/test')
        self.assertIn('Unable to establish connection', err.exception.args[0])
    
    def test_getting_image_links(self):
        response_content = '''
        <a href=http://files.com/wallpapers/cal/may-19-hello-spring-cal-800x480.png \
        title="Hello Spring! - 800x480">800x480</a>,<a href=http://files.com/wallpapers/nocal/may-19-hello-spring-nocal-800x480.png
        title="Hello Spring! - 800x480">800x480</a>,\
        <a href=http://files.com/wallpapers/nocal/may-19-hello-spring-nocal-1024x768.png \
        title="Hello Spring! - 1024x768">1024x768</a>'''
        test_cases= [
            ('800x480',
            [
                'http://files.com/wallpapers/cal/may-19-hello-spring-cal-800x480.png',
                'http://files.com/wallpapers/nocal/may-19-hello-spring-nocal-800x480.png'
            ]),
            (
                '1024x768', 
                ['http://files.com/wallpapers/nocal/may-19-hello-spring-nocal-1024x768.png']
            )
        ] 

        for resolution, exp_output in test_cases:
            with self.subTest(x=resolution):
                self.assertEqual(ImageDownloader(resolution).get_image_links(response_content), 
                                 exp_output
                                )
    
    @mock.patch('app.objects.image_downloader.os')
    def test_creating_directory(self, mock_os):
        base_directory,month,year = '/', 'may',2015
        directory_name = 'Smashing_wallpaper_{0}_{1}'.format(month, year)

        ImageDownloader(self.base_resolution).create_directory(
            base_directory, month, year)
        
        mock_os.makedirs.assert_called_with(
            mock_os.path.join(base_directory, directory_name), 
            exist_ok=True
        )
    
        





if __name__ == '__main__':
    unittest.main()

