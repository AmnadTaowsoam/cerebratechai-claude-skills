---
name: Social Media API Integration
description: Connecting applications with social platforms for posting content, user authentication, analytics, and engagement tracking using OAuth flows, APIs, and webhooks.
---

# Social Media API Integration

> **Current Level:** Intermediate  
> **Domain:** Marketing / Integration

---

## Overview

Social media API integration enables applications to connect with social platforms for posting content, user authentication, analytics, and engagement tracking. Effective integration includes OAuth authentication, rate limiting, webhook handling, and proper error management.

---

## Core Concepts

### Table of Contents

1. [OAuth Flows for Social Platforms](#oauth-flows-for-social-platforms)
2. [Facebook/Meta API](#facebookmeta-api)
3. [Twitter/X API](#twitterx-api)
4. [LinkedIn API](#linkedin-api)
5. [Instagram API](#instagram-api)
6. [Social Sharing Buttons](#social-sharing-buttons)
7. [Open Graph Tags](#open-graph-tags)
8. [Social Login Integration](#social-login-integration)
9. [Rate Limiting Handling](#rate-limiting-handling)
10. [Webhook Handling](#webhook-handling)
11. [Analytics](#analytics)
12. [Best Practices](#best-practices)

---

## OAuth Flows for Social Platforms

### OAuth 2.0 Authorization Code Flow

```typescript
// Generic OAuth 2.0 flow implementation
import express from 'express';
import crypto from 'crypto';

const app = express();

// Generate state parameter for CSRF protection
function generateState(): string {
  return crypto.randomBytes(16).toString('hex');
}

// Store state in session
app.get('/auth/:provider', (req, res) => {
  const { provider } = req.params;
  const state = generateState();
  
  // Store state in session
  req.session.oauthState = state;
  
  const authUrls: Record<string, string> = {
    facebook: `https://www.facebook.com/v18.0/dialog/oauth?${new URLSearchParams({
      client_id: process.env.FACEBOOK_APP_ID!,
      redirect_uri: `${process.env.APP_URL}/auth/facebook/callback`,
      scope: 'public_profile,email',
      state,
      response_type: 'code',
    })}`,
    twitter: `https://twitter.com/i/oauth2/authorize?${new URLSearchParams({
      client_id: process.env.TWITTER_CLIENT_ID!,
      redirect_uri: `${process.env.APP_URL}/auth/twitter/callback`,
      scope: 'tweet.read tweet.write users.read',
      state,
      response_type: 'code',
      code_challenge: generateCodeChallenge(),
      code_challenge_method: 'S256',
    })}`,
    linkedin: `https://www.linkedin.com/oauth/v2/authorization?${new URLSearchParams({
      response_type: 'code',
      client_id: process.env.LINKEDIN_CLIENT_ID!,
      redirect_uri: `${process.env.APP_URL}/auth/linkedin/callback`,
      state,
      scope: 'r_liteprofile r_emailaddress w_member_social',
    })}`,
  };
  
  res.redirect(authUrls[provider]);
});

// OAuth callback handler
app.get('/auth/:provider/callback', async (req, res) => {
  const { provider } = req.params;
  const { code, state } = req.query;
  
  // Verify state
  if (state !== req.session.oauthState) {
    return res.status(400).send('Invalid state parameter');
  }
  
  try {
    const token = await exchangeCodeForToken(provider, code as string);
    const profile = await getUserProfile(provider, token);
    
    // Create or update user
    const user = await findOrCreateUser(profile, provider);
    
    // Generate JWT
    const jwt = generateJWT(user);
    
    res.redirect(`${process.env.FRONTEND_URL}/auth/callback?token=${jwt}`);
  } catch (error) {
    console.error('OAuth error:', error);
    res.redirect(`${process.env.FRONTEND_URL}/auth/error`);
  }
});

// Exchange authorization code for access token
async function exchangeCodeForToken(
  provider: string,
  code: string
): Promise<string> {
  const tokenUrls: Record<string, string> = {
    facebook: 'https://graph.facebook.com/v18.0/oauth/access_token',
    twitter: 'https://api.twitter.com/2/oauth2/token',
    linkedin: 'https://www.linkedin.com/oauth/v2/accessToken',
  };
  
  const body: Record<string, string> = {
    grant_type: 'authorization_code',
    code,
    redirect_uri: `${process.env.APP_URL}/auth/${provider}/callback`,
  };
  
  switch (provider) {
    case 'facebook':
      body.client_id = process.env.FACEBOOK_APP_ID!;
      body.client_secret = process.env.FACEBOOK_APP_SECRET!;
      break;
    case 'twitter':
      body.client_id = process.env.TWITTER_CLIENT_ID!;
      body.client_secret = process.env.TWITTER_CLIENT_SECRET!;
      body.code_verifier = getCodeVerifier();
      break;
    case 'linkedin':
      body.client_id = process.env.LINKEDIN_CLIENT_ID!;
      body.client_secret = process.env.LINKEDIN_CLIENT_SECRET!;
      break;
  }
  
  const response = await fetch(tokenUrls[provider], {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(body),
  });
  
  const data = await response.json();
  return data.access_token;
}
```

### PKCE Flow for Twitter

```typescript
// Twitter uses PKCE (Proof Key for Code Exchange)
function generateCodeVerifier(): string {
  return crypto.randomBytes(32).toString('base64url');
}

function generateCodeChallenge(verifier: string): string {
  return crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');
}

// Store code verifier in session
app.get('/auth/twitter', (req, res) => {
  const verifier = generateCodeVerifier();
  const challenge = generateCodeChallenge(verifier);
  
  req.session.codeVerifier = verifier;
  
  const authUrl = `https://twitter.com/i/oauth2/authorize?${new URLSearchParams({
    client_id: process.env.TWITTER_CLIENT_ID!,
    redirect_uri: `${process.env.APP_URL}/auth/twitter/callback`,
    scope: 'tweet.read tweet.write users.read',
    state: generateState(),
    response_type: 'code',
    code_challenge: challenge,
    code_challenge_method: 'S256',
  })}`;
  
  res.redirect(authUrl);
});
```

---

## Facebook/Meta API

### Authentication

