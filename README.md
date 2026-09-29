# 🚗 Vehicle Lookup API

A simple Flask API to fetch vehicle details from VAHAN database via SMC Insurance.

## 🚀 Deploy on Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

Or manually:
1. Fork this repo
2. Create New Web Service on Render
3. Connect your GitHub repo
4. Deploy!

## 📖 API Documentation

### GET Request
GET /lookup/<vehicle_number>

**Example:**
```bash
curl https://your-api.onrender.com/lookup/MH14ML9572
POST Request

POST /lookup
Content-Type: application/json

{
  "vehicle_number": "MH14ML9572"
}Health Check

GET /health

⚠️ Rate Limits

    10 requests per minute per IP
    Free tier limitations apply

📝 Notes

    Vehicle numbers are automatically cleaned (spaces removed, uppercase)
    API may stop working if SMC Insurance changes their endpoints
    Use responsibly and respect privacy laws

---

## 🚀 Render Pe Deploy Kaise Karein:

### Method 1: One-Click Deploy (Blue Button)
1. Render account banao
2. "Blueprint" option select karo
3. `render.yaml` file upload karo
4. Deploy!

### Method 2: Manual
1. **GitHub Repo Create Karo:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/vehicle-lookup-api.git
   git push -u origin main

    Render Dashboard:
        Login to render.com
        "New +" → "Web Service"
        Connect your GitHub repo
        Settings:
            Name: vehicle-lookup-api
            Runtime: Python 3
            Build Command: pip install -r requirements.txt
            Start Command: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2
        Deploy!

🔗 API Usage Examples:

Deployed URL ke baad aise use karo:
bash

# GET request
curl https://your-api.onrender.com/lookup/MH14ML9572

# POST request
curl -X POST https://your-api.onrender.com/lookup \
  -H "Content-Type: application/json" \
  -d '{"vehicle_number": "UP80FZ7810"}'

# Health check
curl https://your-api.onrender.com/health

⚠️ Important Warnings:

    Rate Limiting: Maine 10 requests/minute ka limit lagaya hai (IP based)
    Legal: VAHAN data sensitive hai, commercial use ke liye permission lo
    API Break: Agar SMC Insurance ne apna API change kiya toh yeh kaam karna band kar dega
    Privacy: Data responsibly use karo

Example:
bash

curl -X POST https://your-api.onrender.com/lookup \
  -H "Content-Type: application/json" \
  -d '{"vehicle_number": "MH14ML9572"}'




