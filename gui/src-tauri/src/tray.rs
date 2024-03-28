use tauri::{
    menu::MenuId,
    tray::{ClickType, TrayIconEvent},
    AppHandle, Manager,
};

pub fn setup(app: AppHandle) {
    // Create a native context menu
    let menu = tauri::menu::MenuBuilder::new(&app)
        .item(&tauri::menu::MenuItem::with_id(
            &app,
            "quit",
            "Quit",
            true,
            None::<&str>,
        )?)
        .build()?;
    // Create the TrayIcon with the menu registered to it
    let tray = tauri::tray::TrayIconBuilder::with_id("main_tray")
        .menu(&menu)
        .build(&app)?;
    // Register a menu event handler
    tray.on_menu_event(move |app, event| match event.id.0.as_str() {
        "quit" => {
            let handle = app.app_handle();
            handle.exit(0);
        }
        _ => {}
    });
    // Give the TrayIcon a pretty face
    tray.set_icon(Some(tauri::Icon::Raw(
        include_bytes!("../icons/icon.png").to_vec(),
    )))
    .unwrap();
    // Handle clicks on the TrayIcon itself
    tray.on_tray_icon_event(move |tray_icon, event| {
        // Get yourself an AppHandle to interact with stuff
        let handle = app.app_handle();
        match event.click_type {
            ClickType::Left => {}
            ClickType::Right => {}
            ClickType::Double => {}
        }
    });
    Ok(())
}