```typescript
import { GraphRequest, GraphRequestManager, AccessToken } from 'react-native-fbsdk-next';

// Login with Facebook
export async function loginWithFacebook(): Promise<{
  accessToken: string;
  userId: string;
}> {
  const result = await AccessToken.getCurrentAccessToken();
  
  if (!result) {
    throw new Error('Facebook login failed');
  }
  
  return {
    accessToken: result.accessToken.toString(),
    userId: result.userID,
  };
}

// Get user profile
export async function getFacebookProfile(accessToken: string): Promise<{
  id: string;
  name: string;
  email: string;
  picture: string;
}> {
  const response = await fetch(
    `https://graph.facebook.com/me?${new URLSearchParams({
      fields: 'id,name,email,picture.width(400)',
      access_token: accessToken,
    })}`
  );
  
  const data = await response.json();
  
  return {
    id: data.id,
    name: data.name,
    email: data.email,
    picture: data.picture?.data?.url,
  };
}

// Refresh access token
export async function refreshFacebookToken(accessToken: string): Promise<string> {
  const response = await fetch(
    `https://graph.facebook.com/oauth/access_token?${new URLSearchParams({
      grant_type: 'fb_exchange_token',
      client_id: process.env.FACEBOOK_APP_ID!,
      client_secret: process.env.FACEBOOK_APP_SECRET!,
      fb_exchange_token: accessToken,
    })}`
  );
  
  const data = await response.json();
  return data.access_token;
}
```

### Posts

```typescript
interface FacebookPost {
  message?: string;
  link?: string;
  picture?: string;
  caption?: string;
  description?: string;
}

// Create a post
export async function createFacebookPost(
  pageId: string,
  pageAccessToken: string,
  post: FacebookPost
): Promise<string> {
  const response = await fetch(
    `https://graph.facebook.com/${pageId}/feed`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...post,
        access_token: pageAccessToken,
      }),
    }
  );
  
  const data = await response.json();
  
  if (data.error) {
    throw new Error(data.error.message);
  }
  
  return data.id;
}

// Upload photo
export async function uploadFacebookPhoto(
  pageId: string,
  pageAccessToken: string,
  photoUrl: string,
  caption?: string
): Promise<string> {
  const response = await fetch(
    `https://graph.facebook.com/${pageId}/photos`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        url: photoUrl,
        caption,
        access_token: pageAccessToken,
      }),
    }
  );
  
  const data = await response.json();
  return data.id;
}

// Schedule post
export async function scheduleFacebookPost(
  pageId: string,
  pageAccessToken: string,
  post: FacebookPost,
  scheduledTime: Date
): Promise<string> {
  const response = await fetch(
    `https://graph.facebook.com/${pageId}/feed`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...post,
        published: false,
        scheduled_publish_time: Math.floor(scheduledTime.getTime() / 1000),
        access_token: pageAccessToken,
      }),
    }
  );
  
  const data = await response.json();
  return data.id;
}

// Delete post
export async function deleteFacebookPost(
  postId: string,
  pageAccessToken: string
): Promise<boolean> {
  const response = await fetch(
    `https://graph.facebook.com/${postId}?${new URLSearchParams({
      access_token: pageAccessToken,
    })}`,
    { method: 'DELETE' }
  );
  
  return response.ok;
}
```

### Page Management

```typescript
// Get user's pages
export async function getUserPages(accessToken: string): Promise<Array<{
  id: string;
  name: string;
  category: string;
  access_token?: string;
}>> {
  const response = await fetch(
    `https://graph.facebook.com/me/accounts?${new URLSearchParams({
      access_token: accessToken,
    })}`
  );
  
  const data = await response.json();
  return data.data;
}

// Get page access token
export async function getPageAccessToken(
  pageId: string,
  userAccessToken: string
): Promise<string> {
  const pages = await getUserPages(userAccessToken);
  const page = pages.find(p => p.id === pageId);
  
  if (!page || !page.access_token) {
    throw new Error('Page access token not found');
  }
  
  return page.access_token;
}

// Get page insights
export async function getPageInsights(
  pageId: string,
  pageAccessToken: string,
  metrics: string[] = ['page_impressions', 'page_engaged_users', 'page_post_engagements'],
  period: 'day' | 'week' | 'days_28' = 'day',
  datePreset?: string
): Promise<any> {
  const params = new URLSearchParams({
    metric: metrics.join(','),
    period,
    access_token: pageAccessToken,
  });
  
  if (datePreset) {
    params.append('date_preset', datePreset);
  }
  
  const response = await fetch(
    `https://graph.facebook.com/${pageId}/insights?${params}`
  );
  
  const data = await response.json();
  return data.data;
}
```

### Insights

```typescript
// Get post insights
export async function getPostInsights(
  postId: string,
  pageAccessToken: string
): Promise<{
  impressions: number;
  reach: number;
  engagements: number;
  clicks: number;
  shares: number;
  comments: number;
}> {
  const response = await fetch(
    `https://graph.facebook.com/${postId}/insights?${new URLSearchParams({
      metric: 'post_impressions,post_reach,post_engaged_users,post_clicks,post_shares,post_comments',
      access_token: pageAccessToken,
    })}`
  );
  
  const data = await response.json();
  const insights = data.data;
  
  return {
    impressions: insights.find((i: any) => i.name === 'post_impressions')?.values[0]?.value || 0,
    reach: insights.find((i: any) => i.name === 'post_reach')?.values[0]?.value || 0,
    engagements: insights.find((i: any) => i.name === 'post_engaged_users')?.values[0]?.value || 0,
    clicks: insights.find((i: any) => i.name === 'post_clicks')?.values[0]?.value || 0,
    shares: insights.find((i: any) => i.name === 'post_shares')?.values[0]?.value || 0,
    comments: insights.find((i: any) => i.name === 'post_comments')?.values[0]?.value || 0,
  };
}

