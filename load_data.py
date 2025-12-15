import csv
import os
import re
from googleapiclient.discovery import build
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from httplib2 import Credentials
from models import db, User, TutorProfile, TutorRequest, TutorAssignment


def get_sheet_rows():
    """Load from Google Sheets if configured. Otherwise fallback to CSV."""

    creds_dict = current_app.config.get("GOOGLE_SHEETS_CREDENTIALS")
    sheet_id = current_app.config.get("GOOGLE_SHEETS_SHEET_ID")
    tabs = current_app.config.get("GOOGLE_SHEETS_TABS")

    # If ANY required Google value is missing → fallback
    if not creds_dict or not sheet_id or not tabs:
        print("No Google Sheets configuration found — loading from CSV instead.")
        return load_from_csv()

    print("Google Sheets detected — loading remotely")

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

    service = build("sheets", "v4", credentials=creds)
    sheet_api = service.spreadsheets()

    tab_list = [t.strip() for t in tabs.split(",")]
    all_rows = []

    for sheet_name in tab_list:
        result = sheet_api.values().get(
            spreadsheetId=sheet_id,
            range=sheet_name
        ).execute()

        rows = result.get("values", [])
        if not rows:
            print(f"⚠ No data in sheet: {sheet_name}")
            continue

        headers = rows[0]
        for r in rows[1:]:
            row_dict = {headers[i]: r[i] if i < len(r) else "" for i in range(len(headers))}
            all_rows.append(row_dict)

    return all_rows


def load_from_csv():
    """Load tutor profiles from local CSV file."""
    csv_path = os.path.join(current_app.root_path, "data", "tutor_profiles.csv")
    
    if not os.path.exists(csv_path):
        print(f"⚠ CSV file not found at path: {csv_path}")
        return []
    
    
    all_rows = []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            all_rows.append(row)

    return all_rows

def load_users():
    if User.query.first():
        print("Users already exist in the database. Skipping user load.")
        return
    
    admin = User(
        name="Admin User",
        email="Email here",
        position="Admin"
    )
    admin.set_password("")
    db.session.add(admin)
    
    professor = User(
        name="Professor Example",
        email="Email here",
        position="Professor"
    )
    professor.set_password("")
    db.session.add(professor)
    
    db.session.commit()
        

def load_tutor_profiles():
    """Load tutor profiles into the database."""
    rows = get_sheet_rows()
    for row in rows:
        profile = TutorProfile(
            name=row.get("Name", ""),
            role=row.get("Role", ""),
            email=row.get("Email", ""),
            image_address=row.get("Image Address", ""),
            interests=row.get("Interests", ""),
            classYear=row.get("Class Year", ""),
            pronouns=row.get("Pronouns", ""),
            hometown=row.get("Hometown", ""),
            majors=row.get("Majors", ""),
            minors=row.get("Minors", ""),
            languages=row.get("Languages", ""),
            active=row.get("active", "True").lower() in ("true", "1", "yes")
        )
        db.session.add(profile)
    db.session.commit()
    print(f"Loaded {len(rows)} tutor profiles into the database.")
    
