# 📘 How to Upload Local Files to Microsoft Fabric Lakehouse Using Python

This guide walks you through **everything from scratch**:

- ✅ Create an **Azure App Registration** (Service Principal)
- ✅ Get **Client ID**, **Client Secret**, and **Tenant ID**
- ✅ Assign **Contributor access** to your Fabric workspace
- ✅ Configure `.env` file
- ✅ Run the Python script to upload files

---

## 1. **Prerequisites**

- An active **Microsoft Fabric workspace** with a Lakehouse created.
- **Azure subscription** linked to your Fabric tenant.
- Python 3.8+ installed.
- Install required packages:
```bash
  pip install azure-storage-file-datalake azure-identity python-dotenv tqdm
```

---

## 2. **Create an App Registration (Service Principal)**

1. Go to **Azure Portal** → **Azure Active Directory** → **App registrations**.
2. Click **New registration**:
   - **Name**: `fabric-uploader-app`
   - **Supported account types**: Single tenant (recommended).
   - Click **Register**.
3. After registration:
   - Copy **Application (client) ID** → this is your `CLIENT_ID`.
   - Copy **Directory (tenant) ID** → this is your `TENANT_ID`.

---

## 3. **Create a Client Secret**

1. In your App Registration, go to **Certificates & secrets**.
2. Under **Client secrets**, click **New client secret**:
   - Add a description (e.g., `fabric-upload-secret`).
   - Choose an expiry (e.g., 6 months).
   - Click **Add**.
3. Copy the **Value** immediately → this is your `CLIENT_SECRET`.

> ⚠️ You won't see the secret again after leaving the page. Save it securely.

---

## 4. **Assign Service Principal to Fabric Workspace**

1. Go to **Microsoft Fabric portal** → **Workspace** where your Lakehouse exists.
2. Click **Manage access** (top-right).
3. Add your **App Registration**:
   - Search by **name** or **Client ID**.
   - Assign **Contributor** role.
4. Save changes.

---

## 5. **Prepare `.env` File**

Create a file named `.env` in the same folder as your script:
```env
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret

WORKSPACE_NAME=your-fabric-workspace-name
LAKEHOUSE_NAME=your-lakehouse-name

LOCAL_FOLDER=/absolute/path/to/local/folder
TARGET_SUBFOLDER=auto_uploaded   # optional
```

---

## 6. **Verify Lakehouse Path**

- Your Lakehouse must exist in the workspace.
- Files will be uploaded under:
```
  Files/auto_uploaded/
```
  inside the Lakehouse.

---

## 7. **Run the Script**
```bash
python upload_to_fabric_final.py
```

You'll see:

- A progress bar for uploads.
- Success message with the Lakehouse path.

---

## ✅ Quick Checklist

- [ ] App Registration created
- [ ] Client ID, Secret, Tenant ID saved
- [ ] Service Principal added as **Contributor** in Fabric workspace
- [ ] `.env` file configured
- [ ] Python dependencies installed
- [ ] Script executed successfully

---