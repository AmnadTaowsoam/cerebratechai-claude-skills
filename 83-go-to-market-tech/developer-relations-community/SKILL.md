---
name: Developer Relations & Community
description: Building and managing developer communities, advocacy programs, and technical content
---

# Developer Relations & Community

## Current Level: Expert (Enterprise Scale)

## Domain: Go-to-Market Tech
## Skill ID: 146

---

## Executive Summary

Developer Relations & Community enables building and managing developer communities, advocacy programs, and technical content to drive adoption and engagement. This capability is essential for growing developer ecosystems, fostering advocacy, and driving product adoption.

### Strategic Necessity

- **Community Growth**: Build and grow developer communities
- **Developer Advocacy**: Create advocate programs
- **Content Creation**: Produce technical content
- **Engagement**: Drive developer engagement
- **Adoption**: Increase product adoption

---

## Technical Deep Dive

### Community Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Developer Relations & Community Framework               │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │   Community  │    │   Advocacy   │    │   Content    │                  │
│  │   Building  │───▶│   Programs   │───▶│   Creation   │                  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                  │
│         │                   │                   │                           │
│         ▼                   ▼                   ▼                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Engagement Channels                            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Forums   │  │  Discord  │  │  Slack    │  │  Meetups  │            │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │   │
│  └───────┼────────────┼────────────┼────────────┼────────────────────┘   │
│          │            │            │            │                         │
│          ▼            ▼            ▼            ▼                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Measurement & Analytics                        │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Metrics  │  │  Analytics│  │  Feedback │  │  Insights  │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Community Building

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CommunityType(Enum):
    """Community types"""
    FORUM = "forum"
    DISCORD = "discord"
    SLACK = "slack"
    MEETUP = "meetup"
    GITHUB = "github"
    STACK_OVERFLOW = "stack_overflow"

class MemberRole(Enum):
    """Member roles"""
    MEMBER = "member"
    CONTRIBUTOR = "contributor"
    MODERATOR = "moderator"
    ADVOCATE = "advocate"
    AMBASSADOR = "ambassador"

@dataclass
class CommunityMember:
    """Community member definition"""
    member_id: str
    name: str
    email: str
    role: MemberRole
    joined_at: str
    last_active: str
    contributions: int
    reputation: int

@dataclass
class Community:
    """Community definition"""
    community_id: str
    name: str
    description: str
    community_type: CommunityType
    members: List[CommunityMember]
    metrics: Dict[str, Any]
    created_at: str
    updated_at: str