// Get video insights
export async function getVideoInsights(
  videoId: string,
  pageAccessToken: string
): Promise<{
  totalViews: number;
  uniqueViews: number;
  averageViewTime: number;
  completionRate: number;
}> {
  const response = await fetch(
    `https://graph.facebook.com/${videoId}/insights?${new URLSearchParams({
      metric: 'total_video_views,total_video_view_unique_views,total_video_view_time_by_age_bucket_and_gender,total_video_complete_views',
      access_token: pageAccessToken,
    })}`
  );
  
  const data = await response.json();
  const insights = data.data;
  
  return {
    totalViews: insights.find((i: any) => i.name === 'total_video_views')?.values[0]?.value || 0,
    uniqueViews: insights.find((i: any) => i.name === 'total_video_view_unique_views')?.values[0]?.value || 0,
    averageViewTime: insights.find((i: any) => i.name === 'total_video_view_time_by_age_bucket_and_gender')?.values[0]?.value || 0,
    completionRate: insights.find((i: any) => i.name === 'total_video_complete_views')?.values[0]?.value || 0,
  };
}
```

---

## Twitter/X API

### Authentication

```typescript
// Twitter OAuth 2.0
export async function loginWithTwitter(): Promise<{
  accessToken: string;
  refreshToken: string;
}> {
  // Get authorization code
  const authUrl = `https://twitter.com/i/oauth2/authorize?${new URLSearchParams({
    client_id: process.env.TWITTER_CLIENT_ID!,
    redirect_uri: `${process.env.APP_URL}/auth/twitter/callback`,
    scope: 'tweet.read tweet.write users.read offline.access',
    response_type: 'code',
    state: generateState(),
    code_challenge: generateCodeChallenge(getCodeVerifier()),
    code_challenge_method: 'S256',
  })}`;
  
  // Redirect user to auth URL
  // After callback, exchange code for tokens
  
  const tokens = await exchangeTwitterCodeForTokens(code);
  return tokens;
}

async function exchangeTwitterCodeForTokens(code: string): Promise<{
  accessToken: string;
  refreshToken: string;
}> {
  const response = await fetch('https://api.twitter.com/2/oauth2/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: `${process.env.APP_URL}/auth/twitter/callback`,
      client_id: process.env.TWITTER_CLIENT_ID!,
      code_verifier: getCodeVerifier(),
    }),
  });
  
  const data = await response.json();
  return {
    accessToken: data.access_token,
    refreshToken: data.refresh_token,
  };
}

// Refresh access token
export async function refreshTwitterToken(refreshToken: string): Promise<string> {
  const response = await fetch('https://api.twitter.com/2/oauth2/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
      client_id: process.env.TWITTER_CLIENT_ID!,
    }),
  });
  
  const data = await response.json();
  return data.access_token;
}
```

### Tweets

```typescript
interface Tweet {
  text: string;
  media?: {
    media_ids: string[];
    tagged_user_ids?: string[];
  };
  reply_settings?: 'mentionedUsers' | 'following' | 'none';
  geo?: {
    place_id: string;
  };
}

// Create a tweet
export async function createTweet(
  accessToken: string,
  tweet: Tweet
): Promise<{ id: string; text: string }> {
  const response = await fetch('https://api.twitter.com/2/tweets', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(tweet),
  });
  
  const data = await response.json();
  
  if (data.errors) {
    throw new Error(data.errors[0].message);
  }
  
  return data.data;
}

// Upload media
export async function uploadTwitterMedia(
  accessToken: string,
  media: Buffer,
  mediaType: 'image/jpeg' | 'image/png' | 'image/gif' | 'video/mp4'
): Promise<string> {
  const response = await fetch('https://upload.twitter.com/1.1/media/upload.json', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'multipart/form-data',
    },
    body: media,
  });
  
  const data = await response.json();
  return data.media_id_string;
}

// Reply to tweet
export async function replyToTweet(
  accessToken: string,
  tweetId: string,
  text: string
): Promise<{ id: string; text: string }> {
  return await createTweet(accessToken, {
    text,
    reply_settings: 'mentionedUsers',
    in_reply_to_tweet_id: tweetId,
  });
}

// Delete tweet
export async function deleteTweet(
  accessToken: string,
  tweetId: string
): Promise<{ id: string; deleted: boolean }> {
  const response = await fetch(`https://api.twitter.com/2/tweets/${tweetId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
  });
  
  const data = await response.json();
  return data.data;
}

// Get tweet by ID
export async function getTweet(
  accessToken: string,
  tweetId: string,
  expansions?: string[]
): Promise<any> {
  const params = new URLSearchParams({
    'tweet.fields': 'created_at,public_metrics,context_annotations,entities',
  });
  
  if (expansions) {
    params.append('expansions', expansions.join(','));
  }
  
  const response = await fetch(
    `https://api.twitter.com/2/tweets/${tweetId}?${params}`,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    }
  );
  
  const data = await response.json();
  return data.data;
}

// Get user timeline
export async function getUserTimeline(
  accessToken: string,
  userId: string,
  options?: {
    maxResults?: number;
    exclude?: 'retweets' | 'replies';
    sinceId?: string;
  }
): Promise<any[]> {
  const params = new URLSearchParams({
    'tweet.fields': 'created_at,public_metrics,context_annotations',
    max_results: (options?.maxResults || 10).toString(),
  });
  
  if (options?.exclude) {
    params.append('exclude', options.exclude);
  }
  
  if (options?.sinceId) {
    params.append('since_id', options.sinceId);
  }
  
  const response = await fetch(
    `https://api.twitter.com/2/users/${userId}/tweets?${params}`,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      },
    }
  );
  
  const data = await response.json();
  return data.data || [];
}
```

### Webhooks

```typescript
import express from 'express';

const app = express();

// Verify webhook challenge
app.get('/webhooks/twitter', (req, res) => {
  const { crc_token } = req.query;
  
  if (crc_token) {
    const hmac = crypto
      .createHmac('sha256', process.env.TWITTER_CONSUMER_SECRET!)
      .update(crc_token as string)
      .digest('base64');
    
    res.json({ response_token: `sha256=${hmac}` });
  } else {
    res.status(400).send('Missing crc_token');
  }
});

// Handle webhook events
app.post('/webhooks/twitter', express.json(), (req, res) => {
  const events = req.body;
  
  events.forEach((event: any) => {
    switch (event.type) {
      case 'tweet_create_events':
        handleNewTweet(event);
        break;
      case 'favorite_events':
        handleLikeEvent(event);
        break;
      case 'follow_events':
        handleFollowEvent(event);
        break;
      case 'direct_message_events':
        handleDirectMessage(event);
        break;
    }
  });
  
  res.status(200).send('OK');
});

function handleNewTweet(event: any): void {
  console.log('New tweet:', event.tweet_create_events[0]);
  // Process new tweet
}

