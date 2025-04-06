"""
Fitness Class API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
from unittest import TestCase
from service.common import status  # HTTP Status Codes
from service.fitness_routes import app, reset_classes


######################################################################
#  T E S T   C A S E S
######################################################################
class FitnessClassTest(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.testing = True

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        reset_classes()
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        pass

######################################################################
#  T E S T   C A S E S
######################################################################

    def test_homepage(self):
        """ It should call the homepage """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_health_check(self):
        """ It should return healthy status """
        resp = self.app.get("/health")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_class(self):
        """ It should create a new class """
        class_name = "Yoga101"
        resp = self.app.post(f"/classes/{class_name}")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        self.assertEqual(data["class_name"], class_name)
        self.assertEqual(data["booked"], 0)

    def test_create_duplicate_class(self):
        """ It should not create a duplicate class """
        class_name = "Yoga101"
        resp = self.app.post(f"/classes/{class_name}")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.get_json()
        self.assertEqual(data["class_name"], class_name)
        self.assertEqual(data["booked"], 0)
        resp = self.app.post(f"/classes/{class_name}")
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

    def test_list_classes(self):
        """ It should list all classes """
        resp = self.app.get("/classes")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 0)
        # create a class and check it appears in the list
        self.app.post("/classes/Yoga101")
        resp = self.app.get("/classes")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 1)

    def test_read_class(self):
        """ It should read class details """
        class_name = "Yoga101"
        self.app.post(f"/classes/{class_name}")
        resp = self.app.get(f"/classes/{class_name}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["class_name"], class_name)
        self.assertEqual(data["booked"], 0)

    def test_book_class(self):
        """ It should book a spot in the class (increment booking count) """
        class_name = "Yoga101"
        resp = self.app.post(f"/classes/{class_name}")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.app.get(f"/classes/{class_name}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["class_name"], class_name)
        self.assertEqual(data["booked"], 0)
        # now book it
        resp = self.app.put(f"/classes/{class_name}/book")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["class_name"], class_name)
        self.assertEqual(data["booked"], 1)

    def test_update_missing_class(self):
        """ It should not book a missing class """
        class_name = "Yoga101"
        resp = self.app.put(f"/classes/{class_name}/book")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_class(self):
        """ It should delete a class """
        class_name = "Yoga101"
        # Create a class
        resp = self.app.post(f"/classes/{class_name}")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Delete it twice should return the same
        resp = self.app.delete(f"/classes/{class_name}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.app.delete(f"/classes/{class_name}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        # Get it to ensure it's really gone
        resp = self.app.get(f"/classes/{class_name}")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
