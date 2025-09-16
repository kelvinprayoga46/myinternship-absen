#!/usr/bin/env python3
"""
Internship Attendance BOT
Author: Kelvin
Description: Automatisasi absen harian di myinternship.id biar ga manual cik
"""
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class MyInternshipAutomation:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://myinternship.id"
        self.csrf_token = None
        self.cookies = None
          
    def get_csrf_token_from_page(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        token_meta = soup.find('meta', attrs={'name': 'csrf-token'})
        if token_meta:
            return token_meta.get('content')
        return None

    def step1_get_login_page(self):
        """Step 1: Mengambil halaman login dan extract CSRF token + cookies"""
        print("Step 1: Mengambil halaman login...")
        
        login_url = f"{self.base_url}/index.php?page=student_login"
        response = self.session.get(login_url)

        if response.status_code == 200:
            self.csrf_token = self.get_csrf_token_from_page(response.text)
            print(f"CSRF Token (Login): {self.csrf_token}")
            print(f"Cookies: {dict(self.session.cookies)}")
            return True
        else:
            print(f"Error: Tidak bisa mengakses halaman login. Status code: {response.status_code}")
            return False
    
    def step2_login(self, nim, password):
        """Step 2: Login dengan NIM dan password"""
        print("Step 2: Melakukan login...")
        
        login_data = {
            'nim': nim,
            'password': password,
            'token': self.csrf_token
        }
        
        login_url = f"{self.base_url}/index.php?form=new_student_login"
        self.session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': self.base_url,
            'Referer': f"{self.base_url}/index.php?page=student_login"
        })
        
        response = self.session.post(login_url, data=login_data, allow_redirects=True)
        
        if response.status_code == 200:
            if "dashboard" in response.url.lower() or "index.php" in response.url:
                print("Login berhasil!")
                self.csrf_token = self.get_csrf_token_from_page(response.text)
                return True
            else:
                print("Login gagal!")
                return False
        else:
            print(f"Error login. Status code: {response.status_code}")
            return False
    
    def step3_get_index_page(self):
        """Step 3: Mengambil halaman index dan update CSRF token + cookies"""
        print("Step 3: Mengambil halaman index...")
        
        index_url = f"{self.base_url}/index.php"
        response = self.session.get(index_url)
        
        if response.status_code == 200:
            self.csrf_token = self.get_csrf_token_from_page(response.text)
            print(f"CSRF Token (Index): {self.csrf_token}")
            return True
        else:
            print(f"Error: Tidak bisa mengakses halaman index. Status code: {response.status_code}")
            return False
    
    def step4_get_attendance_page(self, id_internship=None):
        """Step 4: Mengakses halaman attendance"""
        print("Step 4: Mengakses halaman attendance...")
        
        if id_internship is None:
            id_internship = os.getenv("MYINTERNSHIP_ID_INTERNSHIP", "OTI0OA==")
        
        attendance_url = f"{self.base_url}/index.php?page=attendance_internship&id_internship={id_internship}"
        
        self.session.headers.update({
            'Referer': f"{self.base_url}/index.php"
        })
        
        response = self.session.get(attendance_url)
        
        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')
            add_button = soup.find('button', onclick=lambda x: x and "addhistory_attendance_internship" in x)

            if add_button and 'onclick' in add_button.attrs:
                onclick_content = add_button['onclick']

                jwt_pattern = r"id_internship=([^'\"]+)"
                match = re.search(jwt_pattern, onclick_content)
                if match:
                    jwt_token = match.group(1)
                    print(f"JWT Token ditemukan: {jwt_token}")
                    return jwt_token
            
            print("Tidak bisa menemukan JWT token dari button Add Attendance")
            return None
        else:
            print(f"Error: Tidak bisa mengakses halaman attendance. Status code: {response.status_code}")
            return None
    
    def step5_get_add_attendance_page(self, jwt_token):
        """Step 5: Mengakses halaman add attendance"""
        print("Step 5: Mengakses halaman add attendance...")
        
        add_attendance_url = f"{self.base_url}/index.php?page=addhistory_attendance_internship&id_internship={jwt_token}"
        
        id_internship_param = os.getenv("MYINTERNSHIP_ID_INTERNSHIP", "OTI0OA==")
        self.session.headers.update({
            'Referer': f"{self.base_url}/index.php?page=attendance_internship&id_internship={id_internship_param}"
        })
        
        response = self.session.get(add_attendance_url)
        if response.status_code == 200:
            new_token = self.get_csrf_token_from_page(response.text)
            if new_token:
                self.csrf_token = new_token
            
            return add_attendance_url
        else:
            print(f"Error: Tidak bisa mengakses halaman add attendance. Status code: {response.status_code}")
            return None
    
    def step6_submit_attendance(self, referer_url, attendance_data):
        """Step 6: Submit attendance data"""
        print("Step 6: Submit data attendance...")
        
        default_data = {
            'token': self.csrf_token,
            'id_internship': os.getenv("MYINTERNSHIP_ID_INTERNSHIP_NUMERIC"),
            'nim': os.getenv("MYINTERNSHIP_NIM"),
            'attendance_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'attendance_type': 'Present',
            'check_in': '00:00',
            'check_out': '08:00',
            'description': '<p>ABSEN HARIAN</p>',
            'validation': os.getenv("MYINTERNSHIP_SIGNATURE_BASE64")
        }
        
        if attendance_data:
            default_data.update(attendance_data)
        
        submit_url = f"{self.base_url}/index.php?form=attendance&action=add_history"
        
        self.session.headers.update({
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryWfw8OpfnDt7HEgLI',
            'Origin': self.base_url,
            'Referer': referer_url,
            'Sec-Fetch-Dest': 'empty'
        })
        
        boundary = '----WebKitFormBoundaryWfw8OpfnDt7HEgLI'
        multipart_data = ''
        
        for key, value in default_data.items():
            multipart_data += f'--{boundary}\r\n'
            multipart_data += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
            multipart_data += f'{value}\r\n'
        
        multipart_data += f'--{boundary}--\r\n'
        
        if 'Content-Type' in self.session.headers:
            del self.session.headers['Content-Type']
        
        files = {}
        for key, value in default_data.items():
            if key == 'validation':
                files[key] = (None, value)
            else:
                files[key] = (None, str(value))
        
        response = self.session.post(submit_url, files=files, allow_redirects=True)
        
        if response.status_code == 200:
            print("Attendance berhasil disubmit!")
            print(f"Response URL: {response.url}")
            return True
        else:
            print(f"Error submit attendance. Status code: {response.status_code}")
            print(f"Response content: {response.text[:500]}...")
            return False
    
    def run_automation(self, nim, password, attendance_data=None):
        try:
            if not self.step1_get_login_page():
                return False
            
            time.sleep(0.3)
            if not self.step2_login(nim, password):
                return False
            
            time.sleep(0.3)
            if not self.step3_get_index_page():
                return False
            
            time.sleep(0.3)
            
            jwt_token = self.step4_get_attendance_page()
            if not jwt_token:
                return False
            
            time.sleep(0.3)
            referer_url = self.step5_get_add_attendance_page(jwt_token)
            if not referer_url:
                return False
            
            time.sleep(0.3)
            if not self.step6_submit_attendance(referer_url, attendance_data):
                return False
            
            print("\n=== Automasi selesai dengan sukses! ===")
            return True
            
        except Exception as e:
            print(f"Error dalam automasi: {str(e)}")
            return False

if __name__ == "__main__":
    automation = MyInternshipAutomation()
    
    # Data login
    nim = os.getenv("MYINTERNSHIP_NIM")
    password = os.getenv("MYINTERNSHIP_PASS")

    success = automation.run_automation(nim, password)
    
    if success:
        print("Absensi berhasil!")
    else:
        print("Absensi gagal!")