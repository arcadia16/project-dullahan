import subprocess
import tempfile
import os
import sys
from .nxc_param import *
#from getpass import getpass

class NetExecExtractor:
    def __init__(self, wordlist_path):
        self.wordlist_path = wordlist_path
        self.temp_files = []
    
    def cleanup(self):
        for file in self.temp_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except Exception as e:
                print(f"WARN:: Could not remove temp file {file}: {e}")
    
    def check(self, domain: str, dc: str, username: str, hash: str):
        hash_out = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='_hash.txt')
        hash_out.close()
        self.temp_files.append(hash_out.name)
        print(f"[*] Created temp file {hash_out.name}")
        print("[*] Auth attempt...")
        try:
            cmd = [
                'nxc', 'smb', f'{dc}', '-d', f'{domain}',
                '-u', f'{username}', '-H', f'{hash}'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                print(f"[+] Auth successfull!")
            else:
                print(f"[-] Auth failed : {result.stderr}")
        except subprocess.TimeoutExpired:
            print("[-] Timeout")
        except FileNotFoundError:
            print("[?] NetExec is not installed on the system.")

extractor = NetExecExtractor(wordlist_path="/usr/share/wordlists")
extractor.check(DOMAIN, DC, USER, HASH)