class CommunityBuilder:
    """Community building specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.community_store = CommunityStore(config['community_store'])
        self.forum_manager = ForumManager(config['forum'])
        self.discord_manager = DiscordManager(config['discord'])
        self.slack_manager = SlackManager(config['slack'])
        self.meetup_manager = MeetupManager(config['meetup'])
        
    async def build_community(
        self,
        name: str,
        description: str,
        community_type: CommunityType
    ) -> Community:
        """Build new developer community"""
        logger.info(f"Building community: {name}")
        
        # Generate community ID
        community_id = self._generate_community_id()
        
        # Create community platform
        await self._create_community_platform(community_id, name, community_type)
        
        # Setup community structure
        await self._setup_community_structure(community_id, community_type)
        
        # Create community
        community = Community(
            community_id=community_id,
            name=name,
            description=description,
            community_type=community_type,
            members=[],
            metrics={},
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        
        # Store community
        await self.community_store.create_community(community)
        
        logger.info(f"Community built: {community_id}")
        
        return community
    
    async def _create_community_platform(
        self,
        community_id: str,
        name: str,
        community_type: CommunityType
    ):
        """Create community platform"""
        if community_type == CommunityType.FORUM:
            await self.forum_manager.create_forum(community_id, name)
        elif community_type == CommunityType.DISCORD:
            await self.discord_manager.create_server(community_id, name)
        elif community_type == CommunityType.SLACK:
            await self.slack_manager.create_workspace(community_id, name)
        elif community_type == CommunityType.MEETUP:
            await self.meetup_manager.create_group(community_id, name)
    
    async def _setup_community_structure(
        self,
        community_id: str,
        community_type: CommunityType
    ):
        """Setup community structure"""
        # Create channels/categories
        await self._create_channels(community_id, community_type)
        
        # Create roles/permissions
        await self._create_roles(community_id, community_type)
        
        # Setup moderation
        await self._setup_moderation(community_id, community_type)
        
        # Setup automation
        await self._setup_automation(community_id, community_type)
    
    async def _create_channels(
        self,
        community_id: str,
        community_type: CommunityType
    ):
        """Create community channels"""
        if community_type == CommunityType.DISCORD:
            await self.discord_manager.create_channels(community_id, [
                {'name': 'general', 'type': 'text'},
                {'name': 'introductions', 'type': 'text'},
                {'name': 'help', 'type': 'text'},
                {'name': 'announcements', 'type': 'text'},
                {'name': 'showcase', 'type': 'text'},
                {'name': 'voice', 'type': 'voice'}
            ])
        elif community_type == CommunityType.SLACK:
            await self.slack_manager.create_channels(community_id, [
                {'name': 'general', 'type': 'channel'},
                {'name': 'introductions', 'type': 'channel'},
                {'name': 'help', 'type': 'channel'},
                {'name': 'announcements', 'type': 'channel'},
                {'name': 'showcase', 'type': 'channel'}
            ])
    
    async def _create_roles(
        self,
        community_id: str,
        community_type: CommunityType
    ):
        """Create community roles"""
        if community_type == CommunityType.DISCORD:
            await self.discord_manager.create_roles(community_id, [
                {'name': 'Member', 'permissions': ['read_messages', 'send_messages']},
                {'name': 'Contributor', 'permissions': ['read_messages', 'send_messages', 'embed_links']},
                {'name': 'Moderator', 'permissions': ['read_messages', 'send_messages', 'manage_messages']},
                {'name': 'Advocate', 'permissions': ['read_messages', 'send_messages', 'manage_channels']},
                {'name': 'Ambassador', 'permissions': ['read_messages', 'send_messages', 'manage_roles']}
            ])
    
    async def _setup_moderation(
        self,
        community_id: str,
        community_type: CommunityType
    ):
        """Setup community moderation"""
        # Create moderation rules
        await self._create_moderation_rules(community_id, community_type)
        
        # Setup spam filtering
        await self._setup_spam_filtering(community_id, community_type)
        
        # Setup content filtering
        await self._setup_content_filtering(community_id, community_type)
    
    async def _create_moderation_rules(
        self,
        community_id: str,
        community_type: CommunityType
    ):
        """Create moderation rules"""
        # Define moderation rules
        rules = [
            {'type': 'spam', 'action': 'warn'},
            {'type': 'harassment', 'action': 'mute'},
            {'type': 'offensive', 'action': 'delete'},
            {'type': 'self_promotion', 'action': 'warn'}
        ]
        
        # Apply rules based on community type
        if community_type == CommunityType.DISCORD:
            await self.discord_manager.create_moderation_rules(community_id, rules)
        elif community_type == CommunityType.SLACK:
            await self.slack_manager.create_moderation_rules(community_id, rules)
    
    async def _setup_automation(
        self,
        community_id: str,
        community_type: CommunityType
    ):
        """Setup community automation"""
        # Setup welcome messages
        await self._setup_welcome_messages(community_id, community_type)
        
        # Setup role assignments
        await self._setup_role_assignments(community_id, community_type)
        
        # Setup announcements
        await self._setup_announcements(community_id, community_type)
    
    async def _setup_welcome_messages(
        self,
        community_id: str,
        community_type: CommunityType
    ):
        """Setup welcome messages"""
        welcome_message = """
Welcome to our community! 🎉

We're excited to have you here. Here's what you need to know:

📌 **Rules**
- Be respectful and kind
- No spam or self-promotion
- Help others when you can
- Share your knowledge

🚀 **Getting Started**
- Introduce yourself in #introductions
- Check out our documentation
- Join our weekly calls

💬 **Channels**
- #general - General discussion
- #help - Get help with issues
- #showcase - Share your projects
- #announcements - Important updates

