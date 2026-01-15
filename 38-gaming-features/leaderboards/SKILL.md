# Leaderboards

## Overview

Leaderboards rank players based on scores or achievements. This guide covers global, friends, and time-based leaderboards with Redis for performance.

## Leaderboard Types

### Global Leaderboard
- All players worldwide
- Highest scores overall
- Most competitive

### Friends Leaderboard
- Only friends/connections
- Social comparison
- Personalized

### Time-based Leaderboard
- Daily, weekly, monthly
- Resets periodically
- Fresh competition

### Seasonal Leaderboard
- Limited time events
- Special rewards
- Themed competitions

## Database Schema

```sql
-- players table
CREATE TABLE players (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username VARCHAR(255) UNIQUE NOT NULL,
  display_name VARCHAR(255),
  avatar_url VARCHAR(500),
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_username (username)
);

-- scores table
CREATE TABLE scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  player_id UUID REFERENCES players(id) ON DELETE CASCADE,
  leaderboard_id VARCHAR(100) NOT NULL,
  
  score BIGINT NOT NULL,
  metadata JSONB,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_player_leaderboard (player_id, leaderboard_id),
  INDEX idx_leaderboard_score (leaderboard_id, score DESC)
);

-- leaderboards table
CREATE TABLE leaderboards (
  id VARCHAR(100) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL,
  
  reset_frequency VARCHAR(50),
  last_reset TIMESTAMP,
  next_reset TIMESTAMP,
  
  active BOOLEAN DEFAULT TRUE,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- friendships table
CREATE TABLE friendships (
  player_id UUID REFERENCES players(id) ON DELETE CASCADE,
  friend_id UUID REFERENCES players(id) ON DELETE CASCADE,
  
  status VARCHAR(50) DEFAULT 'pending',
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  PRIMARY KEY (player_id, friend_id),
  INDEX idx_player (player_id),
  INDEX idx_friend (friend_id)
);
```

## Score Submission

```typescript
// services/leaderboard.service.ts
import { PrismaClient } from '@prisma/client';
import Redis from 'ioredis';

const db = new PrismaClient();
const redis = new Redis(process.env.REDIS_URL!);

export class LeaderboardService {
  async submitScore(
    playerId: string,
    leaderboardId: string,
    score: number,
    metadata?: any
  ): Promise<void> {
    // Validate score
    if (score < 0) {
      throw new Error('Invalid score');
    }

    // Check for cheating (basic)
    const isValid = await this.validateScore(playerId, score);
    if (!isValid) {
      throw new Error('Score validation failed');
    }

    // Save to database
    await db.score.create({
      data: {
        playerId,
        leaderboardId,
        score,
        metadata
      }
    });

    // Update Redis sorted set
    await redis.zadd(`leaderboard:${leaderboardId}`, score, playerId);

    // Update player's best score
    await this.updateBestScore(playerId, leaderboardId, score);
  }

  private async updateBestScore(
    playerId: string,
    leaderboardId: string,
    newScore: number
  ): Promise<void> {
    const currentBest = await redis.zscore(
      `leaderboard:${leaderboardId}:best`,
      playerId
    );

    if (!currentBest || newScore > parseInt(currentBest)) {
      await redis.zadd(
        `leaderboard:${leaderboardId}:best`,
        newScore,
        playerId
      );
    }
  }

  private async validateScore(playerId: string, score: number): Promise<boolean> {
    // Get recent scores
    const recentScores = await db.score.findMany({
      where: {
        playerId,
        createdAt: {
          gte: new Date(Date.now() - 60 * 60 * 1000) // Last hour
        }
      },
      orderBy: { score: 'desc' },
      take: 10
    });

    // Check for impossible score jumps
    if (recentScores.length > 0) {
      const maxRecent = Math.max(...recentScores.map(s => s.score));
      if (score > maxRecent * 10) {
        return false; // Suspicious
      }
    }

    return true;
  }
}
```

## Ranking Algorithms