function handleLikeEvent(event: any): void {
  console.log('Tweet liked:', event.favorite_events[0]);
  // Process like event
}

function handleFollowEvent(event: any): void {
  console.log('New follower:', event.follow_events[0]);
  // Process follow event
}

function handleDirectMessage(event: any): void {
  console.log('Direct message:', event.direct_message_events[0]);
  // Process direct message
}
```

---

## LinkedIn API

### Authentication

```typescript
// LinkedIn OAuth 2.0
export async function loginWithLinkedIn(): Promise<{
  accessToken: string;
  expiresIn: number;
}> {
  const authUrl = `https://www.linkedin.com/oauth/v2/authorization?${new URLSearchParams({
    response_type: 'code',
    client_id: process.env.LINKEDIN_CLIENT_ID!,
    redirect_uri: `${process.env.APP_URL}/auth/linkedin/callback`,
    scope: 'r_liteprofile r_emailaddress w_member_social',
    state: generateState(),
  })}`;
  
  // Redirect user to auth URL
  // After callback, exchange code for token
  
  const token = await exchangeLinkedInCodeForToken(code);
  return token;
}

async function exchangeLinkedInCodeForToken(code: string): Promise<{
  accessToken: string;
  expiresIn: number;
}> {
  const response = await fetch('https://www.linkedin.com/oauth/v2/accessToken', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: `${process.env.APP_URL}/auth/linkedin/callback`,
      client_id: process.env.LINKEDIN_CLIENT_ID!,
      client_secret: process.env.LINKEDIN_CLIENT_SECRET!,
    }),
  });
  
  const data = await response.json();
  return {
    accessToken: data.access_token,
    expiresIn: data.expires_in,
  };
}
```

### Posts

```typescript
interface LinkedInPost {
  author: string;
  lifecycleState: 'PUBLISHED' | 'DRAFT';
  specificContent: {
    'com.linkedin.ugc.ShareContent': {
      shareCommentary: {
        text: string;
      };
      shareMediaCategory: 'NONE' | 'IMAGE' | 'VIDEO' | 'ARTICLE';
      media?: Array<{
        status: 'READY';
        description?: {
          text: string;
        };
        media: string; // URN of uploaded media
        title?: {
          text: string;
        };
      }>;
    };
  };
  visibility: {
    'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC' | 'CONNECTIONS';
  };
}

// Create a post
export async function createLinkedInPost(
  accessToken: string,
  post: LinkedInPost
): Promise<string> {
  const response = await fetch('https://api.linkedin.com/v2/ugcPosts', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
      'X-Restli-Protocol-Version': '2.0.0',
    },
    body: JSON.stringify(post),
  });
  
  const data = await response.json();
  
  if (data.error) {
    throw new Error(data.error.message);
  }
  
  return data.id;
}

// Create text post
export async function createTextPost(
  accessToken: string,
  authorUrn: string,
  text: string,
  visibility: 'PUBLIC' | 'CONNECTIONS' = 'PUBLIC'
): Promise<string> {
  return await createLinkedInPost(accessToken, {
    author: authorUrn,
    lifecycleState: 'PUBLISHED',
    specificContent: {
      'com.linkedin.ugc.ShareContent': {
        shareCommentary: { text },
        shareMediaCategory: 'NONE',
      },
    },
    visibility: {
      'com.linkedin.ugc.MemberNetworkVisibility': visibility,
    },
  });
}

// Upload image
export async function uploadLinkedInImage(
  accessToken: string,
  authorUrn: string,
  image: Buffer,
  filename: string
): Promise<string> {
  // Register upload
  const registerResponse = await fetch('https://api.linkedin.com/v2/assets?action=registerUpload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
      'X-Restli-Protocol-Version': '2.0.0',
    },
    body: JSON.stringify({
      registerUploadRequest: {
        owner: authorUrn,
        recipes: ['urn:li:digitalmediaAsset:urn:li:digitalmediaMediaArtifact:(urn:li:digitalmediaAsset:*,urn:li:digitalmediaMediaArtifact:(urn:li:digitalmediaAsset:*,urn:li:digitalmediaMediaArtifact:*))'],
        serviceRelationships: [
          {
            relationshipType: 'OWNER',
            identifier: 'urn:li:userGeneratedContent',
          },
        ],
        supportedUploadMechanism: ['SYNCHRONOUS_UPLOAD'],
      },
    }),
  });
  
  const registerData = await registerResponse.json();
  const uploadUrl = registerData.value.uploadMechanism['com.linkedin.digitalmedia.uploading.MediaUploadRequest'].uploadUrl;
  const assetUrn = registerData.value.asset;
  
  // Upload image
  await fetch(uploadUrl, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/octet-stream',
    },
    body: image,
  });
  
  return assetUrn;
}

// Create image post
export async function createImagePost(
  accessToken: string,
  authorUrn: string,
  text: string,
  imageAssetUrn: string,
  visibility: 'PUBLIC' | 'CONNECTIONS' = 'PUBLIC'
): Promise<string> {
  return await createLinkedInPost(accessToken, {
    author: authorUrn,
    lifecycleState: 'PUBLISHED',
    specificContent: {
      'com.linkedin.ugc.ShareContent': {
        shareCommentary: { text },
        shareMediaCategory: 'IMAGE',
        media: [
          {
            status: 'READY',
            media: imageAssetUrn,
          },
        ],
      },
    },
    visibility: {
      'com.linkedin.ugc.MemberNetworkVisibility': visibility,
    },
  });
}
```

### Company Pages

```typescript
// Get company page
export async function getCompanyPage(
  accessToken: string,
  organizationUrn: string
): Promise<any> {
  const response = await fetch(
    `https://api.linkedin.com/v2/organizations/${organizationUrn}`,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'X-Restli-Protocol-Version': '2.0.0',
      },
    }
  );
  
  return await response.json();
}

// Get company posts
export async function getCompanyPosts(
  accessToken: string,
  organizationUrn: string,
  count: number = 10
): Promise<any[]> {
  const response = await fetch(
    `https://api.linkedin.com/v2/ugcPosts?q=authors&authors=List(${organizationUrn})&count=${count}`,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'X-Restli-Protocol-Version': '2.0.0',
      },
    }
  );
  
  const data = await response.json();
  return data.elements || [];
}

