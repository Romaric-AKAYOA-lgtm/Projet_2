; Script Inno Setup pour créer un installateur de GestionVisite
[Setup]
AppName=Gestion Visite
AppVersion=1.0
DefaultDirName={commonpf}\GestionVisite
DefaultGroupName=Gestion Visite
OutputDir=.\output
OutputBaseFilename=GestionVisite_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\GestionVisite.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commondesktop}\Gestion Visite"; Filename: "{app}\GestionVisite.exe"

[Run]
Filename: "{app}\GestionVisite.exe"; Description: "Lancer Gestion Visite"; Flags: nowait postinstall skipifsilent
