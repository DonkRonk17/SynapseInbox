# SynapseInbox

**Advanced Inbox Filtering for THE_SYNAPSE**

Extends SynapseLink with powerful inbox management - filter, search, and organize your Synapse messages like a pro!

---

## ⚡ Features

- **Unread Tracking** - Never miss a message
- **Smart Filtering** - By sender, recipient, priority
- **Keyword Search** - Find messages instantly
- **Archive System** - Hide old messages
- **Read/Unread Status** - Track what you've seen
- **Zero Dependencies** - Pure Python standard library

---

## 🚀 Quick Start

```python
from synapseinbox import SynapseInbox

# Initialize for your agent
inbox = SynapseInbox(agent_name="ATLAS")

# Check unread messages
unread = inbox.unread()
print(f"{len(unread)} unread messages")

# Filter by sender
from_forge = inbox.filter(from_agent="FORGE")

# Search by keyword
urgent_msgs = inbox.search("urgent")

# Mark as read
inbox.mark_read(msg.msg_id)
```

---

## 💻 CLI Usage

```bash
# Check unread messages
python synapseinbox.py unread --agent ATLAS

# Messages from specific agent
python synapseinbox.py from --agent ATLAS --from FORGE

# Search messages
python synapseinbox.py search --agent ATLAS --query "urgent"

# List with filters
python synapseinbox.py list --agent ATLAS --priority HIGH

# Mark as read
python synapseinbox.py mark-read --agent ATLAS --id msg_001
```

---

## 🙏 Credits

**Built by:** Atlas (Team Brain)  
**Requested by:** Forge (SynapseLink enhancement)  
**For:** Logan Smith / Metaphy LLC  
**Date:** January 18, 2026

**SynapseInbox** - Inbox Zero for AI Agents! 📬
