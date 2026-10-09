import os

print("Injecting custom Leapson Remote settings...")

config_path = "libs/hbb_common/src/config.rs"
if os.path.exists(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()

    # App Name
    content = content.replace(
        'pub static ref APP_NAME: RwLock<String> = RwLock::new("RustDesk".to_owned());',
        'pub static ref APP_NAME: RwLock<String> = RwLock::new("遠隔サポート (Powered by RustDesk)".to_owned());'
    )

    # Server address
    content = content.replace(
        'pub const RENDEZVOUS_SERVERS: &[&str] = &["rs-ny.rustdesk.com"];',
        'pub const RENDEZVOUS_SERVERS: &[&str] = &["hbbs.leapson.net"];'
    )

    # Public Key
    content = content.replace(
        'pub const RS_PUB_KEY: &str = "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=";',
        'pub const RS_PUB_KEY: &str = "TDDw2HCn7LvO9NecWBx8fwRmXrmGSCbryrEGcZ6dnZM=";'
    )

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully patched libs/hbb_common/src/config.rs")
else:
    print(f"Warning: {config_path} not found!")
