# SynapseInbox Examples

**10 Real-World Examples for Synapse Message Management**

---

## Example 1: Check Unread Messages

```python
from synapseinbox import SynapseInbox

inbox = SynapseInbox(agent_name="ATLAS")
unread = inbox.unread()

print(f"You have {len(unread)} unread messages:")
for msg in unread:
    print(f"  [{msg.priority}] {msg.from_agent}: {msg.subject}")
```

**Output:**
```
You have 5 unread messages:
  [HIGH] FORGE: Review SynapseWatcher spec
  [NORMAL] BOLT: Test results ready
  [NORMAL] CLIO: Documentation updated
  [HIGH] LOGAN_BCH: AC Protocol - Check now
  [LOW] NEXUS: Status update
```

**Use case:** Morning inbox check - see what needs attention.

---

## Example 2: Filter by Sender

```python
from synapseinbox import SynapseInbox

inbox = SynapseInbox(agent_name="ATLAS")

# Get all messages from Forge
from_forge = inbox.filter(from_agent="FORGE")

print(f"Messages from Forge: {len(from_forge)}")
for msg in from_forge[:5]:  # Show first 5
    print(f"  {msg.timestamp[:10]}: {msg.subject}")
```

**Output:**
```
Messages from Forge: 23
  2026-01-18: Review SynapseWatcher spec
  2026-01-17: SynapseLink approval needed
  2026-01-17: Tool integration plan
  2026-01-16: Q-Mode roadmap feedback
  2026-01-15: ContextCompressor testing
```

**Use case:** Review all communications from your orchestrator.

---

## Example 3: Search by Keyword

```python
from synapseinbox import SynapseInbox

inbox = SynapseInbox(agent_name="ATLAS")

# Find messages about SynapseWatcher
watcher_msgs = inbox.search("SynapseWatcher")

print(f"Found {len(watcher_msgs)} messages about SynapseWatcher:")
for msg in watcher_msgs:
    print(f"  {msg.from_agent} ({msg.timestamp[:10]}): {msg.subject}")
```

**Output:**
```
Found 7 messages about SynapseWatcher:
  FORGE (2026-01-18): Review SynapseWatcher spec
  BOLT (2026-01-18): SynapseWatcher testing complete
  FORGE (2026-01-17): SynapseWatcher integration targets
  CLIO (2026-01-17): SynapseWatcher documentation needed
  FORGE (2026-01-16): Build SynapseWatcher tool
  ATLAS (2026-01-16): SynapseWatcher v1.0 deployed
  LOGAN (2026-01-16): SynapseWatcher approved
```

**Use case:** Find all messages related to specific project or topic.

---

## Example 4: Priority-Based Workflow

```python
from synapseinbox import SynapseInbox

inbox = SynapseInbox(agent_name="ATLAS")

# Process by priority - urgent first
print("=== URGENT (HIGH/CRITICAL) ===")
urgent = inbox.filter(priority="HIGH", unread_only=True)
for msg in urgent:
    print(f"⚡ {msg.from_agent}: {msg.subject}")
    # Handle urgent message...
    inbox.mark_read(msg.msg_id)

print("\n=== NORMAL PRIORITY ===")
normal = inbox.filter(priority="NORMAL", unread_only=True)
for msg in normal[:3]:  # Top 3
    print(f"📋 {msg.from_agent}: {msg.subject}")

print("\n=== LOW PRIORITY (later) ===")
low = inbox.filter(priority="LOW", unread_only=True)
print(f"📌 {len(low)} low-priority messages to review later")
```

**Output:**
```
=== URGENT (HIGH/CRITICAL) ===
⚡ FORGE: Review SynapseWatcher spec
⚡ LOGAN_BCH: AC Protocol - Check now

=== NORMAL PRIORITY ===
📋 BOLT: Test results ready
📋 CLIO: Documentation updated
📋 NEXUS: Integration complete

=== LOW PRIORITY (later) ===
📌 3 low-priority messages to review later
```

**Use case:** Efficient priority-based workflow - urgent first, low priority later.

---

## Example 5: Messages Directed at You

```python
from synapseinbox import SynapseInbox

inbox = SynapseInbox(agent_name="ATLAS")

# Get messages specifically to you (not ALL_AGENTS broadcasts)
to_me = inbox.filter(to_agent="ATLAS")

direct_messages = [m for m in to_me if "ALL_AGENTS" not in m.to]

print(f"Direct messages to you: {len(direct_messages)}")
for msg in direct_messages[:5]:
    print(f"  {msg.from_agent}: {msg.subject}")
```

**Output:**
```
Direct messages to you: 12
  FORGE: Review SynapseWatcher spec
  BOLT: Need code review on PR #45
  LOGAN: Great work on ContextCompressor
  CLIO: Question about documentation
  BOLT: Test failed - need help
```

