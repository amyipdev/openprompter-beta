python3 -m venv venv
source ../venv/bin/activate
pip3 install -r ../requirements.txt
mkdir -p ~/.config/autostart
cp amyipdev-ops.desktop ~/.config/autostart/amyipdev-ops.desktop
cp discovsets.json.example discovsets.json
cp appsets.json.example appsets.json
cp pygsets.json.example pygsets.json
