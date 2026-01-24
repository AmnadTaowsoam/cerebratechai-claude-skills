---
name: Content Versioning
description: Tracking changes to content over time enabling rollback, comparison, and audit trails with version history, diff viewing, and content lifecycle management.
---

# Content Versioning

> **Current Level:** Intermediate  
> **Domain:** Content Management / Version Control

---

## Overview

Content versioning tracks changes to content over time, enabling rollback, comparison, and audit trails. This guide covers implementation patterns and best practices for managing content versions effectively.

## Versioning Concepts

```
Content Lifecycle:
Draft → Review → Published → Archived

Version States:
- Draft: Work in progress
- Published: Live content
- Archived: Historical versions
```

## Database Schema

```sql
-- content table
CREATE TABLE content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type VARCHAR(50) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  
  current_version_id UUID,
  published_version_id UUID,
  
  status VARCHAR(50) DEFAULT 'draft',
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  published_at TIMESTAMP,
  
  INDEX idx_slug (slug),
  INDEX idx_status (status),
  INDEX idx_type (type)
);

-- content_versions table
CREATE TABLE content_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content_id UUID REFERENCES content(id) ON DELETE CASCADE,
  
  version_number INTEGER NOT NULL,
  
  title VARCHAR(255) NOT NULL,
  body TEXT,
  metadata JSONB,
  
  status VARCHAR(50) DEFAULT 'draft',
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  
  published_at TIMESTAMP,
  archived_at TIMESTAMP,
  
  change_summary TEXT,
  
  INDEX idx_content (content_id),
  INDEX idx_version (content_id, version_number),
  INDEX idx_status (status),
  UNIQUE(content_id, version_number)
);

-- version_changes table
CREATE TABLE version_changes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  version_id UUID REFERENCES content_versions(id) ON DELETE CASCADE,
  
  field_name VARCHAR(100) NOT NULL,
  old_value TEXT,
  new_value TEXT,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_version (version_id)
);

-- scheduled_publishes table
CREATE TABLE scheduled_publishes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content_id UUID REFERENCES content(id) ON DELETE CASCADE,
  version_id UUID REFERENCES content_versions(id) ON DELETE CASCADE,
  
  scheduled_at TIMESTAMP NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  published_at TIMESTAMP,
  
  INDEX idx_content (content_id),
  INDEX idx_scheduled (scheduled_at, status)
);
```

## Version Creation

```typescript
// services/content-version.service.ts
export class ContentVersionService {
  async createVersion(
    contentId: string,
    data: CreateVersionDto,
    userId: string
  ): Promise<ContentVersion> {
    // Get current version number
    const latestVersion = await db.contentVersion.findFirst({
      where: { contentId },
      orderBy: { versionNumber: 'desc' }
    });

    const versionNumber = (latestVersion?.versionNumber || 0) + 1;

    // Create new version
    const version = await db.contentVersion.create({
      data: {
        contentId,
        versionNumber,
        title: data.title,
        body: data.body,
        metadata: data.metadata,
        status: 'draft',
        createdBy: userId,
        changeSummary: data.changeSummary
      }
    });

    // Track changes
    if (latestVersion) {
      await this.trackChanges(latestVersion, version);
    }

    // Update content current version
    await db.content.update({
      where: { id: contentId },
      data: {
        currentVersionId: version.id,
        updatedAt: new Date()
      }
    });

    return version;
  }

  private async trackChanges(
    oldVersion: ContentVersion,
    newVersion: ContentVersion
  ): Promise<void> {
    const changes: VersionChange[] = [];

    // Compare fields
    if (oldVersion.title !== newVersion.title) {
      changes.push({
        versionId: newVersion.id,
        fieldName: 'title',
        oldValue: oldVersion.title,
        newValue: newVersion.title
      });
    }

    if (oldVersion.body !== newVersion.body) {
      changes.push({
        versionId: newVersion.id,
        fieldName: 'body',
        oldValue: oldVersion.body,
        newValue: newVersion.body
      });
    }

    // Save changes
    if (changes.length > 0) {
      await db.versionChange.createMany({
        data: changes
      });
    }
  }
}

interface CreateVersionDto {
  title: string;
  body: string;
  metadata?: Record<string, any>;
  changeSummary?: string;
}

interface VersionChange {
  versionId: string;
  fieldName: string;
  oldValue: string;
  newValue: string;
}
```

