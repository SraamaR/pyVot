
;This file is part of PyVot.
;
; Copyright (C) 2007 Thomas Paviot
;
;PyVot is free software; you can redistribute it and/or modify
;it under the terms of the GNU General Public License as published by
;the Free Software Foundation; either version 2 of the License, or
;(at your option) any later version.
;
;PyVot is distributed in the hope that it will be useful,
;but WITHOUT ANY WARRANTY; without even the implied warranty of
;MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;GNU General Public License for more details.
;
;You should have received a copy of the GNU General Public License
;along with PyVot; if not, write to the Free Software
;Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

[Setup]
;Informations g�n�rales sur l'application
AppName=PyVot 0.6
AppVerName=PyVot 0.6
AppVersion=0.6
AppPublisher=C�drick Faury
AppCopyright=Copyright � 2006-2009 C�drick Faury
AppPublisherURL=http://pyvot.fr/
AppSupportURL=http://pyvot.fr/
AppUpdatesURL=http://pyvot.fr/
;Repertoire d'installation
DefaultDirName={pf}\PyVot
DefaultGroupName=PyVot
LicenseFile=D:\Documents\Developpement\PyVot 0.6\gpl.txt
;Param�tres de compression
;lzma ou zip
Compression=lzma/max
SolidCompression=yes
;Par d�faut, pas besoin d'�tre administrateur pour installer
PrivilegesRequired=none
;Nom du fichier g�n�r� et r�pertoire de destination
OutputBaseFilename=PyVot-0.6
OutputDir=D:\Documents\Developpement\PyVot 0.6\releases
;Dans le panneau de configuration de Windows2000/NT/XP, c'est l'icone de pyMotion.exe qui
;appara�t � gauche du nom du fichier pour la d�sinstallation
UninstallDisplayIcon={app}\images\pyvot.ico
;Fen�tre en background
WindowResizable=false
WindowStartMaximized=true
WindowShowCaption=true
BackColorDirection=lefttoright
WizardImageFile = D:\Documents\Developpement\PyVot 0.6\Images\grand_logo.bmp
WizardSmallImageFile = D:\Documents\Developpement\PyVot 0.6\Images\petit_logo.bmp

[Languages]
Name: fr; MessagesFile: "compiler:Languages\French.isl"

[Messages]
BeveledLabel=PyVot 0.6 installation

[Files]
;
; Fichiers de la distribution
;
Source: D:\Documents\Developpement\PyVot 0.6\src\dist\*.*; DestDir: {app}\bin; Flags : ignoreversion;
Source: D:\Documents\Developpement\PyVot 0.6\*.txt; DestDir: {app}; Flags : ignoreversion;
Source: D:\Documents\Developpement\PyVot 0.6\donnees\*.txt; DestDir: {app}\Donnees; Flags : ignoreversion;
Source: D:\Documents\Developpement\PyVot 0.6\aide\pyvotaide.chm; DestDir: {app}\Aide; Flags : ignoreversion;
Source: D:\Documents\Developpement\PyVot 0.6\aide\html; DestDir: {app}\Aide\html; Flags : ignoreversion recursesubdirs createallsubdirs;
Source: D:\Documents\Developpement\PyVot 0.6\images\*.*; DestDir: {app}\Images; Flags : ignoreversion;
Source: D:\Documents\Developpement\PyVot 0.6\images\Arbre_Alesage\*.*; DestDir: {app}\Images\Arbre_Alesage; Flags : ignoreversion;
Source: D:\Documents\Developpement\PyVot 0.6\images\Arrets\*.*; DestDir: {app}\Images\Arrets; Flags : ignoreversion;
Source: D:\Documents\Developpement\PyVot 0.6\images\Joints\*.*; DestDir: {app}\Images\Joints; Flags : ignoreversion;
Source: D:\Documents\Developpement\PyVot 0.6\images\Roulements\*.*; DestDir: {app}\Images\Roulements; Flags : ignoreversion;
Source: D:\Documents\Developpement\PyVot 0.6\images\Schema\*.*; DestDir: {app}\Images\Schema; Flags : ignoreversion;
Source: D:\Documents\Developpement\PyVot 0.6\exemples\*.*; DestDir: {app}\Exemples; Flags : ignoreversion;

[Tasks]
Name: desktopicon2; Description: Ajouter l'ic�ne PyVot sur le bureau; GroupDescription: Additional icons:; MinVersion: 4,4
Name: fileassoc; Description: Associer le programme PyVot � l'extension .pyv; GroupDescription: "Other tasks:";