```typescript
// Get rankings from Redis
export class RankingService {
  async getGlobalRankings(
    leaderboardId: string,
    limit: number = 100,
    offset: number = 0
  ): Promise<LeaderboardEntry[]> {
    // Get top players from Redis (sorted set)
    const results = await redis.zrevrange(
      `leaderboard:${leaderboardId}:best`,
      offset,
      offset + limit - 1,
      'WITHSCORES'
    );

    const entries: LeaderboardEntry[] = [];

    for (let i = 0; i < results.length; i += 2) {
      const playerId = results[i];
      const score = parseInt(results[i + 1]);
      const rank = offset + (i / 2) + 1;

      // Get player info
      const player = await db.player.findUnique({
        where: { id: playerId }
      });

      if (player) {
        entries.push({
          rank,
          playerId,
          username: player.username,
          displayName: player.displayName,
          avatarUrl: player.avatarUrl,
          score
        });
      }
    }

    return entries;
  }

  async getPlayerRank(playerId: string, leaderboardId: string): Promise<number> {
    const rank = await redis.zrevrank(
      `leaderboard:${leaderboardId}:best`,
      playerId
    );

    return rank !== null ? rank + 1 : -1;
  }

  async getPlayersAroundRank(
    playerId: string,
    leaderboardId: string,
    range: number = 5
  ): Promise<LeaderboardEntry[]> {
    const playerRank = await this.getPlayerRank(playerId, leaderboardId);

    if (playerRank === -1) {
      return [];
    }

    const start = Math.max(0, playerRank - range - 1);
    const end = playerRank + range - 1;

    return this.getGlobalRankings(leaderboardId, end - start + 1, start);
  }
}

interface LeaderboardEntry {
  rank: number;
  playerId: string;
  username: string;
  displayName: string | null;
  avatarUrl: string | null;
  score: number;
}
```

## Friends Leaderboard

```typescript
// services/friends-leaderboard.service.ts
export class FriendsLeaderboardService {
  async getFriendsRankings(
    playerId: string,
    leaderboardId: string
  ): Promise<LeaderboardEntry[]> {
    // Get friend IDs
    const friendships = await db.friendship.findMany({
      where: {
        OR: [
          { playerId, status: 'accepted' },
          { friendId: playerId, status: 'accepted' }
        ]
      }
    });

    const friendIds = friendships.map(f =>
      f.playerId === playerId ? f.friendId : f.playerId
    );

    // Include self
    friendIds.push(playerId);

    // Get scores for all friends
    const scores = await redis.zrevrange(
      `leaderboard:${leaderboardId}:best`,
      0,
      -1,
      'WITHSCORES'
    );

    const friendScores: Array<{ playerId: string; score: number }> = [];

    for (let i = 0; i < scores.length; i += 2) {
      const id = scores[i];
      if (friendIds.includes(id)) {
        friendScores.push({
          playerId: id,
          score: parseInt(scores[i + 1])
        });
      }
    }

    // Sort by score
    friendScores.sort((a, b) => b.score - a.score);

    // Get player info
    const entries: LeaderboardEntry[] = [];

    for (let i = 0; i < friendScores.length; i++) {
      const { playerId: id, score } = friendScores[i];
      
      const player = await db.player.findUnique({
        where: { id }
      });

      if (player) {
        entries.push({
          rank: i + 1,
          playerId: id,
          username: player.username,
          displayName: player.displayName,
          avatarUrl: player.avatarUrl,
          score
        });
      }
    }

    return entries;
  }
}
```

## Time-based Leaderboards

```typescript
// services/time-based-leaderboard.service.ts
export class TimeBasedLeaderboardService {
  async getDailyLeaderboard(leaderboardId: string): Promise<LeaderboardEntry[]> {
    const today = new Date().toISOString().split('T')[0];
    const key = `leaderboard:${leaderboardId}:daily:${today}`;

    return this.getRankingsFromKey(key);
  }

  async getWeeklyLeaderboard(leaderboardId: string): Promise<LeaderboardEntry[]> {
    const weekNumber = this.getWeekNumber(new Date());
    const key = `leaderboard:${leaderboardId}:weekly:${weekNumber}`;

    return this.getRankingsFromKey(key);
  }

  async getMonthlyLeaderboard(leaderboardId: string): Promise<LeaderboardEntry[]> {
    const month = new Date().toISOString().slice(0, 7);
    const key = `leaderboard:${leaderboardId}:monthly:${month}`;

    return this.getRankingsFromKey(key);
  }

  async submitDailyScore(
    playerId: string,
    leaderboardId: string,
    score: number
  ): Promise<void> {
    const today = new Date().toISOString().split('T')[0];
    const key = `leaderboard:${leaderboardId}:daily:${today}`;

    await redis.zadd(key, score, playerId);
    await redis.expire(key, 7 * 24 * 60 * 60); // Keep for 7 days
  }

  private async getRankingsFromKey(key: string): Promise<LeaderboardEntry[]> {
    const results = await redis.zrevrange(key, 0, 99, 'WITHSCORES');

    const entries: LeaderboardEntry[] = [];

    for (let i = 0; i < results.length; i += 2) {
      const playerId = results[i];
      const score = parseInt(results[i + 1]);

      const player = await db.player.findUnique({
        where: { id: playerId }
      });

      if (player) {
        entries.push({
          rank: (i / 2) + 1,
          playerId,
          username: player.username,
          displayName: player.displayName,
          avatarUrl: player.avatarUrl,
          score
        });
      }
    }

    return entries;
  }

  private getWeekNumber(date: Date): string {
    const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
    const pastDaysOfYear = (date.getTime() - firstDayOfYear.getTime()) / 86400000;
    const weekNumber = Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
    
    return `${date.getFullYear()}-W${weekNumber}`;
  }
}
```