## Version Comparison

```typescript
// services/version-comparison.service.ts
import { diffWords, diffLines } from 'diff';

export class VersionComparisonService {
  async compareVersions(
    versionId1: string,
    versionId2: string
  ): Promise<VersionDiff> {
    const [version1, version2] = await Promise.all([
      db.contentVersion.findUnique({ where: { id: versionId1 } }),
      db.contentVersion.findUnique({ where: { id: versionId2 } })
    ]);

    if (!version1 || !version2) {
      throw new Error('Version not found');
    }

    return {
      title: this.diffText(version1.title, version2.title),
      body: this.diffText(version1.body, version2.body),
      metadata: this.diffMetadata(version1.metadata, version2.metadata)
    };
  }

  private diffText(text1: string, text2: string): TextDiff[] {
    const diff = diffWords(text1, text2);

    return diff.map(part => ({
      value: part.value,
      added: part.added || false,
      removed: part.removed || false
    }));
  }

  private diffMetadata(meta1: any, meta2: any): MetadataDiff[] {
    const diffs: MetadataDiff[] = [];
    const allKeys = new Set([
      ...Object.keys(meta1 || {}),
      ...Object.keys(meta2 || {})
    ]);

    allKeys.forEach(key => {
      const value1 = meta1?.[key];
      const value2 = meta2?.[key];

      if (value1 !== value2) {
        diffs.push({
          field: key,
          oldValue: value1,
          newValue: value2
        });
      }
    });

    return diffs;
  }

  async getVersionHistory(contentId: string): Promise<VersionHistory[]> {
    const versions = await db.contentVersion.findMany({
      where: { contentId },
      orderBy: { versionNumber: 'desc' },
      include: {
        createdBy: {
          select: {
            id: true,
            name: true,
            email: true
          }
        }
      }
    });

    return versions.map(v => ({
      id: v.id,
      versionNumber: v.versionNumber,
      status: v.status,
      createdBy: v.createdBy,
      createdAt: v.createdAt,
      changeSummary: v.changeSummary
    }));
  }
}

interface VersionDiff {
  title: TextDiff[];
  body: TextDiff[];
  metadata: MetadataDiff[];
}

interface TextDiff {
  value: string;
  added: boolean;
  removed: boolean;
}

interface MetadataDiff {
  field: string;
  oldValue: any;
  newValue: any;
}

interface VersionHistory {
  id: string;
  versionNumber: number;
  status: string;
  createdBy: any;
  createdAt: Date;
  changeSummary?: string;
}
```

## Rollback Functionality

```typescript
// services/version-rollback.service.ts
export class VersionRollbackService {
  async rollbackToVersion(
    contentId: string,
    versionId: string,
    userId: string
  ): Promise<ContentVersion> {
    const targetVersion = await db.contentVersion.findUnique({
      where: { id: versionId }
    });

    if (!targetVersion) {
      throw new Error('Version not found');
    }

    // Create new version from target version
    const newVersion = await contentVersionService.createVersion(
      contentId,
      {
        title: targetVersion.title,
        body: targetVersion.body,
        metadata: targetVersion.metadata,
        changeSummary: `Rolled back to version ${targetVersion.versionNumber}`
      },
      userId
    );

    return newVersion;
  }

  async restoreDeletedVersion(versionId: string): Promise<ContentVersion> {
    return db.contentVersion.update({
      where: { id: versionId },
      data: {
        archivedAt: null,
        status: 'draft'
      }
    });
  }
}
```

## Draft vs Published