**Use case:** See what requires your specific attention vs team announcements.

---

## Example 6: Inbox Zero Workflow

```python
from synapseinbox import SynapseInbox
from datetime import datetime, timedelta

inbox = SynapseInbox(agent_name="ATLAS")

# Get all unread
unread = inbox.unread()
print(f"Processing {len(unread)} unread messages...")

processed = 0
for msg in unread:
    # Process the message
    print(f"Processing: {msg.from_agent} - {msg.subject}")
    
    # Do the work...
    # ...
    
    # Mark as read
    inbox.mark_read(msg.msg_id)
    processed += 1
    
    # Archive if older than 7 days
    msg_date = datetime.fromisoformat(msg.timestamp)
    if datetime.now() - msg_date > timedelta(days=7):
        inbox.archive(msg.msg_id)
        print(f"  ✅ Archived (old message)")
    else:
        print(f"  ✅ Marked as read")

print(f"\n🎉 Inbox Zero! Processed {processed} messages.")
```

**Output:**
```
Processing 5 unread messages...
Processing: FORGE - Review SynapseWatcher spec
  ✅ Marked as read
Processing: BOLT - Test results ready
  ✅ Marked as read
Processing: CLIO - Documentation updated
  ✅ Archived (old message)
Processing: LOGAN_BCH - AC Protocol - Check now
  ✅ Marked as read
Processing: NEXUS - Status update
  ✅ Archived (old message)

🎉 Inbox Zero! Processed 5 messages.
```

**Use case:** Systematically clear your inbox and achieve inbox zero.

---

## Example 7: Communication Analytics

```python
from synapseinbox import SynapseInbox

inbox = SynapseInbox(agent_name="ATLAS")
stats = inbox.stats()

print("📊 INBOX STATISTICS\n")

print(f"Total messages: {stats['total']}")
print(f"Unread: {stats['unread']} ({stats['unread']/stats['total']*100:.1f}%)")
print(f"Archived: {stats['archived']}")

print("\n📨 Top communicators:")
sorted_senders = sorted(stats['by_sender'].items(), key=lambda x: x[1], reverse=True)
for agent, count in sorted_senders[:5]:
    print(f"  {agent}: {count} messages")

print("\n⚡ Priority breakdown:")
for priority in ["CRITICAL", "HIGH", "NORMAL", "LOW"]:
    count = stats['by_priority'].get(priority, 0)
    if count > 0:
        print(f"  {priority}: {count}")

print("\n📬 Messages to:")
for recipient, count in stats['by_recipient'].items():
    print(f"  {recipient}: {count}")
```

**Output:**
```
📊 INBOX STATISTICS

Total messages: 225
Unread: 12 (5.3%)
Archived: 87

📨 Top communicators:
  BOLT: 67 messages
  FORGE: 45 messages
  LOGAN_BCH: 38 messages
  CLIO: 28 messages
  NEXUS: 23 messages

⚡ Priority breakdown:
  CRITICAL: 2
  HIGH: 23
  NORMAL: 180
  LOW: 20

📬 Messages to:
  ALL_AGENTS: 136
  ATLAS: 89
```

**Use case:** Understand your communication patterns and volume.

---

## Example 8: Combine Filters

```python
from synapseinbox import SynapseInbox

inbox = SynapseInbox(agent_name="ATLAS")

# Complex query: Unread HIGH priority messages from Forge
forge_urgent_unread = inbox.filter(
    from_agent="FORGE",
    priority="HIGH",
    unread_only=True
)

print(f"🔥 Urgent unread from Forge: {len(forge_urgent_unread)}")
for msg in forge_urgent_unread:
    print(f"  {msg.timestamp[:10]}: {msg.subject}")

# Then search within those results
integration_related = [m for m in forge_urgent_unread if "integration" in m.subject.lower()]
print(f"\n🔗 Of those, {len(integration_related)} are about integration")
```

**Output:**
```
🔥 Urgent unread from Forge: 2
  2026-01-18: Review SynapseWatcher spec
  2026-01-17: Tool integration plan

🔗 Of those, 1 are about integration
```

**Use case:** Complex filtering for very specific message queries.

---

## Example 9: Archive Management

```python
from synapseinbox import SynapseInbox
from datetime import datetime, timedelta

inbox = SynapseInbox(agent_name="ATLAS")

# Archive all low-priority messages older than 30 days
cutoff = datetime.now() - timedelta(days=30)

old_low_priority = inbox.filter(priority="LOW", include_archived=False)
archived_count = 0

for msg in old_low_priority:
    msg_date = datetime.fromisoformat(msg.timestamp)
    if msg_date < cutoff:
        inbox.archive(msg.msg_id)
        archived_count += 1

print(f"📁 Archived {archived_count} old low-priority messages")

# View archived messages
archived = inbox.filter(include_archived=True)
all_archived = [m for m in archived if m.msg_id in inbox.state['archived']]
print(f"Total archived: {len(all_archived)}")
```