// Get company statistics
export async function getCompanyStats(
  accessToken: string,
  organizationUrn: string
): Promise<{
  followerCount: number;
  employeeCount: number;
}> {
  const response = await fetch(
    `https://api.linkedin.com/v2/organizationalEntityFollowerStatistics?q=organizationalEntity&organizationalEntity=${organizationUrn}`,
    {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'X-Restli-Protocol-Version': '2.0.0',
      },
    }
  );
  
  const data = await response.json();
  return {
    followerCount: data.elements?.[0]?.totalFollowerCount || 0,
    employeeCount: data.elements?.[0]?.employeeCount || 0,
  };
}
```

---

## Instagram API

### Authentication (via Facebook)

```typescript
// Instagram uses Facebook OAuth
export async function loginWithInstagram(): Promise<{
  accessToken: string;
  userId: string;
}> {
  const authUrl = `https://api.instagram.com/oauth/authorize?${new URLSearchParams({
    client_id: process.env.FACEBOOK_APP_ID!,
    redirect_uri: `${process.env.APP_URL}/auth/instagram/callback`,
    scope: 'user_profile,user_media',
    response_type: 'code',
  })}`;
  
  // Redirect user to auth URL
  // After callback, exchange code for token
  
  const token = await exchangeInstagramCodeForToken(code);
  return token;
}

async function exchangeInstagramCodeForToken(code: string): Promise<{
  accessToken: string;
  userId: string;
}> {
  const response = await fetch(
    `https://api.instagram.com/oauth/access_token`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        client_id: process.env.FACEBOOK_APP_ID!,
        client_secret: process.env.FACEBOOK_APP_SECRET!,
        grant_type: 'authorization_code',
        redirect_uri: `${process.env.APP_URL}/auth/instagram/callback`,
        code,
      }),
    }
  );
  
  const data = await response.json();
  return {
    accessToken: data.access_token,
    userId: data.user_id,
  };
}

// Get long-lived token
export async function getLongLivedToken(shortLivedToken: string): Promise<string> {
  const response = await fetch(
    `https://graph.instagram.com/access_token?${new URLSearchParams({
      grant_type: 'ig_exchange_token',
      client_secret: process.env.FACEBOOK_APP_SECRET!,
      access_token: shortLivedToken,
    })}`
  );
  
  const data = await response.json();
  return data.access_token;
}
```

### Instagram Business API

```typescript
// Get Instagram business account
export async function getInstagramBusinessAccount(
  pageAccessToken: string,
  pageId: string
): Promise<string> {
  const response = await fetch(
    `https://graph.facebook.com/${pageId}?fields=instagram_business_account&access_token=${pageAccessToken}`
  );
  
  const data = await response.json();
  return data.instagram_business_account?.id;
}

// Get user media
export async function getUserMedia(
  accessToken: string,
  userId: string,
  limit: number = 25
): Promise<any[]> {
  const response = await fetch(
    `https://graph.facebook.com/${userId}/media?${new URLSearchParams({
      fields: 'id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count',
      limit: limit.toString(),
      access_token: accessToken,
    })}`
  );
  
  const data = await response.json();
  return data.data || [];
}

// Create media container (for publishing)
export async function createMediaContainer(
  accessToken: string,
  instagramBusinessAccountId: string,
  imageUrl: string,
  caption?: string
): Promise<string> {
  const response = await fetch(
    `https://graph.facebook.com/${instagramBusinessAccountId}/media`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image_url: imageUrl,
        caption,
        access_token: accessToken,
      }),
    }
  );
  
  const data = await response.json();
  return data.id;
}

// Publish media
export async function publishMedia(
  accessToken: string,
  instagramBusinessAccountId: string,
  creationId: string
): Promise<string> {
  const response = await fetch(
    `https://graph.facebook.com/${instagramBusinessAccountId}/media_publish`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        creation_id: creationId,
        access_token: accessToken,
      }),
    }
  );
  
  const data = await response.json();
  return data.id;
}

// Get insights
export async function getInstagramInsights(
  accessToken: string,
  mediaId: string,
  metrics: string[] = ['impressions', 'reach', 'engagement']
): Promise<any> {
  const response = await fetch(
    `https://graph.facebook.com/${mediaId}/insights?${new URLSearchParams({
      metric: metrics.join(','),
      access_token: accessToken,
    })}`
  );
  
  const data = await response.json();
  return data.data;
}
```

---

## Social Sharing Buttons

### React Component

```tsx
import React from 'react';

interface ShareButtonProps {
  url: string;
  title?: string;
  description?: string;
  imageUrl?: string;
  hashtags?: string[];
}

const SocialShareButtons: React.FC<ShareButtonProps> = ({
  url,
  title = '',
  description = '',
  imageUrl = '',
  hashtags = [],
}) => {
  const encodedUrl = encodeURIComponent(url);
  const encodedTitle = encodeURIComponent(title);
  const encodedDescription = encodeURIComponent(description);
  const encodedHashtags = encodeURIComponent(hashtags.join(','));

  const shareUrls = {
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`,
    twitter: `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}&hashtags=${encodedHashtags}`,
    linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`,
    whatsapp: `https://wa.me/?text=${encodedTitle}%20${encodedUrl}`,
    email: `mailto:?subject=${encodedTitle}&body=${encodedDescription}%0A%0A${encodedUrl}`,
    pinterest: `https://pinterest.com/pin/create/button/?url=${encodedUrl}&description=${encodedDescription}&media=${encodeURIComponent(imageUrl)}`,
  };

  const handleShare = (platform: string) => {
    const shareUrl = shareUrls[platform as keyof typeof shareUrls];
    if (shareUrl) {
      window.open(shareUrl, '_blank', 'width=600,height=400');
    }
  };

  return (
    <div className="social-share-buttons">
      <button onClick={() => handleShare('facebook')} aria-label="Share on Facebook">
        <svg>...</svg>
      </button>
      <button onClick={() => handleShare('twitter')} aria-label="Share on Twitter">
        <svg>...</svg>
      </button>
      <button onClick={() => handleShare('linkedin')} aria-label="Share on LinkedIn">
        <svg>...</svg>
      </button>
      <button onClick={() => handleShare('whatsapp')} aria-label="Share on WhatsApp">
        <svg>...</svg>
      </button>
      <button onClick={() => handleShare('email')} aria-label="Share via Email">
        <svg>...</svg>
      </button>
    </div>
  );
};