Let's build something great together! 🚀
"""
        
        if community_type == CommunityType.DISCORD:
            await self.discord_manager.set_welcome_message(community_id, welcome_message)
        elif community_type == CommunityType.SLACK:
            await self.slack_manager.set_welcome_message(community_id, welcome_message)
    
    async def add_member(
        self,
        community_id: str,
        member: CommunityMember
    ) -> Community:
        """Add member to community"""
        logger.info(f"Adding member to community: {community_id}")
        
        # Get community
        community = await self.community_store.get_community(community_id)
        
        # Add member
        community.members.append(member)
        
        # Update community
        community.updated_at = datetime.utcnow().isoformat()
        await self.community_store.update_community(community)
        
        # Send welcome message
        await self._send_welcome_message(community, member)
        
        logger.info(f"Member added: {member.member_id}")
        
        return community
    
    async def _send_welcome_message(
        self,
        community: Community,
        member: CommunityMember
    ):
        """Send welcome message to member"""
        # Send welcome message based on community type
        if community.community_type == CommunityType.DISCORD:
            await self.discord_manager.send_dm(community.community_id, member.member_id, "Welcome!")
        elif community.community_type == CommunityType.SLACK:
            await self.slack_manager.send_dm(community.community_id, member.member_id, "Welcome!")
    
    def _generate_community_id(self) -> str:
        """Generate unique community ID"""
        import uuid
        return f"community_{uuid.uuid4().hex}"

class CommunityStore:
    """Community storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_community(self, community: Community):
        """Create community"""
        # Implementation would store in database
        pass
    
    async def get_community(self, community_id: str) -> Community:
        """Get community"""
        # Implementation would query database
        return None
    
    async def update_community(self, community: Community):
        """Update community"""
        # Implementation would update database
        pass
    
    async def list_communities(self) -> List[Community]:
        """List all communities"""
        # Implementation would query database
        return []

class ForumManager:
    """Forum management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_forum(self, community_id: str, name: str):
        """Create forum"""
        # Implementation would create forum
        pass

class DiscordManager:
    """Discord management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_server(self, community_id: str, name: str):
        """Create Discord server"""
        # Implementation would create Discord server
        pass
    
    async def create_channels(self, community_id: str, channels: List[Dict[str, Any]]):
        """Create Discord channels"""
        # Implementation would create channels
        pass
    
    async def create_roles(self, community_id: str, roles: List[Dict[str, Any]]):
        """Create Discord roles"""
        # Implementation would create roles
        pass
    
    async def create_moderation_rules(self, community_id: str, rules: List[Dict[str, Any]]):
        """Create moderation rules"""
        # Implementation would create rules
        pass
    
    async def set_welcome_message(self, community_id: str, message: str):
        """Set welcome message"""
        # Implementation would set welcome message
        pass
    
    async def send_dm(self, community_id: str, user_id: str, message: str):
        """Send direct message"""
        # Implementation would send DM
        pass

class SlackManager:
    """Slack management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_workspace(self, community_id: str, name: str):
        """Create Slack workspace"""
        # Implementation would create workspace
        pass
    
    async def create_channels(self, community_id: str, channels: List[Dict[str, Any]]):
        """Create Slack channels"""
        # Implementation would create channels
        pass
    
    async def create_moderation_rules(self, community_id: str, rules: List[Dict[str, Any]]):
        """Create moderation rules"""
        # Implementation would create rules
        pass
    
    async def set_welcome_message(self, community_id: str, message: str):
        """Set welcome message"""
        # Implementation would set welcome message
        pass
    
    async def send_dm(self, community_id: str, user_id: str, message: str):
        """Send direct message"""
        # Implementation would send DM
        pass

class MeetupManager:
    """Meetup management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_group(self, community_id: str, name: str):
        """Create Meetup group"""
        # Implementation would create Meetup group
        pass