```typescript
// services/content-publish.service.ts
export class ContentPublishService {
  async publishVersion(versionId: string, userId: string): Promise<void> {
    const version = await db.contentVersion.findUnique({
      where: { id: versionId }
    });

    if (!version) {
      throw new Error('Version not found');
    }

    // Update version status
    await db.contentVersion.update({
      where: { id: versionId },
      data: {
        status: 'published',
        publishedAt: new Date()
      }
    });

    // Update content
    await db.content.update({
      where: { id: version.contentId },
      data: {
        publishedVersionId: versionId,
        status: 'published',
        publishedAt: new Date()
      }
    });

    // Archive previous published version
    const previousPublished = await db.contentVersion.findFirst({
      where: {
        contentId: version.contentId,
        status: 'published',
        id: { not: versionId }
      }
    });

    if (previousPublished) {
      await db.contentVersion.update({
        where: { id: previousPublished.id },
        data: {
          status: 'archived',
          archivedAt: new Date()
        }
      });
    }

    // Log activity
    await this.logPublishActivity(version.contentId, versionId, userId);
  }

  async unpublishContent(contentId: string): Promise<void> {
    await db.content.update({
      where: { id: contentId },
      data: {
        status: 'draft',
        publishedVersionId: null
      }
    });
  }

  private async logPublishActivity(
    contentId: string,
    versionId: string,
    userId: string
  ): Promise<void> {
    await db.activity.create({
      data: {
        type: 'content_published',
        contentId,
        versionId,
        userId,
        createdAt: new Date()
      }
    });
  }
}
```

## Scheduled Publishing

```typescript
// services/scheduled-publish.service.ts
export class ScheduledPublishService {
  async schedulePublish(
    contentId: string,
    versionId: string,
    scheduledAt: Date,
    userId: string
  ): Promise<ScheduledPublish> {
    return db.scheduledPublish.create({
      data: {
        contentId,
        versionId,
        scheduledAt,
        status: 'pending',
        createdBy: userId
      }
    });
  }

  async cancelScheduledPublish(scheduleId: string): Promise<void> {
    await db.scheduledPublish.update({
      where: { id: scheduleId },
      data: { status: 'cancelled' }
    });
  }

  async processScheduledPublishes(): Promise<void> {
    const pending = await db.scheduledPublish.findMany({
      where: {
        status: 'pending',
        scheduledAt: { lte: new Date() }
      }
    });

    for (const schedule of pending) {
      try {
        await contentPublishService.publishVersion(
          schedule.versionId,
          schedule.createdBy
        );

        await db.scheduledPublish.update({
          where: { id: schedule.id },
          data: {
            status: 'completed',
            publishedAt: new Date()
          }
        });
      } catch (error) {
        await db.scheduledPublish.update({
          where: { id: schedule.id },
          data: { status: 'failed' }
        });
      }
    }
  }
}

// Cron job to process scheduled publishes
setInterval(async () => {
  await scheduledPublishService.processScheduledPublishes();
}, 60000); // Every minute
```

## Conflict Resolution

```typescript
// services/conflict-resolution.service.ts
export class ConflictResolutionService {
  async detectConflict(
    contentId: string,
    baseVersionId: string,
    newData: any
  ): Promise<Conflict | null> {
    const [baseVersion, currentVersion] = await Promise.all([
      db.contentVersion.findUnique({ where: { id: baseVersionId } }),
      db.contentVersion.findFirst({
        where: { contentId },
        orderBy: { versionNumber: 'desc' }
      })
    ]);

    if (!baseVersion || !currentVersion) return null;

    // Check if there's a newer version
    if (currentVersion.versionNumber > baseVersion.versionNumber) {
      return {
        baseVersion,
        currentVersion,
        conflicts: this.findConflicts(baseVersion, currentVersion, newData)
      };
    }

    return null;
  }

  private findConflicts(
    baseVersion: ContentVersion,
    currentVersion: ContentVersion,
    newData: any
  ): FieldConflict[] {
    const conflicts: FieldConflict[] = [];

    // Check each field
    if (
      baseVersion.title !== currentVersion.title &&
      newData.title !== currentVersion.title
    ) {
      conflicts.push({
        field: 'title',
        baseValue: baseVersion.title,
        currentValue: currentVersion.title,
        newValue: newData.title
      });
    }

    return conflicts;
  }

  async resolveConflict(
    contentId: string,
    resolutions: Resolution[]
  ): Promise<ContentVersion> {
    const mergedData: any = {};

    resolutions.forEach(resolution => {
      mergedData[resolution.field] = resolution.selectedValue;
    });

    return contentVersionService.createVersion(
      contentId,
      mergedData,
      'system'
    );
  }
}

interface Conflict {
  baseVersion: ContentVersion;
  currentVersion: ContentVersion;
  conflicts: FieldConflict[];
}

interface FieldConflict {
  field: string;
  baseValue: any;
  currentValue: any;
  newValue: any;
}

interface Resolution {
  field: string;
  selectedValue: any;
}
```

