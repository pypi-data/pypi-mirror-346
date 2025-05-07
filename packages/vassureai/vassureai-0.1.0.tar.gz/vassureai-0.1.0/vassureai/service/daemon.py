"""
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
"""

"""
Service integration for VAssureAI framework.

Provides functionality to run the framework as a system service,
supporting both Windows and Linux environments.
"""

import os
import sys
import logging
import asyncio
from typing import Optional
import signal
import platform
from pathlib import Path

from ..core.base.config import BaseConfig
from ..pdf.watcher import PDFWatcher


class ServiceManager:
    """Manager for running framework components as services."""
    
    def __init__(
        self,
        config: Optional[BaseConfig] = None,
        log_path: Optional[str] = None
    ):
        self._config = config or BaseConfig.from_env()
        self._log_path = log_path or os.path.join("logs", "pdf_watcher.log")
        self._setup_logging()
        self._running = False
        
        # Set up signal handlers
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)
    
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        os.makedirs(os.path.dirname(self._log_path), exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self._log_path),
                logging.StreamHandler()
            ]
        )
    
    def _handle_signal(self, signum, frame):
        """Handle system signals."""
        logging.info(f"Received signal {signum}")
        self._running = False
    
    async def run_pdf_watcher(self) -> None:
        """Run the PDF watcher as a service."""
        self._running = True
        watcher = PDFWatcher(config=self._config)
        
        try:
            await watcher.start(daemon=True)
        except Exception as e:
            logging.error(f"PDF watcher service failed: {str(e)}")
            raise
    
    @staticmethod
    def install_service() -> bool:
        """Install framework as a system service."""
        try:
            if platform.system() == "Linux":
                return ServiceManager._install_linux_service()
            elif platform.system() == "Windows":
                return ServiceManager._install_windows_service()
            else:
                logging.error("Unsupported operating system")
                return False
        except Exception as e:
            logging.error(f"Failed to install service: {str(e)}")
            return False
    
    @staticmethod
    def _install_linux_service() -> bool:
        """Install as Linux systemd service."""
        service_name = "vassure_pdf_watcher"
        service_path = "/etc/systemd/system/vassure_pdf_watcher.service"
        
        service_content = f"""[Unit]
Description=VAssureAI PDF Watcher Service
After=network.target

[Service]
Type=simple
ExecStart={sys.executable} -m vassureai service run
WorkingDirectory={os.getcwd()}
User={os.getenv('USER')}
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
        
        try:
            # Write service file
            with open(service_path, 'w') as f:
                f.write(service_content)
            
            # Set permissions
            os.chmod(service_path, 0o644)
            
            # Reload systemd and enable service
            os.system("systemctl daemon-reload")
            os.system(f"systemctl enable {service_name}")
            
            logging.info(f"Installed Linux service: {service_name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to install Linux service: {str(e)}")
            return False
    
    @staticmethod
    def _install_windows_service() -> bool:
        """Install as Windows service."""
        try:
            import win32serviceutil
            import win32service
            import win32event
            import servicemanager
            
            class VAssureService(win32serviceutil.ServiceFramework):
                _svc_name_ = "VAssurePDFWatcher"
                _svc_display_name_ = "VAssureAI PDF Watcher Service"
                
                def __init__(self, args):
                    win32serviceutil.ServiceFramework.__init__(self, args)
                    self.stop_event = win32event.CreateEvent(None, 0, 0, None)
                    self.service_manager = ServiceManager()
                
                def SvcStop(self):
                    self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
                    win32event.SetEvent(self.stop_event)
                
                def SvcDoRun(self):
                    try:
                        asyncio.run(self.service_manager.run_pdf_watcher())
                    except Exception as e:
                        servicemanager.LogErrorMsg(str(e))
            
            # Install the service
            win32serviceutil.HandleCommandLine(VAssureService)
            logging.info("Installed Windows service: VAssurePDFWatcher")
            return True
            
        except Exception as e:
            logging.error(f"Failed to install Windows service: {str(e)}")
            return False


def run_service() -> None:
    """Run the service directly."""
    service = ServiceManager()
    asyncio.run(service.run_pdf_watcher())


if __name__ == "__main__":
    run_service()