export default SocialShareButtons;
```

### Native Share API

```typescript
// Web Share API
export async function nativeShare(shareData: {
  title?: string;
  text?: string;
  url?: string;
}): Promise<void> {
  if (navigator.share) {
    try {
      await navigator.share(shareData);
    } catch (error) {
      console.error('Error sharing:', error);
      throw error;
    }
  } else {
    throw new Error('Web Share API not supported');
  }
}

// Usage
<button onClick={() => nativeShare({
  title: 'Check this out!',
  text: 'I found this amazing article',
  url: 'https://example.com/article'
})}>
  Share
</button>
```

---

## Open Graph Tags

### HTML Meta Tags

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Page Title</title>
  
  <!-- Basic Open Graph -->
  <meta property="og:title" content="Your Page Title">
  <meta property="og:description" content="Your page description">
  <meta property="og:image" content="https://example.com/image.jpg">
  <meta property="og:url" content="https://example.com/page">
  <meta property="og:type" content="website">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@yourhandle">
  <meta name="twitter:creator" content="@authorhandle">
  <meta name="twitter:title" content="Your Page Title">
  <meta name="twitter:description" content="Your page description">
  <meta name="twitter:image" content="https://example.com/image.jpg">
  
  <!-- Additional Open Graph -->
  <meta property="og:site_name" content="Your Site Name">
  <meta property="og:locale" content="en_US">
  <meta property="og:locale:alternate" content="th_TH">
  
  <!-- Article specific -->
  <meta property="article:published_time" content="2024-01-15T10:00:00Z">
  <meta property="article:modified_time" content="2024-01-15T12:00:00Z">
  <meta property="article:author" content="Author Name">
  <meta property="article:section" content="Technology">
  <meta property="article:tag" content="tag1,tag2,tag3">
</head>
<body>
  <!-- Page content -->
</body>
</html>
```

### Dynamic Open Graph Generation

```typescript
// Generate Open Graph tags dynamically
export function generateOpenGraphTags(data: {
  title: string;
  description: string;
  image?: string;
  url: string;
  type?: 'website' | 'article' | 'product';
  twitterCard?: 'summary' | 'summary_large_image' | 'app' | 'player';
  article?: {
    publishedTime?: string;
    modifiedTime?: string;
    author?: string;
    section?: string;
    tags?: string[];
  };
}): string {
  const tags: string[] = [];
  
  // Basic Open Graph
  tags.push(`<meta property="og:title" content="${escapeHtml(data.title)}">`);
  tags.push(`<meta property="og:description" content="${escapeHtml(data.description)}">`);
  tags.push(`<meta property="og:url" content="${escapeHtml(data.url)}">`);
  tags.push(`<meta property="og:type" content="${data.type || 'website'}">`);
  
  if (data.image) {
    tags.push(`<meta property="og:image" content="${escapeHtml(data.image)}">`);
  }
  
  // Twitter Card
  tags.push(`<meta name="twitter:card" content="${data.twitterCard || 'summary_large_image'}">`);
  tags.push(`<meta name="twitter:title" content="${escapeHtml(data.title)}">`);
  tags.push(`<meta name="twitter:description" content="${escapeHtml(data.description)}">`);
  
  if (data.image) {
    tags.push(`<meta name="twitter:image" content="${escapeHtml(data.image)}">`);
  }
  
  // Article specific
  if (data.type === 'article' && data.article) {
    if (data.article.publishedTime) {
      tags.push(`<meta property="article:published_time" content="${data.article.publishedTime}">`);
    }
    if (data.article.modifiedTime) {
      tags.push(`<meta property="article:modified_time" content="${data.article.modifiedTime}">`);
    }
    if (data.article.author) {
      tags.push(`<meta property="article:author" content="${escapeHtml(data.article.author)}">`);
    }
    if (data.article.section) {
      tags.push(`<meta property="article:section" content="${escapeHtml(data.article.section)}">`);
    }
    if (data.article.tags) {
      data.article.tags.forEach(tag => {
        tags.push(`<meta property="article:tag" content="${escapeHtml(tag)}">`);
      });
    }
  }
  
  return tags.join('\n');
}

function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    '&': '&',
    '<': '<',
    '>': '>',
    '"': '"',
    "'": '&#039;',
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}
```

---

## Social Login Integration

### NextAuth.js Configuration

```typescript
// pages/api/auth/[...nextauth].ts
import NextAuth from 'next-auth';
import FacebookProvider from 'next-auth/providers/facebook';
import GoogleProvider from 'next-auth/providers/google';
import TwitterProvider from 'next-auth/providers/twitter';
import LinkedInProvider from 'next-auth/providers/linkedin';

export default NextAuth({
  providers: [
    FacebookProvider({
      clientId: process.env.FACEBOOK_CLIENT_ID!,
      clientSecret: process.env.FACEBOOK_CLIENT_SECRET!,
    }),
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    TwitterProvider({
      clientId: process.env.TWITTER_CLIENT_ID!,
      clientSecret: process.env.TWITTER_CLIENT_SECRET!,
      version: '2.0',
    }),
    LinkedInProvider({
      clientId: process.env.LINKEDIN_CLIENT_ID!,
      clientSecret: process.env.LINKEDIN_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    async signIn({ user, account, profile }) {
      // Custom sign-in logic
      return true;
    },
    async jwt({ token, account, profile }) {
      // Add custom claims to token
      if (account) {
        token.accessToken = account.access_token;
        token.provider = account.provider;
      }
      return token;
    },
    async session({ session, token }) {
      // Add custom data to session
      session.accessToken = token.accessToken as string;
      session.provider = token.provider as string;
      return session;
    },
  },
  pages: {
    signIn: '/auth/signin',
    error: '/auth/error',
  },
});
```

### Custom Social Login Component