```

### Advocacy Programs

```python
class AdvocacyManager:
    """Advocacy program specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.advocate_store = AdvocateStore(config['advocate_store'])
        self.rewards_manager = RewardsManager(config['rewards'])
        
    async def create_advocate_program(
        self,
        name: str,
        description: str,
        tiers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create advocate program"""
        logger.info(f"Creating advocate program: {name}")
        
        # Generate program ID
        program_id = self._generate_program_id()
        
        # Create program
        program = {
            'program_id': program_id,
            'name': name,
            'description': description,
            'tiers': tiers,
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Store program
        await self.advocate_store.create_program(program)
        
        logger.info(f"Advocate program created: {program_id}")
        
        return program
    
    async def recruit_advocates(
        self,
        program_id: str,
        criteria: Dict[str, Any]
    ) -> List[CommunityMember]:
        """Recruit advocates for program"""
        logger.info(f"Recruiting advocates for program: {program_id}")
        
        # Get program
        program = await self.advocate_store.get_program(program_id)
        
        # Find potential advocates
        potential_advocates = await self._find_potential_advocates(criteria)
        
        # Recruit advocates
        recruited_advocates = []
        for member in potential_advocates:
            # Check if member meets criteria
            if await self._meets_criteria(member, criteria):
                # Invite to program
                invited = await self._invite_to_program(member, program)
                if invited:
                    recruited_advocates.append(member)
        
        logger.info(f"Recruited {len(recruited_advocates)} advocates")
        
        return recruited_advocates
    
    async def _find_potential_advocates(
        self,
        criteria: Dict[str, Any]
    ) -> List[CommunityMember]:
        """Find potential advocates"""
        # Implementation would search for potential advocates
        return []
    
    async def _meets_criteria(
        self,
        member: CommunityMember,
        criteria: Dict[str, Any]
    ) -> bool:
        """Check if member meets criteria"""
        # Check contribution count
        if 'min_contributions' in criteria:
            if member.contributions < criteria['min_contributions']:
                return False
        
        # Check reputation
        if 'min_reputation' in criteria:
            if member.reputation < criteria['min_reputation']:
                return False
        
        return True
    
    async def _invite_to_program(
        self,
        member: CommunityMember,
        program: Dict[str, Any]
    ) -> bool:
        """Invite member to program"""
        # Send invitation
        # Implementation would send invitation
        return True
    
    async def track_advocate_activity(
        self,
        program_id: str,
        advocate_id: str,
        activities: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Track advocate activity"""
        logger.info(f"Tracking activity for advocate: {advocate_id}")
        
        # Calculate points
        points = self._calculate_points(activities)
        
        # Update advocate tier
        new_tier = await self._update_advocate_tier(program_id, advocate_id, points)
        
        # Issue rewards
        rewards = await self.rewards_manager.issue_rewards(
            program_id,
            advocate_id,
            new_tier
        )
        
        return {
            'advocate_id': advocate_id,
            'points': points,
            'tier': new_tier,
            'rewards': rewards,
            'tracked_at': datetime.utcnow().isoformat()
        }
    
    def _calculate_points(self, activities: List[Dict[str, Any]]) -> int:
        """Calculate points from activities"""
        points = 0
        
        for activity in activities:
            activity_type = activity['type']
            activity_points = self.config.get('activity_points', {}).get(activity_type, 0)
            points += activity_points
        
        return points
    
    async def _update_advocate_tier(
        self,
        program_id: str,
        advocate_id: str,
        points: int
    ) -> str:
        """Update advocate tier based on points"""
        # Get program
        program = await self.advocate_store.get_program(program_id)
        
        # Find appropriate tier
        current_tier = None
        for tier in program['tiers']:
            if points >= tier['points']:
                current_tier = tier['name']
            else:
                break
        
        # Update advocate tier
        await self.advocate_store.update_advocate_tier(
            program_id,
            advocate_id,
            current_tier
        )
        
        return current_tier
    
    def _generate_program_id(self) -> str:
        """Generate unique program ID"""
        import uuid
        return f"program_{uuid.uuid4().hex}"

class AdvocateStore:
    """Advocate storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_program(self, program: Dict[str, Any]):
        """Create advocate program"""
        # Implementation would store in database
        pass
    
    async def get_program(self, program_id: str) -> Dict[str, Any]:
        """Get advocate program"""
        # Implementation would query database
        return {}
    
    async def update_advocate_tier(
        self,
        program_id: str,
        advocate_id: str,
        tier: str
    ):
        """Update advocate tier"""
        # Implementation would update database
        pass

class RewardsManager:
    """Rewards management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def issue_rewards(
        self,
        program_id: str,
        advocate_id: str,
        tier: str
    ) -> List[Dict[str, Any]]:
        """Issue rewards to advocate"""
        # Get rewards for tier
        rewards = self.config.get('tier_rewards', {}).get(tier, [])
        
        # Issue rewards
        for reward in rewards:
            await self._issue_reward(advocate_id, reward)
        
        return rewards
    
    async def _issue_reward(
        self,
        advocate_id: str,
        reward: Dict[str, Any]
    ):
        """Issue reward to advocate"""
        # Implementation would issue reward
        pass
```

### Content Creation

```python
class ContentCreator:
    """Content creation specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.content_store = ContentStore(config['content_store'])
        self.blog_manager = BlogManager(config['blog'])
        self.video_manager = VideoManager(config['video'])
        self.documentation_manager = DocumentationManager(config['documentation'])
        
    async def create_tutorial(
        self,
        title: str,
        description: str,
        content: str,
        tags: List[str]
    ) -> Dict[str, Any]:
        """Create tutorial content"""
        logger.info(f"Creating tutorial: {title}")
        
        # Generate content ID
        content_id = self._generate_content_id()
        
        # Create content
        tutorial = {
            'content_id': content_id,
            'type': 'tutorial',
            'title': title,
            'description': description,
            'content': content,
            'tags': tags,
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Store content
        await self.content_store.create_content(tutorial)
        
        # Publish to blog
        await self.blog_manager.publish(tutorial)
        
        logger.info(f"Tutorial created: {content_id}")
        
        return tutorial
    
    async def create_video(
        self,
        title: str,
        description: str,
        video_url: str,
        tags: List[str]
    ) -> Dict[str, Any]:
        """Create video content"""
        logger.info(f"Creating video: {title}")
        
        # Generate content ID
        content_id = self._generate_content_id()
        
        # Create content
        video = {
            'content_id': content_id,
            'type': 'video',
            'title': title,
            'description': description,
            'video_url': video_url,
            'tags': tags,
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Store content
        await self.content_store.create_content(video)
        
        # Publish to video platform
        await self.video_manager.publish(video)
        
        logger.info(f"Video created: {content_id}")
        
        return video
    
    async def create_documentation(
        self,
        title: str,
        content: str,
        category: str
    ) -> Dict[str, Any]:
        """Create documentation"""
        logger.info(f"Creating documentation: {title}")
        
        # Generate content ID
        content_id = self._generate_content_id()
        
        # Create content
        documentation = {
            'content_id': content_id,
            'type': 'documentation',
            'title': title,
            'content': content,
            'category': category,
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Store content
        await self.content_store.create_content(documentation)
        
        # Publish to documentation platform
        await self.documentation_manager.publish(documentation)
        
        logger.info(f"Documentation created: {content_id}")
        
        return documentation
    
    def _generate_content_id(self) -> str:
        """Generate unique content ID"""
        import uuid
        return f"content_{uuid.uuid4().hex}"

class ContentStore:
    """Content storage specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def create_content(self, content: Dict[str, Any]):
        """Create content"""
        # Implementation would store in database
        pass
    
    async def get_content(self, content_id: str) -> Dict[str, Any]:
        """Get content"""
        # Implementation would query database
        return {}
    
    async def list_content(
        self,
        content_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List content"""
        # Implementation would query database
        return []

class BlogManager:
    """Blog management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def publish(self, content: Dict[str, Any]):
        """Publish content to blog"""
        # Implementation would publish to blog
        pass

class VideoManager:
    """Video management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def publish(self, content: Dict[str, Any]):
        """Publish content to video platform"""
        # Implementation would publish to YouTube/Vimeo
        pass

class DocumentationManager:
    """Documentation management specialist"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    async def publish(self, content: Dict[str, Any]):
        """Publish content to documentation platform"""
        # Implementation would publish to docs site
        pass
```

---

## Tooling & Tech Stack

### Community Platforms
- **Discord**: Community platform
- **Slack**: Team communication
- **Discourse**: Forum software
- **Discourse**: Forum software
- **Reddit**: Community platform

### Content Platforms
- **YouTube**: Video platform
- **Vimeo**: Video platform
- **Medium**: Blogging platform
- **Ghost**: Blogging platform
- **Hugo**: Static site generator

### Analytics Tools
- **Google Analytics**: Web analytics
- **Mixpanel**: Product analytics
- **Amplitude**: Analytics platform
- **Hotjar**: User behavior analytics

### Automation Tools
- **Zapier**: Automation platform
- **Make**: Automation platform
- **GitHub Actions**: Automation
- **IFTTT**: Automation platform

---

## Configuration Essentials

### Community Configuration

```yaml
# config/community_config.yaml
community:
  platform: "discord"  # discord, slack, forum
  
  channels:
    general:
      name: "general"
      type: "text"
      description: "General discussion"
    
    introductions:
      name: "introductions"
      type: "text"
      description: "Introduce yourself"
    
    help:
      name: "help"
      type: "text"
      description: "Get help with issues"
    
    announcements:
      name: "announcements"
      type: "text"
      description: "Important updates"
    
    showcase:
      name: "showcase"
      type: "text"
      description: "Share your projects"
  
  roles:
    member:
      name: "Member"
      permissions:
        - "read_messages"
        - "send_messages"
    
    contributor:
      name: "Contributor"
      permissions:
        - "read_messages"
        - "send_messages"
        - "embed_links"
    
    moderator:
      name: "Moderator"
      permissions:
        - "read_messages"
        - "send_messages"
        - "manage_messages"
        - "kick_members"
    
    advocate:
      name: "Advocate"
      permissions:
        - "read_messages"
        - "send_messages"
        - "manage_channels"
    
    ambassador:
      name: "Ambassador"
      permissions:
        - "read_messages"
        - "send_messages"
        - "manage_roles"
  
  moderation:
    rules:
      spam:
        action: "warn"
        threshold: 3
      
      harassment:
        action: "mute"
        threshold: 1
      
      offensive:
        action: "delete"
        threshold: 1
      
      self_promotion:
        action: "warn"
        threshold: 2
  
  automation:
    welcome_message: true
    role_assignment: true
    announcements: true
    spam_filtering: true
```

### Advocacy Program Configuration

```yaml
# config/advocacy_config.yaml
advocacy:
  program_name: "Developer Advocates"
  description: "Recognize and reward our most active developers"
  
  tiers:
    - name: "Contributor"
      points: 100
      benefits:
        - "Badge"
        - "Early access"
        - "Newsletter"
    
    - name: "Advocate"
      points: 500
      benefits:
        - "Badge"
        - "Early access"
        - "Newsletter"
        - "Swag"
        - "Discount"
    
    - name: "Ambassador"
      points: 1000
      benefits:
        - "Badge"
        - "Early access"
        - "Newsletter"
        - "Swag"
        - "Discount"
        - "Speaking opportunity"
        - "Conference pass"
  
  activity_points:
    forum_post: 5
    forum_reply: 3
    code_contribution: 50
    bug_report: 20
    documentation_edit: 10
    blog_post: 30
    video_tutorial: 50
    meetup_attendance: 10
    meetup_speaking: 100
  
  rewards:
    contributor:
      - type: "badge"
        name: "Contributor Badge"
      - type: "access"
        name: "Early Access"
      - type: "newsletter"
        name: "Advocate Newsletter"
    
    advocate:
      - type: "badge"
        name: "Advocate Badge"
      - type: "access"
        name: "Early Access"
      - type: "newsletter"
        name: "Advocate Newsletter"
      - type: "swag"
        name: "T-Shirt"
      - type: "discount"
        name: "20% Discount"
    
    ambassador:
      - type: "badge"
        name: "Ambassador Badge"
      - type: "access"
        name: "Early Access"
      - type: "newsletter"
        name: "Ambassador Newsletter"
      - type: "swag"
        name: "Swag Pack"
      - type: "discount"
        name: "30% Discount"
      - type: "opportunity"
        name: "Speaking Opportunity"
      - type: "pass"
        name: "Conference Pass"
```

---

## Code Examples

### Good: Complete Community Workflow

```python
# community/workflow.py
import asyncio
import logging
from typing import Dict, Any

from community.builder import CommunityBuilder
from community.advocacy import AdvocacyManager
from community.content import ContentCreator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_community():
    """Run developer relations workflow"""
    logger.info("=" * 60)
    logger.info("Developer Relations & Community Workflow")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config('config/community_config.yaml')
    
    # Step 1: Build community
    logger.info("\n" + "=" * 60)
    logger.info("Step 1: Building Community")
    logger.info("=" * 60)
    
    community_builder = CommunityBuilder(config)
    community = await community_builder.build_community(
        name="Developer Community",
        description="Community for developers building with our platform",
        community_type=CommunityType.DISCORD
    )
    
    logger.info(f"Community built: {community.community_id}")
    print_community_summary(community)
    
    # Step 2: Create advocacy program
    logger.info("\n" + "=" * 60)
    logger.info("Step 2: Creating Advocacy Program")
    logger.info("=" * 60)
    
    advocacy_config = load_config('config/advocacy_config.yaml')
    advocacy_manager = AdvocacyManager(advocacy_config)
    program = await advocacy_manager.create_advocate_program(
        name=advocacy_config['advocacy']['program_name'],
        description=advocacy_config['advocacy']['description'],
        tiers=advocacy_config['advocacy']['tiers']
    )
    
    logger.info(f"Advocacy program created: {program['program_id']}")
    print_program_summary(program)
    
    # Step 3: Create content
    logger.info("\n" + "=" * 60)
    logger.info("Step 3: Creating Content")
    logger.info("=" * 60)
    
    content_creator = ContentCreator(config)
    
    # Create tutorial
    tutorial = await content_creator.create_tutorial(
        title="Getting Started with Our Platform",
        description="Learn how to get started with our platform",
        content="# Getting Started\n\nWelcome to our platform!",
        tags=["getting-started", "tutorial"]
    )
    
    logger.info(f"Tutorial created: {tutorial['content_id']}")
    
    # Create video
    video = await content_creator.create_video(
        title="Platform Overview",
        description="Overview of our platform features",
        video_url="https://youtube.com/watch?v=example",
        tags=["overview", "video"]
    )
    
    logger.info(f"Video created: {video['content_id']}")
    
    # Print summary
    print_summary(community, program, tutorial, video)

def print_community_summary(community: Community):
    """Print community summary"""
    print(f"\nCommunity Summary:")
    print(f"  Name: {community.name}")
    print(f"  Description: {community.description}")
    print(f"  Type: {community.community_type.value}")
    print(f"  Members: {len(community.members)}")

def print_program_summary(program: Dict[str, Any]):
    """Print program summary"""
    print(f"\nAdvocacy Program Summary:")
    print(f"  Name: {program['name']}")
    print(f"  Description: {program['description']}")
    print(f"  Tiers: {len(program['tiers'])}")
    for tier in program['tiers']:
        print(f"    - {tier['name']}: {tier['points']} points")

def print_summary(
    community: Community,
    program: Dict[str, Any],
    tutorial: Dict[str, Any],
    video: Dict[str, Any]
):
    """Print summary"""
    print("\n" + "=" * 60)
    print("Developer Relations Summary")
    print("=" * 60)
    print(f"Community: {community.name}")
    print(f"Program: {program['name']}")
    print(f"Content Created: 2")
    print(f"  - Tutorial: {tutorial['title']}")
    print(f"  - Video: {video['title']}")

def load_config(filename: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import yaml
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

async def main():
    """Main entry point"""
    await run_community()

if __name__ == "__main__":
    asyncio.run(main())
```

### Bad: Anti-pattern Example

```python
# BAD: No community
def bad_developer_relations():
    # No community
    pass

# BAD: No advocacy
def bad_developer_relations():
    # No advocacy
    create_community()

# BAD: No content
def bad_developer_relations():
    # No content
    create_community()
    create_advocacy()

# BAD: No engagement
def bad_developer_relations():
    # No engagement
    create_community()
    create_advocacy()
    create_content()
```

---

## Standards, Compliance & Security

### Industry Standards
- **Community Management**: Community management best practices
- **Content Creation**: Content creation best practices
- **Advocacy Programs**: Advocacy program best practices
- **Developer Relations**: Developer relations best practices

### Security Best Practices
- **Data Privacy**: Protect user data
- **Content Moderation**: Moderate content appropriately
- **Access Control**: RBAC for community management
- **Audit Logging**: Log all community activities

### Compliance Requirements
- **GDPR**: Data protection compliance
- **Terms of Service**: Enforce community guidelines
- **Content Policy**: Follow content policies
- **Privacy Policy**: Protect user privacy

---

## Quick Start

### 1. Install Dependencies

```bash
pip install pyyaml
pip install discord.py
pip install slack-sdk
```

### 2. Configure Community

```bash
# Copy example config
cp config/community_config.yaml.example config/community_config.yaml

# Edit configuration
vim config/community_config.yaml
```

### 3. Build Community

```bash
python community/workflow.py
```

### 4. View Results

```bash
# View community
cat community/results/community.json

# View program
cat community/results/program.json
```

---

## Production Checklist

### Community Building
- [ ] Platform selected
- [ ] Channels created
- [ ] Roles defined
- [ ] Moderation configured
- [ ] Automation setup

### Advocacy Program
- [ ] Program defined
- [ ] Tiers created
- [ ] Points system defined
- [ ] Rewards configured
- [ ] Recruitment process defined

### Content Creation
- [ ] Content strategy defined
- [ ] Editorial calendar created
- [ ] Content templates created
- [ ] Publishing process defined
- [ ] Analytics configured

### Engagement
- [ ] Welcome messages configured
- [ ] Role assignments automated
- [ ] Announcements scheduled
- [ ] Events planned
- [ ] Feedback channels set up

### Analytics
- [ ] Metrics defined
- [ ] Tracking configured
- [ ] Dashboards created
- [ ] Reports scheduled
- [ ] Insights generated

---

## Anti-patterns

### ❌ Avoid These Practices

1. **No Community**
   ```python
   # BAD: No community
   pass
   ```

2. **No Advocacy**
   ```python
   # BAD: No advocacy
   create_community()
   ```

3. **No Content**
   ```python
   # BAD: No content
   create_community()
   create_advocacy()
   ```

4. **No Engagement**
   ```python
   # BAD: No engagement
   create_community()
   create_advocacy()
   create_content()
   ```

### ✅ Follow These Practices

1. **Build Community**
   ```python
   # GOOD: Build community
   community_builder = CommunityBuilder(config)
   community = await community_builder.build_community(name, description, type)
   ```

2. **Create Advocacy**
   ```python
   # GOOD: Create advocacy
   advocacy_manager = AdvocacyManager(config)
   program = await advocacy_manager.create_advocate_program(name, description, tiers)
   ```

3. **Create Content**
   ```python
   # GOOD: Create content
   content_creator = ContentCreator(config)
   content = await content_creator.create_tutorial(title, description, content, tags)
   ```

4. **Engage**
   ```python
   # GOOD: Engage
   await welcome_members(community)
   await moderate_content(community)
   await respond_to_questions(community)
   ```

---

## Unit Economics & KPIs

### Development Costs
- **Initial Setup**: 20-40 hours
- **Community Building**: 40-80 hours
- **Advocacy Program**: 20-40 hours
- **Content Creation**: 40-80 hours
- **Total**: 120-240 hours

### Operational Costs
- **Community Platforms**: $50-200/month
- **Content Platforms**: $20-100/month
- **Swag**: $500-2000/quarter
- **Event Costs**: $200-1000/event

### ROI Metrics
- **Community Growth**: 50-100% improvement
- **Engagement Rate**: 40-60% improvement
- **Advocate Growth**: 60-80% improvement
- **Content Reach**: 70-90% improvement

### KPI Targets
- **Community Members**: > 1000
- **Active Members**: > 30%
- **Advocate Count**: > 50
- **Content Views**: > 10000/month
- **Engagement Rate**: > 20%

---

## Integration Points / Related Skills

### Upstream Skills
- **136. Business to Technical Spec**: Requirements
- **137. API-First Product Strategy**: API design
- **138. Platform Product Design**: Platform design

### Parallel Skills
- **147. Technical Content Marketing**: Content marketing
- **148. Sales Engineering**: Sales engineering
- **149. Enterprise Sales Alignment**: Sales alignment

### Downstream Skills
- **150. Partner Program Design**: Partner programs
- **151. Analyst Relations**: Analyst relations
- **152. Launch Strategy Execution**: Launch strategy

### Cross-Domain Skills
- **18. Project Management**: Project planning
- **81. SaaS FinOps Pricing**: Pricing strategy
- **82. Technical Product Management**: Product management
- **84. Compliance AI Governance**: Compliance

---

## References & Resources

### Documentation
- [Discord Documentation](https://discord.com/developers/docs)
- [Slack API Documentation](https://api.slack.com/)
- [Community Management Guide](https://www.discourse.org/)

### Best Practices
- [Developer Relations Best Practices](https://www.developerrelations.com/)
- [Community Building Guide](https://www.feverbee.com/)
- [Advocacy Programs](https://www.ambassadorprogram.com/)

### Tools & Libraries
- [Discord.py](https://discordpy.readthedocs.io/)
- [Slack SDK](https://slack.dev/python-tutorial/)
- [Discourse](https://www.discourse.org/)
- [Hugo](https://gohugo.io/)
