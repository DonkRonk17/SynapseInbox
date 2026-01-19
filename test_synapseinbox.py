#!/usr/bin/env python3
"""
Comprehensive test suite for SynapseInbox v1.0

Tests:
- Message loading and parsing
- Filtering (by sender, recipient, priority)
- Searching
- Read/unread tracking
- Archive functionality
- Statistics
- State persistence

Author: Atlas (Team Brain)
Date: January 18, 2026
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
from synapseinbox import SynapseInbox, Message


class TestSynapseInbox(unittest.TestCase):
    """Test suite for SynapseInbox."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary Synapse directory
        self.test_synapse = Path(tempfile.mkdtemp())
        
        # Create test messages
        self.test_messages = [
            {
                "msg_id": "test_001",
                "from": "FORGE",
                "to": ["ATLAS"],
                "subject": "Test Message 1",
                "body": {"content": "This is a test"},
                "priority": "HIGH",
                "timestamp": "2026-01-18T10:00:00"
            },
            {
                "msg_id": "test_002",
                "from": "BOLT",
                "to": ["ATLAS", "ALL_AGENTS"],
                "subject": "Test Message 2",
                "body": {"content": "Another test"},
                "priority": "NORMAL",
                "timestamp": "2026-01-18T11:00:00"
            },
            {
                "msg_id": "test_003",
                "from": "CLIO",
                "to": ["ALL_AGENTS"],
                "subject": "Broadcast Test",
                "body": {"content": "Broadcast message"},
                "priority": "LOW",
                "timestamp": "2026-01-18T12:00:00"
            },
            {
                "msg_id": "test_004",
                "from": "FORGE",
                "to": ["ATLAS"],
                "subject": "Urgent Task",
                "body": {"content": "This is urgent"},
                "priority": "CRITICAL",
                "timestamp": "2026-01-18T13:00:00"
            }
        ]
        
        # Write test messages to temp directory
        for msg in self.test_messages:
            msg_file = self.test_synapse / f"{msg['msg_id']}.json"
            msg_file.write_text(json.dumps(msg, indent=2))
        
        # Create temporary state directory
        self.test_state_dir = Path(tempfile.mkdtemp())
        self.original_home = Path.home
        Path.home = lambda: self.test_state_dir
        
        # Initialize inbox
        self.inbox = SynapseInbox(
            agent_name="ATLAS",
            synapse_path=self.test_synapse
        )
    
    def tearDown(self):
        """Clean up test environment."""
        # Restore Path.home
        Path.home = self.original_home
        
        # Remove temporary directories
        shutil.rmtree(self.test_synapse, ignore_errors=True)
        shutil.rmtree(self.test_state_dir, ignore_errors=True)
    
    def test_01_load_all_messages(self):
        """Test loading all messages."""
        messages = self.inbox.all_messages()
        self.assertEqual(len(messages), 4)
        self.assertIsInstance(messages[0], Message)
    
    def test_02_filter_by_sender(self):
        """Test filtering by sender."""
        from_forge = self.inbox.filter(from_agent="FORGE")
        self.assertEqual(len(from_forge), 2)
        for msg in from_forge:
            self.assertEqual(msg.from_agent, "FORGE")
    
    def test_03_filter_by_recipient(self):
        """Test filtering by recipient."""
        to_atlas = self.inbox.filter(to_agent="ATLAS")
        # Should include messages directly to ATLAS and ALL_AGENTS
        self.assertGreaterEqual(len(to_atlas), 2)
    
    def test_04_filter_by_priority(self):
        """Test filtering by priority."""
        high_priority = self.inbox.filter(priority="HIGH")
        self.assertEqual(len(high_priority), 1)
        self.assertEqual(high_priority[0].priority, "HIGH")
        
        critical = self.inbox.filter(priority="CRITICAL")
        self.assertEqual(len(critical), 1)
    
    def test_05_search_by_keyword(self):
        """Test searching by keyword."""
        test_results = self.inbox.search("test")
        self.assertGreaterEqual(len(test_results), 2)
        
        urgent_results = self.inbox.search("urgent")
        self.assertEqual(len(urgent_results), 1)
        self.assertIn("Urgent", urgent_results[0].subject)
    
    def test_06_unread_tracking(self):
        """Test unread message tracking."""
        # All messages should be unread initially
        unread = self.inbox.unread()
        self.assertEqual(len(unread), 4)
        
        # Mark one as read
        self.inbox.mark_read("test_001")
        unread = self.inbox.unread()
        self.assertEqual(len(unread), 3)
        
        # Mark another as read
        self.inbox.mark_read("test_002")
        unread = self.inbox.unread()
        self.assertEqual(len(unread), 2)
    
    def test_07_mark_multiple_read(self):
        """Test marking multiple messages as read."""
        # Mark all messages as read manually
        for msg in self.inbox.all_messages():
            self.inbox.mark_read(msg.msg_id)
        
        unread = self.inbox.unread()
        self.assertEqual(len(unread), 0)
    
    def test_08_archive_functionality(self):
        """Test archive functionality."""
        # Archive a message
        self.inbox.archive("test_003")
        
        # Should not appear in default filter
        messages = self.inbox.filter()
        msg_ids = [m.msg_id for m in messages]
        self.assertNotIn("test_003", msg_ids)
        
        # Should appear when including archived
        messages_with_archived = self.inbox.filter(include_archived=True)
        msg_ids_with_archived = [m.msg_id for m in messages_with_archived]
        self.assertIn("test_003", msg_ids_with_archived)
    
    def test_09_unarchive(self):
        """Test unarchive functionality."""
        # Archive then unarchive
        self.inbox.archive("test_004")
        self.inbox.unarchive("test_004")
        
        # Should appear in default filter again
        messages = self.inbox.filter()
        msg_ids = [m.msg_id for m in messages]
        self.assertIn("test_004", msg_ids)
    
    def test_10_filter_unread_only(self):
        """Test filtering unread messages only."""
        # Mark some as read
        self.inbox.mark_read("test_001")
        self.inbox.mark_read("test_002")
        
        # Filter unread from FORGE
        unread_from_forge = self.inbox.filter(from_agent="FORGE", unread_only=True)
        # FORGE sent test_001 (read) and test_004 (unread)
        self.assertEqual(len(unread_from_forge), 1)
        self.assertEqual(unread_from_forge[0].msg_id, "test_004")
    
    def test_11_unread_count(self):
        """Test unread count functionality."""
        # Initially all 4 messages are unread
        count = self.inbox.unread_count()
        self.assertEqual(count, 4)
        
        # Mark some as read
        self.inbox.mark_read("test_001")
        self.inbox.mark_read("test_002")
        
        count = self.inbox.unread_count()
        # 4 total - 2 read = 2 unread
        self.assertEqual(count, 2)
        
        # Archive one unread message
        self.inbox.archive("test_003")
        
        count = self.inbox.unread_count()
        # Archived messages don't appear in unread count
        # 2 unread - 1 archived = 1 unread showing
        self.assertEqual(count, 1)
    
    def test_12_state_persistence(self):
        """Test that state persists across instances."""
        # Mark 2 messages as read, archive 1 unread message
        self.inbox.mark_read("test_001")
        self.inbox.mark_read("test_002")
        self.inbox.archive("test_003")  # Archive unread message
        
        # Create new instance
        new_inbox = SynapseInbox(
            agent_name="ATLAS",
            synapse_path=self.test_synapse
        )
        
        # State should be preserved
        unread = new_inbox.unread()
        # 4 total - 2 read - 1 archived = 1 unread showing
        self.assertEqual(len(unread), 1)
        
        messages = new_inbox.filter()
        msg_ids = [m.msg_id for m in messages]
        self.assertNotIn("test_003", msg_ids)  # Should be archived
    
    def test_13_combined_filters(self):
        """Test combining multiple filters."""
        # Mark test_004 as unread (it is by default)
        # Filter: from FORGE, HIGH or CRITICAL priority, unread
        results = self.inbox.filter(
            from_agent="FORGE",
            unread_only=True
        )
        
        # Should get both FORGE messages (test_001 HIGH, test_004 CRITICAL)
        self.assertEqual(len(results), 2)
        
        # Now mark test_001 as read
        self.inbox.mark_read("test_001")
        
        results = self.inbox.filter(
            from_agent="FORGE",
            unread_only=True
        )
        
        # Should only get test_004
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].msg_id, "test_004")
    
    def test_14_case_insensitive_search(self):
        """Test that search is case-insensitive."""
        results_upper = self.inbox.search("TEST")
        results_lower = self.inbox.search("test")
        results_mixed = self.inbox.search("Test")
        
        self.assertEqual(len(results_upper), len(results_lower))
        self.assertEqual(len(results_lower), len(results_mixed))
    
    def test_15_empty_synapse(self):
        """Test handling of empty Synapse directory."""
        empty_synapse = Path(tempfile.mkdtemp())
        
        try:
            empty_inbox = SynapseInbox(
                agent_name="ATLAS",
                synapse_path=empty_synapse
            )
            
            messages = empty_inbox.all_messages()
            self.assertEqual(len(messages), 0)
            
            unread = empty_inbox.unread()
            self.assertEqual(len(unread), 0)
            
            count = empty_inbox.unread_count()
            self.assertEqual(count, 0)
        finally:
            shutil.rmtree(empty_synapse, ignore_errors=True)
    
    def test_16_malformed_message(self):
        """Test handling of malformed message files."""
        # Create a malformed message
        bad_msg = self.test_synapse / "bad_message.json"
        bad_msg.write_text("{ this is not valid json ]")
        
        # Should handle gracefully
        messages = self.inbox.all_messages()
        # Should still get the 4 valid messages
        self.assertEqual(len(messages), 4)
    
    def test_17_priority_levels(self):
        """Test all priority levels."""
        priorities = ["CRITICAL", "HIGH", "NORMAL", "LOW"]
        
        for priority in priorities:
            results = self.inbox.filter(priority=priority)
            self.assertIsInstance(results, list)
            for msg in results:
                self.assertEqual(msg.priority, priority)
    
    def test_18_message_string_representation(self):
        """Test Message __str__ method."""
        messages = self.inbox.all_messages()
        msg_str = str(messages[0])
        
        # Should contain sender, recipient, subject, priority
        self.assertIn("->", msg_str)
        self.assertIn("[", msg_str)
        self.assertIn("]", msg_str)


def run_tests():
    """Run all tests."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSynapseInbox)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    if result.wasSuccessful():
        print(f"[SUCCESS] All {result.testsRun} tests passed!")
    else:
        print(f"[FAILED] {len(result.failures)} failures, {len(result.errors)} errors")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
