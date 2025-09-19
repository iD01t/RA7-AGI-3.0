"""RA7 Premium App: Secure notes with login, AES-256 encryption, and license gating."""
import base64
import json
import os
import threading
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import analytics
import update_checker

STORAGE_FILE = "storage.enc"
KEY_FILE = "app_key.bin"
VALID_LICENSE = "RA7-PREMIUM-2024"
VERSION = "1.0.0"


def load_master_key() -> bytes:
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as fh:
            return fh.read()
    key = AESGCM.generate_key(bit_length=256)
    with open(KEY_FILE, "wb") as fh:
        fh.write(key)
    return key


MASTER_KEY = load_master_key()


def encrypt(data: bytes) -> bytes:
    aesgcm = AESGCM(MASTER_KEY)
    nonce = os.urandom(12)
    return nonce + aesgcm.encrypt(nonce, data, None)


def decrypt(payload: bytes) -> bytes:
    aesgcm = AESGCM(MASTER_KEY)
    nonce, ct = payload[:12], payload[12:]
    return aesgcm.decrypt(nonce, ct, None)


def load_storage() -> dict:
    if not os.path.exists(STORAGE_FILE):
        return {"users": {}}
    with open(STORAGE_FILE, "rb") as fh:
        data = decrypt(fh.read())
    return json.loads(data.decode("utf-8"))


def save_storage(storage: dict) -> None:
    data = json.dumps(storage).encode("utf-8")
    with open(STORAGE_FILE, "wb") as fh:
        fh.write(encrypt(data))


def hash_password(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    salt = salt or os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return salt, kdf.derive(password.encode("utf-8"))


@dataclass
class User:
    username: str
    salt: bytes
    pw_hash: bytes
    license: str = ""


class LoginWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("RA7 Protocol 444")
        self.geometry("320x200")
        self.configure(bg="#000000")
        try:
            self.iconphoto(False, tk.PhotoImage(file="app_icon.png"))
        except Exception:
            pass
        tk.Label(self, text="Protocol 444 Activated", fg="white", bg="black").pack(pady=10)
        threading.Timer(2.0, self.show_login).start()

    def show_login(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text="Username").pack()
        self.user_var = tk.Entry(self)
        self.user_var.pack()
        tk.Label(self, text="Password").pack()
        self.pw_var = tk.Entry(self, show="*")
        self.pw_var.pack()
        tk.Button(self, text="Login", command=self.login).pack(pady=5)
        tk.Button(self, text="Register", command=self.register).pack()

    def login(self) -> None:
        storage = load_storage()
        user = storage["users"].get(self.user_var.get())
        if not user:
            messagebox.showerror("Error", "User not found")
            return
        salt = base64.b64decode(user["salt"])
        _, pw_hash = hash_password(self.pw_var.get(), salt)
        if pw_hash != base64.b64decode(user["pw_hash"]):
            messagebox.showerror("Error", "Incorrect password")
            return
        license_key = user.get("license", "")
        self.destroy()
        analytics.log_event("login")
        MainWindow(self.user_var.get(), license_key).mainloop()

    def register(self) -> None:
        storage = load_storage()
        username = self.user_var.get()
        if username in storage["users"]:
            messagebox.showerror("Error", "User exists")
            return
        salt, pw_hash = hash_password(self.pw_var.get())
        license_key = tk.simpledialog.askstring("License", "Enter license key (optional)") or ""
        storage["users"][username] = {
            "salt": base64.b64encode(salt).decode(),
            "pw_hash": base64.b64encode(pw_hash).decode(),
            "license": license_key,
            "notes": "",
        }
        save_storage(storage)
        analytics.log_event("register")
        if license_key == VALID_LICENSE:
            analytics.log_revenue(9.99)
        referral = analytics.generate_referral_code()
        messagebox.showinfo("Registered", f"User created. Referral code: {referral}")


class MainWindow(tk.Tk):
    def __init__(self, username: str, license_key: str) -> None:
        super().__init__()
        self.username = username
        self.premium = license_key == VALID_LICENSE
        self.title(f"RA7 Notes - {username}")
        self.geometry("500x400")
        self.dark_mode = tk.BooleanVar(value=True)
        self.text = tk.Text(self)
        self.text.pack(expand=True, fill=tk.BOTH)
        self.apply_theme()
        self.setup_menu()
        self.load_notes()
        self.check_updates()

    def apply_theme(self) -> None:
        bg = "#000000" if self.dark_mode.get() else "#FFFFFF"
        fg = "#FFFFFF" if self.dark_mode.get() else "#000000"
        self.configure(bg=bg)
        self.text.configure(bg=bg, fg=fg, insertbackground=fg)

    def setup_menu(self) -> None:
        menu = tk.Menu(self)
        view = tk.Menu(menu, tearoff=0)
        view.add_checkbutton(
            label="Dark Mode",
            onvalue=True,
            offvalue=False,
            variable=self.dark_mode,
            command=self.apply_theme,
        )
        menu.add_cascade(label="View", menu=view)
        menu.add_command(label="Save", command=self.save_notes)
        self.config(menu=menu)

    def load_notes(self) -> None:
        storage = load_storage()
        notes = storage["users"][self.username].get("notes", "")
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, notes)

    def save_notes(self) -> None:
        notes = self.text.get("1.0", tk.END)
        if not self.premium and len(notes) > 100:
            messagebox.showwarning("Premium", "Notes truncated. Enter license to unlock full length.")
            notes = notes[:100]
        storage = load_storage()
        storage["users"][self.username]["notes"] = notes
        save_storage(storage)
        analytics.log_event("save")
        messagebox.showinfo("Saved", "Notes saved")

    def check_updates(self) -> None:
        def worker() -> None:
            if update_checker.is_update_available(VERSION):
                messagebox.showinfo("Update", "A new version is available.")

        threading.Thread(target=worker, daemon=True).start()


def main() -> None:
    analytics.log_event("launch")
    LoginWindow().mainloop()


if __name__ == "__main__":
    main()
