import os

print("Injecting custom Leapson Remote settings (PC-Health-Check)...")

config_path = "libs/hbb_common/src/config.rs"
if os.path.exists(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. App Name
    content = content.replace(
        'pub static ref APP_NAME: RwLock<String> = RwLock::new("RustDesk".to_owned());',
        'pub static ref APP_NAME: RwLock<String> = RwLock::new("PC-Health-Check (Powered by RustDesk)".to_owned());'
    )

    # 2. Server address (ID server)
    content = content.replace(
        'pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"];',
        'pub const RENDEZVOUS_SERVERS: &[&str] = &["hbbs.leapson.net"];'
    )

    # 3. Public Key
    content = content.replace(
        'pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=";',
        'pub const RS_PUB_KEY: &str = "TDDw2HCn7LvO9NecWBx8fwRmXrmGSCbryrEGcZ6dnZM=";'
    )

    # 4. Hard settings: Incoming only + Disable settings
    hard_settings_patch = '''pub static ref HARD_SETTINGS: RwLock<HashMap<String, String>> = RwLock::new({
        let mut m = HashMap::new();
        m.insert("conn-type".to_string(), "incoming".to_string());
        m.insert("disable-settings".to_string(), "Y".to_string());
        m
    });'''
    content = content.replace(
        'pub static ref HARD_SETTINGS: RwLock<HashMap<String, String>> = Default::default();',
        hard_settings_patch
    )

    # 5. Overwrite settings: ID whitelist (1210139263) + Relay server (hbbr.leapson.net:21117)
    overwrite_settings_patch = '''pub static ref OVERWRITE_SETTINGS: RwLock<HashMap<String, String>> = RwLock::new({
        let mut m = HashMap::new();
        m.insert("id-whitelist".to_string(), "1210139263".to_string());
        m.insert("whitelist".to_string(), "1210139263".to_string());
        m.insert("relay-server".to_string(), "hbbr.leapson.net:21117".to_string());
        m
    });'''
    content = content.replace(
        'pub static ref OVERWRITE_SETTINGS: RwLock<HashMap<String, String>> = Default::default();',
        overwrite_settings_patch
    )

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully patched libs/hbb_common/src/config.rs")
else:
    print(f"Warning: {config_path} not found!")

# Also patch Runner.rc for Windows metadata
rc_path = "flutter/windows/runner/Runner.rc"
if os.path.exists(rc_path):
    with open(rc_path, "r", encoding="utf-8") as f:
        rc = f.read()
    rc = rc.replace('VALUE "FileDescription", "遠隔サポート (Powered by RustDesk)"', 'VALUE "FileDescription", "PC-Health-Check (Powered by RustDesk)"')
    rc = rc.replace('VALUE "OriginalFilename", "遠隔サポート.exe"', 'VALUE "OriginalFilename", "leapson-remotej.exe"')
    rc = rc.replace('VALUE "ProductName", "遠隔サポート (Powered by RustDesk)"', 'VALUE "ProductName", "PC-Health-Check (Powered by RustDesk)"')
    with open(rc_path, "w", encoding="utf-8") as f:
        f.write(rc)
    print("Successfully patched Runner.rc")
