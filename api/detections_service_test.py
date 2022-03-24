import unittest
from unittest import mock

from services.DetectionsService import DetectionsService

class DetectionsServiceTest(unittest.TestCase):
    
    def test_get_detections (self):
        client_mock = mock.Mock()
        client_mock.get_detections.return_value = self.__build_client_response()
        detections_list = DetectionsService(client_mock).get_detections(0,0)
        expected_list = self.__build_expected_list()
        self.assertEqual(detections_list, expected_list)

    def test_get_detections_by_maker (self):
        client_mock = mock.Mock()
        client_mock.get_detections_by_maker.return_value = self.__build_client_response_by_maker()
        detections_list = DetectionsService(client_mock).get_detections_by_maker()
        expected_list = self.__build_expected_list_by_maker()
        self.assertEqual(detections_list, expected_list)

    def __build_client_response(self):
        return [
            {'Year': 1995, 'Make': 'GMC', 'Model': 'Sonoma Regular Cab', 'Category': 'Pickup'}, 
            {'Year': 2005, 'Make': 'Volkswagen', 'Model': 'New Beetle', 'Category': 'Hatchback, Convertible'}, 
            {'Year': 2018, 'Make': 'Bentley', 'Model': 'Continental', 'Category': 'Convertible'}, 
            {'Year': 1995, 'Make': 'Toyota', 'Model': 'Paseo', 'Category': 'Coupe'},
            {'Year': 2019, 'Make': 'Ford', 'Model': 'Edge', 'Category': 'SUV'}, 
            {'Year': 2011, 'Make': 'MINI', 'Model': 'Countryman', 'Category': 'Hatchback'}
        ]
        
    
    def __build_expected_list(self):
        return [
            {'Year': 1995, 'Make': 'GMC', 'Model': 'Sonoma Regular Cab', 'Category': 'Pickup'}, 
            {'Year': 2005, 'Make': 'Volkswagen', 'Model': 'New Beetle', 'Category': 'Hatchback, Convertible'}, 
            {'Year': 2018, 'Make': 'Bentley', 'Model': 'Continental', 'Category': 'Convertible'}, 
            {'Year': 1995, 'Make': 'Toyota', 'Model': 'Paseo', 'Category': 'Coupe'},
            {'Year': 2019, 'Make': 'Ford', 'Model': 'Edge', 'Category': 'SUV'}, 
            {'Year': 2011, 'Make': 'MINI', 'Model': 'Countryman', 'Category': 'Hatchback'}
        ]
        
    def __build_client_response_by_maker(self):
        return [
            {
                "Detections_count": 6,
                "Make": "Freightliner"
            },
            {
                "Detections_count": 238,
                "Make": "Chevrolet"
            },
            {
                "Detections_count": 78,
                "Make": "Audi"
            }
        ]    
        
    
    def __build_expected_list_by_maker(self):
        return [
            {
                "Detections_count": 6,
                "Make": "Freightliner"
            },
            {
                "Detections_count": 238,
                "Make": "Chevrolet"
            },
            {
                "Detections_count": 78,
                "Make": "Audi"
            }
        ]    