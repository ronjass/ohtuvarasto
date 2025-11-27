import unittest
from app import app, manager


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        manager.warehouses.clear()
        manager.next_id = 1

    def test_index_empty(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No warehouses yet', response.data)

    def test_create_page_get(self):
        response = self.app.get('/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Warehouse', response.data)

    def test_create_warehouse(self):
        response = self.app.post('/create', data={
            'name': 'Test Warehouse',
            'capacity': '100',
            'initial': '50'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)

    def test_create_warehouse_without_name(self):
        response = self.app.post('/create', data={
            'name': '',
            'capacity': '100',
            'initial': '0'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No warehouses yet', response.data)

    def test_add_content(self):
        self.app.post('/create', data={
            'name': 'Test',
            'capacity': '100',
            'initial': '0'
        })
        response = self.app.post('/add/1', data={
            'amount': '30'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'30.0', response.data)

    def test_remove_content(self):
        self.app.post('/create', data={
            'name': 'Test',
            'capacity': '100',
            'initial': '50'
        })
        response = self.app.post('/remove/1', data={
            'amount': '20'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'30.0', response.data)

    def test_edit_warehouse_get(self):
        self.app.post('/create', data={
            'name': 'Test',
            'capacity': '100',
            'initial': '0'
        })
        response = self.app.get('/edit/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Warehouse', response.data)

    def test_edit_warehouse_post(self):
        self.app.post('/create', data={
            'name': 'Test',
            'capacity': '100',
            'initial': '0'
        })
        response = self.app.post('/edit/1', data={
            'name': 'Updated Name'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Name', response.data)

    def test_delete_warehouse(self):
        self.app.post('/create', data={
            'name': 'Test',
            'capacity': '100',
            'initial': '0'
        })
        response = self.app.post('/delete/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No warehouses yet', response.data)

    def test_edit_nonexistent_warehouse(self):
        response = self.app.get('/edit/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_to_nonexistent_warehouse(self):
        response = self.app.post('/add/999', data={
            'amount': '10'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_remove_from_nonexistent_warehouse(self):
        response = self.app.post('/remove/999', data={
            'amount': '10'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_nonexistent_warehouse(self):
        response = self.app.post('/delete/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
