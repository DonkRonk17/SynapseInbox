#!/usr/bin/env python3
"""
SynapseInbox v1.0 - Advanced Inbox Filtering for THE_SYNAPSE

Extends SynapseLink with powerful inbox filtering, search, and management.
Find exactly the messages you need from THE_SYNAPSE instantly!

Author: Atlas (Team Brain)
Requested by: Forge
Date: January 18, 2026
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

VERSION = "1.0.0"

# Default Synapse path
DEFAULT_SYNAPSE_PATH = Path("D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")


@dataclass
class Message:
    """Represents a Synapse message."""
    msg_id: str
    from_agent: str
    to: List[str]
    subject: str
    body: Dict[str, Any]
    priority: str
    timestamp: str
    filepath: Path
    
    def __str__(self):
        return f"{self.from_agent} -> {', '.join(self.to)}: {self.subject} [{self.priority}]"


class SynapseInbox:
    """
    Advanced inbox management for THE_SYNAPSE.
    
    Usage:
        inbox = SynapseInbox(agent_name="ATLAS")
        
        # Get unread messages
        unread = inbox.unread()
        
        # Filter by sender
        from_forge = inbox.filter(from_agent="FORGE")
        
        # Search by keyword
        urgent = inbox.search("urgent")
        
        # Mark as read
        inbox.mark_read(msg_id)
    """
    
    def __init__(self, agent_name: str, synapse_path: Optional[Path] = None):
        """
        Initialize SynapseInbox.
        
        Args:
            agent_name: Name of current agent (for filtering)
            synapse_path: Path to THE_SYNAPSE/active folder
        """
        self.agent_name = agent_name.upper()
        self.synapse_path = synapse_path or DEFAULT_SYNAPSE_PATH
        
        # Read state file (tracks read messages)
        self.state_file = Path.home() / f".synapseinbox_{self.agent_name.lower()}.json"
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """Load inbox state (read messages, etc.)"""
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text())
            except:
                return {"read_messages": [], "archived": []}
        return {"read_messages": [], "archived": []}
    
    def _save_state(self):
        """Save inbox state."""
        self.state_file.write_text(json.dumps(self.state, indent=2))
    
    def _load_message(self, filepath: Path) -> Optional[Message]:
        """Load a message from file."""
        try:
            data = json.loads(filepath.read_text(encoding='utf-8'))
            return Message(
                msg_id=data.get('msg_id', data.get('message_id', filepath.stem)),
                from_agent=data.get('from', data.get('from_agent', 'UNKNOWN')),
                to=data.get('to', []),
                subject=data.get('subject', ''),
                body=data.get('body', {}),
                priority=data.get('priority', 'NORMAL'),
                timestamp=data.get('timestamp', ''),
                filepath=filepath
            )
        except Exception as e:
            print(f"Error loading {filepath.name}: {e}")
            return None
    
    def all_messages(self) -> List[Message]:
        """Get all messages from Synapse."""
        messages = []
        for filepath in self.synapse_path.glob("*.json"):
            msg = self._load_message(filepath)
            if msg:
                messages.append(msg)
        
        # Sort by timestamp (newest first)
        messages.sort(key=lambda m: m.timestamp, reverse=True)
        return messages
    
    def filter(self,
               from_agent: Optional[str] = None,
               to_agent: Optional[str] = None,
               priority: Optional[str] = None,
               unread_only: bool = False,
               include_archived: bool = False) -> List[Message]:
        """
        Filter messages by criteria.
        
        Args:
            from_agent: Filter by sender
            to_agent: Filter by recipient (defaults to current agent if not specified)
            priority: Filter by priority level
            unread_only: Only show unread messages
            include_archived: Include archived messages
        
        Returns:
            List of matching Message objects
        """
        messages = self.all_messages()
        results = []
        
        # Default to_agent is current agent
        if to_agent is None and not from_agent:
            to_agent = self.agent_name
        
        for msg in messages:
            # Skip archived unless requested
            if not include_archived and msg.msg_id in self.state.get("archived", []):
                continue
            
            # Apply filters
            if from_agent and msg.from_agent != from_agent.upper():
                continue
            
            if to_agent:
                to_list = msg.to if isinstance(msg.to, list) else [msg.to]
                if to_agent.upper() not in to_list and "ALL_AGENTS" not in to_list:
                    continue
            
            if priority and msg.priority != priority.upper():
                continue
            
            if unread_only and msg.msg_id in self.state.get("read_messages", []):
                continue
            
            results.append(msg)
        
        return results
    
    def search(self, query: str, in_body: bool = True) -> List[Message]:
        """
        Search messages by keyword.
        
        Args:
            query: Search term
            in_body: Also search in message body (not just subject)
        
        Returns:
            List of matching messages
        """
        messages = self.all_messages()
        results = []
        query_lower = query.lower()
        
        for msg in messages:
            # Search in subject
            if query_lower in msg.subject.lower():
                results.append(msg)
                continue
            
            # Search in body if requested
            if in_body:
                body_str = json.dumps(msg.body).lower()
                if query_lower in body_str:
                    results.append(msg)
        
        return results
    
    def unread(self, to_me_only: bool = True) -> List[Message]:
        """Get unread messages."""
        return self.filter(
            to_agent=self.agent_name if to_me_only else None,
            unread_only=True
        )
    
    def unread_count(self, to_me_only: bool = True) -> int:
        """Count unread messages."""
        return len(self.unread(to_me_only=to_me_only))
    
    def mark_read(self, msg_id: str):
        """Mark message as read."""
        if msg_id not in self.state.get("read_messages", []):
            self.state.setdefault("read_messages", []).append(msg_id)
            self._save_state()
    
    def mark_unread(self, msg_id: str):
        """Mark message as unread."""
        if msg_id in self.state.get("read_messages", []):
            self.state["read_messages"].remove(msg_id)
            self._save_state()
    
    def archive(self, msg_id: str):
        """Archive a message (hides from default views)."""
        if msg_id not in self.state.get("archived", []):
            self.state.setdefault("archived", []).append(msg_id)
            self._save_state()
    
    def unarchive(self, msg_id: str):
        """Unarchive a message."""
        if msg_id in self.state.get("archived", []):
            self.state["archived"].remove(msg_id)
            self._save_state()
    
    def get_by_id(self, msg_id: str) -> Optional[Message]:
        """Get specific message by ID."""
        for msg in self.all_messages():
            if msg.msg_id == msg_id:
                return msg
        return None


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="SynapseInbox - Advanced Synapse message filtering",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('command', choices=['unread', 'from', 'search', 'list', 'mark-read', 'archive'],
                        help='Command to execute')
    parser.add_argument('--agent', required=True, help='Your agent name (ATLAS, FORGE, etc.)')
    parser.add_argument('--from', dest='from_agent', help='Filter by sender')
    parser.add_argument('--to', help='Filter by recipient')
    parser.add_argument('--priority', choices=['LOW', 'NORMAL', 'HIGH', 'CRITICAL'], help='Filter by priority')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--id', dest='msg_id', help='Message ID')
    parser.add_argument('--all', action='store_true', help='Include all agents (not just messages to you)')
    parser.add_argument('--version', action='version', version=f'SynapseInbox {VERSION}')
    
    args = parser.parse_args()
    
    inbox = SynapseInbox(agent_name=args.agent)
    
    if args.command == 'unread':
        messages = inbox.unread(to_me_only=not args.all)
        print(f"\n📬 UNREAD MESSAGES ({len(messages)}):\n")
        for msg in messages:
            print(f"  [{msg.priority}] {msg}")
        print()
    
    elif args.command == 'from':
        if not args.from_agent:
            print("ERROR: --from required")
            return 1
        messages = inbox.filter(from_agent=args.from_agent)
        print(f"\n📨 FROM {args.from_agent} ({len(messages)}):\n")
        for msg in messages:
            print(f"  [{msg.priority}] {msg.subject}")
        print()
    
    elif args.command == 'search':
        if not args.query:
            print("ERROR: --query required")
            return 1
        messages = inbox.search(args.query)
        print(f"\n🔍 SEARCH '{args.query}' ({len(messages)} results):\n")
        for msg in messages:
            print(f"  {msg}")
        print()
    
    elif args.command == 'list':
        messages = inbox.filter(
            from_agent=args.from_agent,
            to_agent=args.to,
            priority=args.priority
        )
        print(f"\n📋 MESSAGES ({len(messages)}):\n")
        for msg in messages:
            status = "✓" if msg.msg_id in inbox.state.get("read_messages", []) else "○"
            print(f"  {status} [{msg.priority}] {msg}")
        print()
    
    elif args.command == 'mark-read':
        if not args.msg_id:
            print("ERROR: --id required")
            return 1
        inbox.mark_read(args.msg_id)
        print(f"[OK] Marked {args.msg_id} as read")
    
    elif args.command == 'archive':
        if not args.msg_id:
            print("ERROR: --id required")
            return 1
        inbox.archive(args.msg_id)
        print(f"[OK] Archived {args.msg_id}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
