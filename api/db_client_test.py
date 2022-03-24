import unittest
from unittest import mock

from clients.DbClient import DbClient

class DbClientTest(unittest.TestCase):
    
    def test_get_detections (self):
        db_mock = mock.Mock()
        db_mock.detections.find().skip().limit.return_value = self.__build_db_response()

        logger_mock = mock.Mock()
        
        detections_list = DbClient(db_mock,logger_mock).get_detections(0,0)
        expected_list = self.__build_expected_list()
        self.assertEqual(detections_list, expected_list)

    def test_get_detections_by_maker (self):
        db_mock = mock.Mock()
        db_mock.detections.aggregate.return_value = self.__build_db_aggregate_response()
                
        logger_mock = mock.Mock()
        
        detections_list = DbClient(db_mock,logger_mock).get_detections_by_maker()
        expected_list = self.__build_expected_by_maker_list()
        self.assertEqual(detections_list, expected_list)
        
    def test_get_user (self):
        db_mock = mock.Mock()
        db_mock.users.find.return_value = self.__build_db_users_response()
        
        logger_mock = mock.Mock()
        
        user_list = DbClient(db_mock,logger_mock).get_user("mocked_user_1","mocked_password_1")
        expected_user = self.__build_expected_user()
        self.assertEqual(user_list,expected_user)
        
    def test_get_user_list (self):
        db_mock = mock.Mock()
        db_mock.users.find.return_value = self.__build_db_user_list_response()
        
        logger_mock = mock.Mock()
        
        user_list = DbClient(db_mock,logger_mock).get_user_list()
        expected_user = self.__build_expected_user_list()
        self.assertEqual(user_list,expected_user)    
             
    def __build_db_response(self):
        return [
            {'Year': 1995, 'Make': 'GMC', 'Model': 'Sonoma Regular Cab', 'Category': 'Pickup' , '_id' : '1'}, 
            {'Year': 2005, 'Make': 'Volkswagen', 'Model': 'New Beetle', 'Category': 'Hatchback, Convertible', '_id' : '2'}, 
            {'Year': 2018, 'Make': 'Bentley', 'Model': 'Continental', 'Category': 'Convertible', '_id' : '3'}, 
            {'Year': 1995, 'Make': 'Toyota', 'Model': 'Paseo', 'Category': 'Coupe', '_id' : '4'},
            {'Year': 2019, 'Make': 'Ford', 'Model': 'Edge', 'Category': 'SUV', '_id' : '5'}, 
            {'Year': 2011, 'Make': 'MINI', 'Model': 'Countryman', 'Category': 'Hatchback', '_id' : '6'}
        ]

    def __build_db_aggregate_response(self):
        return[
            {
                "Detections_count": 6,
                "_id": "Freightliner"
            },
            {
                "Detections_count": 238,
                "_id": "Chevrolet"
            },
            {
                "Detections_count": 78,
                "_id": "Audi"
            }
        ]    

    def __build_db_users_response(self):
        return[
            {
                "_id": 1,
                "user_id": "mocked_user_1",
                "password": "mocked_password_1"
            }
        ]    

    def __build_db_user_list_response(self):
        return[
            {
                "_id": 1,
                "user_id": "mocked_user_1",
            },
                        {
                "_id": 2,
                "user_id": "mocked_user_2",
            },
            {
                "_id": 3,
                "user_id": "mocked_user_3",
            }
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
        
    def __build_expected_by_maker_list(self):
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
        
    def __build_expected_user(self):
        return {
                "user_id" : "mocked_user_1",
                "password" : "mocked_password_1"
        }
    
    def __build_expected_user_list(self):
        return [
            {
                "user_id" : "mocked_user_1",
            },
            {
                "user_id" : "mocked_user_2",
            },
            {
                "user_id" : "mocked_user_3",
            }
        ]
    