```tsx
import React from 'react';
import { signIn } from 'next-auth/react';

const SocialLoginButtons: React.FC = () => {
  const socialProviders = [
    {
      id: 'google',
      name: 'Google',
      icon: '/icons/google.svg',
      color: '#DB4437',
    },
    {
      id: 'facebook',
      name: 'Facebook',
      icon: '/icons/facebook.svg',
      color: '#4267B2',
    },
    {
      id: 'twitter',
      name: 'Twitter',
      icon: '/icons/twitter.svg',
      color: '#1DA1F2',
    },
    {
      id: 'linkedin',
      name: 'LinkedIn',
      icon: '/icons/linkedin.svg',
      color: '#0077B5',
    },
  ];

  return (
    <div className="social-login-buttons">
      {socialProviders.map((provider) => (
        <button
          key={provider.id}
          onClick={() => signIn(provider.id)}
          className="social-login-button"
          style={{ backgroundColor: provider.color }}
        >
          <img src={provider.icon} alt={provider.name} />
          <span>Continue with {provider.name}</span>
        </button>
      ))}
    </div>
  );
};

export default SocialLoginButtons;
```

---

## Rate Limiting Handling

### Rate Limiter Implementation

```typescript
interface RateLimitConfig {
  requests: number;
  window: number; // in milliseconds
}

interface RateLimiter {
  resetTime: number;
  remaining: number;
}

const rateLimiters: Map<string, RateLimiter> = new Map();

function checkRateLimit(
  key: string,
  config: RateLimitConfig
): { allowed: boolean; resetTime?: number } {
  const now = Date.now();
  const limiter = rateLimiters.get(key);

  if (!limiter || now > limiter.resetTime) {
    // Reset window
    rateLimiters.set(key, {
      resetTime: now + config.window,
      remaining: config.requests - 1,
    });
    return { allowed: true };
  }

  if (limiter.remaining > 0) {
    limiter.remaining--;
    return { allowed: true };
  }

  return {
    allowed: false,
    resetTime: limiter.resetTime,
  };
}

// Platform-specific rate limits
const PLATFORM_RATE_LIMITS: Record<string, RateLimitConfig> = {
  facebook: { requests: 200, window: 3600000 }, // 200 requests/hour
  twitter: { requests: 450, window: 900000 }, // 450 requests/15 min
  linkedin: { requests: 100, window: 3600000 }, // 100 requests/hour
  instagram: { requests: 200, window: 3600000 }, // 200 requests/hour
};

async function makeRateLimitedRequest<T>(
  platform: string,
  requestFn: () => Promise<T>
): Promise<T> {
  const key = `${platform}:${Date.now()}`;
  const config = PLATFORM_RATE_LIMITS[platform];
  
  const { allowed, resetTime } = checkRateLimit(key, config);
  
  if (!allowed) {
    const waitTime = (resetTime! - Date.now()) / 1000;
    throw new Error(`Rate limit exceeded. Retry in ${waitTime.toFixed(0)} seconds`);
  }
  
  return await requestFn();
}
```

### Exponential Backoff

```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      
      if (attempt === maxRetries - 1) {
        break;
      }

      const delay = baseDelay * Math.pow(2, attempt);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError;
}

// Usage with rate-limited requests
async function postToTwitter(accessToken: string, tweet: Tweet): Promise<any> {
  return await retryWithBackoff(
    () => makeRateLimitedRequest('twitter', () => createTweet(accessToken, tweet)),
    3,
    2000
  );
}
```

---

## Webhook Handling

### Generic Webhook Handler

```typescript
import express from 'express';
import crypto from 'crypto';

interface WebhookConfig {
  secret: string;
  platform: string;
}

const webhookConfigs: Record<string, WebhookConfig> = {
  twitter: { secret: process.env.TWITTER_WEBHOOK_SECRET!, platform: 'twitter' },
  facebook: { secret: process.env.FACEBOOK_APP_SECRET!, platform: 'facebook' },
};

function verifyWebhookSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  
  return signature === expectedSignature;
}

app.post('/webhooks/:platform', express.raw({ type: 'application/json' }), (req, res) => {
  const { platform } = req.params;
  const config = webhookConfigs[platform];
  
  if (!config) {
    return res.status(404).send('Unknown platform');
  }
  
  const signature = req.headers['x-hub-signature-256'] as string;
  const payload = req.body.toString();
  
  // Verify signature
  if (!verifyWebhookSignature(payload, signature, config.secret)) {
    return res.status(401).send('Invalid signature');
  }
  
  try {
    const events = JSON.parse(payload);
    processWebhookEvents(config.platform, events);
    res.status(200).send('OK');
  } catch (error) {
    console.error('Webhook processing error:', error);
    res.status(500).send('Error processing webhook');
  }
});

function processWebhookEvents(platform: string, events: any[]): void {
  events.forEach(event => {
    // Route to appropriate handler
    switch (platform) {
      case 'twitter':
        handleTwitterEvent(event);
        break;
      case 'facebook':
        handleFacebookEvent(event);
        break;
    }
  });
}

function handleTwitterEvent(event: any): void {
  console.log('Twitter event:', event);
  // Process Twitter-specific events
}

function handleFacebookEvent(event: any): void {
  console.log('Facebook event:', event);
  // Process Facebook-specific events
}
```

---

## Analytics

### Social Media Analytics

```typescript
interface SocialMetrics {
  platform: string;
  followers: number;
  engagement: number;
  impressions: number;
  clicks: number;
  shares: number;
  comments: number;
}

async function getSocialMetrics(
  accessToken: string,
  platform: string,
  period: 'day' | 'week' | 'month'
): Promise<SocialMetrics> {
  switch (platform) {
    case 'facebook':
      return await getFacebookMetrics(accessToken, period);
    case 'twitter':
      return await getTwitterMetrics(accessToken, period);
    case 'linkedin':
      return await getLinkedInMetrics(accessToken, period);
    default:
      throw new Error(`Unknown platform: ${platform}`);
  }
}

async function getFacebookMetrics(
  accessToken: string,
  period: string
): Promise<SocialMetrics> {
  const pageId = await getPageId(accessToken);
  const insights = await getPageInsights(
    pageId,
    accessToken,
    ['page_impressions', 'page_post_engagements', 'page_engaged_users'],
    period as any
  );
  
  return {
    platform: 'facebook',
    followers: await getPageFollowerCount(pageId, accessToken),
    engagement: insights.find(i => i.name === 'page_post_engagements')?.values[0]?.value || 0,
    impressions: insights.find(i => i.name === 'page_impressions')?.values[0]?.value || 0,
    clicks: 0, // Facebook doesn't provide clicks separately
    shares: 0,
    comments: 0,
  };
}

// Aggregated metrics across platforms
async function getAggregatedMetrics(
  tokens: Record<string, string>,
  period: 'day' | 'week' | 'month'
): Promise<{
  totalFollowers: number;
  totalEngagement: number;
  totalImpressions: number;
  byPlatform: SocialMetrics[];
}> {
  const platforms = Object.keys(tokens);
  const metrics = await Promise.all(
    platforms.map(platform => getSocialMetrics(tokens[platform], platform, period))
  );
  
  return {
    totalFollowers: metrics.reduce((sum, m) => sum + m.followers, 0),
    totalEngagement: metrics.reduce((sum, m) => sum + m.engagement, 0),
    totalImpressions: metrics.reduce((sum, m) => sum + m.impressions, 0),
    byPlatform: metrics,
  };
}
```