## API Design

```typescript
// controllers/version.controller.ts
import { Router } from 'express';

const router = Router();

router.get('/content/:id/versions', async (req, res) => {
  const versions = await versionComparisonService.getVersionHistory(req.params.id);
  res.json(versions);
});

router.get('/versions/:id1/compare/:id2', async (req, res) => {
  const diff = await versionComparisonService.compareVersions(
    req.params.id1,
    req.params.id2
  );
  res.json(diff);
});

router.post('/content/:id/versions', async (req, res) => {
  const version = await contentVersionService.createVersion(
    req.params.id,
    req.body,
    req.user.id
  );
  res.status(201).json(version);
});

router.post('/versions/:id/publish', async (req, res) => {
  await contentPublishService.publishVersion(req.params.id, req.user.id);
  res.json({ success: true });
});

router.post('/versions/:id/rollback', async (req, res) => {
  const version = await versionRollbackService.rollbackToVersion(
    req.body.contentId,
    req.params.id,
    req.user.id
  );
  res.json(version);
});

export default router;
```

## Best Practices

1. **Versioning** - Version all content changes
2. **Comparison** - Provide visual diff tools
3. **Rollback** - Enable easy rollback
4. **Audit Trail** - Track all changes
5. **Scheduled Publishing** - Support scheduled publishes
6. **Conflict Resolution** - Handle concurrent edits
7. **Performance** - Optimize version queries
8. **Storage** - Archive old versions
9. **Permissions** - Control who can publish
10. **Testing** - Test version workflows

---

## Quick Start

### Content Versioning

```typescript
interface ContentVersion {
  id: string
  contentId: string
  version: number
  content: string
  author: string
  createdAt: Date
  status: 'draft' | 'published' | 'archived'
}

async function createVersion(
  contentId: string,
  content: string,
  author: string
): Promise<ContentVersion> {
  // Get latest version
  const latest = await getLatestVersion(contentId)
  const newVersion = latest ? latest.version + 1 : 1
  
  return await db.contentVersions.create({
    data: {
      contentId,
      version: newVersion,
      content,
      author,
      status: 'draft'
    }
  })
}

async function rollbackToVersion(contentId: string, version: number) {
  const version = await db.contentVersions.findUnique({
    where: { contentId_version: { contentId, version } }
  })
  
  await publishVersion(version.id)
}
```

---

## Production Checklist

- [ ] **Versioning System**: Content versioning implemented
- [ ] **Version History**: Complete version history
- [ ] **Diff Viewing**: Visual diff tools
- [ ] **Rollback**: Easy rollback to previous versions
- [ ] **Audit Trail**: Track all changes
- [ ] **Status Management**: Draft/published/archived
- [ ] **Comparison**: Compare versions
- [ ] **Metadata**: Version metadata
- [ ] **Testing**: Test version workflows
- [ ] **Documentation**: Document versioning
- [ ] **Performance**: Optimize version storage
- [ ] **Cleanup**: Archive old versions

---

## Anti-patterns

### ❌ Don't: No Version History

```typescript
// ❌ Bad - Overwrite content
await db.content.update({
  where: { id: contentId },
  data: { content: newContent }
})
// Lost previous version!
```

```typescript
// ✅ Good - Version history
await createVersion(contentId, newContent, author)
// Previous versions preserved
```

### ❌ Don't: Unlimited Versions

```markdown
# ❌ Bad - Keep all versions forever
Version 1, Version 2, ... Version 10000
# Storage bloat!
```

```markdown
# ✅ Good - Archive old versions
Keep last 50 versions
Archive versions older than 1 year
# Manageable storage
```

---

## Integration Points

- **Headless CMS** (`33-content-management/headless-cms/`) - CMS patterns
- **Contentful Integration** (`33-content-management/contentful-integration/`) - CMS integration
- **Versioning** (`01-foundations/versioning/`) - Version control

---

## Further Reading

- [Git Versioning](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- [Content Versioning Best Practices](https://www.contentful.com/developers/docs/concepts/versioning/)

## Resources
- [Diff Algorithms](https://github.com/kpdecker/jsdiff)
- [Content Versioning Best Practices](https://www.contentful.com/blog/2021/04/14/content-versioning/)
