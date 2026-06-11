import subprocess
import platform
import os

class AppLauncher:
    """Handles opening applications on the system"""
    
    def __init__(self):
        self.system = platform.system()
        self.app_paths = self._get_app_paths()
    
    def _get_app_paths(self):
        """Get common application paths based on OS"""
        if self.system == "Darwin":  # macOS
            return {
                "chrome": "/Applications/Google Chrome.app",
                "firefox": "/Applications/Firefox.app",
                "spotify": "/Applications/Spotify.app",
                "discord": "/Applications/Discord.app",
                "slack": "/Applications/Slack.app",
                "vscode": "/Applications/Visual Studio Code.app",
                "finder": "/Applications/Finder.app",
                "mail": "/Applications/Mail.app",
            }
        elif self.system == "Windows":
            return {
                "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                "spotify": "C:\\Users\\{user}\\AppData\\Roaming\\Spotify\\Spotify.exe",
                "discord": "C:\\Users\\{user}\\AppData\\Local\\Discord\\app-{version}\\Discord.exe",
                "slack": "C:\\Users\\{user}\\AppData\\Local\\slack\\slack.exe",
                "vscode": "C:\\Program Files\\Microsoft VS Code\\Code.exe",
                "notepad": "notepad.exe",
            }
        else:  # Linux
            return {
                "chrome": "/usr/bin/google-chrome",
                "firefox": "/usr/bin/firefox",
                "spotify": "/usr/bin/spotify",
                "discord": "/usr/bin/discord",
                "slack": "/usr/bin/slack",
                "vscode": "/usr/bin/code",
            }
    
    def launch_app(self, app_name: str, args: str = "") -> dict:
        """
        Launch an application
        
        Args:
            app_name: Name of the application to launch
            args: Additional arguments to pass to the app
            
        Returns:
            dict with status and message
        """
        app_name = app_name.lower().strip()
        
        try:
            if self.system == "Darwin":  # macOS
                cmd = ["open", "-a", self.app_paths.get(app_name, app_name)]
                if args:
                    cmd.extend(["--args", args])
                subprocess.Popen(cmd)
            
            elif self.system == "Windows":
                path = self.app_paths.get(app_name)
                if path:
                    path = path.format(user=os.getenv("USERNAME"))
                    subprocess.Popen(f"{path} {args}")
                else:
                    subprocess.Popen(f"{app_name} {args}", shell=True)
            
            else:  # Linux
                path = self.app_paths.get(app_name, app_name)
                subprocess.Popen(f"{path} {args}", shell=True)
            
            return {
                "status": "success",
                "message": f"Launched {app_name}"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to launch {app_name}: {str(e)}"
            }
    
    def open_url(self, url: str) -> dict:
        """Open a URL in the default browser"""
        try:
            if self.system == "Darwin":
                subprocess.Popen(["open", url])
            elif self.system == "Windows":
                os.startfile(url)
            else:
                subprocess.Popen(["xdg-open", url])
            
            return {
                "status": "success",
                "message": f"Opened URL: {url}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to open URL: {str(e)}"
            }