## Real-time Updates

```typescript
// services/leaderboard-realtime.service.ts
import { Server as SocketIOServer } from 'socket.io';

export class LeaderboardRealtimeService {
  constructor(private io: SocketIOServer) {
    this.setupHandlers();
  }

  private setupHandlers(): void {
    this.io.on('connection', (socket) => {
      socket.on('subscribe-leaderboard', (leaderboardId: string) => {
        socket.join(`leaderboard:${leaderboardId}`);
      });

      socket.on('unsubscribe-leaderboard', (leaderboardId: string) => {
        socket.leave(`leaderboard:${leaderboardId}`);
      });
    });
  }

  async broadcastScoreUpdate(
    leaderboardId: string,
    entry: LeaderboardEntry
  ): Promise<void> {
    this.io.to(`leaderboard:${leaderboardId}`).emit('score-update', entry);
  }

  async broadcastRankChange(
    leaderboardId: string,
    playerId: string,
    oldRank: number,
    newRank: number
  ): Promise<void> {
    this.io.to(`leaderboard:${leaderboardId}`).emit('rank-change', {
      playerId,
      oldRank,
      newRank
    });
  }
}
```

## Pagination

```typescript
// API endpoint with pagination
export async function getLeaderboard(req: Request, res: Response) {
  const { leaderboardId } = req.params;
  const page = parseInt(req.query.page as string) || 1;
  const limit = parseInt(req.query.limit as string) || 50;
  const offset = (page - 1) * limit;

  const rankings = await rankingService.getGlobalRankings(
    leaderboardId,
    limit,
    offset
  );

  const total = await redis.zcard(`leaderboard:${leaderboardId}:best`);

  res.json({
    data: rankings,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit)
    }
  });
}
```

## Cheating Prevention

```typescript
// services/anti-cheat.service.ts
export class AntiCheatService {
  async detectCheating(playerId: string, score: number): Promise<boolean> {
    // Check score distribution
    const avgScore = await this.getAverageScore(playerId);
    if (score > avgScore * 5) {
      await this.flagSuspiciousScore(playerId, score);
      return true;
    }

    // Check submission frequency
    const recentSubmissions = await this.getRecentSubmissions(playerId);
    if (recentSubmissions > 100) {
      await this.flagSuspiciousActivity(playerId);
      return true;
    }

    // Check for impossible scores
    const maxPossibleScore = await this.getMaxPossibleScore();
    if (score > maxPossibleScore) {
      await this.flagImpossibleScore(playerId, score);
      return true;
    }

    return false;
  }

  private async getAverageScore(playerId: string): Promise<number> {
    const scores = await db.score.findMany({
      where: { playerId },
      select: { score: true }
    });

    if (scores.length === 0) return 0;

    const sum = scores.reduce((acc, s) => acc + s.score, 0);
    return sum / scores.length;
  }

  private async getRecentSubmissions(playerId: string): Promise<number> {
    return db.score.count({
      where: {
        playerId,
        createdAt: {
          gte: new Date(Date.now() - 60 * 60 * 1000) // Last hour
        }
      }
    });
  }

  private async getMaxPossibleScore(): Promise<number> {
    // Game-specific logic
    return 1000000;
  }

  private async flagSuspiciousScore(playerId: string, score: number): Promise<void> {
    await db.suspiciousActivity.create({
      data: {
        playerId,
        type: 'suspicious_score',
        details: { score }
      }
    });
  }

  private async flagSuspiciousActivity(playerId: string): Promise<void> {
    await db.suspiciousActivity.create({
      data: {
        playerId,
        type: 'high_frequency_submissions'
      }
    });
  }

  private async flagImpossibleScore(playerId: string, score: number): Promise<void> {
    await db.suspiciousActivity.create({
      data: {
        playerId,
        type: 'impossible_score',
        details: { score }
      }
    });
  }
}
```

## Best Practices

1. **Redis** - Use Redis for fast rankings
2. **Caching** - Cache leaderboard data
3. **Pagination** - Always paginate results
4. **Real-time** - Use WebSocket for live updates
5. **Validation** - Validate all scores
6. **Anti-cheat** - Implement cheat detection
7. **Time-based** - Support periodic resets
8. **Friends** - Provide social leaderboards
9. **Analytics** - Track leaderboard engagement
10. **Performance** - Optimize for scale

## Resources

- [Redis Sorted Sets](https://redis.io/docs/data-types/sorted-sets/)
- [Leaderboard Design Patterns](https://redis.com/solutions/use-cases/leaderboards/)
- [Game Leaderboards](https://aws.amazon.com/blogs/gametech/building-game-leaderboards-with-amazon-elasticache-for-redis/)