[Icons]
Name: {group}\PyVot 0.6;Filename: {app}\bin\pyvot.exe; WorkingDir: {app}\bin; IconFileName: {app}\bin\pyvot.exe
Name: {group}\Aide Pyvot 0.6; Filename: {app}\aide\pyvotaide.chm; Comment: Aide en ligne; IconFileName: {app}\aide\pyvotaide.chm
Name: {group}\D�sinstaller Pyvot; Filename: {app}\unins000.exe;IconFileName: {app}\unins000.exe
;
; On ajoute sur le Bureau l'ic�ne PyVot
;
Name: {userdesktop}\PyVot 0.6;   Filename: {app}\bin\pyvot.exe; WorkingDir: {app}\bin; MinVersion: 4,4; Tasks: desktopicon2; IconFileName: {app}\bin\pyvot.exe

[_ISTool]
Use7zip=true

[Registry]
Root: HKCR; SubKey: .pyv; ValueType: string; ValueData: Projet PyVot; Flags: uninsdeletekey
Root: HKCR; SubKey: Projet PyVot; ValueType: string; Flags: uninsdeletekey; ValueData: Projet PyVot
Root: HKCR; SubKey: Projet PyVot\Shell\Open\Command; ValueType: string; ValueData: """{app}\bin\pyvot.exe"" ""%1"""; Flags: uninsdeletekey;
Root: HKCR; Subkey: Projet PyVot\DefaultIcon; ValueType: string; ValueData: {app}\Images\fichier-pyv.ico,0; Flags: uninsdeletekey;
; et une clef pour indiquer que pyvot est install�
Root: HKLM; Subkey: SOFTWARE\PyVot; Flags: uninsdeletekey;
Root: HKLM; Subkey: SOFTWARE\PyVot; ValueName: "UninstallPath" ; ValueType: string; ValueData: {uninstallexe}; Flags: uninsdeletekey;

[code]
function PyVotInstalled():Boolean;
begin
  if RegKeyExists(HKEY_LOCAL_MACHINE,'SOFTWARE\PyVot\') then
    Result:=True
  else if RegKeyExists(HKEY_CLASSES_ROOT,'.pyv') then
    Result:=True
  else
    Result:=False;
end;


function GetUninstallPath(): String;
var
  ResultPath: String;
begin
  if RegQueryStringValue(HKEY_LOCAL_MACHINE,'SOFTWARE\PyVot\','UninstallPath', ResultPath) then
    Result := ResultPath
  else
    Result := ExpandConstant('{pf}\PyVot\unins000.exe')
End;


function NextButtonClick(CurPageID: Integer): Boolean;
var
  ResultCode: integer;
begin
  if (CurPageID = wpWelcome) and (PyVotInstalled()) then
    if MsgBox('Une pr�c�dente version de PyVot est d�ja install�e !'#13 +
              'Il est conseill� de la desinstaller.'#13#13 +
              'Vouler vous d�sinstaller la version pr�c�dente de PyVot ?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      if Exec(GetUninstallPath(), '', '', SW_SHOW,
              ewWaitUntilTerminated, ResultCode) then
        begin
          // handle success if necessary; ResultCode contains the exit code
        end
        else
        begin
          MsgBox('La d�sinstallation automatique de PyVot � �chou�e !'#13#13 +
                 'Veuillez d�sinstaller la version pr�c�dente de PyVot manuellement.', mbCriticalError, MB_OK);
          // handle failure if necessary; ResultCode contains the error code
        end;
    end;
  Result := True;
end;



procedure DesinstallerPyVot();
begin
  if MsgBox('Une pr�c�dente version de PyVot est d�ja install�e ! Il est conseill� de la desinstaller. Vouler vous d�sinstaller PyVot avant d''en installer une nouvelle version ?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      //
    end;
end;

//function InitializeSetup(): Boolean;
//begin
//  if PyVotInstalled then
//    Msgbox('Une pr�c�dente version de PyVot est d�ja install�e ! D�sinstaller PyVot avant d'en installer une nouvelle version.',mbConfirmation,MB_Ok);
//end;

//function GetPSPadPath(Default: String) : String;
//begin
//   RepPSPad:=Copy(RepPSPad,2,Length(RepPSPad)-1);
//   Result:=ExtractFilePath(RepPSPad);
//end;