---

## Best Practices

### Security

```typescript
// Store access tokens securely
import { encrypt, decrypt } from './crypto';

async function storeSocialToken(
  userId: string,
  platform: string,
  accessToken: string,
  refreshToken?: string
): Promise<void> {
  const encryptedToken = encrypt(accessToken);
  
  await db.socialAccount.upsert({
    where: {
      userId_platform: {
        userId,
        platform,
      },
    },
    create: {
      userId,
      platform,
      accessToken: encryptedToken,
      refreshToken: refreshToken ? encrypt(refreshToken) : null,
    },
    update: {
      accessToken: encryptedToken,
      refreshToken: refreshToken ? encrypt(refreshToken) : null,
    },
  });
}

async function getSocialToken(
  userId: string,
  platform: string
): Promise<{ accessToken: string; refreshToken?: string } | null> {
  const account = await db.socialAccount.findUnique({
    where: {
      userId_platform: {
        userId,
        platform,
      },
    },
  });
  
  if (!account) {
    return null;
  }
  
  return {
    accessToken: decrypt(account.accessToken),
    refreshToken: account.refreshToken ? decrypt(account.refreshToken) : undefined,
  };
}
```

### Error Handling

```typescript
class SocialMediaError extends Error {
  constructor(
    public platform: string,
    public code: string,
    message: string
  ) {
    super(message);
    this.name = 'SocialMediaError';
  }
}

async function handleSocialMediaError(error: any, platform: string): Promise<never> {
  if (error.code === 429) {
    throw new SocialMediaError(platform, 'RATE_LIMIT', 'Rate limit exceeded');
  }
  
  if (error.code === 401) {
    throw new SocialMediaError(platform, 'UNAUTHORIZED', 'Access token expired or invalid');
  }
  
  if (error.code === 403) {
    throw new SocialMediaError(platform, 'FORBIDDEN', 'Insufficient permissions');
  }
  
  throw new SocialMediaError(platform, 'UNKNOWN', error.message || 'Unknown error');
}
```

---

---

## Quick Start

### Facebook API Integration

```javascript
const { Facebook } = require('fb')

const fb = new Facebook({
  appId: process.env.FB_APP_ID,
  appSecret: process.env.FB_APP_SECRET
})

// Post to page
async function postToFacebook(pageId, message) {
  const accessToken = await getPageAccessToken(pageId)
  
  await fb.api(`/${pageId}/feed`, 'post', {
    message: message,
    access_token: accessToken
  })
}
```

### Twitter API Integration

```javascript
const Twitter = require('twitter')

const client = new Twitter({
  consumer_key: process.env.TWITTER_API_KEY,
  consumer_secret: process.env.TWITTER_API_SECRET,
  access_token_key: process.env.TWITTER_ACCESS_TOKEN,
  access_token_secret: process.env.TWITTER_ACCESS_TOKEN_SECRET
})

// Tweet
async function tweet(message) {
  await client.post('statuses/update', { status: message })
}
```

---

## Production Checklist

- [ ] **OAuth Setup**: OAuth flows configured for platforms
- [ ] **API Keys**: Secure API keys and tokens
- [ ] **Rate Limiting**: Handle rate limits properly
- [ ] **Error Handling**: Handle API errors gracefully
- [ ] **Webhooks**: Set up webhooks for events
- [ ] **Social Login**: Social login integration
- [ ] **Sharing**: Social sharing buttons
- [ ] **Open Graph**: Open Graph tags for sharing
- [ ] **Analytics**: Track social media metrics
- [ ] **Testing**: Test with real accounts
- [ ] **Documentation**: Document integration
- [ ] **Monitoring**: Monitor API usage

---

## Anti-patterns

### ❌ Don't: Expose API Keys

```javascript
// ❌ Bad - API keys in code
const client = new Twitter({
  consumer_key: 'abc123',  // Exposed!
  consumer_secret: 'def456'
})
```

```javascript
// ✅ Good - Environment variables
const client = new Twitter({
  consumer_key: process.env.TWITTER_API_KEY,
  consumer_secret: process.env.TWITTER_API_SECRET
})
```

### ❌ Don't: Ignore Rate Limits

```javascript
// ❌ Bad - No rate limiting
for (const post of posts) {
  await tweet(post)  // May hit rate limit!
}
```

```javascript
// ✅ Good - Rate limiting
const rateLimiter = require('rate-limiter-flexible')
const limiter = new rateLimiter.RateLimiter({
  points: 300,  // 300 tweets
  duration: 900  // per 15 minutes
})

for (const post of posts) {
  await limiter.consume('twitter')
  await tweet(post)
}
```

---

## Integration Points

- **OAuth2** (`10-authentication-authorization/oauth2/`) - OAuth flows
- **Email Marketing** (`28-marketing-integration/email-marketing/`) - Multi-channel
- **Analytics** (`23-business-analytics/`) - Social analytics

---

## Further Reading

- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Twitter API](https://developer.twitter.com/en/docs)
- [LinkedIn API](https://docs.microsoft.com/en-us/linkedin/)

## Resources

- [Facebook Graph API Documentation](https://developers.facebook.com/docs/graph-api/)
- [Twitter API Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [LinkedIn API Documentation](https://learn.microsoft.com/en-us/linkedin/shared/references/v2/api/)
- [Instagram Graph API Documentation](https://developers.facebook.com/docs/instagram-api/)
- [Open Graph Protocol](https://ogp.me/)
- [NextAuth.js Documentation](https://next-auth.js.org/)
