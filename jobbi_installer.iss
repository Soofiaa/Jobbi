; ─────────────────────────────────────────────────────────
;  Jobbi — Job Tracker  |  Inno Setup Script
; ─────────────────────────────────────────────────────────

#define AppName        "Jobbi"
#define AppVersion     "1.0.0"
#define AppPublisher   "Sofía Menzel"
#define AppURL         "https://github.com/tu_usuario/jobbi"
#define AppExeName     "Jobbi.exe"
#define DistFolder     "dist\Jobbi"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes
OutputDir=installer
OutputBaseFilename=Jobbi_Setup_v{#AppVersion}
; IconFilename=jobbi.ico          ; descomenta si tienes ícono
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon";    Description: "Crear acceso directo en el &Escritorio";    GroupDescription: "Accesos directos:"; Flags: unchecked
Name: "startmenuicon";  Description: "Crear acceso directo en el menú de &Inicio"; GroupDescription: "Accesos directos:"

[Files]
Source: "{#DistFolder}\*";  DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\Jobbi\.env";  DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Menú inicio
Name: "{group}\{#AppName}";          Filename: "{app}\{#AppExeName}"
Name: "{group}\Desinstalar {#AppName}"; Filename: "{uninstallexe}"
; Escritorio (solo si el usuario lo eligió)
Name: "{autodesktop}\{#AppName}";    Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; \
    Description: "Abrir {#AppName} ahora"; \
    Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Messages]
WelcomeLabel2=Este asistente instalará [name/ver] en tu computador.%n%nSe recomienda cerrar todas las aplicaciones antes de continuar.
FinishedLabel=La instalación de [name] ha finalizado.%nPuedes abrirlo desde el menú Inicio o el acceso directo en el Escritorio.