**Output:**
```
📁 Archived 15 old low-priority messages
Total archived: 102
```

**Use case:** Clean up old messages while keeping them accessible.

---

## Example 10: Automated Monitoring

```python
from synapseinbox import SynapseInbox
from synapsewatcher import SynapseWatcher

def auto_inbox_check():
    """Automatically check inbox and alert on urgent messages."""
    inbox = SynapseInbox(agent_name="ATLAS")
    
    # Check unread urgent
    urgent = inbox.filter(priority="HIGH", unread_only=True)
    critical = inbox.filter(priority="CRITICAL", unread_only=True)
    
    if critical:
        print(f"🚨 CRITICAL: {len(critical)} critical unread messages!")
        for msg in critical:
            print(f"  {msg.from_agent}: {msg.subject}")
    
    elif urgent:
        print(f"⚡ {len(urgent)} urgent unread messages")
        for msg in urgent:
            print(f"  {msg.from_agent}: {msg.subject}")
    
    # Check messages from orchestrator
    forge_unread = inbox.filter(from_agent="FORGE", unread_only=True)
    if forge_unread:
        print(f"📋 {len(forge_unread)} unread messages from Forge (orchestrator)")
    
    # Stats summary
    stats = inbox.stats()
    print(f"\n📊 Inbox: {stats['unread']} unread of {stats['total']} total")

# Run every 5 minutes
watcher = SynapseWatcher()
watcher.add_callback(auto_inbox_check, interval=300)
print("🤖 Automated inbox monitoring started!")
watcher.start()
```

**Output:**
```
🤖 Automated inbox monitoring started!

[5 minutes later]
⚡ 2 urgent unread messages
  FORGE: Review SynapseWatcher spec
  LOGAN_BCH: AC Protocol - Check now
📋 1 unread messages from Forge (orchestrator)

📊 Inbox: 5 unread of 225 total

[5 minutes later]
📊 Inbox: 3 unread of 227 total
```

**Use case:** Continuous automated inbox monitoring for urgent items.

---

## Command Line Examples

```bash
# Check unread messages
python synapseinbox.py unread --agent ATLAS

# Messages from Forge
python synapseinbox.py from FORGE --agent ATLAS

# Unread messages from Forge
python synapseinbox.py from FORGE --agent ATLAS --unread

# Search for keyword
python synapseinbox.py search "SynapseWatcher" --agent ATLAS

# High priority messages
python synapseinbox.py list --agent ATLAS --priority HIGH

# Mark specific message as read
python synapseinbox.py mark-read cursor_forge_2026-01-18_058 --agent ATLAS

# Mark all as read
python synapseinbox.py mark-all-read --agent ATLAS

# View statistics
python synapseinbox.py stats --agent ATLAS

# Archive old message
python synapseinbox.py archive old_msg_123 --agent ATLAS

# Reset state (clear read/archived tracking)
python synapseinbox.py clear-state --agent ATLAS
```

---

## Integration Examples

### With SynapseLink (Send/Receive)

```python
from synapselink import SynapseLink
from synapseinbox import SynapseInbox

# Forge sends message
synapse = SynapseLink()
synapse.send_message(
    to="ATLAS",
    subject="Review SynapseWatcher",
    body={"task": "code_review", "priority": "high"}
)

# Atlas receives and processes
inbox = SynapseInbox(agent_name="ATLAS")
new_msgs = inbox.unread()
for msg in new_msgs:
    if "SynapseWatcher" in msg.subject:
        print(f"Got it! {msg.subject}")
        inbox.mark_read(msg.msg_id)
```

### With TaskQueuePro

```python
from synapseinbox import SynapseInbox
from taskqueuepro import TaskQueuePro

# Check inbox, create tasks for urgent messages
inbox = SynapseInbox(agent_name="ATLAS")
queue = TaskQueuePro()

urgent_unread = inbox.filter(priority="HIGH", unread_only=True)
for msg in urgent_unread:
    # Create task from message
    queue.add_task(
        title=f"Handle: {msg.subject}",
        description=f"From {msg.from_agent}",
        assigned_to="ATLAS",
        priority="HIGH",
        metadata={"msg_id": msg.msg_id}
    )
    inbox.mark_read(msg.msg_id)

print(f"Created {len(urgent_unread)} tasks from urgent messages")
```

---

**Need more examples?** Check the main [README.md](README.md) for detailed API documentation.
