import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_suite():
    print("\n--- Starting LM-Inspect AI API Verification Suite ---")

    # 1. Health check
    print("\n1. Testing GET /api/v1/health...")
    r = client.get("/api/v1/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    print(f"   [PASS] Health check: {r.json()}")

    # 2. Dashboard Stats
    print("\n2. Testing GET /api/v1/dashboard/stats...")
    r = client.get("/api/v1/dashboard/stats")
    assert r.status_code == 200
    data = r.json()
    assert "totalInspections" in data
    assert "recentInspections" in data
    print(f"   [PASS] Total Inspections: {data['totalInspections']}, Rate: {data['complianceRate']}%")

    # 3. Inspections History
    print("\n3. Testing GET /api/v1/inspections/history...")
    r = client.get("/api/v1/inspections/history")
    assert r.status_code == 200
    inspections = r.json()
    assert len(inspections) > 0
    print(f"   [PASS] Retrieved {len(inspections)} inspection records")

    # 4. Filter Inspections History
    print("\n4. Testing GET /api/v1/inspections/history with search & status filter...")
    r = client.get("/api/v1/inspections/history?search=Cookies&status=NON-COMPLIANT")
    assert r.status_code == 200
    filtered = r.json()
    assert len(filtered) >= 1
    print(f"   [PASS] Filtered results count: {len(filtered)}")

    # 5. Image Upload (POST /api/v1/images/upload)
    print("\n5. Testing POST /api/v1/images/upload...")
    # Create a small dummy JPEG
    dummy_image_content = (
        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00"
        b"\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19"
        b"\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.' \",#\x1c\x1c(7),01444\x1f'9=82<.342\xff"
        b"\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01"
        b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xda\x00\x08"
        b"\x01\x01\x00\x00?\x00\xbf\x00\xff\xd9"
    )
    files = {"image": ("test_label.jpg", dummy_image_content, "image/jpeg")}
    data = {"scanType": "Back Label"}
    r = client.post("/api/v1/images/upload", files=files, data=data)
    assert r.status_code == 200, f"Upload failed: {r.text}"
    upload_res = r.json()
    assert "fileId" in upload_res
    assert "imageUrl" in upload_res
    print(f"   [PASS] Uploaded File: {upload_res['fileId']}, URL: {upload_res['imageUrl']}")

    # 6. Extract Declarations (POST /api/v1/declarations/extract)
    print("\n6. Testing POST /api/v1/declarations/extract...")
    extract_req = {
        "fileId": upload_res["fileId"],
        "imageUrl": upload_res["imageUrl"],
        "scanType": "Back Label",
    }
    r = client.post("/api/v1/declarations/extract", json=extract_req)
    assert r.status_code == 200, f"Extract failed: {r.text}"
    extract_res = r.json()
    assert "extractedDeclarations" in extract_res
    assert "boundingBoxes" in extract_res
    print(f"   [PASS] Extracted {len(extract_res['extractedDeclarations'])} declarations, {len(extract_res['boundingBoxes'])} bounding boxes")

    # 7. Validate Declarations (POST /api/v1/rules/validate)
    print("\n7. Testing POST /api/v1/rules/validate...")
    validate_req = {
        "declarations": extract_res["extractedDeclarations"],
        "productMetadata": {"name": "Test Cookies"},
    }
    r = client.post("/api/v1/rules/validate", json=validate_req)
    assert r.status_code == 200, f"Validate failed: {r.text}"
    val_res = r.json()
    assert "overallStatus" in val_res
    assert "complianceScore" in val_res
    assert "violations" in val_res
    print(f"   [PASS] Status: {val_res['overallStatus']}, Score: {val_res['complianceScore']}, Violations: {len(val_res['violations'])}")

    # 8. Analyze Product Pipeline (POST /api/v1/inspections/analyze)
    print("\n8. Testing POST /api/v1/inspections/analyze...")
    analyze_req = {
        "productName": "SuperFresh Oat Cookies",
        "brand": "SuperFresh Foods",
        "category": "Food & Bakery",
        "manufacturer": "SuperFresh Bakery Ltd., Delhi",
        "sku": "SF-OAT-200G",
        "location": "Retail Mart, New Delhi",
        "scanType": "Back Label",
        "imageUrl": upload_res["imageUrl"],
        "fileId": upload_res["fileId"],
    }
    r = client.post("/api/v1/inspections/analyze", json=analyze_req)
    assert r.status_code == 200, f"Analyze failed: {r.text}"
    analysis = r.json()
    new_insp_id = analysis["inspectionId"]
    assert "inspectionId" in analysis
    print(f"   [PASS] Created inspection: {new_insp_id}, Status: {analysis['status']}")

    # 9. Get Compliance Result (GET /api/v1/inspections/{id}/compliance)
    print(f"\n9. Testing GET /api/v1/inspections/{new_insp_id}/compliance...")
    r = client.get(f"/api/v1/inspections/{new_insp_id}/compliance")
    assert r.status_code == 200, f"Compliance result failed: {r.text}"
    comp_res = r.json()
    assert comp_res["inspectionId"] == new_insp_id
    assert "declarations" in comp_res
    assert "violations" in comp_res
    print(f"   [PASS] Compliance Dossier retrieved: Score={comp_res['complianceScore']}, Declarations={len(comp_res['declarations'])}")

    # 10. Get Violations (GET /api/v1/violations)
    print("\n10. Testing GET /api/v1/violations...")
    r = client.get("/api/v1/violations?severity=HIGH")
    assert r.status_code == 200
    viols = r.json()
    assert len(viols) >= 1
    print(f"   [PASS] High severity violations count: {len(viols)}")

    # 11. Get Product Details (GET /api/v1/products/{id})
    print("\n11. Testing GET /api/v1/products/PROD-001...")
    r = client.get("/api/v1/products/PROD-001")
    assert r.status_code == 200
    prod_details = r.json()
    assert "product" in prod_details
    assert "inspections" in prod_details
    print(f"   [PASS] Product {prod_details['product']['name']} has {len(prod_details['inspections'])} inspections")

    # 12. Generate Report (GET /api/v1/inspections/{id}/report)
    print(f"\n12. Testing GET /api/v1/inspections/{new_insp_id}/report...")
    r = client.get(f"/api/v1/inspections/{new_insp_id}/report")
    assert r.status_code == 200
    report = r.json()
    assert "certificateNumber" in report
    assert "findingsSummary" in report
    assert "officer" in report
    print(f"   [PASS] Report generated: Certificate={report['certificateNumber']}, Notice Required={report['showCauseNoticeRequired']}")

    # 13. Analytics Summary (GET /api/v1/analytics/summary)
    print("\n13. Testing GET /api/v1/analytics/summary...")
    r = client.get("/api/v1/analytics/summary")
    assert r.status_code == 200
    analytics = r.json()
    assert "inspectionsTrend" in analytics
    assert "violationsByCategory" in analytics
    print(f"   [PASS] Analytics summary retrieved: {len(analytics['inspectionsTrend'])} trend points, {len(analytics['violationsByCategory'])} categories")

    print("\n============================================================")
    print(">>> ALL 13 ENDPOINT & INTEGRATION TESTS PASSED SUCCESSFULLY! <<<")
    print("============================================================\n")

if __name__ == "__main__":
    test_api_suite()
