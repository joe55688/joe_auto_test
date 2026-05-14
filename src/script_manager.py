"""Module for managing recorded scripts"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from . import config

logger = logging.getLogger(__name__)


class ScriptManager:
    """Manages recording scripts"""

    def __init__(self, scripts_dir: Path = None):
        """Initialize script manager
        
        Args:
            scripts_dir: Directory to store scripts
        """
        self.scripts_dir = scripts_dir or config.SCRIPTS_DIR
        self.scripts_dir.mkdir(parents=True, exist_ok=True)

    def save_script(self, name: str, events: List[Dict[str, Any]], description: str = "") -> bool:
        """Save a recording script
        
        Args:
            name: Script name
            events: List of recorded events
            description: Optional description
            
        Returns:
            True if successful
        """
        try:
            # Sanitize filename
            safe_name = self._sanitize_filename(name)
            filepath = self.scripts_dir / f"{safe_name}{config.SCRIPT_EXTENSION}"
            
            # Create script metadata
            script_data = {
                'name': name,
                'description': description,
                'created_at': datetime.now().isoformat(),
                'modified_at': datetime.now().isoformat(),
                'event_count': len(events),
                'duration': events[-1]['timestamp'] if events else 0,
                'events': events
            }
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(script_data, f, indent=2)
            
            logger.info(f"Script saved: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving script: {e}")
            return False

    def load_script(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a recording script
        
        Args:
            name: Script name
            
        Returns:
            Script data or None if not found
        """
        try:
            safe_name = self._sanitize_filename(name)
            filepath = self.scripts_dir / f"{safe_name}{config.SCRIPT_EXTENSION}"
            
            if not filepath.exists():
                logger.warning(f"Script not found: {filepath}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                script_data = json.load(f)
            
            logger.info(f"Script loaded: {filepath}")
            return script_data
            
        except Exception as e:
            logger.error(f"Error loading script: {e}")
            return None

    def delete_script(self, name: str) -> bool:
        """Delete a recording script
        
        Args:
            name: Script name
            
        Returns:
            True if successful
        """
        try:
            safe_name = self._sanitize_filename(name)
            filepath = self.scripts_dir / f"{safe_name}{config.SCRIPT_EXTENSION}"
            
            if filepath.exists():
                filepath.unlink()
                logger.info(f"Script deleted: {filepath}")
                return True
            else:
                logger.warning(f"Script not found: {filepath}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting script: {e}")
            return False

    def list_scripts(self) -> List[Dict[str, Any]]:
        """List all available scripts
        
        Returns:
            List of script metadata
        """
        scripts = []
        try:
            for filepath in self.scripts_dir.glob(f"*{config.SCRIPT_EXTENSION}"):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    script_info = {
                        'name': data.get('name', filepath.stem),
                        'description': data.get('description', ''),
                        'created_at': data.get('created_at', ''),
                        'modified_at': data.get('modified_at', ''),
                        'event_count': data.get('event_count', 0),
                        'duration': data.get('duration', 0),
                        'filepath': str(filepath)
                    }
                    scripts.append(script_info)
                    
                except Exception as e:
                    logger.warning(f"Error reading script {filepath}: {e}")
            
            logger.info(f"Found {len(scripts)} scripts")
            return scripts
            
        except Exception as e:
            logger.error(f"Error listing scripts: {e}")
            return []

    def rename_script(self, old_name: str, new_name: str) -> bool:
        """Rename a script
        
        Args:
            old_name: Current script name
            new_name: New script name
            
        Returns:
            True if successful
        """
        try:
            old_safe = self._sanitize_filename(old_name)
            new_safe = self._sanitize_filename(new_name)
            
            old_path = self.scripts_dir / f"{old_safe}{config.SCRIPT_EXTENSION}"
            new_path = self.scripts_dir / f"{new_safe}{config.SCRIPT_EXTENSION}"
            
            if not old_path.exists():
                logger.warning(f"Script not found: {old_path}")
                return False
            
            # Load script
            with open(old_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update name
            data['name'] = new_name
            data['modified_at'] = datetime.now().isoformat()
            
            # Save to new path
            with open(new_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            # Delete old file
            old_path.unlink()
            
            logger.info(f"Script renamed: {old_name} -> {new_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error renaming script: {e}")
            return False

    def export_script(self, name: str, export_path: str) -> bool:
        """Export a script to another location
        
        Args:
            name: Script name
            export_path: Path to export to
            
        Returns:
            True if successful
        """
        try:
            script_data = self.load_script(name)
            if not script_data:
                return False
            
            export_file = Path(export_path)
            export_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(script_data, f, indent=2)
            
            logger.info(f"Script exported to {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting script: {e}")
            return False

    def import_script(self, import_path: str) -> bool:
        """Import a script from another location
        
        Args:
            import_path: Path to import from
            
        Returns:
            True if successful
        """
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                logger.error(f"Import file not found: {import_path}")
                return False
            
            with open(import_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            name = data.get('name', import_file.stem)
            events = data.get('events', [])
            description = data.get('description', '')
            
            return self.save_script(name, events, description)
            
        except Exception as e:
            logger.error(f"Error importing script: {e}")
            return False

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Sanitize filename
        
        Args:
            name: Filename to sanitize
            
        Returns:
            Sanitized filename
        """
        # Remove special characters
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
        sanitized = "".join(c for c in name if c in safe_chars or c == " ")
        sanitized = sanitized.replace(" ", "_")
        return sanitized or "untitled"
