"""
Test suite for Search Logs and Symptom Checker APIs
Tests all endpoints and functionality
"""
import pytest
from uuid import uuid4, UUID
from datetime import datetime
from decimal import Decimal
from fastapi.testclient import TestClient
from app.main import app

# These imports would work with your actual app structure
# from app.models import Base, User, SearchLog, SymptomChecker
# from app.database import get_db

# For now, this is a template test file


class TestSearchLogsAPI:
    """Test cases for Search Logs API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Setup test client"""
        with TestClient(app) as client:
            yield client
    
    @pytest.fixture
    def test_user_id(self):
        """Valid test user ID"""
        return str(uuid4())
    
    @pytest.fixture
    def test_search_log_data(self, test_user_id):
        """Sample search log data"""
        return {
            "user_id": test_user_id,
            "query": "symptoms of diabetes",
            "results_count": 45
        }
    
    # ====================================================================
    # CREATE SEARCH LOG TESTS
    # ====================================================================
    
    def test_create_search_log_success(self, client, test_search_log_data):
        """Test successfully creating a search log"""
        response = client.post("/api/search-logs", json=test_search_log_data)
        assert response.status_code == 201
        data = response.json()
        assert data["query"] == test_search_log_data["query"]
        assert data["results_count"] == test_search_log_data["results_count"]
        assert data["user_id"] == test_search_log_data["user_id"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_search_log_nonexistent_user(self, client):
        """Test creating search log with nonexistent user"""
        data = {
            "user_id": str(uuid4()),
            "query": "test query",
            "results_count": 10
        }
        response = client.post("/api/search-logs", json=data)
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
    
    def test_create_search_log_missing_fields(self, client, test_user_id):
        """Test creating search log with missing required fields"""
        data = {
            "user_id": test_user_id
            # Missing query
        }
        response = client.post("/api/search-logs", json=data)
        assert response.status_code == 422
    
    def test_create_search_log_default_results(self, client, test_user_id):
        """Test creating search log with default results_count"""
        data = {
            "user_id": test_user_id,
            "query": "test query"
            # results_count should default to 0
        }
        response = client.post("/api/search-logs", json=data)
        assert response.status_code == 201
        assert response.json()["results_count"] == 0
    
    # ====================================================================
    # LIST SEARCH LOGS TESTS
    # ====================================================================
    
    def test_get_all_search_logs_empty(self, client):
        """Test getting search logs when none exist"""
        response = client.get("/api/search-logs")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_with_pagination(self, client, test_search_log_data):
        """Test pagination with skip and limit"""
        # Create multiple logs
        for i in range(15):
            data = test_search_log_data.copy()
            data["query"] = f"query {i}"
            client.post("/api/search-logs", json=data)
        
        # Test pagination
        response = client.get("/api/search-logs?skip=0&limit=5")
        assert response.status_code == 200
        assert len(response.json()) == 5
        
        response = client.get("/api/search-logs?skip=5&limit=5")
        assert len(response.json()) == 5
    
    def test_get_logs_filter_by_user(self, client, test_user_id):
        """Test filtering logs by user_id"""
        other_user = str(uuid4())
        
        # Create logs for user 1
        for i in range(2):
            client.post("/api/search-logs", json={
                "user_id": test_user_id,
                "query": f"user1 query {i}",
                "results_count": 10
            })
        
        # Create logs for user 2
        for i in range(3):
            client.post("/api/search-logs", json={
                "user_id": other_user,
                "query": f"user2 query {i}",
                "results_count": 20
            })
        
        # Filter by user 1
        response = client.get(f"/api/search-logs?user_id={test_user_id}")
        assert response.status_code == 200
        logs = response.json()
        assert len(logs) == 2
        assert all(log["user_id"] == test_user_id for log in logs)
    
    # ====================================================================
    # GET SINGLE SEARCH LOG TESTS
    # ====================================================================
    
    def test_get_single_search_log(self, client, test_search_log_data):
        """Test getting a single search log by ID"""
        create_response = client.post("/api/search-logs", json=test_search_log_data)
        log_id = create_response.json()["id"]
        
        response = client.get(f"/api/search-logs/{log_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == log_id
        assert data["query"] == test_search_log_data["query"]
    
    def test_get_nonexistent_search_log(self, client):
        """Test getting search log that doesn't exist"""
        fake_id = str(uuid4())
        response = client.get(f"/api/search-logs/{fake_id}")
        assert response.status_code == 404
    
    # ====================================================================
    # GET USER SEARCH LOGS TESTS
    # ====================================================================
    
    def test_get_user_search_logs(self, client, test_user_id, test_search_log_data):
        """Test getting all logs for a user"""
        for i in range(3):
            data = test_search_log_data.copy()
            data["query"] = f"query {i}"
            client.post("/api/search-logs", json=data)
        
        response = client.get(f"/api/search-logs/user/{test_user_id}")
        assert response.status_code == 200
        logs = response.json()
        assert len(logs) == 3
        assert all(log["user_id"] == test_user_id for log in logs)
    
    def test_get_user_logs_nonexistent_user(self, client):
        """Test getting logs for nonexistent user"""
        fake_user_id = str(uuid4())
        response = client.get(f"/api/search-logs/user/{fake_user_id}")
        assert response.status_code == 404
    
    # ====================================================================
    # UPDATE SEARCH LOG TESTS
    # ====================================================================
    
    def test_update_search_log_results_count(self, client, test_search_log_data):
        """Test updating search log results count"""
        create_response = client.post("/api/search-logs", json=test_search_log_data)
        log_id = create_response.json()["id"]
        
        update_data = {"results_count": 100}
        response = client.put(f"/api/search-logs/{log_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["results_count"] == 100
    
    def test_update_nonexistent_log(self, client):
        """Test updating log that doesn't exist"""
        fake_id = str(uuid4())
        response = client.put(
            f"/api/search-logs/{fake_id}",
            json={"results_count": 50}
        )
        assert response.status_code == 404
    
    # ====================================================================
    # DELETE SEARCH LOG TESTS
    # ====================================================================
    
    def test_delete_search_log(self, client, test_search_log_data):
        """Test deleting a search log"""
        create_response = client.post("/api/search-logs", json=test_search_log_data)
        log_id = create_response.json()["id"]
        
        response = client.delete(f"/api/search-logs/{log_id}")
        assert response.status_code == 204
        
        # Verify deleted
        response = client.get(f"/api/search-logs/{log_id}")
        assert response.status_code == 404
    
    def test_delete_user_search_logs(self, client, test_user_id, test_search_log_data):
        """Test deleting all logs for a user"""
        for i in range(3):
            data = test_search_log_data.copy()
            data["query"] = f"query {i}"
            client.post("/api/search-logs", json=data)
        
        response = client.delete(f"/api/search-logs/user/{test_user_id}/all")
        assert response.status_code == 204
        
        # Verify all deleted
        response = client.get(f"/api/search-logs/user/{test_user_id}")
        assert response.json() == []


class TestSymptomCheckerAPI:
    """Test cases for Symptom Checker API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Setup test client"""
        with TestClient(app) as client:
            yield client
    
    @pytest.fixture
    def test_symptom_data(self):
        """Sample symptom checker data"""
        return {
            "symptoms": "cough, fever, body ache",
            "suggested_disease": "Common Cold or Influenza",
            "confidence_score": 0.85
        }
    
    # ====================================================================
    # CREATE SYMPTOM CHECKER TESTS
    # ====================================================================
    
    def test_create_symptom_checker_success(self, client, test_symptom_data):
        """Test successfully creating a symptom checker record"""
        response = client.post("/api/symptom-checkers", json=test_symptom_data)
        assert response.status_code == 201
        data = response.json()
        assert data["symptoms"] == test_symptom_data["symptoms"]
        assert data["suggested_disease"] == test_symptom_data["suggested_disease"]
        assert float(data["confidence_score"]) == test_symptom_data["confidence_score"]
        assert "id" in data
    
    def test_create_with_invalid_confidence_too_high(self, client):
        """Test creating with confidence > 1.0"""
        data = {
            "symptoms": "test",
            "suggested_disease": "test",
            "confidence_score": 1.5
        }
        response = client.post("/api/symptom-checkers", json=data)
        assert response.status_code == 422
        assert "Confidence score must be between" in response.json()["detail"]
    
    def test_create_with_invalid_confidence_negative(self, client):
        """Test creating with negative confidence"""
        data = {
            "symptoms": "test",
            "suggested_disease": "test",
            "confidence_score": -0.5
        }
        response = client.post("/api/symptom-checkers", json=data)
        assert response.status_code == 422
    
    def test_create_with_valid_confidence_boundaries(self, client):
        """Test creating with boundary confidence values"""
        # Test 0.0
        data = {
            "symptoms": "test0",
            "suggested_disease": "disease",
            "confidence_score": 0.0
        }
        response = client.post("/api/symptom-checkers", json=data)
        assert response.status_code == 201
        
        # Test 1.0
        data = {
            "symptoms": "test1",
            "suggested_disease": "disease",
            "confidence_score": 1.0
        }
        response = client.post("/api/symptom-checkers", json=data)
        assert response.status_code == 201
    
    # ====================================================================
    # LIST SYMPTOM CHECKERS TESTS
    # ====================================================================
    
    def test_get_all_symptom_checkers_empty(self, client):
        """Test getting checkers when none exist"""
        response = client.get("/api/symptom-checkers")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_with_pagination(self, client, test_symptom_data):
        """Test pagination"""
        for i in range(15):
            data = test_symptom_data.copy()
            data["symptoms"] = f"symptom {i}"
            client.post("/api/symptom-checkers", json=data)
        
        response = client.get("/api/symptom-checkers?skip=0&limit=5")
        assert len(response.json()) == 5
    
    def test_filter_by_confidence(self, client):
        """Test filtering by minimum confidence"""
        # Create records with different confidence levels
        confidences = [0.50, 0.70, 0.80, 0.90, 0.95]
        for i, conf in enumerate(confidences):
            data = {
                "symptoms": f"symptom {i}",
                "suggested_disease": "disease",
                "confidence_score": conf
            }
            client.post("/api/symptom-checkers", json=data)
        
        # Filter by min_confidence
        response = client.get("/api/symptom-checkers?min_confidence=0.80")
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 3  # 0.80, 0.90, 0.95
        assert all(float(r["confidence_score"]) >= 0.80 for r in results)
    
    def test_filter_invalid_confidence(self, client):
        """Test filtering with invalid confidence"""
        response = client.get("/api/symptom-checkers?min_confidence=1.5")
        assert response.status_code == 422
    
    # ====================================================================
    # GET SINGLE SYMPTOM CHECKER TESTS
    # ====================================================================
    
    def test_get_single_symptom_checker(self, client, test_symptom_data):
        """Test getting a single record by ID"""
        create_response = client.post("/api/symptom-checkers", json=test_symptom_data)
        record_id = create_response.json()["id"]
        
        response = client.get(f"/api/symptom-checkers/{record_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == record_id
    
    def test_get_nonexistent_record(self, client):
        """Test getting record that doesn't exist"""
        fake_id = str(uuid4())
        response = client.get(f"/api/symptom-checkers/{fake_id}")
        assert response.status_code == 404
    
    # ====================================================================
    # SEARCH BY SYMPTOMS TESTS
    # ====================================================================
    
    def test_search_by_symptoms_exact_match(self, client):
        """Test searching by symptoms with exact keyword"""
        data = {
            "symptoms": "headache, fever, sore throat",
            "suggested_disease": "Strep Throat",
            "confidence_score": 0.88
        }
        client.post("/api/symptom-checkers", json=data)
        
        response = client.get("/api/symptom-checkers/search/by-symptoms?symptoms=headache")
        assert response.status_code == 200
        results = response.json()
        assert len(results) > 0
        assert "headache" in results[0]["symptoms"].lower()
    
    def test_search_by_symptoms_case_insensitive(self, client):
        """Test case-insensitive symptom search"""
        data = {
            "symptoms": "Chest Pain",
            "suggested_disease": "Cardiac Issue",
            "confidence_score": 0.90
        }
        client.post("/api/symptom-checkers", json=data)
        
        # Search with lowercase
        response = client.get("/api/symptom-checkers/search/by-symptoms?symptoms=chest")
        assert response.status_code == 200
        assert len(response.json()) > 0
    
    def test_search_by_symptoms_not_found(self, client):
        """Test searching for non-existent symptoms"""
        response = client.get("/api/symptom-checkers/search/by-symptoms?symptoms=nonexistent")
        assert response.status_code == 200
        assert response.json() == []
    
    # ====================================================================
    # SEARCH BY DISEASE TESTS
    # ====================================================================
    
    def test_search_by_disease(self, client):
        """Test searching by disease name"""
        data = {
            "symptoms": "chest pain, shortness of breath",
            "suggested_disease": "Myocardial Infarction (Heart Attack)",
            "confidence_score": 0.95
        }
        client.post("/api/symptom-checkers", json=data)
        
        response = client.get("/api/symptom-checkers/search/by-disease?disease=infarction")
        assert response.status_code == 200
        results = response.json()
        assert len(results) > 0
    
    def test_search_by_disease_case_insensitive(self, client):
        """Test case-insensitive disease search"""
        data = {
            "symptoms": "persistent cough",
            "suggested_disease": "Tuberculosis",
            "confidence_score": 0.88
        }
        client.post("/api/symptom-checkers", json=data)
        
        response = client.get("/api/symptom-checkers/search/by-disease?disease=tubercul")
        assert response.status_code == 200
        assert len(response.json()) > 0
    
    # ====================================================================
    # UPDATE SYMPTOM CHECKER TESTS
    # ====================================================================
    
    def test_update_confidence_score(self, client, test_symptom_data):
        """Test updating confidence score"""
        create_response = client.post("/api/symptom-checkers", json=test_symptom_data)
        record_id = create_response.json()["id"]
        
        update_data = {"confidence_score": 0.92}
        response = client.put(f"/api/symptom-checkers/{record_id}", json=update_data)
        assert response.status_code == 200
        assert float(response.json()["confidence_score"]) == 0.92
    
    def test_update_with_invalid_confidence(self, client, test_symptom_data):
        """Test updating with invalid confidence"""
        create_response = client.post("/api/symptom-checkers", json=test_symptom_data)
        record_id = create_response.json()["id"]
        
        update_data = {"confidence_score": 1.5}
        response = client.put(f"/api/symptom-checkers/{record_id}", json=update_data)
        assert response.status_code == 422
    
    def test_update_all_fields(self, client, test_symptom_data):
        """Test updating all fields"""
        create_response = client.post("/api/symptom-checkers", json=test_symptom_data)
        record_id = create_response.json()["id"]
        
        update_data = {
            "symptoms": "new symptoms",
            "suggested_disease": "new disease",
            "confidence_score": 0.75
        }
        response = client.put(f"/api/symptom-checkers/{record_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["symptoms"] == "new symptoms"
        assert data["suggested_disease"] == "new disease"
    
    # ====================================================================
    # DELETE SYMPTOM CHECKER TESTS
    # ====================================================================
    
    def test_delete_symptom_checker(self, client, test_symptom_data):
        """Test deleting a record"""
        create_response = client.post("/api/symptom-checkers", json=test_symptom_data)
        record_id = create_response.json()["id"]
        
        response = client.delete(f"/api/symptom-checkers/{record_id}")
        assert response.status_code == 204
        
        # Verify deleted
        response = client.get(f"/api/symptom-checkers/{record_id}")
        assert response.status_code == 404
    
    # ====================================================================
    # COMBINED WORKFLOW TESTS
    # ====================================================================
    
    def test_search_logs_workflow(self, client, test_user_id):
        """Test complete search logs workflow"""
        # 1. Create
        create_data = {
            "user_id": test_user_id,
            "query": "symptoms of diabetes",
            "results_count": 50
        }
        create_response = client.post("/api/search-logs", json=create_data)
        assert create_response.status_code == 201
        log_id = create_response.json()["id"]
        
        # 2. Retrieve
        get_response = client.get(f"/api/search-logs/{log_id}")
        assert get_response.status_code == 200
        
        # 3. Update
        update_response = client.put(
            f"/api/search-logs/{log_id}",
            json={"results_count": 75}
        )
        assert update_response.status_code == 200
        assert update_response.json()["results_count"] == 75
        
        # 4. Delete
        delete_response = client.delete(f"/api/search-logs/{log_id}")
        assert delete_response.status_code == 204
    
    def test_symptom_checker_workflow(self, client):
        """Test complete symptom checker workflow"""
        # 1. Create
        create_data = {
            "symptoms": "fever, chills",
            "suggested_disease": "Malaria or Dengue",
            "confidence_score": 0.78
        }
        create_response = client.post("/api/symptom-checkers", json=create_data)
        assert create_response.status_code == 201
        record_id = create_response.json()["id"]
        
        # 2. Get
        get_response = client.get(f"/api/symptom-checkers/{record_id}")
        assert get_response.status_code == 200
        
        # 3. Search
        search_response = client.get("/api/symptom-checkers/search/by-symptoms?symptoms=fever")
        assert len(search_response.json()) > 0
        
        # 4. Update
        update_response = client.put(
            f"/api/symptom-checkers/{record_id}",
            json={"confidence_score": 0.82}
        )
        assert update_response.status_code == 200
        
        # 5. Delete
        delete_response = client.delete(f"/api/symptom-checkers/{record_id}")
        assert delete_response.status_code == 204


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
