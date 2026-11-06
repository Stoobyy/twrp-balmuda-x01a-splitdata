from pathlib import Path
import json, hashlib
r=Path(__file__).resolve().parents[1]
f=(r/'recovery.fstab').read_text()
for mount,base in [('/data','userdata'),('/metadata','metadata')]:
    rows=[l for l in f.splitlines() if l.startswith(mount+' ')]
    assert len(rows)==1
    fields=rows[0].split()
    assert fields[2].endswith('/'+base)
    assert 'slotselect' in fields[3].split(';')
assert '/dev/block/sda1' not in f
b=(r/'BoardConfig.mk').read_text()
assert 'AB_OTA_UPDATER := true' in b
assert '2099-12-31' not in b
assert 'device/kyocera/X01A_splitdata' in b
for p in json.loads((r/'evidence/recovery-header.json').read_text())['prebuilts']:
    data=(r/'prebuilt'/p['name']).read_bytes()
    assert len(data)==p['size_bytes']
    assert hashlib.sha256(data).hexdigest()==p['sha256']
print('PASS: slot mapping, build identity, and live-device prebuilt hashes')
